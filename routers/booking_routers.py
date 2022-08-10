"""Endpoints for Booking."""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud import booking_utils
from db import get_db
from schemas.booking_schemas import BookingCreate, BookingFull, BookingUpdate

router = APIRouter()


@router.get(
    "/bookings",
    summary="Get all bookings",
    response_model=List[BookingFull],
    tags=["booking"],
)
def get_bookings(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Get all bookings.

    Parameters
    ----------
    skip : int
        Specifies the number of qualifying rows to exclude.
    limit : int
        If given, no more than that many rows will be returned.
    db : Session
        Current database

    Returns
    -------
    List[BookingFull]
        a list of all bookings issued that are present in the db
    """
    bookings = booking_utils.get_bookings(db=db, skip=skip, limit=limit)
    return bookings


@router.get(
    "/bookings/{booking_id}",
    summary="Get booking by id",
    response_model=BookingFull,
    tags=["booking"],
)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    """
    Get an booking by ID.

    Parameters
    ----------
    db : Session
        Current database

    booking_id : int
        ID of the booking to retrieve

    Returns
    -------
    BookingFull
        BookingFull object with all info about the booking
    """
    booking = booking_utils.get_booking(db=db, booking_id=booking_id)
    return booking


@router.post(
    "/bookings",
    summary="Create a new booking",
    response_model=BookingFull,
    tags=["booking"],
)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    """
    Create a new booking.

    Parameters
    ----------
    db : Session
        Current database

    booking : BookingCreate
        BookingCreate with all the necessary info
        to create a new booking

    Returns
    -------
    BookingFull
        BookingFull object with all info about the newly created booking
    """
    return booking_utils.create_booking(db=db, booking=booking)


@router.put(
    "/bookings/{booking_id}",
    summary="Update a booking",
    response_model=BookingFull,
    tags=["booking"],
)
def update_booking(
    booking_id: int, booking: BookingUpdate, db: Session = Depends(get_db)
):
    """
    Update an existing booking.

    Parameters
    ----------
    db : Session
        Current database

    booking : BookingUpdate
        Booking object with all the optional data to update for the booking
    booking_id : int
        ID of the booking to update

    Returns
    -------
    BookingFull
        BookingFull object with all info of the newly updated booking
    """
    return booking_utils.update_booking(
        db=db, booking_id=booking_id, booking=booking
    )


@router.delete(
    "/bookings/{booking_id}",
    summary="Delete a booking",
    response_model=str,
    tags=["booking"],
)
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    """
    Delete an existing booking.

    Parameters
    ----------
    db: Session
        Current database

    booking_id: int
        ID of the booking to delete

    Returns
    -------
    str
        string with info about successful deletion
    """
    return booking_utils.delete_booking(booking_id=booking_id, db=db)
