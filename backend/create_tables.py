# ruff: noqa: E402
#!/usr/bin/env python3
"""
Initialize database tables from SQLAlchemy models.
Run this once to create all tables in the database.
"""
import sys
from pathlib import Path

backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

# now imports
from app.database import engine, Base  # noqa: E402

def create_tables():
    """Create all tables defined in models."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully!")

if __name__ == "__main__":
    create_tables()
