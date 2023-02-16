from typing import Union, List

from pydantic import Field, PositiveInt, PositiveFloat

from .base import BaseModel

__all__ = [
    'PriceFields',
    'BTC',
    'Price',
    'ReadPriceQuery',
    'UnitPrice',
]


class PriceFields:
    usdt = Field(description='Price USDT', example=1)
    rub = Field(description='Price RUB', example=1)


class BasePrice(BaseModel):
    """Base model for price."""


class BTC(BasePrice):
    BTCUSDT: Union[PositiveInt, PositiveFloat] = PriceFields.usdt
    BTCRUB: Union[PositiveInt, PositiveFloat] = PriceFields.rub


class Price(BasePrice):
    BTC: BTC


class UnitPrice(BasePrice):
    name_pair: str
    price: Union[PositiveInt, PositiveFloat]
    prefix_in_redis: str = 'price_'


# Query
class ReadPriceQuery(BasePrice):
    currencies: List[str] = ['BTCUSDT', 'BTCRUB', ]
    prefix_in_redis: str = 'price_'
