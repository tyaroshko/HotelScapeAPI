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
    """Create new client."""
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
    """Update existing client."""
    _client = get_client(db=db, client_id=client_id)
    if not _client:
        raise HTTPException(
            status_code=404, detail=f"No client found with id {client_id}"
        )
    if client.first_name:
        _client.first_name = client.first_name
    if client.last_name:
        _client.last_name = client.last_name
    if client.email:
        _client.email = client.email
    if client.phone:
        _client.phone = client.phone
    if client.address:
        _client.address = client.address
    db.commit()
    db.refresh(_client)
    return _client


def delete_client(db: Session, client_id: int):
    """Remove existing client."""
    _client = get_client(db=db, client_id=client_id)
    if not _client:
        raise HTTPException(
            status_code=404, detail=f"No client found with id {client_id}"
        )
    db.delete(_client)
    db.commit()
    return {"result": f"Successfully deleted client with id {client_id}"}
