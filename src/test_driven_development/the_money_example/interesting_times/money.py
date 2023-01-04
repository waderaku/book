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
        return Dollar(amount, "USD")

    @classmethod
    def franc(cls, amount: int) -> Money:
        return Franc(amount, "CHF")

    def currency(self) -> str:
        return self._currency

    def times(self, multiplier: int) -> Money:
        return Money(self._amount * multiplier, self._currency)


class Dollar(Money):
    def __init__(self, amount: int, currency: str):
        super().__init__(amount, currency)


class Franc(Money):
    def __init__(self, amount: int, currency: str):
        super().__init__(amount, currency)
