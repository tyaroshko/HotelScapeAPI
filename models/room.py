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

from db import Base


class NumberOfBeds(str, enum.Enum):
    """Possible options for NumberOfBeds."""

    single_bed = "single_bed"
    double_beds = "double_beds"
    twin_beds = "twin_beds"
    king_size_bed = "king_size_bed"


class RoomBookingStatus(str, enum.Enum):
    """Possible options for RoomBookingStatus."""

    vacant = "vacant"
    booked = "booked"
    occupied = "occupied"


class RoomCleanlinessStatus(str, enum.Enum):
    """Possible options for RoomCleanlinessStatus."""

    clean = "clean"
    dirty = "dirty"


class Room(Base):
    """Room class -> creating 'rooms' table."""

    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    description = Column(String, default="")
    room_type_id = Column(Integer, ForeignKey("room_types.id"))
    floor = Column(Integer, CheckConstraint("floor>0"), nullable=False)
    facility_id = Column(Integer, ForeignKey("facilities.id"))
    booking_status = Column(Enum(RoomBookingStatus))
    cleanliness_status = Column(Enum(RoomCleanlinessStatus))


class Facility(Base):
    """Facility class -> creating 'facility' table."""

    __tablename__ = "facilities"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String, nullable=False)


class RoomType(Base):
    """RoomType class -> creating 'room_types' table."""

    __tablename__ = "room_types"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String, nullable=False)
    number_of_beds = Column(Enum(NumberOfBeds))
    capacity = Column(String, nullable=False, default="1")
    price = Column(Float, index=True)


class Feature(Base):
    """Facility class -> creating 'facility' table."""

    __tablename__ = "features"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String, nullable=False)


class FeatureToRoomType(Base):
    """Creates many-to-many relationship between features and room_types."""

    __tablename__ = "features_to_room_types"

    room_type_id = Column(
        Integer, ForeignKey("room_types.id"), primary_key=True
    )
    feature_id = Column(Integer, ForeignKey("features.id"), primary_key=True)
