"""CRUD functions which include using different tables."""
from fastapi import HTTPException
from sqlalchemy.orm import Session

from crud.room_utils import get_room, get_room_type
from models.booking import Booking
from models.room import FeatureToRoomType
from schemas.room_schemas import FeatureList


def get_bookings_for_room(
    db: Session, room_id: int, skip: int = 0, limit: int = 100
):
    """Get all bookings for the specified room."""
    _room = get_room(db=db, room_id=room_id)
    if not _room:
        raise HTTPException(
            status_code=404, detail=f"No room found with id {room_id}"
        )
    _bookings = (
        db.query(Booking)
        .filter(Booking.room_id == room_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return _bookings


def add_feature_to_room_type(db: Session, feature_id: int, room_type_id: int):
    """Add a new feature to a specified room type."""
    pass


def get_features_for_roomtype(
    db: Session, room_type_id: int, skip: int = 0, limit: int = 100
):
    """Get all features of the specified room type."""
    _room_type = get_room_type(db=db, room_type_id=room_type_id)
    if not _room_type:
        raise HTTPException(
            status_code=404,
            detail=f"No room type found with id {room_type_id}",
        )
    _features = (
        db.query(FeatureToRoomType)
        .filter(FeatureToRoomType.room_type_id == room_type_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return _features


def get_features_for_room(
    db: Session, room_id: int, skip: int = 0, limit: int = 100
):
    """Get all features of the specified room."""
    _room = get_room(db=db, room_id=room_id)
    if not _room:
        raise HTTPException(
            status_code=404, detail=f"No room found with id {room_id}"
        )
    _room_type_id = _room.room_type_id
    return get_features_for_roomtype(
        db=db, room_type_id=_room_type_id, skip=skip, limit=limit
    )


def get_room_types_with_feature(db: Session, features_list: FeatureList):
    """Get all room types with specified feature."""
    # _room_types = db.query(RoomType).filter(RoomType.)
    pass
