from fastapi import APIRouter, Path
from app.schemas.quote_schema import QuoteResponse
from app.services.quote_service import get_quote

router = APIRouter(
    prefix="/stock",
    tags=["Quotes"]
)

@router.get("/{ticker}", response_model=QuoteResponse)
def get_price(
    ticker: str = Path(..., description="Stock ticker, example: PETR4")
):
    return get_quote(ticker)