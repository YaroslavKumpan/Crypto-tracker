import asyncio

from celery import Celery

from app.clients.deribit import DeribitClient
from app.core.config import settings
from app.db.session import async_session
from app.repositories.price_repository import PriceRepository
from app.services.price_service import PriceService

celery = Celery("tasks", broker=settings.REDIS_URL)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60.0, fetch_prices.s())


@celery.task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
def fetch_prices(self):
    asyncio.run(run())


async def run():
    client = DeribitClient()

    async with async_session() as db:
        repo = PriceRepository(db)
        service = PriceService(repo)

        btc = await client.get_price("btc_usd")
        eth = await client.get_price("eth_usd")

        await service.save_price("btc_usd", btc)
        await service.save_price("eth_usd", eth)