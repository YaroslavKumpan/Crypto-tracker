from sqlalchemy import Column, Integer, String, Float, BigInteger, Index

from app.db.base import Base


class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True)
    ticker = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(BigInteger, nullable=False)

    __table_args__ = (
        Index("idx_ticker_timestamp", "ticker", "timestamp"),
    )