from fastapi.routing import APIRouter

from efmarketplace.web.api import (
    auth,
    categories,
    cities,
    countries,
    docs,
    favorites,
    prices,
    subcategories,
    ticket,
    users,
)
from efmarketplace.web.api.admin_ import notification as admin_notification

api_router = APIRouter()
api_router.include_router(docs.router)
api_router.include_router(users.router, prefix="/user", tags=["User"])
api_router.include_router(
    users.router_create_user, prefix="/user", tags=["User Create"]
)
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(countries.router, prefix="/country", tags=["Country"])
api_router.include_router(cities.router, prefix="/city", tags=["City"])
api_router.include_router(categories.router, prefix="/category", tags=["Category"])
api_router.include_router(
    subcategories.router, prefix="/subcategory", tags=["Subcategory"]
)
api_router.include_router(prices.router, prefix="/price", tags=["Price"])
api_router.include_router(ticket.router, prefix="/ticket", tags=["Ticket"])
api_router.include_router(
    admin_notification.router, prefix="/admin-notification", tags=["Admin-Notification"]
)
api_router.include_router(favorites.router, prefix="/favorites", tags=["Favorites"])
