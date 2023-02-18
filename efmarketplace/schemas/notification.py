from typing import Union
from datetime import datetime
from enum import Enum

from pydantic import Field, PositiveInt

from .base import BaseModel
from .user import UserFields

__all__ = [
    'NotificationFields',
    'NotificationStatusFields',
    'NotificationStatus',
    'Notification',
    'CreateNotificationCommand',
    'ReadNotificationQuery',
    'ReadNotificationWithUserQuery',
    'StatusReceivedNotification',
]


class StatusReceivedNotification(Enum):
    ANY = 'any'
    NOT_READ = 'not read'
    READ = 'read'


class NotificationFields:
    id = Field(description='Notification ID', example=2)
    name = Field(description='Notification name, title', example='all for packing')
    sender = Field(description='Sender name', example='administration')
    whom = Field(description='What kind of notification ?',
                 example='alerts to everyone')
    text = Field(description='Text notification', example='text notification')
    created = Field(description='Creation time', example='2023-02-17 15:18:01')
    which = Field(description='What is the status of notifications ?',
                  example=StatusReceivedNotification.ANY.value)


class NotificationStatusFields:
    id = Field(description='Notification status ID', example=2)
    user_id = Field(description='Recipient ID', example=2)
    notification_id = Field(description='Notification ID', example=2)
    status = Field(description='Status notification',
                   example=False,
                   default=False)


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


# Commands.
class CreateNotificationCommand(BaseNotification):
    name: str = NotificationFields.name
    sender: str = NotificationFields.sender
    whom: str = NotificationFields.whom
    text: str = NotificationFields.text


# Query
class ReadNotificationQuery(BaseNotification):
    which: StatusReceivedNotification = NotificationFields.which


class ReadNotificationWithUserQuery(BaseNotification):
    user_uid: Union[PositiveInt, str] = UserFields.id
    which: StatusReceivedNotification = NotificationFields.which
