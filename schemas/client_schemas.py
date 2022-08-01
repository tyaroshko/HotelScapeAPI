from typing import Optional

from pydantic import BaseModel


class ClientBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    address: Optional[str]


class ClientAdditionalInfo(ClientBase):
    id: int

    class Config:
        orm_mode = True


class ClientCreate(ClientBase):
    class Config:
        orm_mode = True
