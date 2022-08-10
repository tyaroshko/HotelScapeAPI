"""CRUD functions to manage users."""
from uuid import UUID, uuid4

from fastapi import HTTPException
from sqlalchemy.orm import Session

from auth.utils import get_hashed_password
from models.user import User
from schemas.user_schemas import UserAuth


def get_user_by_id(db: Session, user_id: UUID):
    """Get user by id."""
    _user = db.query(User).filter(User.id == user_id).first()
    if not _user:
        raise HTTPException(
            status_code=404, detail=f"No user found with id {user_id}"
        )
    return _user


def get_user_by_username(db: Session, username: str):
    """Get user by username."""
    _user = db.query(User).filter(User.username == username).first()
    if not _user:
        raise HTTPException(
            status_code=404, detail=f"No user found with username {username}"
        )
    return _user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Get all users."""
    pass


def create_user(db: Session, user: UserAuth):
    """Create new user."""
    user_exists = get_user_by_username(db=db, username=user.username)
    if user_exists:
        raise HTTPException(
            status=400,
            detail=f"User with username {user.username} already exists",
        )
    _user = User(
        id=str(uuid4()),
        username=user.username,
        hashed_password=get_hashed_password(user.password),
    )
    db.add(_user)
    db.commit()
    db.refresh(_user)
    return _user
