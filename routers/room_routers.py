"""Endpoints for Room, Facility, Feature and RoomType."""
import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud import misc_crud, room_utils
from auth.deps import get_current_user
from db import get_db
from schemas.booking_schemas import BookingFull
from schemas.client_schemas import ClientFull
from schemas.room_schemas import (
    FacilityCreate,
    FacilityFull,
    FacilityUpdate,
    FeatureCreate,
    FeatureFull,
    FeatureUpdate,
    RoomCreate,
    RoomFilter,
    RoomFull,
    RoomTypeList,
    RoomTypeCreate,
    RoomTypeFull,
    RoomTypeUpdate,
    RoomUpdate,
)
from schemas.user_schemas import ResultSchema, UserAuth

router = APIRouter()

# Room routers


@router.get(
    "/rooms",
    summary="Get all rooms",
    response_model=List[RoomFull],
    tags=["room"],
)
def get_rooms(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Get all rooms.

        Args
            skip : int
                Specifies the number of qualifying rows to exclude.
            limit : int
                If given, no more than that many rows will be returned.
            db : Session
                Current database

        Returns:
            rooms : List[RoomList]
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
def get_room(
    room_id: int,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Get an existing room by ID.

        Args:
            db : Session
                Current database
            room_id : int
                ID of the room to retrieve

        Returns:
            room : RoomFull
                RoomFull object with all info about the room
    """
    return room_utils.get_room(db=db, room_id=room_id)


@router.post(
    "/rooms",
    summary="Create a new room",
    response_model=RoomFull,
    tags=["room"],
)
def create_room(
    room: RoomCreate,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Create a new room.

        Args:
            db : Session
                Current database
            room : RoomCreate
                RoomCreate object with all the
                necessary data to create a new room

        Returns:
            room : RoomFull
                RoomFull object with all info of the newly created room
    """
    return room_utils.create_room(db=db, room=room)


@router.put(
    "/rooms/{room_id}",
    summary="Update an existing room",
    response_model=RoomFull,
    tags=["room"],
)
def update_room(
    room_id: int,
    room: RoomUpdate,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Update an existing room.

        Args:
            db : Session
                Current database
            room : RoomUpdate
                RoomUpdate object with all
                the optional data to update for the room
            room_id : int
                ID of the room to update

        Returns:
            str : RoomFull
                RoomFull object with all info of the newly updated room
    """
    return room_utils.update_room(db=db, room_id=room_id, room=room)


@router.delete(
    "/rooms/{room_id}",
    summary="Delete an existing room",
    response_model=ResultSchema,
    tags=["room"],
)
def delete_room(
    room_id: int,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Delete an existing room.

        Args:
            db: Session
                Current database
            room_id: int
                ID of the room to delete

        Returns:
            result : str
                string with info about successful deletion
    """
    return room_utils.delete_room(room_id=room_id, db=db)


@router.get(
    "/rooms/{room_id}/booking_status",
    summary="Get booking status of a room",
    response_model=ResultSchema,
    tags=["room"],
)
def get_room_booking_status(
    room_id: int,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Get booking status of a room.

        Args
        db: Session
            Current database

        room_id: int
            ID of the room to get the booking status of

        Returns:
            result : dict
                result with the booking status of the room
    """
    return room_utils.get_room_booking_status(room_id=room_id, db=db)


@router.get(
    "/rooms/{room_id}/cleanliness_status",
    summary="Get cleanliness status of a room",
    response_model=ResultSchema,
    tags=["room"],
)
def get_room_cleanliness_status(
    room_id: int,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Get cleanliness status of a room.

        Args:
            db: Session
                Current database
            room_id: int
                ID of the room to get the cleanliness status of

        Returns:
            result : dict
                result with the cleanliness status of the room
    """
    return room_utils.get_room_cleanliness_status(room_id=room_id, db=db)


@router.get(
    "/rooms/{room_id}/guest",
    summary="Get current resident of the room",
    response_model=ClientFull,
    tags=["room"],
)
def get_room_guest_now(
    room_id: int,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Check who is currently living in the room.
    If room is vacant, raises an exception.

        Args:
            skip : int
                Specifies the number of qualifying rows to exclude.
            limit : int
                If given, no more than that many rows will be returned.
            db: Session
                Current database
            room_id : int
                ID of the room to get the current resident of
        Returns:
            guest : ClientFull
                guest who is currently living in the room
    """
    return room_utils.get_room_guest_now(db=db, room_id=room_id)


# Room types routers


@router.get(
    "/room_types",
    summary="Get all room types",
    response_model=List[RoomTypeList],
    tags=["room_type"],
)
def get_room_types(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Get all room types.

        Args:
            skip : int
                Specifies the number of qualifying rows to exclude.
            limit : int
                If given, no more than that many rows will be returned.
            db: Session
                Current database

        Returns:
            List[RoomTypeList]
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
def get_room_type(
    room_type_id: int,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Get an existing room type by ID.

        Args:
            db : Session
                Current database

            room_type_id : int
                ID of the room type to retrieve

        Returns:
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
def create_room_type(
    room_type: RoomTypeCreate,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Create a new room type.

        Args:
            db : Session
                Current database

            room_type : RoomTypeCreate
                RoomTypeCreate object with all the necessary data
                to create a new room type

        Returns:
            RoomTypeFull
                RoomTypeFull object with all info
                of the newly created room type
    """
    return room_utils.create_room_type(db=db, room_type=room_type)


@router.put(
    "/room_types/{room_type_id}",
    summary="Update an existing room type",
    response_model=RoomTypeFull,
    tags=["room_type"],
)
def update_room_type(
    room_type_id: int,
    room_type: RoomTypeUpdate,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Update an existing room type.

        Args:
            db : Session
                Current database
            room_type : RoomTypeUpdate
                RoomTypeUpdate object with all the optional data
                to update for the room type
            room_id : int
                ID of the room to update

        Returns:
            RoomTypeFull
                RoomTypeFull object with all
                info of the newly updated room type
    """
    return room_utils.update_room_type(
        db=db, room_type_id=room_type_id, room_type=room_type
    )


@router.delete(
    "/room_types/{room_type_id}",
    summary="Delete an existing room type",
    response_model=ResultSchema,
    tags=["room_type"],
)
def delete_room_type(
    room_type_id: int,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Delete an existing room type.

        Args:
            db: Session
                Current database
            room_type_id: int
                ID of the room type to delete

        Returns:
            str
                string with info about successful deletion
    """
    return room_utils.delete_room_type(room_type_id=room_type_id, db=db)


@router.get(
    "/room_types/{room_type_id}/features",
    summary="Get all features of a room type",
    response_model=List[FeatureFull],
    tags=["room_type"],
)
def get_features_for_roomtype(
    room_type_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Get all features of an existing room type.

        Args:
            db: Session
                Current database
            room_type_id: int
                ID of the room type
            skip : int
                Specifies the number of qualifying rows to exclude.
            limit : int
                If given, no more than that many rows will be returned.

        Returns:
            List[FeatureFull]
                list with all features of a room
    """
    return misc_crud.get_features_for_roomtype(
        db=db, room_type_id=room_type_id, skip=skip, limit=limit
    )


@router.post(
    "/room_types/{room_type_id}/features",
    summary="Add an existing feature to a room type",
    response_model=ResultSchema,
    tags=["room_type"],
)
def add_feature_to_roomtype(
    room_type_id: int,
    feature_id: int,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Add an existing feature to an existing room type.

        Args:
            db: Session
                Current database
            room_type_id: int
                ID of the room type
            feature_id: int
                ID of the feature to add

        Returns:
            result : dict
                result with successul addition
    """
    return misc_crud.add_feature_to_room_type(
        db=db, room_type_id=room_type_id, feature_id=feature_id
    )


@router.delete(
    "/room_types/{room_type_id}/features",
    summary="Delete an existing feature from a room type",
    response_model=ResultSchema,
    tags=["room_type"],
)
def delete_feature_from_roomtype(
    room_type_id: int,
    feature_id: int,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Delete an existing feature to an existing room type.

        Args:
            db: Session
                Current database
            room_type_id: int
                ID of the room type
            feature_id: int
                ID of the feature to delete

        Returns:
            result : dict
                result with successul addition
    """
    return misc_crud.delete_feature_from_room_type(
        db=db, room_type_id=room_type_id, feature_id=feature_id
    )


# Features routers


@router.get(
    "/features",
    summary="Get all features",
    response_model=List[FeatureFull],
    tags=["feature"],
)
def get_features(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Get all existing features.

        Args:
            db : Session
                Current database
            feature_id : int
                ID of the feature to retrieve

        Returns:
            FeatureFull
                FeatureFull object with all info about the room type
    """
    features = room_utils.get_features(db=db, skip=skip, limit=limit)
    return features


@router.get(
    "/features/{feature_id}",
    summary="Get feature by ID",
    response_model=FeatureFull,
    tags=["feature"],
)
def get_feature(
    feature_id: int,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Get an existing feature by ID.

        Args:
            db : Session
                Current database
            feature_id : int
                ID of the feature to retrieve

        Returns:
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
def create_feature(
    feature: FeatureCreate,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Create a new feature.

        Args:
            db : Session
                Current database

            feature : FeatureCreate
                FeatureCreate object with all the necessary data
                to create a new room type

        Returns:
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
    feature_id: int,
    feature: FeatureUpdate,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Update an existing feature.

        Args:
            db : Session
                Current database

            feature : FeatureUpdate
                RoomTypeUpdate object with all the optional data
                to update for the room type
            feature_id : int
                ID of the feature to update

        Returns:
            FeatureFull
                FeatureFull object with all info of the newly updated feature
    """
    return room_utils.update_feature(
        db=db, feature_id=feature_id, feature=feature
    )


@router.delete(
    "/features/{feature_id}",
    summary="Delete an existing feature",
    response_model=ResultSchema,
    tags=["feature"],
)
def delete_feature(
    feature_id: int,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Delete an existing feature.

        Args:
            db: Session
                Current database

            feature_id: int
                ID of the feature to delete

        Returns:
            result : dict
                result with info about successful deletion
    """
    return room_utils.delete_feature(feature_id=feature_id, db=db)


@router.get(
    "/facilities",
    summary="Get all facilities",
    response_model=List[FacilityFull],
    tags=["facility"],
)
def get_facilities(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Get all hotel facilities.

        Args:
            skip : int
                Specifies the number of qualifying rows to exclude.
            limit : int, optional
                If given, no more than that many rows will be returned.
            db: Session
                Current database

        Returns:
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
def get_facility(
    facility_id: int,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Get an existing facility by ID.

        Args:
            db : Session
                Current database

            facility_id : int
                ID of the hotel facility to retrieve

        Returns:
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
def create_facility(
    facility: FacilityCreate,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Create a new facility.

        Args:
            db : Session
                Current database
            feature : FacilityCreate
                FacilityCreate object with all the necessary
                data to create a new hotel facility

        Returns:
            FacilityFull
                FacilityFull object with
                all info of the newly created hotel facility
    """
    return room_utils.create_facility(db=db, facility=facility)


@router.put(
    "/facilities/{facility_id}",
    summary="Update an existing facility",
    response_model=FacilityFull,
    tags=["facility"],
)
def update_facility(
    facility_id: int,
    facility: FacilityUpdate,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Update an existing facility.

        Args:
            db: Session
                Current database

            facility_id: int
                ID of the facility to update

        Returns:
            FacilityFull
                FacilityFull object with all
                info about the newly updatedfacility
    """
    return room_utils.update_facility(
        db=db, facility_id=facility_id, facility=facility
    )


@router.delete(
    "/facilities/{facility_id}",
    summary="Delete an existing facility",
    response_model=ResultSchema,
    tags=["facility"],
)
def delete_facility(
    facility_id: int,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Delete an existing facility.

        Args:
        db: Session
            Current database

        facility_id: int
            ID of the facility to delete

        Returns:
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
    user: UserAuth = Depends(get_current_user),
):
    """
    Get all bookings for specified room.

        Args:
            skip : int
                Specifies the number of qualifying rows to exclude.
            limit : int
                If given, no more than that many rows will be returned.
            db: Session
                Current database

            room_id : int
                ID of the room to get the bookings for
        Returns:
            List[BookingFull]
                a list of all bookings that
                correspond to the room with ID of {room_id}
    """
    return misc_crud.get_bookings_for_room(
        db=db, room_id=room_id, skip=skip, limit=limit
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
    user: UserAuth = Depends(get_current_user),
):
    """
    Get all features for specified room.

    Args:
        skip : int
            Specifies the number of qualifying rows to exclude.
        limit : int
            If given, no more than that many rows will be returned.
        db: Session
            Current database

        room_id: int
            ID of the room type to get the features for

    Returns:
        List[FeatureFull]
            a list of all features that
            correspond to the room with ID of {room_id}
    """
    return misc_crud.get_features_for_room(
        db=db, room_id=room_id, skip=skip, limit=limit
    )


@router.get(
    "/features/{feature_id}/room_types",
    response_model=List[RoomTypeList],
    summary="Get all room types which have a feature",
    tags=["feature"],
)
def get_room_types_with_feature(
    feature_id: int,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Get all room types which have a specific feature.

        Args:
            feature_id: int
                ID of the feature
            db: Session
                Current database

        Returns:
            List[RoomTypeFull]
                list of sorted rooms
    """
    return misc_crud.get_room_types_with_feature(db=db, feature_id=feature_id)


@router.post(
    "/rooms/filter",
    summary="Filter rooms by any parameters",
    response_model=List[RoomFull],
    tags=["room"],
)
def filter_rooms(
    room: RoomFilter,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Filter rooms.

        Args:
            room: RoomFilter
                RoomFilter with optional parameters of filtering
            db: Session
                Current database

        Returns:
            List[RoomFull]
                list of sorted rooms
    """
    return room_utils.filter_rooms(db=db, room=room)


@router.get(
    "/rooms/sort",
    response_model=List[RoomFull],
    tags=["room"],
    summary="Sort rooms",
)
def sort_rooms(
    order: str,
    order_by: str,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Sort rooms.

        Args:
            order : str
                Specified order -> asc or desc.
            order_by : str
                Value to order by.
            db: Session
                Current database

        Returns:
            List[RoomTypeFull]
                list of sorted rooms
    """
    return room_utils.sort_rooms(db=db, order=order, order_by=order_by)


@router.post(
    "/room_types/filter/by_price",
    response_model=List[RoomTypeFull],
    tags=["room_type"],
    summary="Filter room types by price",
)
def filter_room_types_by_price(
    operator: str,
    value: float,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Filter room types by price.

        Args:
            operator : str
                Equivalent to ge, le, lt etc.
            value : str
                Value to filter by.
            db: Session
                Current database

        Returns:
            List[RoomTypeFull]
                list of filtered room types by price
    """
    return room_utils.filter_room_types_by_price(
        db=db, operator=operator, value=value
    )


@router.post(
    "/room_types/sort",
    response_model=List[RoomTypeFull],
    tags=["room_type"],
    summary="Sort room types",
)
def sort_room_types(
    order: str,
    order_by: str,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Sort room types.

        Args:
            order : str
                Specified order -> asc or desc.
            order_by : str
                Value to order by.
            db: Session
                Current database

        Returns:
            List[RoomTypeFull]
                list of sorted room types
    """
    return room_utils.sort_room_types(db=db, order=order, order_by=order_by)


@router.get(
    "/rooms/{room_id}/availability",
    response_model=ResultSchema,
    tags=["room"],
    summary="Check room availability by date",
)
def check_room_availability_by_date(
    start_date: datetime.date,
    end_date: datetime.date,
    room_id: int,
    db: Session = Depends(get_db),
):
    return room_utils.check_room_availability_by_date(
        start_date=start_date, end_date=end_date, room_id=room_id, db=db
    )
