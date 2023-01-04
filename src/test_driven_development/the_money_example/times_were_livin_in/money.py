from __future__ import annotations

from abc import abstractmethod


class Money:
    def __init__(self, amount: int, currency: str):
        self._amount = amount
        self._currency = currency

    def __eq__(self, o: object) -> bool:
        if not issubclass(type(o), Money):
            return False
        return o._amount == self._amount and type(self) is type(o)

    @classmethod
    def dollar(cls, amount: int) -> Money:
        return Dollar(amount, "USD")

    @classmethod
    def franc(cls, amount: int) -> Money:
        return Franc(amount, "CHF")

    @abstractmethod
    def times(self, amount: int) -> Money:
        raise NotImplementedError()

    def currency(self) -> str:
        return self._currency


class Dollar(Money):
    def __init__(self, amount: int, currency: str):
        super().__init__(amount, currency)

    def times(self, multiplier: int) -> Dollar:
        return Money.dollar(self._amount * multiplier)


class Franc(Money):
    def __init__(self, amount: int, currency: str):
        super().__init__(amount, currency)

    def times(self, multiplier: int) -> Franc:
        return Money.franc(self._amount * multiplier)
