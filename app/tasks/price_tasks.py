import asyncio
import logging
import time

from celery import Celery

from app.clients.deribit import DeribitClient
from app.core.config import settings
from app.db.models import Price
from app.db.sync_session import SessionLocal

logger = logging.getLogger(__name__)

celery_app = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

# каждые 60 секунд
celery_app.conf.beat_schedule = {
    "fetch-prices-every-minute": {
        "task": "app.tasks.price_tasks.fetch_prices",
        "schedule": 60.0,
    },
}


async def fetch_all_prices():
    client = DeribitClient()
    return await client.get_prices(["btc_usd", "eth_usd"])


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={"max_retries": 3})
def fetch_prices(self):
    logger.info("Fetching prices...")

    btc_price, eth_price = asyncio.run(fetch_all_prices())

    db = SessionLocal()

    try:
        now = int(time.time())

        if not isinstance(btc_price, Exception):
            db.add(Price(ticker="btc_usd", price=btc_price, timestamp=now))
        else:
            logger.error(f"BTC error: {btc_price}")

        if not isinstance(eth_price, Exception):
            db.add(Price(ticker="eth_usd", price=eth_price, timestamp=now))
        else:
            logger.error(f"ETH error: {eth_price}")

        db.commit()
        logger.info("Saved prices")

    except Exception as e:
        db.rollback()
        logger.error(f"DB error: {e}")
        raise

    finally:
        db.close()
