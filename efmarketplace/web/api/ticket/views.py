from fastapi import APIRouter, status
from fastapi.param_functions import Depends, Security
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from pydantic import PositiveInt

from efmarketplace import schemas
from efmarketplace.db.dao.ticket import TicketDAO, TicketResponseDAO
from efmarketplace.pkg.types.integeres import PositiveIntWithZero
from efmarketplace.services.authorization import auth_only

router = APIRouter(dependencies=[Depends(auth_only), Security(HTTPBearer())])


@router.get(
    "/", response_model=schemas.TicketsWithPagination, status_code=status.HTTP_200_OK
)
async def get_tickets(
    limit: PositiveInt = 10,
    offset: PositiveIntWithZero = 0,
    ticket_dao: TicketDAO = Depends(),
):
    query = schemas.ReadAllTicketQuery(limit=limit, offset=offset)
    return await ticket_dao.get_all_tickets(query=query)


@router.post("/", response_model=schemas.Ticket, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    cmd: schemas.CreateTicketCommand,
    ticket_dao: TicketDAO = Depends(),
    authorize: AuthJWT = Depends(),
):
    user_uid = authorize.get_raw_jwt()["uid"]
    cmd = schemas.CreateTicketWithUserIDCommand(**cmd.dict(), sender_id=user_uid)
    return await ticket_dao.create(cmd=cmd)


@router.post(
    "/ticket-response",
    response_model=schemas.TicketResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_ticket_response(
    cmd: schemas.CreateTicketResponseCommand,
    ticket_response_dao: TicketResponseDAO = Depends(),
    authorize: AuthJWT = Depends(),
):
    user_uid = authorize.get_raw_jwt()["uid"]
    cmd = schemas.CreateTicketResponseWithUserIDCommand(
        **cmd.dict(), sender_id=user_uid
    )
    return await ticket_response_dao.create(cmd=cmd)


@router.get(
    "/{ticket_id}", response_model=schemas.Ticket, status_code=status.HTTP_200_OK
)
async def get_ticket_by_id(
    ticket_id: PositiveInt,
    ticket_dao: TicketDAO = Depends(),
):
    return await ticket_dao.read_by_id(id_=ticket_id)
