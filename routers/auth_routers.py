"""Endpoints for User."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth.deps import get_current_user
from auth.utils import (
    create_access_token,
    create_refresh_token,
    verify_password,
)
from crud import auth_crud
from db import get_db
from schemas.user_schemas import SystemUser, TokenSchema, UserAuth, UserOut

router = APIRouter()


@router.post(
    "/signup", summary="Create new user", response_model=UserOut, tags=["auth"]
)
def create_user(user: UserAuth, db: Session = Depends(get_db)):
    """
    Create a new user --> signup.

        Args:
            db : Session
                Current database
            user : UserAuth
                UserAuth object with username and password

        Returns:
            user : UserOut
                UserOut object with username and UUID of the signed up user
    """
    user_exists = auth_crud.get_user_by_username_for_signup(
        db=db, username=user.username
    )
    if user_exists:
        raise HTTPException(
            status_code=400,
            detail="User with username {username} already exists",
        )
    user = auth_crud.create_user(db=db, user=user)
    return user


@router.post(
    "/login",
    summary="Create access and refresh tokens for user",
    response_model=TokenSchema,
    tags=["auth"],
)
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    Create access and refresh tokens for user --> login.

        Args:
            db : Session
                Current database
            form_data: OAuth2PasswordRequestForm
                data with username and hashed
                password of the user who wants to login

        Returns:
            tokens : TokenSchema
                dict with access token and refresh
                token of the user who logged in
    """
    _user = auth_crud.get_user_by_username_for_login(
        db=db, username=form_data.username
    )
    if not _user:
        raise HTTPException(status_code=400, detail="Incorrect username")
    _hashed_password = _user.hashed_password
    if not verify_password(form_data.password, _hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password",
        )

    return {
        "access_token": create_access_token(_user.username),
        "refresh_token": create_refresh_token(_user.username),
    }


@router.get(
    "/me",
    summary="Get details of currently logged in user",
    response_model=UserOut,
    tags=["auth"],
)
def get_me(user: SystemUser = Depends(get_current_user)):
    """
    Create access and refresh tokens for user --> login.

        Args:
            db : Session
                Current database
            user:
                SystemUser object which establishes the current user

        Returns:
            UserOut
                UserOut object with user's username and UUID
    """
    return user
