"""Tables to manage many-to-many relationships."""

from sqlalchemy import Column, Integer, Table, ForeignKey
from db import Base

BookingsToClients = Table(
    "bookings_to_clients",
    Base.metadata,
    Column(
        "client_id",
        Integer,
        ForeignKey("clients.id", onupdate="CASCADE", ondelete="CASCADE"),
    ),
    Column(
        "booking_id",
        Integer,
        ForeignKey("bookings.id", onupdate="CASCADE", ondelete="CASCADE"),
    ),
)

BookingsToRooms = Table(
    "bookings_to_rooms",
    Base.metadata,
    Column(
        "room_id",
        Integer,
        ForeignKey("rooms.id", onupdate="CASCADE", ondelete="CASCADE"),
    ),
    Column(
        "booking_id",
        Integer,
        ForeignKey("bookings.id", onupdate="CASCADE", ondelete="CASCADE"),
    ),
)

FeaturesToRoomTypes = Table(
    "features_to_room_types",
    Base.metadata,
    Column(
        "room_type_id",
        Integer,
        ForeignKey("room_types.id", onupdate="CASCADE", ondelete="CASCADE"),
    ),
    Column(
        "feature_id",
        Integer,
        ForeignKey("features.id", onupdate="CASCADE", ondelete="CASCADE"),
    ),
)
