from tortoise import ForeignKeyFieldInstance, fields, models

from efmarketplace.db.models.user import User
from efmarketplace.schemas.ticket import TicketStatus

__all__ = [
    "TicketModel",
    "TicketResponseModel",
]


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
    created = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "ticket_responses"
