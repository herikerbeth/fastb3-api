from decimal import Decimal, ROUND_HALF_UP

FOUR_DECIMALS = Decimal("0.0001")


def normalize_b3_ticker(ticker: str) -> str:
    ticker = ticker.strip().upper()
    if not ticker.endswith(".SA"):
        ticker += ".SA"
    return ticker


def to_decimal(value):
    if value is None:
        return None
    return Decimal(value).quantize(FOUR_DECIMALS, rounding=ROUND_HALF_UP)