"""Deps to use for user authorization."""
from datetime import datetime
from typing import Any, Union

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from auth.utils import ALGORITHM, JWT_SECRET_KEY
from crud.auth_crud import get_user_by_username_for_login
from db import get_db
from schemas.user_schemas import SystemUser, TokenPayload

reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reuseable_oauth)
) -> SystemUser:
    """Get the current user."""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=401,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.jwt, ValidationError):
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user: Union[dict[str, Any], None] = get_user_by_username_for_login(
        db=db, username=token_data.sub
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Could not find user",
        )

    return SystemUser(
        id=user.id,
        username=user.username,
        hashed_password=user.hashed_password,
    )
