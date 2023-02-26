from typing import List

from loguru import logger
from tortoise.exceptions import OperationalError
from tortoise.transactions import in_transaction

from efmarketplace import schemas
from efmarketplace.db.models.notification import Notification
from efmarketplace.db.models.notification_status import NotificationStatus
from efmarketplace.db.models.user import User
from efmarketplace.web.api.exceptions.notification import InvalidIDsInRequest

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
                n = await Notification.create(**cmd.dict())
                user_ids = await User.all().only("id")
                await NotificationStatus.bulk_create(objects=[
                    NotificationStatus(user_id=u.id, notification_id=n.id)
                    for u in user_ids
                ])
        except OperationalError as e:
            logger.error(f"...{e}")
        else:
            return schemas.Notification.from_orm(n)

    @staticmethod
    async def create_for_specific_users(
        cmd: schemas.CreateNotificationSpecificUsersCommand,
    ) -> schemas.Notification:
        try:
            async with in_transaction():
                n = await Notification.create(**cmd.dict())
                await NotificationStatus.bulk_create(objects=[
                    NotificationStatus(user_id=id_, notification_id=n.id)
                    for id_ in cmd.user_ids
                ])
        except OperationalError:
            raise InvalidIDsInRequest
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
        ).prefetch_related("notification")
        result = await NotificationDAO.orm_notification_status_in_pydantic(
            statuses=statuses
        )
        return result

    @staticmethod
    async def mark_as_read(
        query: schemas.MarkAsReadNotificationWithUserUIDCommand,
    ) -> List[schemas.Notification]:
        await NotificationStatus.filter(
            user_id=query.user_uid, notification_id__in=query.uid_notifications
        ).select_for_update().update(status=True)

        statuses = await NotificationStatus.filter(
            user_id=query.user_uid, notification_id__in=query.uid_notifications
        ).prefetch_related("notification")

        result = await NotificationDAO.orm_notification_status_in_pydantic(
            statuses=statuses
        )
        return result
