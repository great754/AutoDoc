import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.process import ProcessMetadata
from app.schemas.process import (
    ProcessMetadataUpdate,
    ProcessMetadataResponse,
    ProcessListResponse,
)
from app.core.file_storage import save_upload_file, read_upload_file, delete_upload_file
from app.core.ollama_service import ollama_service

router = APIRouter(prefix="/process", tags=["process"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/", response_model=ProcessMetadataResponse, status_code=status.HTTP_201_CREATED
)
def create_process(
    project_name: str = Form(...),
    purpose: str = Form(...),
    business_summary: str = Form(...),
    stakeholders: str = Form(...),
    flow_file: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    """
    Create a new RPA process metadata entry with optional power automate flow upload.
    Flow files are stored locally in the uploads/ directory.
    """
    # Parse stakeholders from JSON string
    from app.schemas.process import StakeholderInfo
    stakeholders_list = [StakeholderInfo(**s) for s in json.loads(stakeholders)]
    stakeholders_data = [s.model_dump() for s in stakeholders_list]

    # Handle power automate flow file upload
    flow_filepath = None
    flow_filename = None
    if flow_file:
        flow_filename, flow_filepath = save_upload_file(flow_file, None)  # Process ID unknown yet

    new_process = ProcessMetadata(
        project_name=project_name,
        purpose=purpose,
        business_summary=business_summary,
        stakeholders=stakeholders_data,
        flow_filename=flow_filename,
        flow_filepath=flow_filepath,
        status="pending",
    )

    db.add(new_process)
    db.commit()
    db.refresh(new_process)

    # Update filepath with process ID for better organization
    if flow_filepath:
        # Extract base name and reorganize
        from pathlib import Path

        old_path = Path(flow_filepath)
        process_dir = Path("uploads") / f"process_{new_process.id}"
        new_path = process_dir / old_path.name
        old_file = Path(flow_filepath)
        new_file = Path(new_path)
        new_file.parent.mkdir(parents=True, exist_ok=True)
        if old_file.exists():
            old_file.rename(new_file)
        new_process.flow_filepath = str(new_path)
        db.commit()

    return new_process


@router.get("/", response_model=List[ProcessListResponse])
def list_processes(db: Session = Depends(get_db)):
    """List all RPA process metadata entries."""
    processes = db.query(ProcessMetadata).all()
    return processes


@router.get("/{process_id}", response_model=ProcessMetadataResponse)
def get_process(process_id: int, db: Session = Depends(get_db)):
    """Get a specific RPA process metadata entry."""
    process = db.query(ProcessMetadata).filter(ProcessMetadata.id == process_id).first()

    if not process:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Process with id {process_id} not found",
        )

    return process


@router.put("/{process_id}", response_model=ProcessMetadataResponse)
def update_process(
    process_id: int,
    data: ProcessMetadataUpdate,
    db: Session = Depends(get_db),
):
    """Update an RPA process metadata entry."""
    process = db.query(ProcessMetadata).filter(ProcessMetadata.id == process_id).first()

    if not process:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Process with id {process_id} not found",
        )

    # Update only provided fields
    if data.project_name is not None:
        process.project_name = data.project_name
    if data.purpose is not None:
        process.purpose = data.purpose
    if data.business_summary is not None:
        process.business_summary = data.business_summary
    if data.stakeholders is not None:
        process.stakeholders = [s.model_dump() for s in data.stakeholders]

    db.commit()
    db.refresh(process)

    return process


@router.delete("/{process_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_process(process_id: int, db: Session = Depends(get_db)):
    """Delete an RPA process metadata entry and its flow file."""
    process = db.query(ProcessMetadata).filter(ProcessMetadata.id == process_id).first()

    if not process:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Process with id {process_id} not found",
        )

    # Delete flow file if exists
    if process.flow_filepath:
        delete_upload_file(process.flow_filepath)

    db.delete(process)
    db.commit()

    return None


@router.post("/{process_id}/analyze", response_model=ProcessMetadataResponse)
def analyze_process_with_ollama(process_id: int, db: Session = Depends(get_db)):
    """
    Send process metadata to Ollama for analysis.
    Uses gpt-oss:120b-cloud model to generate comprehensive documentation.
    """
    process = db.query(ProcessMetadata).filter(ProcessMetadata.id == process_id).first()

    if not process:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Process with id {process_id} not found",
        )

    # Update status to processing
    process.status = "processing"
    db.commit()

    try:
        # Read flow content if file exists
        flow_content = None
        if process.flow_filepath:
            print(f"Reading flow file from: {process.flow_filepath}")
            try:
                flow_content = read_upload_file(process.flow_filepath)
                print(f"Successfully read flow file. Size: {len(flow_content)} characters")
            except Exception as e:
                print(f"Error reading flow file: {str(e)}")
                raise

        # Call Ollama for analysis
        print("Calling Ollama service for analysis...")
        analysis = ollama_service.generate_analysis(
            project_name=process.project_name,
            purpose=process.purpose,
            business_summary=process.business_summary,
            stakeholders=process.stakeholders,
            flow_content=flow_content,
        )

        print("Analysis complete. Storing result...")
        # Store analysis result
        process.ollama_analysis = analysis
        process.status = "processed"
        process.error_message = None
        db.commit()
        db.refresh(process)

        return process

    except Exception as e:
        # Store error
        print(f"Exception in analyze endpoint: {type(e).__name__}: {str(e)}")
        process.status = "error"
        process.error_message = str(e)
        db.commit()
        db.refresh(process)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}",
        )


@router.get("/{process_id}/flow")
def get_process_flow(process_id: int, db: Session = Depends(get_db)):
    """Download the power automate flow file for a process."""
    process = db.query(ProcessMetadata).filter(ProcessMetadata.id == process_id).first()

    if not process:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Process with id {process_id} not found",
        )

    if not process.flow_filepath:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No power automate flow file for this process",
        )

    try:
        flow_content = read_upload_file(process.flow_filepath)
        return {
            "filename": process.flow_filename,
            "content": json.loads(flow_content)
            if flow_content.strip().startswith("{")
            else flow_content,
        }
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flow file not found on disk",
        )
