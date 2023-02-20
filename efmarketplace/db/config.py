from typing import List

from efmarketplace.settings import settings

MODELS_MODULES: List[str] = [
    "efmarketplace.db.models.user",
    "efmarketplace.db.models.country",
    "efmarketplace.db.models.city",
    "efmarketplace.db.models.category",
    "efmarketplace.db.models.subcategory",
    "efmarketplace.db.models.notification",
    "efmarketplace.db.models.notification_status",
    "efmarketplace.db.models.ticket_models",
]

TORTOISE_CONFIG = {  # noqa: WPS407
    "connections": {
        "default": str(settings.db_url),
    },
    "apps": {
        "models": {
            "models": MODELS_MODULES + ["aerich.models"],
            "default_connection": "default",
        },
    },
}
