from typing import Any
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db import Base
from db import get_db
from auth.deps import get_current_user
from main import app
from db import (
    POSTGRES_PASSWORD,
    POSTGRES_SERVER,
    POSTGRES_TEST_DATABASE,
    POSTGRES_USER,
)
from routers import (
    auth_routers,
    room_routers,
    client_routers,
    booking_routers,
    invoice_routers,
)


def start_application():
    app = FastAPI()
    app.include_router(auth_routers.router)
    app.include_router(room_routers.router)
    app.include_router(client_routers.router)
    app.include_router(booking_routers.router)
    app.include_router(invoice_routers.router)
    return app


SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:"
    "{POSTGRES_PASSWORD}"
    f"@{POSTGRES_SERVER}/{POSTGRES_TEST_DATABASE}"
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client_not_auth(
    app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides = {}
    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def client_auth(
    app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    def user_auth():
        pass

    app.dependency_overrides[get_db] = _get_test_db
    app.dependency_overrides[get_current_user] = user_auth
    with TestClient(app) as client:
        yield client
