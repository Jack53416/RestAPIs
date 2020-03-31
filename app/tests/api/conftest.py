import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app import models
from app.core.jwt import create_user_access_token
from app.tests.utils.factories import UserFactory


@pytest.fixture
def app() -> FastAPI:
    from app.main import app
    return app


@pytest.fixture
def client(app) -> TestClient:
    return TestClient(app)


@pytest.fixture(scope='class')
def admin_user(top_level_session) -> models.User:
    return UserFactory.create(is_superuser=True)


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
