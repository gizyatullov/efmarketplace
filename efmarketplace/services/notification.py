from typing import List, Union

from efmarketplace import schemas
from efmarketplace.db.dao import NotificationDAO

__all__ = ['NotificationService', ]


class NotificationService:
    repository: NotificationDAO

    def __init__(self, notification_repository: NotificationDAO):
        self.repository = notification_repository

    async def create_notification_for_all(self, cmd: schemas.CreateNotificationCommand
                                          ) -> schemas.Notification:
        return await self.repository.create_for_all(cmd=cmd)
