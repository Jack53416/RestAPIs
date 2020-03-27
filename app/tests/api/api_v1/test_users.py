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
    assert (
        PaginatedResponse(**response.json()).json(exclude={'links'}) ==
        PaginatedResponse(count=1,
                          pages=Paginator.default_page,
                          page_size=Paginator.default_page_size,
                          data=[User(**test_user.__dict__)]).json(exclude={'links'}),
    )


def test_create_user(app: FastAPI, authorized_client: TestClient, user_factory: UserFactory, db_session: Session):
    user = user_factory.build()
    response = authorized_client.post(app.url_path_for('users:create-user'),
                                      UserCreate(**user.__dict__, password='asd').json())

    assert response.status_code == status.HTTP_200_OK
    response_user = User(**response.json())
    assert (
            response_user.dict(exclude={'id', 'date_joined'}) ==
            User(**user.__dict__).dict(exclude={'id', 'date_joined'})
    )

    db_user = crud.user.get(db_session, response_user.id)
    assert response_user.json() == User(**db_user.__dict__).json()


def test_ordering_username(app: FastAPI, authorized_client: TestClient, test_user, user_factory: UserFactory):
    user_number = 5
    user_list: List[DBUser] = [
        user_factory.create() for _ in range(user_number)
    ]
    user_list.append(test_user)

    response = authorized_client.get(app.url_path_for('users:list-users'), params={'ordering': 'username'})
    json_resp = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert json_resp.get('count') == user_number + 1

    expected_response = sorted([user.username for user in user_list])
    actual_response = [user.get('username') for user in json_resp.get('data')]

    assert actual_response == expected_response
