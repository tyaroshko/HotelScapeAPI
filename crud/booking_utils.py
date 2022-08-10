"""CRUD functions for Booking."""

import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from crud import client_utils, room_utils
from models.booking import Booking
from schemas.booking_schemas import BookingCreate, BookingUpdate


def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    """Get all bookings."""
    return db.query(Booking).offset(skip).limit(limit).all()


def get_booking(db: Session, booking_id: int):
    """Get booking by id."""
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
    if booking.start_date < datetime.date or booking.end_date < datetime.date:
        raise HTTPException(status_code=400, detail="Incorrect date")
    _booking = Booking(
        client_id=booking.client_id,
        room_id=booking.room_id,
        start_date=booking.start_date,
        end_date=booking.end_date,
        discount_percent=booking.discount_percent,
        total_price=booking.total_price,
        ts_created=datetime.datetime.now,
        ts_updated=datetime.datetime.now,
    )
    db.add(_booking)
    db.commit()
    db.refresh(_booking)
    return _booking


def update_booking(db: Session, booking_id: int, booking: BookingUpdate):
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
    if booking.start_date and booking.start_date > datetime.date:
        _booking.start_date = booking.start_date
    else:
        raise HTTPException(status_code=400, detail="Incorrect date")
    if booking.end_date:
        _booking.end_date = booking.end_date
    else:
        raise HTTPException(status_code=400, detail="Incorrect date")
    if booking.discount_percent:
        _booking.discount_percent = booking.discount_percent
    if booking.total_price:
        _booking.total_price = booking.total_price
    _booking.ts_updated = datetime.datetime.now
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
    return f"Successfully deleted booking with id {booking_id}"
