from typing import List, Optional

from efmarketplace import schemas
from efmarketplace.db.models.ticket_models import TicketModel, TicketResponseModel
from efmarketplace.web.api import exceptions

__all__ = [
    "TicketResponseDAO",
    "TicketDAO",
]


class TicketResponseDAO:
    """Class for accessing ticketresponse table."""

    @staticmethod
    async def create(
        cmd: schemas.CreateTicketResponseWithUserIDCommand,
    ) -> schemas.TicketResponse:
        if not await TicketModel.exists(id=cmd.ticket_id):
            raise exceptions.NotFound(
                message=f"Not found ticket with ID {cmd.ticket_id}")
        ticket_response = await TicketResponseModel.create(**cmd.dict())
        return schemas.TicketResponse.from_orm(ticket_response)


class TicketDAO:
    """Class for accessing ticket table."""

    @staticmethod
    async def create(cmd: schemas.CreateTicketWithUserIDCommand) -> schemas.Ticket:
        t = await TicketModel.create(**cmd.dict())
        return schemas.Ticket.from_orm(t)

    @staticmethod
    async def get_all_tickets(limit: int, offset: int) -> List[schemas.Ticket]:
        t = await TicketModel.all().offset(offset).limit(limit)
        return [schemas.Ticket.from_orm(item) for item in t]

    @staticmethod
    async def read_by_id(id_: int) -> Optional[schemas.Ticket]:
        t = await TicketModel.get(id=id_)
        return schemas.Ticket.from_orm(t)
