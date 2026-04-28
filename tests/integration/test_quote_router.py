from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.schemas.quote_schema import QuoteResponse

client = TestClient(app)

def test_root_returns_200():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to FastB3 API"}

@patch("app.routers.quote_router.get_quote")
def test_get_price_returns_valid_quote(mock_service):
    mock_service.return_value = {
        "data": {
            "symbol": "PETR4.SA",
            "open": "43.2500",
            "high": "44.2700",
            "low": "43.0100",
            "price": "43.9000",
            "volume": 47876000,
            "date": "2026-03-09",
            "previous_close": "42.1100",
            "change": "1.7900",
            "change_percent": "4.2508"
        }
    }

    response = client.get("/stock/PETR4")

    assert response.status_code == 200

    quote_response = QuoteResponse(**response.json())
    quote = quote_response.data
    assert quote.symbol == "PETR4.SA"
    assert quote.price > 0
    assert quote.high > 0
    assert quote.low > 0

def test_get_price_invalid_symbol_returns_404():
    response = client.get("/stock/INVALID")

    assert response.status_code == 404