from decimal import Decimal
from unittest.mock import patch, MagicMock, PropertyMock
import pytest
from fastapi import HTTPException
from app.services.etf_service import get_etf_info
from app.schemas.etf_schema import ETFResponse


def mock_etf_info():
    return {
        "symbol": "TEST.SA",
        "shortName": "Test ETF",
        "regularMarketPrice": 123.45,
        "currency": "BRL",
        "marketCap": 1_000_000_000,
        "sector": "Finance",
    }


@patch("app.services.etf_service.yf.Ticker")
def test_get_etf_info_success(mock_Ticker):
    # Arrange
    mock_ticker = MagicMock()
    mock_ticker.info = mock_stock_info()
    mock_Ticker.return_value = mock_ticker

    # Act
    response = get_etf_info("test")

    # Assert
    assert isinstance(response, ETFResponse)

    etf = response.data

    assert etf.symbol == "TEST.SA"
    assert etf.name == "Test ETF"
    assert etf.price == Decimal("123.4500")
    assert etf.currency == "BRL"
    assert etf.market_cap == 1_000_000_000
    assert etf.sector == "Finance"

    mock_Ticker.assert_called_once_with("TEST.SA")


@patch("app.services.etf_service.yf.Ticker")
def test_get_etf_info_not_found(mock_Ticker):
    # Arrange
    mock_ticker = MagicMock()
    mock_ticker.info = {}
    mock_Ticker.return_value = mock_ticker

    # Act & Assert
    with pytest.raises(HTTPException) as exc:
        get_etf_info("unknown")

    assert exc.value.status_code == 404
    assert "not found" in exc.value.detail

    mock_Ticker.assert_called_once_with("UNKNOWN.SA")


@patch("app.services.etf_service.yf.Ticker")
def test_get_etf_info_info_missing_symbol(mock_Ticker):
    # Arrange
    mock_ticker = MagicMock()
    mock_ticker.info = {"symbol": "DIFFERENT"}
    mock_Ticker.return_value = mock_ticker

    # Act & Assert
    with pytest.raises(HTTPException) as exc:
        get_etf_info("test")

    assert exc.value.status_code == 404
    assert "not found" in exc.value.detail

    mock_Ticker.assert_called_once_with("TEST.SA")


@patch("app.services.etf_service.yf.Ticker")
def test_get_etf_info_generic_error(mock_Ticker):
    # Arrange
    mock_ticker = MagicMock()

    type(mock_ticker).info = PropertyMock(side_effect=RuntimeError("Network error"))

    mock_Ticker.return_value = mock_ticker

    # Act & Assert
    with pytest.raises(HTTPException) as exc:
        get_etf_info("test")

    assert exc.value.status_code == 500
    assert "Network error" in exc.value.detail

    mock_Ticker.assert_called_once_with("TEST.SA")