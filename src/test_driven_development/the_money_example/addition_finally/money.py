from __future__ import annotations

from src.test_driven_development.the_money_example.addition_finally.expressioin import (
    Expression,
)


class Money(Expression):
    def __init__(self, amount: int, currency: str):
        self._amount = amount
        self._currency = currency

    def __eq__(self, o: object) -> bool:
        if not issubclass(type(o), Money):
            return False
        return o._amount == self._amount and self._currency == o._currency

    def currency(self) -> str:
        return self._currency

    def times(self, multiplier: int) -> Money:
        return Money(self._amount * multiplier, self._currency)

    def plus(self, addend: Money) -> Expression:
        return Money(self._amount + addend._amount, self._currency)

    @classmethod
    def dollar(cls, amount: int) -> Money:
        return Money(amount, "USD")

    @classmethod
    def franc(cls, amount: int) -> Money:
        return Money(amount, "CHF")
