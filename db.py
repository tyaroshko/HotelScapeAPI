"""Database creation and usage."""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_SERVER = os.environ["POSTGRES_SERVER"]
POSTGRES_DATABASE = os.environ["POSTGRES_DATABASE"]
POSTGRES_TEST_DATABASE = os.environ["POSTGRES_TEST_DATABASE"]

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
