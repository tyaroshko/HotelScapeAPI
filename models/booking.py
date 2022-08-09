"""Booking model."""

import datetime

from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer

from db import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    client_id = Column(Integer, ForeignKey("clients.id"))
    start_date = Column(Date)
    end_date = Column(Date)
    discount_percent = Column(Float, default=0.0)
    total_price = Column(Float, nullable=False)
    ts_created = Column(DateTime, default=datetime.datetime.now)
    ts_updated = Column(DateTime, default=datetime.datetime.now)
