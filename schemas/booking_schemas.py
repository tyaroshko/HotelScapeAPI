"""Schemas for models associated with Booking."""

import datetime
from typing import Optional
from pydantic import BaseModel


class BookingBase(BaseModel):
    client_id: int
    start_date: datetime.date
    end_date: datetime.date
    discount_percent: float
    total_price: float


class BookingFull(BookingBase):
    id: int
    ts_created: datetime.datetime
    ts_updated: datetime.datetime

    class Config:
        orm_mode = True


class BookingCreate(BookingBase):
    class Config:
        orm_mode = True


class BookingUpdate(BaseModel):
    client_id: Optional[int]
    start_date: Optional[datetime.date]
    end_date: Optional[datetime.date]
    discount_percent: Optional[float]
    total_price: Optional[float]
    ts_created: Optional[datetime.datetime]
    ts_updated: datetime.datetime.now
