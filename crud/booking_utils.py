"""CRUD functions for Booking."""

from typing import Optional
import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from crud import client_utils, room_utils
from models.booking import Booking
from schemas.booking_schemas import BookingCreate, BookingFilter


def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    """Get all bookings."""
    return db.query(Booking).offset(skip).limit(limit).all()


def get_booking(db: Session, booking_id: int):
    """Get booking by ID."""
    _booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not _booking:
        raise HTTPException(
            status_code=404, detail=f"No booking found with id {booking_id}"
        )
    return _booking


def create_booking(db: Session, booking: BookingCreate):
    """Create new booking."""
    if not client_utils.get_client(db=db, client_id=booking.client_id):
        raise HTTPException(
            status_code=404,
            detail=f"No client found with id {booking.client_id}",
        )
    if not room_utils.get_room(db=db, room_id=booking.room_id):
        raise HTTPException(
            status_code=404,
            detail=f"No room found with id {booking.room_id}",
        )
    if (
        booking.start_date < datetime.date.today()
        or booking.end_date <= datetime.date.today()
        or booking.end_date < booking.start_date
    ):
        raise HTTPException(status_code=400, detail="Incorrect date")
    length_of_stay = (booking.end_date - booking.start_date).days
    _room = room_utils.get_room(db=db, room_id=booking.room_id)
    _room_type = room_utils.get_room_type(
        db=db, room_type_id=_room.room_type_id
    )
    calculate_price = _room_type.price * length_of_stay
    _booking = Booking(
        client_id=booking.client_id,
        room_id=booking.room_id,
        start_date=booking.start_date,
        end_date=booking.end_date,
        total_price=calculate_price,
        ts_created=datetime.datetime.now(),
        ts_updated=datetime.datetime.now(),
    )
    db.add(_booking)
    db.commit()
    db.refresh(_booking)
    return _booking


def update_booking(db: Session, booking_id: int, booking: BookingCreate):
    """Update existing booking."""
    _booking = get_booking(db=db, booking_id=booking_id)
    if not _booking:
        raise HTTPException(
            status_code=404, detail=f"No booking found with id {booking_id}"
        )
    if not client_utils.get_client(db=db, client_id=booking.client_id):
        raise HTTPException(
            status_code=404,
            detail=f"No client with id {booking.client_id} found",
        )
    if not room_utils.get_room(db=db, room_id=booking.room_id):
        raise HTTPException(
            status_code=404,
            detail=f"No room with id {booking.room_id} found",
        )
    if booking.client_id:
        _booking.client_id = booking.client_id
    if booking.start_date and booking.start_date > datetime.date.today():
        _booking.start_date = booking.start_date
    else:
        raise HTTPException(status_code=400, detail="Incorrect date")
    if booking.end_date:
        _booking.end_date = booking.end_date
    else:
        raise HTTPException(status_code=400, detail="Incorrect date")
    if booking.total_price:
        _booking.total_price = booking.total_price
    _booking.ts_updated = datetime.datetime.now()
    db.commit()
    db.refresh(_booking)
    return _booking


def delete_booking(db: Session, booking_id: int):
    """Remove existing booking."""
    _booking = get_booking(db=db, booking_id=booking_id)
    if not _booking:
        raise HTTPException(
            status_code=404, detail=f"No booking found with id {booking_id}"
        )
    db.delete(_booking)
    db.commit()
    return {"result": f"Successfully deleted booking with id {booking_id}"}


def filter_bookings(db: Session, booking: Optional[BookingFilter]):
    """Filter bookings."""
    query = db.query(Booking)
    if booking.client_id:
        query = query.filter(Booking.client_id == booking.client_id)
    if booking.room_id:
        query = query.filter(Booking.room_id == booking.room_id)
    if booking.start_date:
        query = query.filter(Booking.start_date == booking.start_date)
    if booking.end_date:
        query = query.filter(Booking.end_date == booking.end_date)
    if booking.total_price:
        query = query.filter(Booking.total_price == booking.total_price)
    filtered_bookings = query.all()
    return filtered_bookings


def sort_bookings(db: Session, order: str, order_by: str):
    """Sort room types by its properties."""
    dct = {
        "id": Booking.id,
        "start_date": Booking.start_date,
        "end_date": Booking.end_date,
        "client_id": Booking.client_id,
        "room_id": Booking.room_id,
        "total_price": Booking.total_price,
        "ts_created": Booking.ts_created,
        "ts_updated": Booking.ts_updated,
    }
    if order_by not in dct.keys():
        raise HTTPException(
            status_code=400, detail="Such order_by is not supported"
        )
    if order == "desc":
        sorted_query = db.query(Booking).order_by(dct[order_by].desc())
    elif order == "asc":
        sorted_query = db.query(Booking).order_by(dct[order_by].asc())
    else:
        raise HTTPException(
            status_code=400, detail="Such order is not supported"
        )
    sorted_bookings = sorted_query.all()
    return sorted_bookings
