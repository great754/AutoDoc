import uuid
from pathlib import Path
from fastapi import UploadFile


# Create uploads directory if it doesn't exist
UPLOADS_DIR = Path(__file__).resolve().parent.parent.parent / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)


def save_upload_file(upload_file: UploadFile, process_id: int) -> tuple[str, str]:
    """
    Save an uploaded file locally and return (filename, filepath).

    Args:
        upload_file: FastAPI UploadFile object
        process_id: Process ID to organize files

    Returns:
        Tuple of (original_filename, saved_filepath_relative)
    """
    # Create process-specific directory
    process_dir = UPLOADS_DIR / f"process_{process_id}"
    process_dir.mkdir(exist_ok=True)

    # Generate unique filename to avoid collisions
    file_extension = Path(upload_file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = process_dir / unique_filename

    # Save file to disk
    content = upload_file.file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    # Return original filename and relative path
    relative_path = str(file_path.relative_to(UPLOADS_DIR.parent))
    return upload_file.filename, relative_path


def read_upload_file(filepath: str) -> str:
    """Read an uploaded file and return its content as string."""
    file_path = UPLOADS_DIR.parent / filepath
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    # Try reading with UTF-8 first, fall back to latin-1 if that fails
    try:
        return file_path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        print(f"Warning: UTF-8 decode failed for {filepath}, trying latin-1")
        return file_path.read_text(encoding='latin-1')


def delete_upload_file(filepath: str) -> bool:
    """Delete an uploaded file."""
    file_path = UPLOADS_DIR.parent / filepath
    if file_path.exists():
        file_path.unlink()
        return True
    return False
