from typing import List, Type

from efmarketplace import schemas
from efmarketplace.db.dao.notification import NotificationDAO

__all__ = [
    "NotificationService",
]


class NotificationService:
    repository: Type[NotificationDAO]

    def __init__(self, notification_repository: Type[NotificationDAO]):
        self.repository = notification_repository

    async def create_notification_for_all(
        self, cmd: schemas.CreateNotificationCommand
    ) -> schemas.Notification:
        return await self.repository.create_for_all(cmd=cmd)

    async def read_user_notifications(
        self, query: schemas.ReadNotificationWithUserUIDQuery
    ) -> List[schemas.Notification]:
        return await self.repository.read(query=query)

    async def mark_as_read(
        self, query: schemas.MarkAsReadNotificationWithUserUIDCommand
    ):
        return await self.repository.mark_as_read(query=query)
