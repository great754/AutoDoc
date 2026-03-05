from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from app.database import Base


class ProcessMetadata(Base):
    __tablename__ = "process_metadata"

    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String(200), nullable=False, index=True)
    purpose = Column(Text, nullable=False)  # Why does this project exist
    business_summary = Column(
        Text, nullable=False
    )  # High level summary of what the business process does
    stakeholders = Column(JSON, nullable=False)  # List of stakeholder names/roles
    flow_filename = Column(String(255), nullable=True)  # Original filename
    flow_filepath = Column(
        String(500), nullable=True
    )
    created_by = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    ollama_analysis = Column(
        Text, nullable=True
    )
    status = Column(
        String(50), default="pending", nullable=False
    )
    error_message = Column(String(500), nullable=True)
