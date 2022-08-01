from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from crud import crud
from db import get_db
from models.room import Room
from schemas.schemas import RoomCreate, RoomTypeCreate

router = APIRouter()


@router.get("/rooms")
async def get_all_rooms(
    skip: int = 0, limit: int = 0, db: Session = Depends(get_db)
):
    rooms = crud.get_all_rooms(db=db, skip=skip, limit=limit)
    return rooms


@router.get("/rooms/{room_id}")
async def get_room(room_id: int, db: Session = Depends(get_db)):
    return db.query(Room).filter(Room.id == room_id).first()


@router.post("/rooms")
async def create_new_room(room: RoomCreate, db: Session = Depends(get_db)):
    return crud.create_room(db=db, room=room)


@router.delete("/rooms/{room_id}")
async def delete_room(room_id: int, db: Session = Depends(get_db)):
    return crud.remove_room(room_id=room_id, db=db)


@router.post("/room_types")
async def create_room_type(
    room_type: RoomTypeCreate, db: Session = Depends(get_db)
):
    return crud.create_room_type(db=db, room_type=room_type)


@router.get("/room_types/{room_type_id}")
async def get_room_type_by_id(
    room_type_id: int, db: Session = Depends(get_db)
):
    room_type = crud.get_room_type_by_id(db=db, room_type_id=room_type_id)
    if room_type is None:
        raise HTTPException(status_code=404, detail="Room type not found")
    return room_type


@router.get("/room_types")
async def get_room_types(
    skip: int = 0, limit: int = 0, db: Session = Depends(get_db)
):
    room_types = crud.get_all_room_types(db=db, skip=skip, limit=limit)
    return room_types


@router.delete("/room_types/{room_type_id}")
async def delete_room_type(room_type_id: int, db: Session = Depends(get_db)):
    return crud.remove_room_type(room_type_id=room_type_id, db=db)
