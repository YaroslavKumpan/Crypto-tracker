import time

from app.db.models import Price


class PriceService:
    def __init__(self, repo):
        self.repo = repo

    async def save_price(self, ticker, price):
        obj = Price(
            ticker=ticker,
            price=price,
            timestamp=int(time.time())
        )
        await self.repo.create(obj)

    async def get_all(self, ticker):
        return await self.repo.get_all(ticker)

    async def get_latest(self, ticker):
        return await self.repo.get_latest(ticker)

    async def get_filtered(self, ticker, from_ts, to_ts):
        return await self.repo.get_by_range(ticker, from_ts, to_ts)