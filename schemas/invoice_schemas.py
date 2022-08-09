"""Schemas for models associated with Invoice."""

import datetime

from pydantic import BaseModel
from typing import Optional
from models.invoice import PaymentMethod


class InvoiceBase(BaseModel):
    payment_method: PaymentMethod
    invoice_amount: float


class InvoiceCreate(InvoiceBase):
    booking_id: int
    client_id: int
    ts_issued: datetime.datetime

    class Config:
        orm_mode = True


class InvoiceUpdate(InvoiceCreate):
    payment_method: Optional[PaymentMethod]
    invoice_amount: Optional[float]
    booking_id: Optional[int]
    client_id: Optional[int]
    ts_issued: Optional[datetime.datetime]
    ts_paid: Optional[datetime.datetime]


class InvoiceFull(InvoiceBase):
    booking_id: int
    client_id: int
    ts_issued: datetime.datetime
    ts_paid: datetime.datetime

    class Config:
        orm_mode = True
