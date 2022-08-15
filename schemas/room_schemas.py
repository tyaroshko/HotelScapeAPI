"""Schemas for models associated with Room."""

from typing import List, Optional
from pydantic import BaseModel
from models.room import RoomAvailabilityStatus, RoomCleanlinessStatus

# Room schemas


class RoomBase(BaseModel):
    id: int
    room_type_id: int
    floor: int
    facility_id: int


class RoomList(RoomBase):
    class Config:
        orm_mode = True


class RoomFull(RoomBase):
    booking_status: RoomAvailabilityStatus
    cleanliness_status: RoomCleanlinessStatus

    class Config:
        orm_mode = True


class RoomCreate(RoomBase):
    description: Optional[str] = None
    booking_status: RoomAvailabilityStatus
    cleanliness_status: RoomCleanlinessStatus

    class Config:
        orm_mode = True


class RoomFilter(BaseModel):
    description: Optional[str]
    room_type_id: Optional[int]
    floor: Optional[int]
    facility_id: Optional[int]
    booking_status: Optional[RoomAvailabilityStatus]
    cleanliness_status: Optional[RoomCleanlinessStatus]

    class Config:
        orm_mode = True


class RoomUpdate(BaseModel):
    description: Optional[str]
    room_type_id: Optional[int]
    floor: Optional[int]
    facility_id: Optional[int]
    booking_status: Optional[RoomAvailabilityStatus]
    cleanliness_status: Optional[RoomCleanlinessStatus]


# Room type schemas


class RoomTypeBase(BaseModel):
    name: str
    capacity: str
    price: float


class RoomTypeFull(RoomTypeBase):
    id: int

    class Config:
        orm_mode = True


class RoomTypeList(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class RoomTypeCreate(RoomTypeBase):
    class Config:
        orm_mode = True


class RoomTypeFilter(BaseModel):
    id: Optional[int]
    name: Optional[str]
    capacity: Optional[str]
    price: Optional[float]


class RoomTypeUpdate(BaseModel):
    name: Optional[str]
    capacity: Optional[str]
    price: Optional[float]


# Feature schemas


class FeatureBase(BaseModel):
    name: str


class FeatureFull(FeatureBase):
    id: int

    class Config:
        orm_mode = True


class FeatureCreate(FeatureBase):
    class Config:
        orm_mode = True


class FeatureFilter(BaseModel):
    name: Optional[str]


class FeatureUpdate(BaseModel):
    name: Optional[str]


class FeatureList(BaseModel):
    list_of_features: List[FeatureFull]


# Facility schemas


class FacilityBase(BaseModel):
    name: str


class FacilityFull(FacilityBase):
    id: int

    class Config:
        orm_mode = True


class FacilityCreate(FacilityBase):
    class Config:
        orm_mode = True


class FacilityFilter(BaseModel):
    name: Optional[str]


class FacilityUpdate(BaseModel):
    name: Optional[str]
