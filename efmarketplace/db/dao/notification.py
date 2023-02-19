from typing import List, Union

from tortoise import models
from tortoise.transactions import in_transaction
from loguru import logger

from .base import BaseDAO
from efmarketplace import schemas
from efmarketplace.db.models.notification import Notification
from efmarketplace.db.models.notification_status import NotificationStatus
from efmarketplace.db.models.user import User
from tortoise.exceptions import OperationalError

__all__ = ['NotificationDAO', ]


class NotificationDAO(BaseDAO):
    @staticmethod
    async def create_for_all(cmd: schemas.CreateNotificationCommand
                             ) -> schemas.Notification:
        try:
            async with in_transaction():
                n = Notification(**cmd.dict())
                await n.save()
                users = await User.all()
                [await NotificationStatus(user_id=u.id,
                                          notification_id=n.id).save() for u in users]
        except OperationalError as e:
            logger.error(f"...{e}")
        else:
            return schemas.Notification.from_orm(n)

    # async def read(self, ):
