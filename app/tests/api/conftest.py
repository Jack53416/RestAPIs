import pytest
from app import models
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core import config
from app.core.jwt import create_user_access_token
from app.core.security import get_password_hash
from app.tests.utils.factories import UserFactory
from app.tests.utils.session import TestSession


@pytest.fixture(autouse=True)
def patch_api_session(mocker, db_session):
    mocker.patch('app.api.utils.db.SessionLocal', TestSession)


@pytest.fixture
def app() -> FastAPI:
    from app.main import app
    return app


@pytest.fixture
def client(app) -> TestClient:
    return TestClient(app)


@pytest.fixture(scope='class')
def admin_user(top_level_session) -> models.User:
    return UserFactory.create(is_superuser=True, hashed_password=get_password_hash(config.FIRST_SUPERUSER_PASSWORD))


@pytest.fixture
def token(admin_user) -> str:
    return create_user_access_token(admin_user)


@pytest.fixture
def authorized_client(client: TestClient, token: str):
    client.headers = {
        "Authorization": f"Bearer {token}",
        **client.headers,
    }
    return client
