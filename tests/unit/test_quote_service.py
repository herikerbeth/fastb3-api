from unittest.mock import patch
import pandas as pd
import pytest
from fastapi import HTTPException
from app.services.quote_service import get_quote
from app.schemas.quote_schema import QuoteResponse


@patch("app.services.quote_service.yf.Ticker")
def test_get_quote_returns_valid_quote(mock_ticker):

    mock_ticker.return_value.history.return_value = mock_stock_history()

    quote_response = get_quote("PETR4")

    assert isinstance(quote_response, QuoteResponse)

    quote = quote_response.data

    assert quote.symbol == "PETR4.SA"
    assert quote.price > 0
    assert quote.volume >= 0
    assert quote.high >= quote.low

@patch("app.services.quote_service.yf.Ticker")
def test_get_quote_returns_404_when_symbol_not_found(mock_ticker):

    df = pd.DataFrame()

    mock_ticker.return_value.history.return_value = df

    with pytest.raises(HTTPException) as exc:
        get_quote("INVALID")

    assert exc.value.status_code == 404

@patch("app.services.quote_service.yf.Ticker")
def test_get_quote_calculates_price_change(mock_ticker):

    mock_ticker.return_value.history.return_value = mock_stock_history()

    data = get_quote("PETR4")
    quote = data.data

    history = mock_stock_history()

    previous_close = history.iloc[0]["Close"]
    current_price = history.iloc[1]["Close"]

    expected_change = current_price - previous_close
    expected_change_percent = (expected_change / previous_close) * 100

    assert float(quote.change) == pytest.approx(expected_change)
    assert float(quote.change_percent) == pytest.approx(expected_change_percent)

@patch("app.services.quote_service.yf.Ticker")
def test_get_quote_returns_positive_change(mock_ticker):

    mock_ticker.return_value.history.return_value = mock_stock_history()

    data = get_quote("PETR4")
    quote = data.data

    assert quote.is_positive is True

@patch("app.services.quote_service.yf.Ticker")
def test_get_quote_returns_negative_change(mock_ticker):

    df = pd.DataFrame(
        [
            {"Open": 43.2500, "High": 44.2700, "Low": 43.0100, "Close": 42.11, "Volume": 47876000},
            {"Open": 42.1100, "High": 43.1300, "Low": 41.0900, "Close": 41.11, "Volume": 47876000}
        ],
        index=pd.to_datetime(["2026-02-01", "2026-03-02"])
    )

    mock_ticker.return_value.history.return_value = df

    data = get_quote("PETR4")
    quote = data.data

    previous_close = df.iloc[0]["Close"]
    current_price = df.iloc[1]["Close"]

    expected_change = current_price - previous_close
    expected_change_percent = (expected_change / previous_close) * 100

    assert float(quote.change) == pytest.approx(expected_change)
    assert float(quote.change_percent) == pytest.approx(expected_change_percent, rel=1e-3)
    assert quote.is_positive is False

def mock_stock_history():
    return pd.DataFrame(
        [
            {"Open": 43.2500, "High": 44.2700, "Low": 43.0100, "Close": 41.11, "Volume": 47876000},
            {"Open": 42.1100, "High": 43.1300, "Low": 41.0900, "Close": 42.11, "Volume": 47876000}
        ],
        index=pd.to_datetime(["2026-02-01", "2026-03-02"])
    )