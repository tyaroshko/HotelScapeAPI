import enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Enum

from db import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    description = Column(String)
    room_type_id = Column(Integer, ForeignKey("room_types.id"), nullable=False)
    room_type_name = Column(String, ForeignKey("room_types.name"), nullable=False)
    current_price = Column(Float, nullable=False)
    is_free = Column(Boolean, default=False)

class NumberOfBeds(enum.Enum):
    single_bed = 1
    double_beds = 2
    twin_beds = 3
    king_size_bed = 4

class RoomType(Base):
    __tablename__ = "room_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    number_of_beds = Column(Enum(NumberOfBeds))
    satelite_tv = Column(Boolean, default=False)
    minibar = Column(Boolean, default=False)
    air_conditiong_or_fan_cooling = Column(Boolean, default=False)
    in_room_safe = Column(Boolean, default=False)
    tea_coffee_making = Column(Boolean, default=False)
