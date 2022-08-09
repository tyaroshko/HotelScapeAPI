"""Util function to help with user authentification."""
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Union

import jwt
from dotenv import load_dotenv
from passlib.context import CryptContext

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

ACCESS_TOKEN_EXPIRE_MINUTES = 10  # 10 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY")

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    """Get hashed password."""
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    """Verify if password is correct."""
    return password_context.verify(password, hashed_pass)


def create_access_token(
    subject: Union[str, Any], expires_delta: int = None
) -> str:
    """Create access token for the user."""
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(
    subject: Union[str, Any], expires_delta: int = None
) -> str:
    """Create refresh token for the user."""
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=REFRESH_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt
