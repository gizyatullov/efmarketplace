from typing import Dict

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status


@pytest.mark.anyio
async def test_price_receipt(client: AsyncClient, fastapi_app: FastAPI) -> None:
    url = fastapi_app.url_path_for('price')
    response = await client.post(url)
    assert response.status_code == status.HTTP_200_OK

    payload: Dict = response.json()
    assert payload.get('BTC') is not None
    assert payload.get('BTC').get('BTCUSDT') is not None
    assert payload.get('BTC').get('BTCRUB') is not None
