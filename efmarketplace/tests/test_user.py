from fastapi import FastAPI, status
from httpx import AsyncClient


async def test_register(client: AsyncClient, fastapi_app: FastAPI):
    response = await client.post(
        "/api/user", json={
            "username": "test_good",
            "password": "password",
            "role_name": "user",
            "uid_captcha": "d22dee4f-44af-4b25-831a-5ba7bc75bca4",
            "value_captcha": "51iu6v9s"
        }
    )

    assert response.status_code == status.HTTP_201_CREATED
