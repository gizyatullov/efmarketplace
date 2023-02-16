from typing import Dict

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status


@pytest.mark.anyio
async def test_captcha_receipt(client: AsyncClient, fastapi_app: FastAPI) -> None:
    url = fastapi_app.url_path_for('captcha')
    response = await client.post(url)
    assert response.status_code == status.HTTP_201_CREATED

    payload: Dict = response.json()
    assert payload.get('uid') is not None
    assert payload.get('image') is not None
