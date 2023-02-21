"""Services for efmarketplace."""
from captcha.image import ImageCaptcha

from efmarketplace.db.dao.category import CategoryDAO
from efmarketplace.db.dao.city import CityDAO
from efmarketplace.db.dao.country import CountryDAO
from efmarketplace.db.dao.notification import NotificationDAO
from efmarketplace.db.dao.subcategory import SubcategoryDAO
from efmarketplace.db.dao.user import UserDAO

from .auth import AuthService
from .category import CategoryService
from .city import CityService
from .country import CountryService
from .notification import NotificationService
from .price import PriceService
from .subcategory import SubcategoryService
from .user import UserService

__all__ = [
    "user_service",
    "auth_service",
    "country_service",
    "city_service",
    "category_service",
    "subcategory_service",
    "notification_service",
    "price_service",
]

image_captcha = ImageCaptcha()

user_service = UserService(user_repository=UserDAO)
auth_service = AuthService(user_service=user_service, image_captcha=image_captcha)
country_service = CountryService(country_repository=CountryDAO)
city_service = CityService(city_repository=CityDAO)
category_service = CategoryService(category_repository=CategoryDAO)
subcategory_service = SubcategoryService(subcategory_repository=SubcategoryDAO)
notification_service = NotificationService(notification_repository=NotificationDAO)
price_service = PriceService()
