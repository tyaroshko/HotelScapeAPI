"""Invoice model."""

import datetime
import enum

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer

from db import Base


class PaymentMethod(str, enum.Enum):
    credit_card = "credit_card"
    debit_card = "debit_card"
    cash = "cash"


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(
        Integer, ForeignKey("bookings.id", ondelete="SET NULL")
    )
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="SET NULL"))
    payment_method = Column(Enum(PaymentMethod))
    invoice_amount = Column(Float, nullable=False)
    ts_issued = Column(DateTime, default=datetime.datetime.now)
    ts_paid = Column(DateTime)
