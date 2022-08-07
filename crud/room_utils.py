"""CRUD functions for Room, Facility, Feature and RoomType."""
from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.room import Facility, Feature, Room, RoomType
from schemas.room_schemas import (
    FacilityCreate,
    FeatureCreate,
    RoomCreate,
    RoomTypeCreate,
)

# Room CRUD


def get_rooms(db: Session, skip: int = 0, limit: int = 500):
    """Get all rooms."""
    return db.query(Room).offset(skip).limit(limit).all()


def get_room(db: Session, room_id: int):
    """Get room by id."""
    _room = db.query(Room).filter(Room.id == room_id).first()
    if not _room:
        raise HTTPException(
            status_code=404, detail=f"No room found with id {room_id}"
        )
    return _room


def create_room(db: Session, room: RoomCreate):
    """Create new room."""
    _room = Room(
        id=room.id,
        description=room.description,
        room_type_id=room.room_type_id,
        floor=room.floor,
        facility_id=room.facility_id,
        booking_status=room.booking_status,
        cleanliness_status=room.cleanliness_status,
    )
    db.add(_room)
    db.commit()
    db.refresh(_room)
    return _room


def update_room(db: Session, room_id: int, room: RoomCreate):
    """Update existing room."""
    _room = get_room(db=db, room_id=room_id)
    if not _room:
        raise HTTPException(
            status_code=404, detail=f"No room found with id {room_id}"
        )
    _room.description = room.description
    _room.room_type_id = room.room_type_id
    _room.floor = room.floor
    _room.facility_id = room.facility_id
    _room.booking_status = room.booking_status
    _room.cleanliness_status = room.cleanliness_status
    db.commit()
    db.refresh(_room)
    return _room


def delete_room(db: Session, room_id: int):
    """Remove existing room."""
    _room = get_room(db=db, room_id=room_id)
    if not _room:
        raise HTTPException(
            status_code=404, detail=f"No room found with id {room_id}"
        )
    db.delete(_room)
    db.commit()
    return f"Deleted room with id {room_id}"


def get_room_booking_status(db: Session, room_id: int):
    """Get booking state of specific room."""
    _room = get_room(db=db, room_id=room_id)
    if not _room:
        raise HTTPException(
            status_code=404, detail=f"No room found with id {room_id}"
        )
    return _room.booking_status


def get_room_cleanliness_status(db: Session, room_id: int):
    """Get cleanliness state of specific room."""
    _room = get_room(db=db, room_id=room_id)
    if not _room:
        raise HTTPException(
            status_code=404, detail=f"No room found with id {room_id}"
        )
    return _room.cleanliness_status


# Room types CRUD


def get_room_types(db: Session, skip: int = 0, limit: int = 0):
    """Get all room types."""
    return db.query(RoomType).offset(skip).limit(limit).all()


def get_room_type(db: Session, room_type_id: int):
    """Get room type by id."""
    _room_type = db.query(RoomType).filter(RoomType.id == room_type_id).first()
    if not _room_type:
        raise HTTPException(
            status_code=404,
            detail=f"No room type found with id {room_type_id}",
        )
    return _room_type


def create_room_type(db: Session, room_type: RoomTypeCreate):
    """Create new room type."""
    _room_type = RoomType(
        name=room_type.name, capacity=room_type.capacity, price=room_type.price
    )
    db.add(_room_type)
    db.commit()
    db.refresh(_room_type)
    return _room_type


def update_room_type(
    db: Session, room_type_id: int, room_type: RoomTypeCreate
):
    """Update an existing room type."""
    _room_type = get_room_type(db=db, room_type_id=room_type_id)
    if not _room_type:
        raise HTTPException(
            status_code=404,
            detail=f"No room type found with id {room_type_id}",
        )
    _room_type.name = room_type.name
    _room_type.capacity = room_type.capacity
    _room_type.price = room_type.price
    db.commit()
    db.refresh(_room_type)
    return _room_type


def delete_room_type(db: Session, room_type_id: int):
    """Remove an existing room type."""
    _room_type = get_room_type(db=db, room_type_id=room_type_id)
    if not _room_type:
        raise HTTPException(
            status_code=404,
            detail=f"No room type found with id {room_type_id}",
        )
    db.delete(_room_type)
    db.commit()
    return _room_type


# Room features CRUD


def get_features(db: Session, skip: int = 0, limit: int = 100):
    """Get all features."""
    return db.query(Feature).offset(skip).limit(limit).all()


def get_feature(db: Session, feature_id: int):
    """Get feature by id."""
    _feature = db.query(Feature).filter(Feature.id == feature_id).first()
    if not _feature:
        raise HTTPException(
            status_code=404, detail=f"No feature found with id {feature_id}"
        )


def create_feature(db: Session, feature: FeatureCreate):
    """Create new feature."""
    _feature = Feature(name=feature.name)
    db.add(_feature)
    db.commit()
    db.refresh(_feature)
    return _feature


def update_feature(db: Session, feature_id: int, feature: FeatureCreate):
    """Update an existing feature."""
    _feature = get_feature(db=db, feature_id=feature_id)
    if not _feature:
        raise HTTPException(
            status_code=404, detail=f"No feature found with id {feature_id}"
        )
    _feature.name = feature.name
    db.commit()
    db.refresh(_feature)
    return _feature


def delete_feature(db: Session, feature_id: int):
    """Delete an existing feature."""
    _feature = get_feature(db=db, feature_id=feature_id)
    if not _feature:
        raise HTTPException(
            status_code=404, detail=f"No feature found with id {feature_id}"
        )
    db.delete(_feature)
    db.commit()
    return _feature


# Facility CRUD


def get_facilities(db: Session, skip: int = 0, limit: int = 100):
    """Get all facilities."""
    return db.query(Facility).offset(skip).limit(limit).all()


def get_facility(db: Session, facility_id: int):
    """Get facility by id."""
    _facility = db.query(Facility).filter(Facility.id == facility_id).first()
    if not _facility:
        raise HTTPException(
            status_code=404, detail=f"No facility found with id {facility_id}"
        )


def create_facility(db: Session, facility: FacilityCreate):
    """Create new feature."""
    _facility = Facility(name=facility.name)
    db.add(_facility)
    db.commit()
    db.refresh(_facility)
    return _facility


def update_facility(db: Session, facility_id: int, facility: FeatureCreate):
    """Update an existing feature."""
    _facility = get_facility(db=db, facility_id=facility_id)
    if not _facility:
        raise HTTPException(
            status_code=404, detail=f"No facility found with id {facility_id}"
        )
    _facility.name = facility.name
    db.commit()
    db.refresh(_facility)
    return _facility


def delete_facility(db: Session, facility_id: int):
    """Delete an existing feature."""
    _facility = get_facility(db=db, facility_id=facility_id)
    if not _facility:
        raise HTTPException(
            status_code=404, detail=f"No facility found with id {facility_id}"
        )
    db.delete(_facility)
    db.commit()
    return _facility


# Crossover CRUD
