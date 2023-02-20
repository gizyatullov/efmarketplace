from fastapi import APIRouter, status, Depends, BackgroundTasks

from efmarketplace import schemas
from efmarketplace.services import notification_service

__all__ = [
    "router",
]

router = APIRouter()


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
