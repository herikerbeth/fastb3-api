import yfinance as yf
from fastapi import HTTPException

from app.schemas.etf_schema import ETFResponse, ETFInfo
from app.utils.finance import normalize_b3_ticker


def get_etf_info(ticker: str) -> ETFResponse:
    ticker = normalize_b3_ticker(ticker)

    try:
        etf = yf.Ticker(ticker)
        info = etf.info

        if not info or info.get("symbol") != ticker:
            raise HTTPException(
                status_code=404,
                detail=f"ETF '{ticker}' not found."
            )

        etf_data = ETFInfo(
            symbol=ticker,
            name=info.get("shortName", "N/A"),
            price=info.get("regularMarketPrice"),
            currency=info.get("currency", "BRL"),
            market_cap=info.get("marketCap"),
            sector=info.get("sector"),
        )

        return ETFResponse(data=etf_data)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))