from enum import Enum

from efmarketplace.db.models.user import User
from tortoise import ForeignKeyFieldInstance, fields, models


class TicketStatus(Enum):
    """Status for TicketModel status field."""

    NEW = "new"
    ACTIVE = "active"
    CLOSED = "closed"


class TicketModel(models.Model):
    """Ticket model."""

    id = fields.IntField(pk=True)
    tag = fields.TextField()
    content = fields.TextField()
    status = fields.CharEnumField(TicketStatus, default=TicketStatus.NEW.value)
    sender: ForeignKeyFieldInstance[User] = fields.ForeignKeyField(
        "models.User",
        related_name="sender_id",
    )
    created = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "tickets"


class TicketResponseModel(models.Model):
    """Model for response on ticket."""

    id = fields.IntField(pk=True)
    content = fields.TextField()
    sender: ForeignKeyFieldInstance[User] = fields.ForeignKeyField(
        "models.User",
        related_name="ticket_sender",
    )
    ticket: ForeignKeyFieldInstance[TicketModel] = fields.ForeignKeyField(
        "models.TicketModel",
        related_name="ticket_response",
    )
    created = fields.DatetimeField()

    class Meta:
        table = "ticket_responses"
