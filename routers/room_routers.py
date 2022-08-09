"""Endpoints for Room, Facility, Feature and RoomType."""
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud import misc_crud, room_utils
from db import get_db
from schemas.booking_schemas import BookingFull
from schemas.room_schemas import (
    FacilityCreate,
    FacilityFull,
    FacilityUpdate,
    FeatureCreate,
    FeatureFull,
    FeatureUpdate,
    RoomCreate,
    RoomFull,
    RoomTypeCreate,
    RoomTypeFull,
    RoomTypeUpdate,
    RoomUpdate,
)

router = APIRouter()

# Room routers


@router.get(
    "/rooms",
    summary="Get all rooms",
    response_model=List[RoomFull],
    tags=["room"],
)
def get_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all rooms.

    Parameters
    ----------
    skip : int
        Specifies the number of qualifying rows to exclude.
    limit : int
        If given, no more than that many rows will be returned.
    db : Session
        Current database

    Returns
    -------
    List[RoomFull]
        a list of all rooms present in db
    """
    rooms = room_utils.get_rooms(db=db, skip=skip, limit=limit)
    return rooms


@router.get(
    "/rooms/{room_id}",
    summary="Get room by ID",
    response_model=RoomFull,
    tags=["room"],
)
def get_room(room_id: int, db: Session = Depends(get_db)):
    """
    Get an existing room by ID.

    Parameters
    ----------
    db : Session
        Current database

    room_id : int
        ID of the room to retrieve

    Returns
    -------
    RoomFull
        RoomFull object with all info about the room
    """
    return room_utils.get_room(db=db, room_id=room_id)


@router.post(
    "/rooms",
    summary="Create a new room",
    response_model=RoomFull,
    tags=["room"],
)
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    """
    Create a new room.

    Parameters
    ----------
    db : Session
        Current database

    room : RoomCreate
        RoomCreate object with all the necessary data to create a new room

    Returns
    -------
    RoomFull
        RoomFull object with all info of the newly created room
    """
    return room_utils.create_room(db=db, room=room)


@router.put(
    "/rooms/{room_id}",
    summary="Update an existing room",
    response_model=RoomFull,
    tags=["room"],
)
def update_room(room_id: int, room: RoomUpdate, db: Session = Depends(get_db)):
    """
    Update an existing room.

    Parameters
    ----------
    db : Session
        Current database

    room : RoomUpdate
        RoomUpdate object with all the optional data to update for the room
    room_id : int
        ID of the room to update

    Returns
    -------
    RoomFull
        RoomFull object with all info of the newly updated room
    """
    return room_utils.update_room(db=db, room_id=room_id, room=room)


@router.delete(
    "/rooms/{room_id}",
    summary="Delete an existing room",
    response_model=str,
    tags=["room"],
)
def delete_room(room_id: int, db: Session = Depends(get_db)):
    """
    Delete an existing room.

    Parameters
    ----------
    db: Session
        Current database

    room_id: int
        ID of the room to delete

    Returns
    -------
    str
        string with info about successful deletion
    """
    return room_utils.delete_room(room_id=room_id, db=db)


# @router.post("/rooms/filter")
# def filter_rooms(filter: RoomFilter, db: Session = Depends(get_db)):
#     return room_utils.get_rooms_filter(db=db, filter=filter)


@router.get(
    "/rooms/{room_id}/booking_status",
    summary="Get booking status of a room",
    response_model=str,
    tags=["room"],
)
def get_room_booking_status(room_id: int, db: Session = Depends(get_db)):
    """
    Get booking status of a room.

    Parameters
    ----------
    db: Session
        Current database

    room_id: int
        ID of the room to get the booking status of

    Returns
    -------
    str
        string with the booking status of the room
    """
    return room_utils.get_room_booking_status(room_id=room_id, db=db)


@router.get(
    "/rooms/{room_id}/cleanliness_status",
    summary="Get cleanliness status of a room",
    response_model=str,
    tags=["room"],
)
def get_room_cleanliness_status(room_id: int, db: Session = Depends(get_db)):
    """
    Get cleanliness status of a room.

    Parameters
    ----------
    db: Session
        Current database

    room_id: int
        ID of the room to get the cleanliness status of

    Returns
    -------
    str
        string with the cleanliness status of the room
    """
    return room_utils.get_room_cleanliness_status(room_id=room_id, db=db)


# Room types routers


@router.get(
    "/room_types",
    summary="Get all room types",
    response_model=List[RoomTypeFull],
    tags=["room_type"],
)
def get_room_types(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Get all room types.

    Parameters
    ----------
    skip : int
        Specifies the number of qualifying rows to exclude.
    limit : int
        If given, no more than that many rows will be returned.
    db: Session
        Current database

    Returns
    -------
    List[RoomTypeFull]
        a list of all room types present in db
    """
    room_types = room_utils.get_room_types(db=db, skip=skip, limit=limit)
    return room_types


@router.get(
    "/room_types/{room_type_id}",
    summary="Get room type by ID",
    response_model=RoomTypeFull,
    tags=["room_type"],
)
def get_room_type(room_type_id: int, db: Session = Depends(get_db)):
    """
    Get an existing room type by ID.

    Parameters
    ----------
    db : Session
        Current database

    room_type_id : int
        ID of the room type to retrieve

    Returns
    -------
    RoomTypeFull
        RoomTypeFull object with all info about the room type
    """
    room_type = room_utils.get_room_type(db=db, room_type_id=room_type_id)
    return room_type


@router.post(
    "/room_types",
    summary="Create a new room type",
    response_model=RoomTypeFull,
    tags=["room_type"],
)
def create_room_type(room_type: RoomTypeCreate, db: Session = Depends(get_db)):
    """
    Create a new room type.

    Parameters
    ----------
    db : Session
        Current database

    room_type : RoomTypeCreate
        RoomTypeCreate object with all the necessary data to create a new room type

    Returns
    -------
    RoomTypeFull
        RoomTypeFull object with all info of the newly created room type
    """
    return room_utils.create_room_type(db=db, room_type=room_type)


@router.put(
    "/room_types/{room_type_id}",
    summary="Update an existing room type",
    response_model=RoomTypeFull,
    tags=["room_type"],
)
def update_room_type(
    room_type_id: int, room_type: RoomTypeUpdate, db: Session = Depends(get_db)
):
    """
    Update an existing room type.

    Parameters
    ----------
    db : Session
        Current database

    room_type : RoomTypeUpdate
        RoomTypeUpdate object with all the optional data to update for the room type
    room_id : int
        ID of the room to update

    Returns
    -------
    RoomTypeFull
        RoomTypeFull object with all info of the newly updated room type
    """
    return room_utils.update_room_type(
        db=db, room_type_id=room_type_id, room_type=room_type
    )


@router.delete(
    "/room_types/{room_type_id}",
    summary="Delete an existing room type",
    response_model=str,
    tags=["room_type"],
)
def delete_room_type(room_type_id: int, db: Session = Depends(get_db)):
    """
    Delete an existing room type.

    Parameters
    ----------
    db: Session
        Current database

    room_type_id: int
        ID of the room type to delete

    Returns
    -------
    str
        string with info about successful deletion
    """
    return room_utils.delete_room_type(room_type_id=room_type_id, db=db)


# Features routers


@router.get(
    "/features/{feature_id}",
    summary="Get feature by ID",
    response_model=FeatureFull,
    tags=["feature"],
)
def get_feature(feature_id: int, db: Session = Depends(get_db)):
    """
    Get an existing feature by ID.

    Parameters
    ----------
    db : Session
        Current database

    feature_id : int
        ID of the feature to retrieve

    Returns
    -------
    FeatureFull
        FeatureFull object with all info about the room type
    """
    feature = room_utils.get_feature(db=db, feature_id=feature_id)
    return feature


@router.post(
    "/features",
    summary="Create a new feature",
    response_model=FeatureFull,
    tags=["feature"],
)
def create_feature(feature: FeatureCreate, db: Session = Depends(get_db)):
    """
    Create a new feature.

    Parameters
    ----------
    db : Session
        Current database

    feature : FeatureCreate
        FeatureCreate object with all the necessary data to create a new room type

    Returns
    -------
    FeatureFull
        FeatureFull object with all info of the newly created feature
    """
    return room_utils.create_feature(db=db, feature=feature)


@router.put(
    "/features/{feature_id}",
    summary="Update an existing feature",
    response_model=FeatureFull,
    tags=["feature"],
)
def update_feature(
    feature_id: int, feature: FeatureUpdate, db: Session = Depends(get_db)
):
    """
    Update an existing feature.

    Parameters
    ----------
    db : Session
        Current database

    feature : FeatureUpdate
        RoomTypeUpdate object with all the optional data to update for the room type
    feature_id : int
        ID of the feature to update

    Returns
    -------
    FeatureFull
        FeatureFull object with all info of the newly updated feature
    """
    return room_utils.update_feature(
        db=db, feature_id=feature_id, feature=feature
    )


@router.delete(
    "/features/{feature_id}",
    summary="Delete an existing feature",
    response_model=str,
    tags=["feature"],
)
def delete_feature(feature_id: int, db: Session = Depends(get_db)):
    """
    Delete an existing feature.

    Parameters
    ----------
    db: Session
        Current database

    feature_id: int
        ID of the feature to delete

    Returns
    -------
    str
        string with info about successful deletion
    """
    return room_utils.delete_feature(feature_id=feature_id, db=db)


@router.get(
    "/facilities",
    summary="Get all facilities",
    response_model=List[FacilityFull],
    tags=["facility"],
)
def get_facilities(
    skip: int = 0, limit: int = 0, db: Session = Depends(get_db)
):
    """
    Get all hotel facilities.

    Parameters
    ----------
    skip : int
        Specifies the number of qualifying rows to exclude.
    limit : int, optional
        If given, no more than that many rows will be returned.
    db: Session
        Current database

    Returns
    -------
    List[FacilityFull]
        a list of all facilities of hotel facilities present in db
    """
    facilities = room_utils.get_facilities(db=db, skip=skip, limit=limit)
    return facilities


@router.get(
    "/facilities/{facility_id}",
    summary="Get facility by ID",
    response_model=FacilityFull,
    tags=["facility"],
)
def get_facility(facility_id: int, db: Session = Depends(get_db)):
    """
    Get an existing facility by ID.

    Parameters
    ----------
    db : Session
        Current database

    facility_id : int
        ID of the hotel facility to retrieve

    Returns
    -------
    FacilityFull
        FacilityFull object with all info about the hotel facility
    """
    facility = room_utils.get_facility(db=db, facility_id=facility_id)
    return facility


@router.post(
    "/facilities",
    summary="Create a new hotel facility",
    response_model=FacilityFull,
    tags=["facility"],
)
def create_facility(facility: FacilityCreate, db: Session = Depends(get_db)):
    """
    Create a new facility.

    Parameters
    ----------
    db : Session
        Current database

    feature : FacilityCreate
        FacilityCreate object with all the necessary data to create a new hotel facility

    Returns
    -------
    FacilityFull
        FacilityFull object with all info of the newly created hotel facility
    """
    return room_utils.create_facility(db=db, facility=facility)


@router.put(
    "/facilities/{facility_id}",
    summary="Update an existing facility",
    response_model=FacilityFull,
    tags=["facility"],
)
def update_facility(
    facility_id: int, facility: FacilityUpdate, db: Session = Depends(get_db)
):
    """
    Update an existing facility.

    Parameters
    ----------
    db: Session
        Current database

    facility_id: int
        ID of the facility to update

    Returns
    -------
    FacilityFull
        FacilityFull object with all info about the newly updatedfacility
    """
    return room_utils.update_facility(
        db=db, facility_id=facility_id, facility=facility
    )


@router.delete(
    "/facilities/{facility_id}",
    summary="Delete an existing facility",
    response_model=str,
    tags=["facility"],
)
def delete_facility(facility_id: int, db: Session = Depends(get_db)):
    """
    Delete an existing facility.

    Parameters
    ----------
    db: Session
        Current database

    facility_id: int
        ID of the facility to delete

    Returns
    -------
    str
        string with info about successful deletion
    """
    return room_utils.delete_facility(facility_id=facility_id, db=db)


@router.get(
    "/rooms/{room_id}/bookings",
    summary="Get all bookings for a room",
    response_model=List[BookingFull],
    tags=["room"],
)
def get_bookings_for_room(
    room_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Get all bookings for specified room.

    Parameters
    ----------
    skip : int
        Specifies the number of qualifying rows to exclude.
    limit : int
        If given, no more than that many rows will be returned.
    db: Session
        Current database

    room_id : int
        ID of the room to get the bookings for
    Returns
    -------
    List[BookingFull]
        a list of all bookings that correspond to the room with ID of {room_id}
    """
    return misc_crud.get_bookings_for_room(
        db=db, room_id=room_id, skip=skip, limit=limit
    )


@router.get(
    "/room_types/{room_type_id}/features",
    summary="Get all features for a room type",
    response_model=List[FeatureFull],
    tags=["room_type"],
)
def get_features_for_room_type(
    room_type_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Get all features for specified room type.

    Parameters
    ----------
    skip : int
        Specifies the number of qualifying rows to exclude.
    limit : int
        If given, no more than that many rows will be returned.
    db: Session
        Current database

    room_type_id: int
        ID of the room type to get the features for

    Returns
    -------
    List[FeatureFull]
        a list of all features that correspond
        to the room type with ID of {room_type_id}
    """
    return misc_crud.get_features_for_roomtype(
        db=db, room_type_id=room_type_id, skip=skip, limit=limit
    )


@router.get(
    "/rooms/{room_id}/features",
    summary="Get all features for a room",
    response_model=List[FeatureFull],
    tags=["room"],
)
def get_features_for_room(
    room_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Get all features for specified room.

    Parameters
    ----------
    skip : int
        Specifies the number of qualifying rows to exclude.
    limit : int
        If given, no more than that many rows will be returned.
    db: Session
        Current database

    room_id: int
        ID of the room type to get the features for

    Returns
    -------
    List[FeatureFull]
        a list of all features that correspond to the room with ID of {room_id}
    """
    return misc_crud.get_features_for_room(
        db=db, room_id=room_id, skip=skip, limit=limit
    )
