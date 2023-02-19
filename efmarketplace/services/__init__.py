"""Services for fastapi_template."""
from captcha.image import ImageCaptcha
from efmarketplace.db.dao.city import CityDAO
from efmarketplace.db.dao.country import CountryDAO
from efmarketplace.db.dao.user import UserDAO
from efmarketplace.db.dao.notification import NotificationDAO

from .auth import AuthService
from .city import CityService
from .country import CountryService
from .user import UserService
from .notification import NotificationService
from .price import PriceService

__all__ = [
    "user_service",
    "auth_service",
    "country_service",
    "city_service",
    "notification_service",
    "price_service",
]

image_captcha = ImageCaptcha()

user_service = UserService(user_repository=UserDAO)
auth_service = AuthService(user_service=user_service, image_captcha=image_captcha)
country_service = CountryService(country_repository=CountryDAO)
city_service = CityService(city_repository=CityDAO)
notification_service = NotificationService(
    notification_repository=NotificationDAO
)
price_service = PriceService()
