"""CRUD functions for Client."""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.client import Client
from schemas.client_schemas import ClientCreate


def get_clients(db: Session, skip: int = 0, limit: int = 100):
    """Get all clients."""
    return db.query(Client).offset(skip).limit(limit).all()


def get_client(db: Session, client_id: int):
    """Get client by id."""
    _client = db.query(Client).filter(Client.id == client_id).first()
    if not _client:
        raise HTTPException(
            status_code=404, detail=f"No client found with id {client_id}"
        )
    return _client


def create_client(db: Session, client: ClientCreate):
    """Create new booking."""
    _client = Client(
        first_name=client.first_name,
        last_name=client.last_name,
        email=client.email,
        phone=client.phone,
        address=client.address,
    )
    db.add(_client)
    db.commit()
    db.refresh(_client)
    return _client


def update_client(db: Session, client_id: int, client: ClientCreate):
    """Update existing booking."""
    _client = get_client(db=db, client_id=client_id)
    if not _client:
        raise HTTPException(
            status_code=404, detail=f"No client found with id {client_id}"
        )
    _client.first_name = client.first_name
    _client.last_name = client.last_name
    _client.email = client.email
    _client.phone = client.phone
    _client.address = client.address
    db.commit()
    db.refresh(_client)
    return _client


def delete_client(db: Session, client_id: int):
    """Remove existing room."""
    _client = get_client(db=db, client_id=client_id)
    if not _client:
        raise HTTPException(
            status_code=404, detail=f"No client found with id {client_id}"
        )
    db.delete(_client)
    db.commit()
    return f"Successfully deleted client with id {client_id}"
