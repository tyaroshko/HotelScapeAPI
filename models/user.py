"""User models."""

from uuid import uuid4
from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID

from db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True), default=uuid4, primary_key=True, index=True
    )
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
