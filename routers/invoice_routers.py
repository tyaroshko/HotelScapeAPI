"""Endpoints for Invoice."""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud import invoice_utils
from db import get_db
from schemas.invoice_schemas import InvoiceCreate, InvoiceFull, InvoiceUpdate
from schemas.user_schemas import ResultSchema, UserAuth
from auth.deps import get_current_user

router = APIRouter()


@router.get(
    "/invoices",
    summary="Get all issued invoices",
    tags=["invoice"],
    response_model=List[InvoiceFull],
)
def get_invoices(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Get all issued invoices.

        Args
            skip : int
                Specifies the number of qualifying rows to exclude.
            limit : int
                If given, no more than that many rows will be returned.
            db : Session
                Current database

        Returns:
            List[InvoiceFull]
                a list of all invoices issued that are present in the db
    """
    invoices = invoice_utils.get_invoices(db=db, skip=skip, limit=limit)
    return invoices


@router.get(
    "/invoices/{invoice_id}",
    summary="Get an invoice by ID",
    tags=["invoice"],
    response_model=InvoiceFull,
)
def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Get an issued invoice by ID.

        Args:
            db : Session
                Current database

            invoice_id : int
                ID of the invoice to retrieve

        Returns:
            InvoiceFull
                InvoiceFull object with all info about the invoice
    """
    invoice = invoice_utils.get_invoice(db=db, invoice_id=invoice_id)
    return invoice


@router.post(
    "/invoices",
    summary="Create a new invoice",
    tags=["invoice"],
    response_model=InvoiceFull,
)
def create_invoice(
    invoice: InvoiceCreate,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Issue a new invoice.

        Args:
            db : Session
                Current database
            invoice : InvoiceCreate
                InvoiceCreate with all the necessary info
                to issue a new invoice

        Returns:
            InvoiceFull
                InvoiceFull object with all info
                about the newly created invoice
    """
    return invoice_utils.create_invoice(db=db, invoice=invoice)


@router.put(
    "/invoices/{invoice_id}",
    summary="Update an existing invoice",
    tags=["invoice"],
    response_model=InvoiceFull,
)
def update_invoice(
    invoice_id: int,
    invoice: InvoiceUpdate,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Update an existing invoice.

        Args:
            db : Session
                Current database

            invoice : InvoiceUpdate
                Invoice object with all the
                optional data to update for the invoice
            invoice_id : int
                ID of the invoice to update

        Returns:
            InvoiceFull
                InvoiceFull object with all info of the newly updated invoice
    """
    return invoice_utils.update_invoice(
        db=db, invoice_id=invoice_id, invoice=invoice
    )


@router.delete(
    "/invoices/{invoice_id}",
    summary="Delete an existing invoice",
    tags=["invoice"],
    response_model=ResultSchema,
)
def delete_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):
    """
    Delete an existing invoice.

        Args:
            db: Session
                Current database

            invoice_id: int
                ID of the invoice to delete

        Returns:
            str
                string with info about successful deletion
    """
    return invoice_utils.create_invoice(invoice_id=invoice_id, db=db)
