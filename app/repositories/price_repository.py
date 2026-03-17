from sqlalchemy import select
from app.db.models import Price


class PriceRepository:
    def __init__(self, db):
        self.db = db

    async def create(self, obj: Price):
        self.db.add(obj)
        await self.db.commit()

    async def get_all(self, ticker):
        res = await self.db.execute(
            select(Price).where(Price.ticker == ticker)
        )
        return res.scalars().all()

    async def get_latest(self, ticker):
        res = await self.db.execute(
            select(Price)
            .where(Price.ticker == ticker)
            .order_by(Price.timestamp.desc())
            .limit(1)
        )
        return res.scalar()

    async def get_by_range(self, ticker, from_ts, to_ts):
        res = await self.db.execute(
            select(Price).where(
                Price.ticker == ticker,
                Price.timestamp.between(from_ts, to_ts)
            )
        )
        return res.scalars().all()