from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from pydantic import BaseModel, Field, field_validator

FOUR_DECIMALS = Decimal("0.0001")

class GlobalQuote(BaseModel):
    symbol: str

    open_price: Decimal
    high: Decimal
    low: Decimal
    price: Decimal

    volume: int

    latest_trading_day: date

    previous_close: Decimal
    change: Decimal

    change_percent: Decimal

    @field_validator(
        "open_price",
        "high",
        "low",
        "price",
        "previous_close",
        "change",
        "change_percent",
        mode="before",
    )
    def round_decimal(cls, v):
        if v is None:
            return v
        return Decimal(v).quantize(FOUR_DECIMALS, rounding=ROUND_HALF_UP)

    @classmethod
    def remove_percent(cls, v):
        return Decimal(v.replace("%", ""))
    
    @property
    def is_positive(self) -> bool:
        return self.change > 0
    
    def change_percent_fraction(self) -> float:
        return self.change_percent / 100

    model_config = {
        "populate_by_name": True
    }

class QuoteResponse(BaseModel):
    global_quote: GlobalQuote = Field(...)

    model_config = {
        "populate_by_name": True
    }