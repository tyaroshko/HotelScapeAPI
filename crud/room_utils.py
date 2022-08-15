"""CRUD functions for Room, Facility, Feature and RoomType."""

import datetime
from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.booking import Booking

from models.room import Facility, Feature, Room, RoomType
from crud.client_utils import get_client
from schemas.room_schemas import (
    FacilityCreate,
    FeatureCreate,
    RoomCreate,
    RoomFilter,
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
    _room = db.query(Room).filter(Room.id == room.id).first()
    if _room:
        raise HTTPException(
            status_code=400, detail=f"Room with id {room.id} already exists"
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
    return {"result": f"Successfully deleted room with id {room_id}"}


def get_room_booking_status(db: Session, room_id: int):
    """Get booking state of specific room."""
    _room = get_room(db=db, room_id=room_id)
    if not _room:
        raise HTTPException(
            status_code=404, detail=f"No room found with id {room_id}"
        )
    return {"result": f"{_room.booking_status}"}


def get_room_cleanliness_status(db: Session, room_id: int):
    """Get cleanliness state of specific room."""
    _room = get_room(db=db, room_id=room_id)
    if not _room:
        raise HTTPException(
            status_code=404, detail=f"No room found with id {room_id}"
        )
    return {"result": f"{_room.cleanliness_status}"}


def filter_rooms(db: Session, room: Optional[RoomFilter]):
    """Filter rooms by its parameters."""
    query = db.query(Room)
    if room.description:
        query = query.filter(Room.description == room.description)
    if room.room_type_id:
        query = query.filter(Room.room_type_id == room.room_type_id)
    if room.floor:
        query = query.filter(Room.floor == room.floor)
    if room.facility_id:
        query = query.filter(Room.facility_id == room.facility_id)
    if room.booking_status:
        query = query.filter(Room.booking_status == room.booking_status)
    if room.cleanliness_status:
        query = query.filter(
            Room.cleanliness_status == room.cleanliness_status
        )
    filtered_rooms = query.all()
    return filtered_rooms


def sort_rooms(db: Session, order: str, order_by: str):
    """Sort rooms by its properties."""
    dct = {
        "id": Room.id,
        "room_type_id": Room.room_type_id,
        "floor": Room.floor,
        "facility_id": Room.facility_id,
        "booking_status": Room.booking_status,
        "cleanliness_status": Room.cleanliness_status,
    }
    if order_by not in dct.keys():
        raise HTTPException(
            status_code=400, detail="Such order_by is not supported"
        )
    if order == "desc":
        sorted_query = db.query(Room).order_by(dct[order_by].desc())
    elif order == "asc":
        sorted_query = db.query(Room).order_by(dct[order_by].asc())
    else:
        raise HTTPException(
            status_code=400, detail="Such order is not supported"
        )
    sorted_rooms = sorted_query.all()
    return sorted_rooms


def get_room_guest_now(db: Session, room_id: int):
    """Get current room's guest."""
    _room = get_room(db=db, room_id=room_id)
    if not _room:
        raise HTTPException(
            status_code=404, detail=f"No room found with id {room_id}"
        )
    _booking = (
        db.query(Booking)
        .filter(
            Booking.room_id == room_id,
            Booking.start_date <= datetime.date.today(),
            Booking.end_date >= datetime.date.today(),
        )
        .first()
    )
    if not _booking:
        raise HTTPException(
            status_code=400, detail=f"Room with id {room_id} is currently free"
        )
    _client = get_client(db=db, client_id=_booking.client_id)
    return _client


# Room types CRUD


def get_room_types(db: Session, skip: int = 0, limit: int = 100):
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
    return {"result": f"Successfully deleted room type with id {room_type_id}"}


def filter_room_types_by_price(db: Session, operator: str, value: float):
    """Filter room types by price."""
    dct = {
        ">=": RoomType.price >= value,
        "<=": RoomType.price <= value,
        "==": RoomType.price == value,
        "!=": RoomType.price != value,
        ">": RoomType.price > value,
        "<": RoomType.price < value,
    }
    if operator not in dct.keys():
        raise HTTPException(
            status_code=400, detail="Such operator is not supported"
        )
    filtered_room_types = db.query(RoomType).filter(dct[operator]).all()
    return filtered_room_types


def sort_room_types(db: Session, order: str, order_by: str):
    """Sort room types by its properties."""
    dct = {
        "id": RoomType.id,
        "name": RoomType.name,
        "price": RoomType.price,
        "capacity": RoomType.capacity,
    }
    if order_by not in dct.keys():
        raise HTTPException(
            status_code=400, detail="Such order_by is not supported"
        )
    if order == "desc":
        sorted_query = db.query(Room).order_by(dct[order_by].desc())
    elif order == "asc":
        sorted_query = db.query(Room).order_by(dct[order_by].asc())
    else:
        raise HTTPException(
            status_code=400, detail="Such order is not supported"
        )
    sorted_room_types = sorted_query.all()
    return sorted_room_types


# Room features CRUD


def get_features(db: Session, skip: int = 0, limit: int = 100):
    """Get all features."""
    _features = db.query(Feature).offset(skip).limit(limit).all()
    return _features


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
    return {"result": f"Successfully deleted feature with id {feature_id}"}


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
    return _facility


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
    return {"result": f"Successfully deleted facility with id {facility_id}"}


def check_room_availability_by_date(
    start_date: datetime.date,
    end_date: datetime.date,
    room_id: int,
    db: Session,
):
    """Check if room is free on a given date."""
    _bookings = db.query(Booking).filter(Booking.room_id == room_id).all()
    if not _bookings:
        return {"result": "vacant"}
    for _booking in _bookings:
        if (
            (
                _booking.start_date <= start_date
                and _booking.end_date >= end_date
            )
            or (
                _booking.start_date >= start_date
                and _booking.end_date <= end_date
            )
            or (
                _booking.start_date >= start_date
                and _booking.start_date <= end_date
            )
            or (
                _booking.end_date >= start_date
                and _booking.end_date <= end_date
            )
        ):
            return {"result": "booked"}
    return {"result": "vacant"}
