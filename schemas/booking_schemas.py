"""Schemas for models associated with Booking."""

import datetime
from typing import Optional
from pydantic import BaseModel


class BookingBase(BaseModel):
    client_id: int
    room_id: int
    start_date: datetime.date
    end_date: datetime.date

class BookingBaseInfo(BookingBase):
    class Config:
        orm_mode = True

class BookingFull(BookingBase):
    id: int
    total_price: float
    ts_created: datetime.datetime
    ts_updated: datetime.datetime

    class Config:
        orm_mode = True


class BookingList(BookingBase):
    id: int

    class Config:
        orm_mode = True


class BookingCreate(BookingBase):
    class Config:
        orm_mode = True


class BookingFilter(BaseModel):
    client_id: Optional[int]
    room_id: Optional[int]
    start_date: Optional[datetime.date]
    end_date: Optional[datetime.date]
    total_price: Optional[float]

    class Config:
        orm_mode = True


class BookingUpdate(BookingFilter):
    class Config:
        orm_mode = True
