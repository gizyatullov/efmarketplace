from datetime import datetime
from enum import Enum
from typing import List, Union

from pydantic import Field, PositiveInt

from efmarketplace.pkg.types.integeres import PositiveIntWithZero

from .base import BaseModel
from .general import ForPaginationFields
from .user import UserFields

__all__ = [
    "NotificationFields",
    "NotificationStatusFields",
    "NotificationStatus",
    "Notification",
    "NotificationsWithPagination",
    "CreateNotificationCommand",
    "CreateNotificationSpecificUsersCommand",
    "MarkAsReadNotificationCommand",
    "MarkAsReadNotificationWithUserUIDCommand",
    "ReadNotificationQuery",
    "ReadNotificationWithUserUIDQuery",
    "StatusReceivedNotification",
]


class StatusReceivedNotification(str, Enum):
    ANY = "any"
    NOT_READ = "not read"
    READ = "read"


class NotificationFields:
    id = Field(description="Notification ID", example=2)
    name = Field(description="Notification name, title", example="all for packing")
    sender = Field(description="Sender name", example="administration")
    whom = Field(
        description="What kind of notification ?", example="alerts to everyone"
    )
    text = Field(description="Text notification", example="text notification")
    created = Field(description="Creation time", example="2023-02-17 15:18:01")
    view = Field(description="Viewed Notifications ?", example=False)
    uid_notifications = Field(
        description="Mark notifications as read by the user", example=[1, 51, 94]
    )


class NotificationStatusFields:
    id = Field(description="Notification status ID", example=2)
    user_id = Field(description="Recipient ID", example=2)
    notification_id = Field(description="Notification ID", example=2)
    status = Field(description="Status notification", example=False, default=False)


class BaseNotificationStatus(BaseModel):
    """Base model for notification status."""

    class Config:
        orm_mode = True


class BaseNotification(BaseModel):
    """Base model for notification."""

    class Config:
        orm_mode = True


class NotificationStatus(BaseNotificationStatus):
    id: PositiveInt = NotificationStatusFields.id
    user_id: PositiveInt = NotificationStatusFields.user_id
    notification_id: PositiveInt = NotificationStatusFields.notification_id
    status: bool = NotificationStatusFields.status


class Notification(BaseNotification):
    id: PositiveInt = NotificationFields.id
    name: str = NotificationFields.name
    sender: str = NotificationFields.sender
    whom: str = NotificationFields.whom
    text: str = NotificationFields.text
    created: datetime = NotificationFields.created


class NotificationsWithPagination(BaseNotification):
    items: List[Notification] = []
    total: PositiveIntWithZero = ForPaginationFields.total
    page: PositiveIntWithZero = ForPaginationFields.page
    size: PositiveInt = ForPaginationFields.size


# Commands.
class CreateNotificationCommand(BaseNotification):
    name: str = NotificationFields.name
    sender: str = NotificationFields.sender
    whom: str = NotificationFields.whom
    text: str = NotificationFields.text


class CreateNotificationSpecificUsersCommand(BaseNotification):
    user_ids: List[Union[PositiveInt, str]] = UserFields.ids
    name: str = NotificationFields.name
    sender: str = NotificationFields.sender
    whom: str = NotificationFields.whom
    text: str = NotificationFields.text


class MarkAsReadNotificationCommand(BaseNotification):
    uid_notifications: List[
        Union[PositiveInt, str]
    ] = NotificationFields.uid_notifications


class MarkAsReadNotificationWithUserUIDCommand(BaseNotification):
    user_uid: Union[PositiveInt, str] = UserFields.id
    uid_notifications: List[
        Union[PositiveInt, str]
    ] = NotificationFields.uid_notifications


# Query
class ReadNotificationQuery(BaseNotification):
    view: bool = NotificationFields.view
    limit: PositiveInt = 10
    offset: PositiveIntWithZero = 0


class ReadNotificationWithUserUIDQuery(BaseNotification):
    user_uid: Union[PositiveInt, str] = UserFields.id
    view: bool = NotificationFields.view
    limit: PositiveInt = 10
    offset: PositiveIntWithZero = 0
