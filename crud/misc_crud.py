"""CRUD functions which include using different tables."""
from fastapi import HTTPException
from sqlalchemy.orm import Session

from crud import room_utils, client_utils
from models.booking import Booking
from models.room import Room


def get_bookings_for_room(
    db: Session, room_id: int, skip: int = 0, limit: int = 100
):
    """Get all bookings for the specified room."""
    _room = room_utils.get_room(db=db, room_id=room_id)
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
    if not room_utils.get_feature(db=db, feature_id=feature_id):
        raise HTTPException(
            status_code=404, detail=f"No feature found with id {feature_id}"
        )
    if not room_utils.get_room_type(db=db, room_type_id=room_type_id):
        raise HTTPException(
            status_code=404,
            detail=f"No room type found with id {room_type_id}",
        )
    _room_type = room_utils.get_room_type(db=db, room_type_id=room_type_id)
    _feature = room_utils.get_feature(db=db, feature_id=feature_id)
    _room_type.features.append(_feature)
    db.commit()
    db.refresh(_room_type)
    response = {
        "result": f"Successfully added feature (id={feature_id}) \
to room_type (id={room_type_id})"
    }
    return response


def delete_feature_from_room_type(
    db: Session, feature_id: int, room_type_id: int
):
    """Add a new feature to a specified room type."""
    if not room_utils.get_feature(db=db, feature_id=feature_id):
        raise HTTPException(
            status_code=404, detail=f"No feature found with id {feature_id}"
        )
    if not room_utils.get_room_type(db=db, room_type_id=room_type_id):
        raise HTTPException(
            status_code=404,
            detail=f"No room type found with id {room_type_id}",
        )
    _room_type = room_utils.get_room_type(db=db, room_type_id=room_type_id)
    _feature = room_utils.get_feature(db=db, feature_id=feature_id)
    if _feature not in _room_type.features:
        raise HTTPException(
            status_code=404,
            detail=f"Room type with id {room_type_id} \
does not have a feature with id {feature_id}",
        )
    _room_type.features.remove(_feature)
    db.commit()
    db.refresh(_room_type)
    response = {
        "result": f"Successfully deleted feature \
(id={feature_id}) from room_type (id={room_type_id})"
    }
    return response


def get_features_for_roomtype(
    db: Session, room_type_id: int, skip: int = 0, limit: int = 100
):
    """Get all features of the specified room type."""
    _room_type = room_utils.get_room_type(db=db, room_type_id=room_type_id)
    if not _room_type:
        raise HTTPException(
            status_code=404,
            detail=f"No room type found with id {room_type_id}",
        )
    _features = _room_type.features
    return _features


def get_features_for_room(
    db: Session, room_id: int, skip: int = 0, limit: int = 100
):
    """Get all features of the specified room."""
    _room = room_utils.get_room(db=db, room_id=room_id)
    if not _room:
        raise HTTPException(
            status_code=404, detail=f"No room found with id {room_id}"
        )
    _room_type_id = _room.room_type_id
    return get_features_for_roomtype(
        db=db, room_type_id=_room_type_id, skip=skip, limit=limit
    )


def get_room_types_with_feature(db: Session, feature_id: int):
    """Get all room types with specified feature."""
    _feature = room_utils.get_feature(db=db, feature_id=feature_id)
    room_types = _feature.room_types
    room_types_ids = [room_type.id for room_type in room_types]
    rooms = db.query(Room).filter(Room.room_type_id.in_(room_types_ids)).all()
    return rooms


def get_bookings_of_client(db: Session, client_id: int):
    """Get all bookings made by a client."""
    _client = client_utils.get_client(db=db, client_id=client_id)
    if not _client:
        raise HTTPException(
            status_code=404, detail=f"No client found with id {client_id}"
        )
    client_bookings = _client.bookings
    return client_bookings
