from tortoise import models, fields

__all__ = [
    'Notification',
]


class Notification(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    sender = fields.CharField(max_length=255)
    whom = fields.CharField(max_length=255)
    text = fields.TextField()
    created = fields.DatetimeField(auto_now_add=True)

    statuses = fields.ReverseRelation['NotificationStatus']

    class Meta:
        table = 'notifications'
        ordering = ['-created']

    def __str__(self):
        return f'Notification ({self.name})'
