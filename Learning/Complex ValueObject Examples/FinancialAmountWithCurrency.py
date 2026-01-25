from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from valueobject import ValueObject


@dataclass(frozen=True)
class CurrencyCode:
    """Currency code value object"""
    code: str

    def __post_init__(self):
        if len(self.code) != 3 or not self.code.isalpha():
            raise ValueError("Currency code must be 3 letters")


@dataclass(frozen=True)
class Money(ValueObject):
    amount: Decimal
    currency: CurrencyCode
    exchange_rate: Optional[Decimal] = None

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")
        if self.exchange_rate is not None and self.exchange_rate <= 0:
            raise ValueError("Exchange rate must be positive")


# Usage
money = Money(Decimal('99.99'), CurrencyCode('USD'), Decimal('1.25'))
print(repr(money))  # Money(amount=Decimal('99.99'), currency=CurrencyCode(code='USD'), exchange_rate=Decimal('1.25'))