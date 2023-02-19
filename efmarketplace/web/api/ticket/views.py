from typing import List

from efmarketplace.db.dao.ticket import TicketDAO, TicketResponseDAO
from efmarketplace.web.api.ticket.schema import (
    Ticket,
    TicketCreate,
    TicketResponse,
    TicketResponseCreate,
)
from efmarketplace.web.api.users.auth import auth_required
from efmarketplace.web.api.users.controler import check_auth
from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends

router = APIRouter()


@router.get("/ticket", response_model=List[Ticket])
@auth_required
async def get_ticket_models(
    limit: int = 10,
    offset: int = 0,
    ticket_dao: TicketDAO = Depends(),
) -> List[Ticket]:
    """Retrieve all ticket objects from the database.

    :param ticket_dao: DAO for ticket_models
    :param limit: limit of ticket objects, defaults to 10.
    :param offset: offset of ticket objects, defaults to 0.
    :return: return tickets
    """
    return await ticket_dao.get_all_tickets(limit=limit, offset=offset)


@router.post("/ticket")
@auth_required
async def post_ticket_models(
    new_ticket_object: TicketCreate,
    ticket_dao: TicketDAO = Depends(),
) -> Ticket:
    """Add single ticket to session.

    :param new_ticket_object: new ticket model object
    :param ticket_dao: DAO for ticket models
    :return: creating ticket object
    """
    user = await check_auth()
    return await ticket_dao.create_ticket_model(user, **new_ticket_object.dict())


@router.post("/ticketResponse")
@auth_required
async def post_ticket_response_models(
    new_ticket_response_object: TicketResponseCreate,
    ticket_response_dao: TicketResponseDAO = Depends(),
) -> TicketResponse:  # type: ignore
    """Add single ticket_response to session.

    :param new_ticket_response_object: new ticket_response object
    :param ticket_response_dao: DAO for ticketresponse models
    :return: creating ticket_response object
    """
    user = await check_auth()
    ticket = await TicketDAO.filter(
        new_ticket_response_object.ticket_id,
    )
    if not ticket:
        raise HTTPException(status_code=404, detail="Item not found")
    return await ticket_response_dao.create_ticket_response_model(
        user,
        **new_ticket_response_object.dict(),
    )


@router.get("/tickets/{ticket_id}", response_model=None)
@auth_required
async def get_ticket_models_by_id(ticket_id: int) -> Ticket:
    ticket = await TicketDAO.filter(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Item not found")
    return ticket
