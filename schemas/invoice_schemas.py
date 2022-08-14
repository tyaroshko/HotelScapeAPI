"""Schemas for models associated with Invoice."""

import datetime

from pydantic import BaseModel
from typing import Optional
from models.invoice import PaymentMethod


class InvoiceBase(BaseModel):
    booking_id: int
    client_id: int
    payment_method: PaymentMethod
    invoice_amount: float


class InvoiceCreate(InvoiceBase):
    class Config:
        orm_mode = True


class InvoiceUpdate(BaseModel):
    booking_id: Optional[int]
    client_id: Optional[int]
    payment_method: Optional[PaymentMethod]
    invoice_amount: Optional[float]
    booking_id: Optional[int]
    client_id: Optional[int]


class InvoiceFull(InvoiceBase):
    ts_issued: datetime.datetime

    class Config:
        orm_mode = True
