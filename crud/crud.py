from pkg_resources import safe_extra
from psycopg2 import IntegrityError
from sqlalchemy.orm import Session

from models.room import Room, RoomType
from schemas.schemas import RoomCreate, RoomTypeCreate, RoomTypeBase


def get_all_rooms(db: Session, skip: int = 0, limit: int = 0):
    return db.query(Room).offset(skip).limit(limit).all()


def get_room(db: Session, room_id: int):
    return db.query(Room).filter(Room.id == room_id).first()


def create_room(db: Session, room: RoomCreate):
    _room = Room(
        id = room.id,
        description = room.description,
        room_type_id = room.room_type_id,
        room_type_name = room.room_type_name,
        current_price = room.current_price
    )
    db.add(_room)
    db.commit()
    db.refresh(_room)
    return _room

def get_all_room_types(db: Session, skip: int = 0, limit: int = 0):
    return db.query(RoomType).offset(skip).limit(limit).all()

def get_room_type_by_id(db: Session, room_type_id: int):
    return db.query(RoomType).filter(RoomType.id == room_type_id).first()

def create_room_type(db: Session, room_type: RoomTypeCreate):
    _room_type = RoomType(
        name = room_type.name,
        number_of_beds = room_type.number_of_beds,
        satelite_tv = room_type.satelite_tv,
        minibar = room_type.minibar,
        conditioner_or_fan = room_type.conditioner_or_fan,
        in_room_safe = room_type.in_room_safe,
        tea_coffee_making = room_type.tea_coffee_making
    )

    db.add(_room_type)
    try:
        db.commit()
    except IntegrityError:
        return "Invalid request"
    db.refresh(_room_type)
    return _room_type

def remove_room_type(db: Session, room_type_id: int):
    _room_type = get_room_type_by_id(db=db, room_type_id=room_type_id)
    db.delete(_room_type)
    db.commit()
    return _room_type
