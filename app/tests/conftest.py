import logging

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest_factoryboy import register
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from app.core import config
from app.core.jwt import create_user_access_token
from app.core.security import get_password_hash
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
    engine = create_engine(config.TEST_DATABASE_URI, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)

    @event.listens_for(engine, "connect")
    def do_connect(dbapi_connection, connection_record):
        # disable pysqlite's emitting of the BEGIN statement entirely.
        # also stops it from emitting COMMIT before any DDL.
        dbapi_connection.isolation_level = None

    @event.listens_for(engine, "begin")
    def do_begin(conn):
        # emit our own BEGIN
        conn.execute("BEGIN")

    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(scope='class')
def top_level_session(engine, request):
    connection = engine.connect()
    transaction = connection.begin()
    SessionLocal.configure(bind=connection)
    session = TestSession()
    request.cls.Session = session
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def db_session(top_level_session: Session):
    top_level_session.begin_nested()

    @event.listens_for(top_level_session, 'after_transaction_end')
    def restart_savepoint(session: Session, transaction: any):
        if transaction.nested and not transaction._parent.nested:
            session.expire_all()
            session.begin_nested()

    yield top_level_session

    top_level_session.rollback()