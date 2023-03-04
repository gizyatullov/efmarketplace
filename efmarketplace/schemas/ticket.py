from datetime import datetime
from enum import Enum
from typing import List

from pydantic import Field, PositiveInt

from efmarketplace.pkg.types.integeres import PositiveIntWithZero

from .base import BaseModel
from .general import ForPaginationFields
from .user import UserFields

__all__ = [
    "TicketStatus",
    "TicketFields",
    "Ticket",
    "TicketResponse",
    "TicketsWithPagination",
    "ReadAllTicketQuery",
    "CreateTicketCommand",
    "CreateTicketWithUserIDCommand",
    "CreateTicketResponseCommand",
    "CreateTicketResponseWithUserIDCommand",
]


class TicketStatus(str, Enum):
    """Status for TicketModel status field."""

    NEW = "new"
    ACTIVE = "active"
    CLOSED = "closed"


class TicketFields:
    id = Field(description="ID.", example=2)
    tag = Field(description="Ticket tag.", example="?")
    content = Field(description="Content.", example="?")
    status = Field(description="Status.", example=TicketStatus.NEW.value)
    created = Field(
        description="When created ?",
        example="2022-09-21 12:00:00",
    )
    ticket_id = Field(description="ID ticket", example=2)


class BaseTicket(BaseModel):
    """Base model for ticket."""

    class Config:
        orm_mode = True


class Ticket(BaseTicket):
    id: PositiveInt = TicketFields.id
    tag: str = TicketFields.tag
    content: str = TicketFields.content
    status: TicketStatus = TicketFields.status
    sender_id: PositiveInt = UserFields.id
    created: datetime = TicketFields.created


class TicketResponse(BaseTicket):
    id: PositiveInt = TicketFields.id
    content: str = TicketFields.content
    sender_id: PositiveInt = UserFields.id
    ticket_id: PositiveInt = TicketFields.ticket_id
    created: datetime = TicketFields.created


class TicketsWithPagination(BaseTicket):
    items: List[Ticket]
    total: PositiveIntWithZero = ForPaginationFields.total
    page: PositiveIntWithZero = ForPaginationFields.page
    size: PositiveInt = ForPaginationFields.size


# Query
class ReadAllTicketQuery(BaseTicket):
    limit: PositiveInt = 10
    offset: PositiveIntWithZero = 0


# Commands.
class CreateTicketCommand(BaseTicket):
    tag: str = TicketFields.tag
    content: str = TicketFields.content


class CreateTicketWithUserIDCommand(CreateTicketCommand):
    sender_id: PositiveInt = UserFields.id


class CreateTicketResponseCommand(BaseTicket):
    ticket_id: PositiveInt = TicketFields.ticket_id
    content: str = TicketFields.content


class CreateTicketResponseWithUserIDCommand(CreateTicketResponseCommand):
    sender_id: PositiveInt = UserFields.id
