import logging

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest_factoryboy import register
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core import config
from app.core.jwt import create_user_access_token
from app.db.base_class import Base
from app.db.session import SessionLocal
from app.schemas import User
from app.tests.utils.session import TestSession
from .utils.factories import UserFactory

logger = logging.getLogger('fixtures')
logger.setLevel(logging.INFO)

register(UserFactory)


@pytest.fixture(scope='session')
def engine():
    return create_engine(config.TEST_DATABASE_URI, connect_args={"check_same_thread": False})


@pytest.fixture(scope='session')
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(scope='session')
def connection(engine):
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(scope='function', autouse=False)
def db_session(connection, tables):
    # begin the nested transaction
    transaction = connection.begin()
    SessionLocal.configure(autocommit=False, autoflush=False, bind=connection)

    session: Session = SessionLocal()
    # session.begin_nested()
    yield session
    # roll back the broader transaction
    # session.rollback()
    transaction.rollback()
    TestSession.remove()


@pytest.fixture
def app() -> FastAPI:
    from app.main import app
    return app


@pytest.fixture
def client(app) -> TestClient:
    return TestClient(app)


@pytest.fixture
def test_user(user_factory, db_session) -> User:
    return user_factory(is_superuser=True)


@pytest.fixture
def token(test_user: User) -> str:
    return create_user_access_token(test_user)


@pytest.fixture
def authorized_client(client: TestClient, token: str):
    client.headers = {
        "Authorization": f"Bearer {token}",
        **client.headers,
    }
    return client
