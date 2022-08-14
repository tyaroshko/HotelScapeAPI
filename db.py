"""Database creation and usage."""

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
POSTGRES_TEST_DATABASE = os.getenv("POSTGRES_TEST_DATABASE")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:"
    "{POSTGRES_PASSWORD}"
    f"@{POSTGRES_SERVER}/{POSTGRES_DATABASE}"
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Get the working database."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
