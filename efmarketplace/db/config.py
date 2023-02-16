from typing import List

from efmarketplace.settings import settings

MODELS_MODULES: List[str] = [
    'aerich.models',
    'efmarketplace.db.models.user',
    'efmarketplace.db.models.country',
    'efmarketplace.db.models.city',
    'efmarketplace.db.models.category',
    'efmarketplace.db.models.subcategory',
]  # noqa: WPS407

TORTOISE_CONFIG = {  # noqa: WPS407
    'connections': {
        'default': str(settings.db_url),
    },
    'apps': {
        'models': {
            'models': MODELS_MODULES,
            'default_connection': 'default',
        },
    },
}
