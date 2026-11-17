from sqlmodel import create_engine, Session, SQLModel
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:local_secret_password@localhost:5432/ai_automation_db")

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    """Creates all physical tables in PostgreSQL if they do not exist."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Provides a clean database transaction session per API request."""
    with Session(engine) as session:
        yield session
