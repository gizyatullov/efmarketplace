import datetime

from pydantic import BaseModel

from efmarketplace.db.models.ticket import TicketResponseModel, TicketStatus
from tortoise.contrib.pydantic import pydantic_model_creator


class TicketCreate(BaseModel):
    """DTO for creating new TicketModel."""

    tag: str
    content: str

    class Config:
        orm_mode = True


class Ticket(TicketCreate):
    """DTO for TicketModel."""

    id: int
    sender_id: int
    created: datetime.datetime
    status: TicketStatus

    class Config:
        orm_mode = True


class TicketResponseCreate(BaseModel):
    """DTO for creating TicketResponseModel."""

    ticket_id: int
    content: str

    class Config:
        orm_mode = True


TicketResponse = pydantic_model_creator(TicketResponseModel)
