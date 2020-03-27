from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette import status

from app.models import User as DBUser
from app.schemas import User


def test_token_valid(app: FastAPI, authorized_client: TestClient, test_user: DBUser):
    response = authorized_client.post(app.url_path_for('login:verify-token'))
    assert response.status_code == status.HTTP_200_OK
    assert User(**response.json()).json() == User(**test_user.__dict__).json()

