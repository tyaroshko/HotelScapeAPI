from email.policy import default
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, DateTime, ForeignKey
import datetime

from db import Base


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    guest_id = Column(Integer)
    start_date = Column(Date, default=datetime.date)
    end_date = Column(Date, default=datetime.date)
    ts_created = Column(DateTime, default=datetime.datetime.now)
    ts_updated = Column(DateTime, default=datetime.datetime.now)

class ReservedRoom(Base):
    __tablename__ = "reserved_rooms"

    id = Column(Integer, primary_key=True)
    reservation_id = Column(Integer, ForeignKey("reservations.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))

