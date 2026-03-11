import yfinance as yf
from fastapi import HTTPException
from app.schemas.quote_schema import QuoteResponse, GlobalQuote


def get_quote(ticker: str) -> QuoteResponse:
    ticker_b3 = ticker.upper()

    if not ticker_b3.endswith(".SA"):
        ticker_b3 += ".SA"

    stock = yf.Ticker(ticker_b3)
    data = stock.history(period="2d")

    if data.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Ticker '{ticker}' not found."
        )

    today = data.iloc[-1]
    yesterday = data.iloc[-2] if len(data) > 1 else today

    open_price = float(today["Open"])
    high = float(today["High"])
    low = float(today["Low"])
    close = float(today["Close"])
    volume = int(today["Volume"])
    previous_close = float(yesterday["Close"])

    change = close - previous_close
    change_percent = (change / previous_close) * 100

    trading_day = today.name.date()

    quote = GlobalQuote(
        symbol=ticker_b3,
        open_price=open_price,
        high=high,
        low=low,
        price=close,
        volume=volume,
        latest_trading_day=trading_day,
        previous_close=previous_close,
        change=change,
        change_percent=change_percent
    )

    return QuoteResponse(global_quote=quote)