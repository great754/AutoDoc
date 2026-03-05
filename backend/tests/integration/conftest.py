import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url

# . sets up a client fixture that connects to the database,
# creates tables, and cleans the data after each test.
BACKEND_ROOT = Path(__file__).resolve().parents[2]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


DEFAULT_INTEGRATION_DB_URL = (
    "mysql+pymysql://autodoc_user:autodoc_pass@127.0.0.1:3306/autodoc_test"
)


def _get_integration_database_url() -> str:
    return os.getenv("INTEGRATION_DATABASE_URL", DEFAULT_INTEGRATION_DB_URL)


def _ensure_test_database_exists(database_url: str) -> None:
    """Create the test database if it doesn't exist using root credentials."""
    parsed = make_url(database_url)
    if not parsed.database:
        return

    # Connect as root to create test database and grant permissions
    root_url = parsed.set(username="root", password="rootpassword", database="mysql")
    admin_engine = create_engine(
        root_url, pool_pre_ping=True, isolation_level="AUTOCOMMIT"
    )

    try:
        with admin_engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{parsed.database}`"))
            # Grant all privileges to the app user
            conn.execute(
                text(
                    f"GRANT ALL PRIVILEGES ON `{parsed.database}`.* TO '{parsed.username}'@'%'"
                )
            )
            conn.execute(text("FLUSH PRIVILEGES"))
    finally:
        admin_engine.dispose()


@pytest.fixture(scope="session")
def client():
    db_url = _get_integration_database_url()
    _ensure_test_database_exists(db_url)

    # Set DATABASE_URL before any app imports to ensure fresh connection
    os.environ["DATABASE_URL"] = db_url

    # Clear any cached app modules to force reload with new DATABASE_URL
    modules_to_clear = [key for key in sys.modules.keys() if key.startswith("app.")]
    for module in modules_to_clear:
        del sys.modules[module]

    from app.database import Base, engine
    from app.main import app

    Base.metadata.create_all(bind=engine)

    with TestClient(app) as test_client:
        yield test_client

    engine.dispose()


@pytest.fixture(autouse=True)
def clean_users_table(client):
    from app.database import SessionLocal
    from app.models.user import User

    db = SessionLocal()
    try:
        db.query(User).delete()
        db.commit()
    finally:
        db.close()

    yield
