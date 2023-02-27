from fastapi import APIRouter, BackgroundTasks, Depends, Security, status
from fastapi.security import HTTPBearer

from efmarketplace import schemas
from efmarketplace.services import notification_service
from efmarketplace.services.authorization import auth_only_admin

__all__ = [
    "router",
]

router = APIRouter(dependencies=[Depends(auth_only_admin), Security(HTTPBearer())])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    description="Creates a notification for all users.",
)
async def create_notification_for_all(
    cmd: schemas.CreateNotificationCommand,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(notification_service.create_notification_for_all, cmd=cmd)
    return {"message": "Notification sent in the background"}


@router.post(
    "/specific",
    response_model=schemas.Notification,
    status_code=status.HTTP_201_CREATED,
    description="Creates a notification for_specific users.",
)
async def create_notification_for_all(
    cmd: schemas.CreateNotificationSpecificUsersCommand,
):
    return await notification_service.create_for_specific_users(cmd=cmd)
