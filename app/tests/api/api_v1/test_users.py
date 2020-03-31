import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette import status

from app import crud, schemas
from app.db.paginator import Paginator
from app.models.user import User as DBUser
from app.schemas import UserCreate, User
from app.schemas.common import PaginatedResponse
from app.tests.utils.factories import UserFactory


@pytest.mark.usefixtures('top_level_session', 'db_session')
class TestOrdering(object):
    user_number = 5
    fields = list(schemas.User.schema(by_alias=False)['properties'].keys())

    @pytest.fixture(scope='class', autouse=True)
    def users(self, top_level_session: any, request: any, admin_user: DBUser):
        user_list = [
            UserFactory.create() for _ in range(self.user_number)
        ]
        user_list.append(admin_user)
        request.cls.user_list = user_list

    @pytest.mark.parametrize('order_field', fields)
    def test_ordering_username_asc(self,
                                   order_field,
                                   app: FastAPI,
                                   authorized_client: TestClient):
        aliased_field = schemas.common.to_camel_case(order_field)
        response = authorized_client.get(app.url_path_for('users:list-users'), params={'ordering': aliased_field})
        assert response.status_code == status.HTTP_200_OK

        response = PaginatedResponse.parse_raw(response.content)
        assert response.count == len(self.user_list)
        expected_response = sorted([getattr(user, order_field) for user in self.user_list])
        actual_response = [getattr(User.parse_obj(user), order_field) for user in response.data]

        assert actual_response == expected_response


def test_create_user(app: FastAPI, authorized_client: TestClient, user_factory: UserFactory, db_session: Session):
    user = user_factory.build()
    response = authorized_client.post(app.url_path_for('users:create-user'),
                                      UserCreate(**user.__dict__, password='asd').json())
    assert response.status_code == status.HTTP_200_OK
    response_user = User.parse_raw(response.content)
    db_user = crud.user.get(db_session, response_user.id)
    assert response_user == User.parse_obj(db_user.__dict__)


def test_list_response(app: FastAPI, authorized_client: TestClient, admin_user: DBUser):
    response = authorized_client.get(app.url_path_for('users:list-users'))
    assert response.status_code == status.HTTP_200_OK
    response = PaginatedResponse.parse_raw(response.content)
    assert response.count == 1
    assert response.page_size == Paginator.default_page_size
    assert response.pages == 1
    assert len(response.data) == 1
    assert User.parse_obj(admin_user.__dict__) == User.parse_obj(response.data.pop())


def test_get_user_detail(app: FastAPI, authorized_client: TestClient, admin_user: DBUser):
    response = authorized_client.get(app.url_path_for('users:get-user', user_id=str(admin_user.id)))
    assert response.status_code == status.HTTP_200_OK
    assert User.parse_raw(response.content) == User.parse_obj(admin_user.__dict__)
