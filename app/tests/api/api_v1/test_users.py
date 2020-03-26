from fastapi.testclient import TestClient
from starlette import status

from app.db.paginator import Paginator
from app.models.user import User as DBUser
from app.schemas import User
from app.schemas.common import PaginatedResponse


def test_list_response(authorized_client: TestClient, test_user: DBUser):
    response = authorized_client.get('api/v1/users')
    assert response.status_code == status.HTTP_200_OK
    assert (
            PaginatedResponse(**response.json()).json(exclude={'links'}) ==
            PaginatedResponse(count=1,
                              pages=Paginator.default_page,
                              page_size=Paginator.default_page_size,
                              data=[User(**test_user.__dict__)]).json(exclude={'links'}),
            )
