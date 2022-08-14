"""CRUD functions for Invoice."""

import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session

from crud import booking_utils, client_utils
from models.invoice import Invoice
from schemas.invoice_schemas import InvoiceCreate, InvoiceUpdate


def get_invoices(db: Session, skip: int = 0, limit: int = 100):
    """Get all invoices."""
    return db.query(Invoice).offset(skip).limit(limit).all()


def get_invoice(db: Session, invoice_id: int):
    """Get invoice by id."""
    _invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not _invoice:
        raise HTTPException(
            status_code=404, detail=f"No invoice found with id {invoice_id}"
        )
    return _invoice


def create_invoice(db: Session, invoice: InvoiceCreate):
    """Create new invoice."""
    if not booking_utils.get_booking(db=db, booking_id=invoice.booking_id):
        raise HTTPException(
            status_code=404,
            detail=f"No booking with id {invoice.booking_id} found",
        )
    if not client_utils.get_client(db=db, client_id=invoice.client_id):
        raise HTTPException(
            status_code=404,
            detail=f"No client with id {invoice.client_id} found",
        )
    _booking = booking_utils.get_booking(db=db, booking_id=invoice.booking_id)
    _invoice = Invoice(
        booking_id=invoice.booking_id,
        client_id=_booking.client_id,
        payment_method=invoice.payment_method,
        invoice_amount=_booking.total_price,
        ts_issued=datetime.datetime.now(),
    )
    db.add(_invoice)
    db.commit()
    db.refresh(_invoice)
    return _invoice


def update_invoice(db: Session, invoice_id: int, invoice: InvoiceUpdate):
    """Update existing invoice."""
    _invoice = get_invoice(db=db, invoice_id=invoice_id)
    if not _invoice:
        raise HTTPException(
            status_code=404, detail=f"No invoice found with id {invoice_id}"
        )
    if not booking_utils.get_booking(db=db, booking_id=invoice.booking_id):
        raise HTTPException(
            status_code=404,
            detail=f"No booking with id {invoice.booking_id} found",
        )
    if not client_utils.get_client(db=db, client_id=invoice.client_id):
        raise HTTPException(
            status_code=404,
            detail=f"No client with id {invoice.client_id} found",
        )
    if invoice.booking_id:
        _invoice.booking_id = invoice.booking_id
    if invoice.client_id:
        _invoice.client_id = invoice.client_id
    if invoice.payment_method:
        _invoice.payment_method = invoice.payment_method
    if invoice.invoice_amount:
        _invoice.invoice_amount = invoice.invoice_amount
    if invoice.ts_paid:
        _invoice.ts_paid = invoice.ts_paid
    db.commit()
    db.refresh(_invoice)
    return _invoice


def delete_invoice(db: Session, invoice_id: int):
    """Remove existing invoice."""
    _invoice = get_invoice(db=db, invoice_id=invoice_id)
    if not _invoice:
        raise HTTPException(
            status_code=404, detail=f"No invoice found with id {invoice_id}"
        )
    db.delete(_invoice)
    db.commit()
    return {"result": f"Successfully deleted invoice with id {invoice_id}"}
