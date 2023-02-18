from fastapi.routing import APIRouter

from efmarketplace.web.api import (auth,
                                   docs,
                                   users,
                                   countries,
                                   cities,
                                   categories,
                                   subcategories,
                                   prices,
                                   ticket,
                                   admin_notification, )

api_router = APIRouter()
api_router.include_router(docs.router)
api_router.include_router(users.router, prefix='/user', tags=['User'])
api_router.include_router(auth.router, prefix='/auth', tags=['Auth'])
api_router.include_router(countries.router, prefix='/country', tags=['Country'])
api_router.include_router(cities.router, prefix='/city', tags=['City'])
api_router.include_router(categories.router, prefix='/category', tags=['Category'])
api_router.include_router(subcategories.router, prefix='/subcategory',
                          tags=['Subcategory'])
api_router.include_router(prices.router, prefix='/price', tags=['Price'])
api_router.include_router(ticket.router, tags=['Ticket'])
api_router.include_router(admin_notification.router,
                          prefix='/admin-notification',
                          tags=['Admin-Notification'])
