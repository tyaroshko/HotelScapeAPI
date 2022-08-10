"""Endpoints for Client."""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud import client_utils
from db import get_db
from schemas.client_schemas import ClientCreate, ClientFull, ClientUpdate

router = APIRouter()


@router.get(
    "/clients",
    summary="Get all clients",
    tags=["client"],
    response_model=List[ClientFull],
)
def get_clients(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Get all clients.

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
    List[ClientFull]
        a list of all clients that are present in the db
    """
    clients = client_utils.get_clients(db=db, skip=skip, limit=limit)
    return clients


@router.get(
    "/clients/{client_id}",
    summary="Get a client by ID",
    tags=["client"],
    response_model=ClientFull,
)
def get_client(client_id: int, db: Session = Depends(get_db)):
    """
    Get a specific client by ID.

    Parameters
    ----------
    db : Session
        Current database

    client_id : int
        ID of the client to retrieve

    Returns
    -------
    ClientFull
        ClientFull object with all info about the specified client
    """
    client = client_utils.get_client(db=db, client_id=client_id)
    return client


@router.post(
    "/clients",
    summary="Create a new client",
    tags=["client"],
    response_model=ClientFull,
)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    """
    Create a new client.

    Parameters
    ----------
    db : Session
        Current database

    client : ClientCreate
        ClientCreate with all the necessary info
        to create a new client

    Returns
    -------
    ClientFull
        ClientFull object with all info about the newly created client
    """
    return client_utils.create_client(db=db, client=client)


@router.put(
    "/clients/{client_id}",
    summary="Update an existing client",
    tags=["client"],
    response_model=ClientFull,
)
def update_client(
    client_id: int, client: ClientUpdate, db: Session = Depends(get_db)
):
    """
    Update an existing client.

    Parameters
    ----------
    db : Session
        Current database

    client : Client
        Invoice object with all the optional data to update for the invoice
    client_id : int
        ID of the client to update

    Returns
    -------
    ClientFull
        ClientFull object with all info about the newly updated client
    """
    return client_utils.update_client(
        db=db, client_id=client_id, client=client
    )


@router.delete(
    "/clients/{client_id}",
    summary="Delete an existing client",
    tags=["client"],
    response_model=str,
)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    """
    Remove an existing client.

    Parameters
    ----------
    db: Session
        Current database

    invoice_id: int
        ID of the client to delete

    Returns
    -------
    str
        string with info about successful deletion
    """
    return client_utils.delete_client(client_id=client_id, db=db)
