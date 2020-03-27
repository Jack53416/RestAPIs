from typing import List

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette import status

from app import crud
from app.db.paginator import Paginator
from app.models.user import User as DBUser
from app.schemas import User, UserCreate
from app.schemas.common import PaginatedResponse
from app.tests.utils.factories import UserFactory


def test_list_response(app: FastAPI, authorized_client: TestClient, test_user: DBUser):
    response = authorized_client.get(app.url_path_for('users:list-users'))
    assert response.status_code == status.HTTP_200_OK
    response = PaginatedResponse.parse_raw(response.content)
    assert response.count == 1
    assert response.page_size == Paginator.default_page_size
    assert response.pages == 1
    assert len(response.data) == 1
    assert User.parse_obj(test_user.__dict__) == User.parse_obj(response.data.pop())


def test_create_user(app: FastAPI, authorized_client: TestClient, user_factory: UserFactory, db_session: Session):
    user = user_factory.build()
    response = authorized_client.post(app.url_path_for('users:create-user'),
                                      UserCreate(**user.__dict__, password='asd').json())

    assert response.status_code == status.HTTP_200_OK
    response_user = User.parse_raw(response.content)
    db_user = crud.user.get(db_session, response_user.id)
    assert response_user == User.parse_obj(db_user.__dict__)


def test_ordering_username_asc(app: FastAPI, authorized_client: TestClient, test_user, user_factory: UserFactory):
    user_number = 5
    user_list: List[DBUser] = [
        user_factory.create() for _ in range(user_number)
    ]
    user_list.append(test_user)

    response = authorized_client.get(app.url_path_for('users:list-users'), params={'ordering': 'username'})
    assert response.status_code == status.HTTP_200_OK

    response = PaginatedResponse.parse_raw(response.content)
    assert response.count == user_number + 1

    expected_response = sorted([user.username for user in user_list])
    actual_response = [user.get('username') for user in response.data]

    assert actual_response == expected_response


def test_get_user_detail(app: FastAPI, authorized_client: TestClient, test_user: DBUser):
    response = authorized_client.get(app.url_path_for('users:get-user', user_id=str(test_user.id)))
    assert response.status_code == status.HTTP_200_OK
    assert User.parse_raw(response.content) == User.parse_obj(test_user.__dict__)
