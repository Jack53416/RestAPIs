import logging
from typing import NamedTuple, List

import pytest
from fastapi.testclient import TestClient
from starlette import status

logger = logging.getLogger(__name__)


class Endpoint(NamedTuple):
    url: str
    methods: List[str]

    def __str__(self):
        return self.url

    def __repr__(self):
        return str(self)


class PathTest(NamedTuple):
    url: str
    method: str

    def __str__(self):
        return f'{self.method} - {self.url}'


secured_endpoints = [
    Endpoint('login/test-token', ['post']),
    Endpoint('users/', ['get', 'post']),
    Endpoint('users/1', ['get']),
    Endpoint('projects/', ['get']),
]

secured_paths = [PathTest(endpoint.url, method) for endpoint in secured_endpoints for method in endpoint.methods]


@pytest.mark.parametrize('endpoint', secured_paths, ids=str)
def test_anonymous_access_denied(client: TestClient, endpoint):
    response = client.request(method=endpoint.method, url=f'api/v1/{endpoint.url}')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'WWW-Authenticate' in response.headers
    assert response.headers.get('WWW-Authenticate') == 'Bearer'
