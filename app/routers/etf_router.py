from fastapi import APIRouter, Path
from app.schemas.etf_schema import ETFResponse
from app.services.etf_service import get_etf_info

router = APIRouter(
    prefix="/etf", 
    tags=["ETFs"]
)

@router.get("/{ticker}", response_model=ETFResponse)
def get_etf(
    ticker: str = Path(..., description="ETF ticker, example: GOLD11")
):
    return get_etf_info(ticker)