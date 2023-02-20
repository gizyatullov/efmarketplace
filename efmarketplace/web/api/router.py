from efmarketplace.web.api import (
    auth,
    cities,
    countries,
    categories,
    subcategories,
    prices,
    docs,
    echo,
    monitoring,
    ticket,
    users,
    admin_notification,
)
from fastapi.routing import APIRouter

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
api_router.include_router(echo.router, prefix="/echo", tags=["Echo"])
api_router.include_router(users.router, prefix="/user", tags=["User"])
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(countries.router, prefix="/country", tags=["Country"])
api_router.include_router(cities.router, prefix="/city", tags=["City"])
api_router.include_router(categories.router, prefix='/category', tags=['Category'])
api_router.include_router(subcategories.router, prefix='/subcategory',
                          tags=['Subcategory'])
api_router.include_router(prices.router, prefix='/price', tags=['Price'])
api_router.include_router(ticket.router, prefix="", tags=["ticket"])
api_router.include_router(admin_notification.router,
                          prefix='/admin-notification',
                          tags=['Admin-Notification'])
