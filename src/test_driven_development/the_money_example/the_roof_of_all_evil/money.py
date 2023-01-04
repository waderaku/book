from __future__ import annotations


class Money:
    def __init__(self, amount: int, currency: str):
        self._amount = amount
        self._currency = currency

    def __eq__(self, o: object) -> bool:
        if not issubclass(type(o), Money):
            return False
        return o._amount == self._amount and self._currency == o._currency

    @classmethod
    def dollar(cls, amount: int) -> Money:
        return Money(amount, "USD")

    @classmethod
    def franc(cls, amount: int) -> Money:
        return Money(amount, "CHF")

    def currency(self) -> str:
        return self._currency

    def times(self, multiplier: int) -> Money:
        return Money(self._amount * multiplier, self._currency)
