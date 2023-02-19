from typing import List, Union, Type

from efmarketplace import schemas
from efmarketplace.db.dao.notification import NotificationDAO

__all__ = ['NotificationService', ]


class NotificationService:
    repository: Type[NotificationDAO]

    def __init__(self, notification_repository: Type[NotificationDAO]):
        self.repository = notification_repository

    async def create_notification_for_all(self, cmd: schemas.CreateNotificationCommand
                                          ) -> schemas.Notification:
        return await self.repository.create_for_all(cmd=cmd)
