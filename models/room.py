from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float

from db import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    room_name = Column(String, index=True)
    description = Column(String)
    room_type_id = Column(Integer, ForeignKey("room_types.id"), nullable=False)
    room_type_name = Column(String, ForeignKey("room_types.name"), nullable=False)
    current_price = Column(Float, nullable=False)
    is_free = Column(Boolean, default=False)

class RoomType(Base):
    __tablename__ = "room_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
