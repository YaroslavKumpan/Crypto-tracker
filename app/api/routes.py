from fastapi import APIRouter, Depends, Query
from app.db.session import get_db
from app.repositories.price_repository import PriceRepository
from app.services.price_service import PriceService

router = APIRouter()


def get_service(db=Depends(get_db)):
    return PriceService(PriceRepository(db))


@router.get("/prices")
async def get_all(ticker: str = Query(...), service=Depends(get_service)):
    return await service.get_all(ticker)


@router.get("/prices/latest")
async def get_latest(ticker: str = Query(...), service=Depends(get_service)):
    return await service.get_latest(ticker)


@router.get("/prices/filter")
async def get_filtered(
    ticker: str = Query(...),
    from_ts: int = Query(...),
    to_ts: int = Query(...),
    service=Depends(get_service),
):
    return await service.get_filtered(ticker, from_ts, to_ts)


@router.get("/health")
async def health():
    return {"status": "ok"}