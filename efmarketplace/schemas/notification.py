from typing import Union
from datetime import datetime

from pydantic import Field, PositiveInt

from .base import BaseModel

__all__ = [
    'NotificationStatusFields',
]


class NotificationStatusFields:
    id = Field(description='Notification status ID', example=2)
    recipient_id = Field(description='Recipient ID', example=2)
    status = Field(description='Status notification',
                   example=False,
                   default=False)


class NotificationFields:
    id = Field(description='Notification ID', example=2)
    name = Field(description='Notification name, title', example='all for packing')
    sender = Field(description='Sender name', example='administration')
    whom = Field(description='What kind of notification ?',
                 example='alerts to everyone')
    text = Field(description='Text notification', example='text notification')
    status = Field(description='Notification status', example=NotificationStatusFields)
    created = Field(description='Creation time', example='2023-02-17 15:18:01')


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
    recipient_id: PositiveInt = NotificationStatusFields.recipient_id
    status: bool = NotificationStatusFields.status


class Notification(BaseNotification):
    id: PositiveInt = NotificationFields.id
    name: str = NotificationFields.name
    sender: str = NotificationFields.sender
    whom: str = NotificationFields.whom
    text: str = NotificationFields.text
    status: NotificationStatus = NotificationFields.status
    created: datetime = NotificationFields.created


# Commands.
class CreateNotificationCommand(BaseNotification):
    name: str = NotificationFields.name
    sender: str = NotificationFields.sender
    whom: str = NotificationFields.whom
    text: str = NotificationFields.text


# Query
class ReadNotificationQuery(BaseModel):
    user_uid: Union[PositiveInt, str]
    which: str
