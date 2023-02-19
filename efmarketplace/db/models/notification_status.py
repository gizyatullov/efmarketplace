from tortoise import models, fields

from .notification import Notification
from .user import User

__all__ = [
    'NotificationStatus',
]


class NotificationStatus(models.Model):
    id = fields.IntField(pk=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        model_name='models.User',
        related_name='notification_statuses'
    )
    notification: fields.ForeignKeyRelation[Notification] = fields.ForeignKeyField(
        model_name='models.Notification',
        related_name='statuses')
    status = fields.BooleanField(default=False)

    class Meta:
        table = 'notification_statuses'
        ordering = ['-status']
        unique_together = (("user_id", "notification_id"),)

    def __str__(self):
        return f'NotificationStatus ({self.id})'
