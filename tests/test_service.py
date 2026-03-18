import pytest
from app.services.price_service import PriceService


class FakeRepo:
    def __init__(self):
        self.data = []

    async def create(self, obj):
        self.data.append(obj)


@pytest.mark.asyncio
async def test_save_price():
    repo = FakeRepo()
    service = PriceService(repo)

    await service.save_price("btc_usd", 100)

    assert len(repo.data) == 1