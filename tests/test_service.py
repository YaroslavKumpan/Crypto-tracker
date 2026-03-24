import asyncio
from app.services.price_service import PriceService


class FakeRepo:
    def __init__(self):
        self.data = []
        self.latest = None

    async def create(self, obj):
        self.data.append(obj)

    async def get_all(self, ticker):
        return [item for item in self.data if item.ticker == ticker]

    async def get_latest(self, ticker):
        filtered = [item for item in self.data if item.ticker == ticker]
        return filtered[-1] if filtered else None

    async def get_by_range(self, ticker, from_ts, to_ts):
        return [
            item
            for item in self.data
            if item.ticker == ticker and from_ts <= item.timestamp <= to_ts
        ]


def test_save_price():
    repo = FakeRepo()
    service = PriceService(repo)

    asyncio.run(service.save_price("btc_usd", 100))

    assert len(repo.data) == 1


def test_get_latest():
    repo = FakeRepo()
    service = PriceService(repo)

    asyncio.run(service.save_price("btc_usd", 100))
    asyncio.run(service.save_price("btc_usd", 101))

    latest = asyncio.run(service.get_latest("btc_usd"))
    assert latest.price == 101


def test_get_filtered():
    repo = FakeRepo()
    service = PriceService(repo)

    asyncio.run(service.save_price("btc_usd", 100))
    first_ts = repo.data[0].timestamp

    result = asyncio.run(service.get_filtered("btc_usd", first_ts, first_ts))
    assert len(result) == 1
