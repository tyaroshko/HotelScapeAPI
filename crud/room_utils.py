"""CRUD functions for Room, Facility, Feature and RoomType."""
from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.room import Facility, Feature, Room, RoomType
from schemas.room_schemas import (
    FacilityCreate,
    FeatureCreate,
    RoomCreate,
    RoomTypeCreate,
    RoomTypeUpdate,
    RoomUpdate,
)

# Room CRUD


def get_rooms(db: Session, skip: int = 0, limit: int = 100):
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
    if not get_room_type(db=db, room_type_id=room.room_type_id):
        raise HTTPException(
            status_code=404,
            detail=f"No room type with id {room.room_type_id} found",
        )
    if not get_facility(db=db, facility_id=room.facility_id):
        raise HTTPException(
            status_code=404,
            detail=f"No facility with id {room.facility_id} found",
        )
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


def update_room(db: Session, room_id: int, room: RoomUpdate):
    """Update existing room."""
    _room = get_room(db=db, room_id=room_id)
    if not _room:
        raise HTTPException(
            status_code=404, detail=f"No room found with id {room_id}"
        )
    if room.description:
        _room.description = room.description
    if room.room_type_id:
        if not get_room_type(db=db, room_type_id=room.room_type_id):
            raise HTTPException(
                status_code=404,
                detail=f"No room type found with id {room.room_type_id}",
            )
        _room.room_type_id = room.room_type_id
    if room.floor:
        _room.floor = room.floor
    if room.facility_id:
        if not get_facility(db=db, facility_id=room.facility_id):
            raise HTTPException(
                status_code=404,
                detail=f"No facility found with id {room.facility_id}",
            )
        _room.facility_id = room.facility_id
    if room.booking_status:
        _room.booking_status = room.booking_status
    if room.cleanliness_status:
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
    return f"Successfully deleted room with id {room_id}"


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
    db: Session, room_type_id: int, room_type: RoomTypeUpdate
):
    """Update an existing room type."""
    _room_type = get_room_type(db=db, room_type_id=room_type_id)
    if not _room_type:
        raise HTTPException(
            status_code=404,
            detail=f"No room type found with id {room_type_id}",
        )
    if room_type.name:
        _room_type.name = room_type.name
    if room_type.capacity:
        _room_type.capacity = room_type.capacity
    if room_type.price:
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
    return f"Successfully deleted room type with id {room_type_id}"


# Room features CRUD


def get_feature(db: Session, feature_id: int):
    """Get feature by id."""
    _feature = db.query(Feature).filter(Feature.id == feature_id).first()
    if not _feature:
        raise HTTPException(
            status_code=404, detail=f"No feature found with id {feature_id}"
        )
    return _feature


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
    if feature.name:
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
    return f"Successfully deleted feature with id {feature_id}"


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
    """Create new facility."""
    _facility = Facility(name=facility.name)
    db.add(_facility)
    db.commit()
    db.refresh(_facility)
    return _facility


def update_facility(db: Session, facility_id: int, facility: FeatureCreate):
    """Update an existing facility."""
    _facility = get_facility(db=db, facility_id=facility_id)
    if not _facility:
        raise HTTPException(
            status_code=404, detail=f"No facility found with id {facility_id}"
        )
    if facility.name:
        _facility.name = facility.name
    db.commit()
    db.refresh(_facility)
    return _facility


def delete_facility(db: Session, facility_id: int):
    """Delete an existing facility."""
    _facility = get_facility(db=db, facility_id=facility_id)
    if not _facility:
        raise HTTPException(
            status_code=404, detail=f"No facility found with id {facility_id}"
        )
    db.delete(_facility)
    db.commit()
    return f"Successfully deleted facility with id {facility_id}"
