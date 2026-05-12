import yfinance as yf
from fastapi import HTTPException
from app.schemas.quote_schema import QuoteResponse, Quote
from app.utils.finance import normalize_b3_ticker


def get_quote(ticker: str) -> QuoteResponse:
    ticker = normalize_b3_ticker(ticker)

    stock = yf.Ticker(ticker)
    data = stock.history(period="2d")

    if data.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Ticker '{ticker}' not found."
        )

    today = data.iloc[-1]
    yesterday = data.iloc[-2] if len(data) > 1 else today

    quote = Quote(
        symbol=ticker,
        open=today["Open"],
        high=today["High"],
        low=today["Low"],
        price=today["Close"],
        volume=int(today["Volume"]),
        date=today.name.date(),
        previous_close=yesterday["Close"],
        change=today["Close"] - yesterday["Close"],
        change_percent=((today["Close"] - yesterday["Close"]) / yesterday["Close"]) * 100,
    )

    return QuoteResponse(data=quote)