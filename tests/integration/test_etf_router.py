from decimal import Decimal
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app
from app.schemas.etf_schema import ETFResponse

client = TestClient(app)


@patch("app.routers.etf_router.get_etf_info")
def test_get_etf_info_returns_valid_info(mock_service):

    mock_service.return_value = {
        "data": {
            "symbol": "TEST.SA",
            "name": "Test ETF",
            "price": Decimal("123.45"),
            "currency": "USD",
            "market_cap": 1_000_000_000,
            "sector": "Finance",
        }
    }

    response = client.get("/etf/TEST")

    assert response.status_code == 200

    etf_info = ETFResponse(**response.json())

    etf = etf_info.data

    assert etf.symbol == "TEST.SA"
    assert etf.name == "Test ETF"
    assert etf.price == Decimal("123.4500")
    assert etf.currency == "USD"
    assert etf.market_cap == 1_000_000_000
    assert etf.sector == "Finance"


def test_get_etf_info_invalid_symbol_returns_404():
    response = client.get("/etf/INVALID")

    assert response.status_code == 404