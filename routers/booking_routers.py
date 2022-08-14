"""Endpoints for Booking."""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud import booking_utils
from db import get_db
from schemas.booking_schemas import (
    BookingCreate,
    BookingFilter,
    BookingFull,
    BookingList,
    BookingUpdate,
)
from auth.deps import reuseable_oauth
from schemas.user_schemas import ResultSchema, UserAuth
from auth.deps import get_current_user

router = APIRouter()


@router.get(
    "/bookings",
    summary="Get all bookings",
    response_model=List[BookingList],
    tags=["booking"],
)
def get_bookings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Get all bookings.

        Args
            skip : int
                Specifies the number of qualifying rows to exclude.
            limit : int
                If given, no more than that many rows will be returned.
            db : Session
                Current database

        Returns:
            List[BookingList]
                a list of all bookings issued that are present in the db
    """
    bookings = booking_utils.get_bookings(db=db, skip=skip, limit=limit)
    return bookings


@router.get(
    "/bookings/{booking_id}",
    summary="Get booking by ID",
    response_model=BookingFull,
    tags=["booking"],
)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Get a booking by ID.

        Args:
            db : Session
                Current database
            booking_id : int
                ID of the booking to retrieve

        Returns:
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
def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Create a new booking.

        Args:
            db : Session
                Current database
            booking : BookingCreate
                BookingCreate with all the necessary info
                to create a new booking

        Returns:
            BookingFull
                BookingFull object with
                all info about the newly created booking
    """
    return booking_utils.create_booking(db=db, booking=booking)


@router.put(
    "/bookings/{booking_id}",
    summary="Update a booking",
    response_model=BookingUpdate,
    tags=["booking"],
)
def update_booking(
    booking_id: int,
    booking: BookingUpdate,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Update an existing booking.

        Args:
            db : Session
                Current database
            booking : BookingUpdate
                Booking object with all
                the optional data to update for the booking
            booking_id : int
                ID of the booking to update

        Returns:
            BookingFull
                BookingFull object with all info of the newly updated booking
    """
    return booking_utils.update_booking(
        db=db, booking_id=booking_id, booking=booking
    )


@router.delete(
    "/bookings/{booking_id}",
    summary="Delete a booking",
    response_model=ResultSchema,
    tags=["booking"],
)
def delete_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Delete an existing booking.

        Args:
            db: Session
                Current database
            booking_id: int
                ID of the booking to delete

        Returns:
            result : dict
                result with info about successful deletion
    """
    return booking_utils.delete_booking(booking_id=booking_id, db=db)


@router.post(
    "/bookings/filter",
    response_model=List[BookingList],
    tags=["booking"],
    summary="Filter bookings",
)
def filter_bookings(
    booking: BookingFilter,
    db: Session = Depends(get_db),
    token: str = Depends(reuseable_oauth),
):
    """
    Filter bookings.

        Args:
            room: RoomFilter
                BookingFilter with optional parameters of filtering
            db: Session
                Current database

        Returns:
            List[BookingList]
                list of sorted bookings
    """
    return booking_utils.filter_bookings(db=db, booking=booking)


@router.get(
    "/bookings/sort",
    response_model=List[BookingFull],
    tags=["booking"],
    summary="Sort bookings",
)
def sort_bookings(
    order: str,
    order_by: str,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Sort bookings.

        Args:
            order : str
                Specified order -> asc or desc.
            order_by : str
                Value to order by.
            db: Session
                Current database

        Returns:
            List[BookingFull]
                list of sorted bookings
    """
    return booking_utils.sort_bookings(db=db, order=order, order_by=order_by)
