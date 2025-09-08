# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# For Week 1, use SQLite (file-based). Simple, zero config.
SQLALCHEMY_DATABASE_URL = "sqlite:///./notes.db"

# For SQLite only: check_same_thread must be False for FastAPI dev server
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},echo=True
)

# Session factory: one session per request (we'll wire this in routes later)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models (we’ll create Note model in the next chunk)
Base = declarative_base()
