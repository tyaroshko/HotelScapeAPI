"""Schemas for models associated with Client."""
from typing import Optional

from pydantic import BaseModel


class ClientBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    address: Optional[str]


class ClientFull(ClientBase):
    id: int
    phone: str
    address: Optional[str]

    class Config:
        orm_mode = True


class ClientCreate(ClientBase):
    phone: str
    address: Optional[str]

    class Config:
        orm_mode = True


class ClientUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]
