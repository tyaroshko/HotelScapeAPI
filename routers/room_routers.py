from math import factorial
from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy import String
from sqlalchemy.orm import Session
from crud import room_utils
from db import get_db
from schemas.room_schemas import (
    FacilityCreate,
    FacilityFull,
    FeatureFull,
    RoomFilter,
    RoomFull,
    RoomCreate,
    RoomTypeFull,
    RoomTypeCreate,
    FeatureCreate,
)
from typing import List

router = APIRouter()

# Room routers


@router.get("/rooms", response_model=List[RoomFull])
def get_rooms(skip: int = 0, limit: int = 500, db: Session = Depends(get_db)):
    rooms = room_utils.get_rooms(db=db, skip=skip, limit=limit)
    return rooms


@router.get("/rooms/{room_id}", response_model=RoomFull)
def get_room(room_id: int, db: Session = Depends(get_db)):
    return room_utils.get_room(db=db, room_id=room_id)


@router.post("/rooms", response_model=RoomFull)
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    return room_utils.create_room(db=db, room=room)


@router.put("/rooms/{room_id}", response_model=RoomFull)
def update_room(room_id: int, room: RoomCreate, db: Session = Depends(get_db)):
    return room_utils.update_room(db=db, room_id=room_id, room=room)


@router.delete("/rooms/{room_id}", response_model=str)
def delete_room(room_id: int, db: Session = Depends(get_db)):
    return room_utils.delete_room(room_id=room_id, db=db)


# @router.post("/rooms/filter")
# def filter_rooms(filter: RoomFilter, db: Session = Depends(get_db)):
#     return room_utils.get_rooms_filter(db=db, filter=filter)


@router.get("/rooms/{room_id}/booking_status", response_model=str)
def get_room_booking_status(room_id: int, db: Session = Depends(get_db)):
    return room_utils.get_room_booking_status(room_id=room_id, db=db)


@router.get("/rooms/{room_id}/cleanliness_status", response_model=str)
def get_room_cleanliness_status(room_id: int, db: Session = Depends(get_db)):
    return room_utils.get_room_cleanliness_status(room_id=room_id, db=db)


# Room types routers


@router.get("/room_types", response_model=List[RoomTypeFull])
def get_room_types(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    room_types = room_utils.get_room_types(db=db, skip=skip, limit=limit)
    return room_types


@router.get("/room_types/{room_type_id}", response_model=RoomTypeFull)
def get_room_type(room_type_id: int, db: Session = Depends(get_db)):
    room_type = room_utils.get_room_type(db=db, room_type_id=room_type_id)
    return room_type


@router.post("/room_types", response_model=RoomTypeFull)
def create_room_type(room_type: RoomTypeCreate, db: Session = Depends(get_db)):
    return room_utils.create_room_type(db=db, room_type=room_type)


@router.put("/room_types/{room_type_id}", response_model=RoomTypeFull)
def update_room_type(
    room_type_id: int, room_type: RoomTypeCreate, db: Session = Depends(get_db)
):
    return room_utils.update_room_type(
        db=db, room_type_id=room_type_id, room_type=room_type
    )


@router.delete("/room_types/{room_type_id}")
def delete_room_type(room_type_id: int, db: Session = Depends(get_db)):
    return room_utils.delete_room_type(room_type_id=room_type_id, db=db)


# Features routers


@router.get("/features", response_model=List[FeatureFull])
def get_features(skip: int = 0, limit: int = 0, db: Session = Depends(get_db)):
    features = room_utils.get_features(db=db, skip=skip, limit=limit)
    return features


@router.get("/features/{feature_id}", response_model=FeatureFull)
def get_feature(feature_id: int, db: Session = Depends(get_db)):
    feature = room_utils.get_feature(db=db, feature_id=feature_id)
    return feature


@router.post("/features", response_model=FeatureFull)
def create_feature(feature: FeatureCreate, db: Session = Depends(get_db)):
    return room_utils.create_feature(db=db, feature=feature)


@router.put("/features/{feature_id}", response_model=FeatureFull)
def update_feature(
    feature_id: int, feature: FeatureCreate, db: Session = Depends(get_db)
):
    return room_utils.update_feature(
        db=db, feature_id=feature_id, feature=feature
    )


@router.delete("/features/{feature_id}")
def delete_feature(feature_id: int, db: Session = Depends(get_db)):
    return room_utils.delete_feature(feature_id=feature_id, db=db)


@router.get("/facilities", response_model=List[FacilityFull])
def get_facilities(
    skip: int = 0, limit: int = 0, db: Session = Depends(get_db)
):
    facilities = room_utils.get_facilities(db=db, skip=skip, limit=limit)
    return facilities


@router.get("/facilities/{facility_id}", response_model=FacilityFull)
def get_facility(facility_id: int, db: Session = Depends(get_db)):
    facility = room_utils.get_facility(db=db, facility_id=facility_id)
    return facility


@router.post("/facilities", response_model=FacilityFull)
def create_facility(facility: FacilityCreate, db: Session = Depends(get_db)):
    return room_utils.create_facility(db=db, facility=facility)


@router.put("/facilities/{facility_id}", response_model=FacilityFull)
def update_facility(
    facility_id: int, facility: FacilityCreate, db: Session = Depends(get_db)
):
    return room_utils.update_facility(
        db=db, facility_id=facility_id, facility=facility
    )


@router.delete("/facilities/{facility_id}")
def delete_facility(facility_id: int, db: Session = Depends(get_db)):
    return room_utils.delete_facility(facility_id=facility_id, db=db)
