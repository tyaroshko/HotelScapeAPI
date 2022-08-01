from typing import Optional, Union

from pydantic import BaseModel

from models.room import RoomType, NumberOfBeds

class RoomBase(BaseModel):
    id: int
    description: Optional[str]
    room_type_id: int
    room_type_name: str
    current_price: float

class RoomCreate(RoomBase):

    class Config:
        orm_mode = True

class RoomTypeBase(BaseModel):
    name: str
    number_of_beds: NumberOfBeds
    satelite_tv = False
    minibar = False
    conditioner_or_fan = False
    in_room_safe = False
    tea_coffee_making = False

class RoomTypeAdditionalInfo(RoomTypeBase):
    id: int

    class Config:
        orm_mode = True

class RoomTypeCreate(RoomTypeBase):

    class Config:
        orm_mode = True
