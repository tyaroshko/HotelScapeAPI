"""Schemas for models associated with User."""

from uuid import UUID

from pydantic import BaseModel, Field


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class UserAuth(BaseModel):
    username: str = Field(...)
    password: str = Field(..., min_length=8, max_length=24)


class UserOut(BaseModel):
    id: UUID
    username: str

    class Config:
        orm_mode = True


class SystemUser(UserOut):
    hashed_password: str
