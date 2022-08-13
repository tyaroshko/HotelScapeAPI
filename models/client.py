"""Client model."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db import Base
from models.misc_tables import BookingsToClients


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String)
    bookings = relationship(
        "Booking", secondary=BookingsToClients, back_populates="clients"
    )
