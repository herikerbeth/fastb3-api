from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from pydantic import BaseModel, Field, field_validator

from app.utils.finance import to_decimal

class Quote(BaseModel):
    symbol: str

    open: Decimal
    high: Decimal
    low: Decimal
    price: Decimal

    volume: int
    date: date

    previous_close: Decimal
    change: Decimal
    change_percent: Decimal

    @field_validator(
        "open",
        "high",
        "low",
        "price",
        "previous_close",
        "change",
        "change_percent",
        mode="before",
    )
    def normalize_decimals(cls, v):
        return to_decimal(v)

    @property
    def is_positive(self) -> bool:
        return self.change > 0

    def change_percent_fraction(self) -> float:
        return float(self.change_percent / 100)


class QuoteResponse(BaseModel):
    data: Quote = Field(...)