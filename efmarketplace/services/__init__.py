"""Services for efmarketplace."""
from captcha.image import ImageCaptcha

from efmarketplace.db.dao import (user_repository,
                                  country_repository,
                                  city_repository,
                                  category_repository,
                                  subcategory_repository, )
from .auth import AuthService
from .user import UserService
from .country import CountryService
from .city import CityService
from .category import CategoryService
from .subcategory import SubcategoryService
from .price import PriceService

__all__ = [
    'user_service',
    'auth_service',
    'country_service',
    'city_service',
    'category_service',
    'subcategory_service',
    'price_service',
]

image_captcha = ImageCaptcha()

user_service = UserService(user_repository=user_repository)
auth_service = AuthService(user_service=user_service,
                           image_captcha=image_captcha)
country_service = CountryService(
    country_repository=country_repository
)
city_service = CityService(
    city_repository=city_repository
)
category_service = CategoryService(
    category_repository=category_repository
)
subcategory_service = SubcategoryService(
    subcategory_repository=subcategory_repository
)
price_service = PriceService()
