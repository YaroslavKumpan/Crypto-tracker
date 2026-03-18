from fastapi import APIRouter, Depends, Query, HTTPException

from app.db.session import get_db
from app.repositories.price_repository import PriceRepository
from app.schemas.price import PriceResponse
from app.services.price_service import PriceService

router = APIRouter()


VALID_TICKERS = ("btc_usd", "eth_usd")


def get_service(db=Depends(get_db)):
    return PriceService(PriceRepository(db))


def validate_ticker(ticker: str):
    if ticker not in VALID_TICKERS:
        raise HTTPException(status_code=400, detail="Invalid ticker")


@router.get("/prices", response_model=list[PriceResponse])
async def get_all(
    ticker: str = Query(...),
    service: PriceService = Depends(get_service),
):
    validate_ticker(ticker)

    data = await service.get_all(ticker)

    if not data:
        raise HTTPException(status_code=404, detail="No data found")

    return data


@router.get("/prices/latest", response_model=PriceResponse)
async def get_latest(
    ticker: str = Query(...),
    service: PriceService = Depends(get_service),
):
    validate_ticker(ticker)

    data = await service.get_latest(ticker)

    if not data:
        raise HTTPException(status_code=404, detail="Not found")

    return data


@router.get("/prices/filter", response_model=list[PriceResponse])
async def get_filtered(
    ticker: str = Query(...),
    from_ts: int = Query(...),
    to_ts: int = Query(...),
    service: PriceService = Depends(get_service),
):
    validate_ticker(ticker)

    data = await service.get_filtered(ticker, from_ts, to_ts)

    if not data:
        raise HTTPException(status_code=404, detail="No data found")

    return data


@router.get("/health")
async def health():
    return {"status": "ok"}