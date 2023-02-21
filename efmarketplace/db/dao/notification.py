from typing import List, Union

from loguru import logger
from tortoise import models
from tortoise.exceptions import OperationalError
from tortoise.transactions import in_transaction

from efmarketplace import schemas
from efmarketplace.db.models.notification import Notification
from efmarketplace.db.models.notification_status import NotificationStatus
from efmarketplace.db.models.user import User

from .base import BaseDAO

__all__ = [
    "NotificationDAO",
]


class NotificationDAO(BaseDAO):
    @staticmethod
    async def create_for_all(
        cmd: schemas.CreateNotificationCommand,
    ) -> schemas.Notification:
        try:
            async with in_transaction():
                n = Notification(**cmd.dict())
                await n.save()
                users = await User.all()
                [
                    await NotificationStatus(user_id=u.id, notification_id=n.id).save()
                    for u in users
                ]
        except OperationalError as e:
            logger.error(f"...{e}")
        else:
            return schemas.Notification.from_orm(n)

    @staticmethod
    async def orm_notification_status_in_pydantic(
        statuses: List[NotificationStatus],
    ) -> List[schemas.Notification]:
        result = []
        for item in statuses:
            n = schemas.Notification(
                id=item.notification_id,
                name=item.notification.name,
                sender=item.notification.sender,
                whom=item.notification.whom,
                text=item.notification.text,
                status=item.status,
                created=item.notification.created,
            )
            result.append(n)
        return result

    @staticmethod
    async def read(
        query: schemas.ReadNotificationWithUserUIDQuery,
    ) -> List[schemas.Notification]:
        statuses = await NotificationStatus.filter(
            user_id=query.user_uid, status=query.view
        ).select_related("notification")
        result = await NotificationDAO.orm_notification_status_in_pydantic(
            statuses=statuses
        )
        return result

    @staticmethod
    async def mark_as_read(
        query: schemas.MarkAsReadNotificationWithUserUIDCommand,
    ) -> List[schemas.Notification]:
        n = await NotificationStatus.filter(
            user_id=query.user_uid, notification_id__in=query.uid_notifications
        ).update(status=True)

        statuses = await NotificationStatus.filter(
            user_id=query.user_uid, notification_id__in=query.uid_notifications
        ).select_related("notification")

        result = await NotificationDAO.orm_notification_status_in_pydantic(
            statuses=statuses
        )
        return result
