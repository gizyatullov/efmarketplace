import asyncio
from random import choice

from faker import Faker
from faker.providers import (
    address,
    bank,
    company,
    date_time,
    internet,
    job,
    lorem,
    person,
    python,
)
from loguru import logger

from efmarketplace import schemas
from efmarketplace.db import models

__all__ = [
    "start_fill",
]

QUANTITY_ITEMS = 12

fake = Faker()
fake.add_provider(lorem)
fake.add_provider(address)
fake.add_provider(person)
fake.add_provider(company)
fake.add_provider(date_time)
fake.add_provider(python)
fake.add_provider(bank)
fake.add_provider(internet)
fake.add_provider(job)


async def fill_user():
    if await models.User.all().count():
        return
    for_save = []
    for _ in range(QUANTITY_ITEMS):
        u = models.User(
            username=fake.unique.user_name(),
            role_name=fake.enum(schemas.UserRole),
            is_seller=fake.pybool(),
            btc_balance=fake.pyfloat(min_value=0.0, max_value=9999.9),
            btc_address=fake.bban(),
            otp=fake.bban(),
            city=fake.city(),
            avatar=fake.dga(),
            created=fake.date_time_this_decade(),
            is_banned=fake.pybool(),
            user_ban_date=fake.date_time_this_decade(),
        )
        await u.set_password(password=fake.word())
        for_save.append(u)
    await models.User.bulk_create(for_save)


async def fill_category():
    if await models.Category.all().count():
        return
    for_save = []
    for _ in range(QUANTITY_ITEMS):
        c = models.Category(name=fake.word())
        for_save.append(c)
    await models.Category.bulk_create(for_save)


async def fill_subcategory():
    if await models.Subcategory.all().count():
        return
    category_ids = [item.id for item in await models.Category.all().only("id")]
    for_save = []
    for _ in range(QUANTITY_ITEMS):
        sc = models.Subcategory(name=fake.word(), category_id=choice(category_ids))
        for_save.append(sc)
    await models.Subcategory.bulk_create(for_save)


async def fill_country():
    if await models.Country.all().count():
        return
    for_save = []
    for _ in range(QUANTITY_ITEMS):
        c = models.Country(name=fake.country())
        for_save.append(c)
    await models.Country.bulk_create(for_save)


async def fill_city():
    if await models.City.all().count():
        return
    country_ids = [item.id for item in await models.Country.all().only("id")]
    for_save = []
    for _ in range(QUANTITY_ITEMS):
        c = models.City(name=fake.city(), country_id=choice(country_ids))
        for_save.append(c)
    await models.City.bulk_create(for_save)


async def fill_notification():
    if await models.Notification.all().count():
        return
    for_save = []
    for _ in range(QUANTITY_ITEMS):
        n = models.Notification(
            name=fake.text(max_nb_chars=30),
            sender=fake.job(),
            whom=fake.job(),
            text=fake.text(max_nb_chars=200),
            created=fake.date_time_this_decade(),
        )
        for_save.append(n)
    await models.Notification.bulk_create(for_save)


async def fill_notification_status():
    if await models.NotificationStatus.all().count():
        return
    notification_ids = [item.id for item in await models.Notification.all().only("id")]
    user_ids = [item.id for item in await models.User.all().only("id")]
    for_save = []
    for _ in range(QUANTITY_ITEMS):
        ns = models.NotificationStatus(
            user_id=choice(user_ids),
            notification_id=choice(notification_ids),
            status=fake.pybool(),
        )
        for_save.append(ns)
    await models.NotificationStatus.bulk_create(for_save)


async def fill_ticket():
    if await models.TicketModel.all().count():
        return
    user_ids = [item.id for item in await models.User.all().only("id")]
    for_save = []
    for _ in range(QUANTITY_ITEMS):
        t = models.TicketModel(
            tag=fake.word(),
            content=fake.text(max_nb_chars=200),
            status=fake.enum(schemas.TicketStatus),
            sender_id=choice(user_ids),
            created=fake.date_time_this_decade(),
        )
        for_save.append(t)
    await models.TicketModel.bulk_create(for_save)


async def fill_ticket_response():
    if await models.TicketResponseModel.all().count():
        return
    user_ids = [item.id for item in await models.User.all().only("id")]
    ticket_ids = [item.id for item in await models.TicketModel.all().only("id")]
    for_save = []
    for _ in range(QUANTITY_ITEMS):
        tr = models.TicketResponseModel(
            content=fake.text(max_nb_chars=200),
            sender_id=choice(user_ids),
            ticket_id=choice(ticket_ids),
            created=fake.date_time_this_decade(),
        )
        for_save.append(tr)
    await models.TicketResponseModel.bulk_create(for_save)


for_call = [
    fill_user,
    fill_category,
    fill_subcategory,
    fill_country,
    fill_city,
    fill_notification,
    fill_notification_status,
    fill_ticket,
    fill_ticket_response,
]


async def s():
    for call in for_call:
        logger.info(f"Call {call.__name__} table")
        await call()


def start_fill():
    loop = asyncio.get_event_loop()
    loop.create_task(s())
