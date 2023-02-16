"""DAO classes."""
from .user import UserDAO
from .country import CountryDAO
from .city import CityDAO
from .category import CategoryDAO
from .subcategory import SubcategoryDAO

__all__ = [
    'UserDAO',
    'user_repository',
    'CountryDAO',
    'country_repository',
    'CityDAO',
    'city_repository',
    'CategoryDAO',
    'category_repository',
    'SubcategoryDAO',
    'subcategory_repository',
]

user_repository = UserDAO()
country_repository = CountryDAO()
city_repository = CityDAO()
category_repository = CategoryDAO()
subcategory_repository = SubcategoryDAO()
