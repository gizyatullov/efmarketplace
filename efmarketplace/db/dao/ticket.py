from datetime import datetime
from types import coroutine
from typing import List, Optional

from efmarketplace.db.models.ticket import (TicketModel,
                                            TicketResponseModel,
                                            TicketStatus, )
from efmarketplace.web.api.ticket.schema import Ticket, TicketResponse

__all__ = [
    "TicketResponseDAO",
    "ticket_response_repository",
    "TicketDAO",
    "ticket_repository",
]


class TicketResponseDAO:
    """Class for accessing ticketresponse table."""

    async def create_ticket_response_model(
        self,
        user: coroutine,  # type: ignore
        ticket_id: int,
        content: str,
    ) -> TicketResponse:  # type: ignore
        """Add single ticketresponse to table.

        :param user: user
        :param ticket_id: id of ticket
        :param content: content for ticket
        :return: ticketresponse
        """
        ticket = await TicketModel.filter(id=ticket_id).first()
        ticket_response = await TicketResponseModel.create(
            ticket=ticket,
            created=datetime.now(),
            sender=user,
            content=content,
        )
        return await TicketResponse.from_tortoise_orm(ticket_response)


ticket_response_repository = TicketResponseDAO()


class TicketDAO:
    """Class for accessing ticket table."""

    async def create_ticket_model(
        self,
        user: coroutine,  # type: ignore
        tag: str,
        content: str,
    ) -> Ticket:
        """
        Add single ticket to table.

        :param user: user
        :param tag: tag for ticket
        :param content: content for ticket
        :return: ticket
        """
        ticket = await TicketModel.create(
            status=TicketStatus.NEW,
            created=datetime.now(),
            sender=user,
            tag=tag,
            content=content,
        )
        return Ticket(**dict(ticket))

    async def get_all_tickets(self, limit: int, offset: int) -> List[Ticket]:
        """Get all ticket models with limit/offset pagination.

        :param limit: limit of ticket objects, defaults to 10.
        :param offset: offset of ticket objects, defaults to 0.
        :return: list of tickets
        """
        tickets = await TicketModel.all().offset(offset).limit(limit)
        return [Ticket(**dict(el)) for el in tickets]

    @staticmethod
    async def filter(ticket_id: int) -> Optional[Ticket]:
        """Get specific ticket model by id.

        :param ticket_id: id of ticket
        :return: ticked filtered by id
        """
        ticket = await TicketModel.filter(id=ticket_id).first()
        if not ticket:
            return None
        return Ticket(**dict(ticket))


ticket_repository = TicketDAO()
