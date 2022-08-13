"""Room, RoomType, Facility, Feature, FeatureToRoomType models."""
import enum

from sqlalchemy import (
    CheckConstraint,
    Column,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from models.misc_tables import BookingsToRooms, FeaturesToRoomTypes
from db import Base

# NumberOfBeds enum choice


class RoomTypeName(str, enum.Enum):
    """Possible options for RoomTypeName."""

    single = "single"
    double = "double"
    triple = "triple"
    quad = "quad"
    queen = "queen"
    king = "king"
    twin = "twin"
    hollywood_twin = "hollywood_twin"
    double_double = "double_double"
    studio = "studio"
    suite = "suite"
    mini_suite = "mini_suite"
    president_suite = "president_suite"
    for_extended_stay = "for_extended_stay"
    connecting_rooms = "connecting_rooms"
    murphy = "murphy"
    accessible = "accessible"
    cabana = "cabana"


# Room booking status
class RoomAvailabilityStatus(str, enum.Enum):
    """Possible options for RoomAvailabilityStatus."""

    vacant = "vacant"
    occupied = "occupied"


# Room cleanliness status
class RoomCleanlinessStatus(str, enum.Enum):
    """Possible options for RoomCleanlinessStatus."""

    clean = "clean"
    dirty = "dirty"


class Room(Base):
    """Room class -> creating 'rooms' table."""

    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    description = Column(String, default="")
    room_type_id = Column(
        Integer, ForeignKey("room_types.id", ondelete="SET NULL")
    )
    floor = Column(Integer, CheckConstraint("floor>0"), nullable=False)
    facility_id = Column(
        Integer, ForeignKey("facilities.id", ondelete="SET NULL")
    )
    booking_status = Column(Enum(RoomAvailabilityStatus))
    cleanliness_status = Column(Enum(RoomCleanlinessStatus))
    bookings = relationship(
        "Booking", secondary=BookingsToRooms, back_populates="rooms"
    )


class Facility(Base):
    """Facility class -> creating 'facility' table."""

    __tablename__ = "facilities"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String, nullable=False)


class RoomType(Base):
    """RoomType class -> creating 'room_types' table."""

    __tablename__ = "room_types"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(Enum(RoomTypeName))
    capacity = Column(String, nullable=False, default="1")
    price = Column(Float, index=True)
    features = relationship(
        "Feature", secondary=FeaturesToRoomTypes, back_populates="room_types"
    )


class Feature(Base):
    """Feature class -> creating 'features' table."""

    __tablename__ = "features"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String, nullable=False)
    room_types = relationship(
        "RoomType", secondary=FeaturesToRoomTypes, back_populates="features"
    )
