import datetime
import logging

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app import crud
from app.core import config
from app.core.jwt import create_user_access_token
from app.db.base_class import Base
from app.schemas import User, UserCreate

logger = logging.getLogger('fixtures')
logger.setLevel(logging.INFO)


@pytest.fixture(scope='session')
def engine():
    return create_engine(config.TEST_DATABASE_URI, connect_args={"check_same_thread": False})


@pytest.fixture(scope='session')
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def connection(engine, tables):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    connection = engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    yield connection
    # put back the connection to the connection pool
    connection.close()
    # roll back the broader transaction
    transaction.rollback()


@pytest.fixture
def db_session(connection):
    # use the connection with the already started transaction
    session = Session(autocommit=False, autoflush=False, bind=connection)
    yield session
    session.close()


@pytest.fixture(autouse=True)
def _mock_db_connection(mocker, connection):
    """
    This will alter application database connection settings, once and for all the tests
    in unit tests module.
    :param mocker: pytest-mock plugin fixture
    :param engine: sql alchemy engine class
    :return: True upon successful monkey-patching
    """
    test_session = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    mocker.patch('app.api.utils.db.SessionLocal', test_session)
    return True


@pytest.fixture
def app() -> FastAPI:
    from app.main import app
    return app


@pytest.fixture
def client(app) -> TestClient:
    return TestClient(app)


@pytest.fixture
def test_user(db_session: Session) -> User:
    user_in = UserCreate(
        email=config.FIRST_SUPERUSER,
        username=config.FIRST_SUPERUSER,
        first_name=config.FIRST_SUPERUSER,
        last_name=config.FIRST_SUPERUSER,
        is_staff=True,
        is_active=True,
        is_eeci=True,
        date_joined=datetime.datetime.now(datetime.timezone.utc),
        password=config.FIRST_SUPERUSER_PASSWORD,
        is_superuser=True,
    )
    return crud.user.create(db_session, obj_in=user_in)


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
