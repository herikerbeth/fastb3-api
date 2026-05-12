from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, field_validator

from app.utils.finance import to_decimal


class ETFInfo(BaseModel):
    symbol: str
    name: str
    price: Optional[Decimal]
    currency: str
    market_cap: Optional[int]
    sector: Optional[str]

    @field_validator("price", mode="before")
    def validate_price(cls, v):
        return to_decimal(v)


class ETFResponse(BaseModel):
    data: ETFInfo