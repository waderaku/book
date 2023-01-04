from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.test_driven_development.the_money_example.mixed_currencies.bank import Bank

from src.test_driven_development.the_money_example.mixed_currencies.expressioin import (
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

    def times(self, multiplier: int) -> Expression:
        return Money(self._amount * multiplier, self._currency)

    def plus(self, addend: Expression) -> Expression:
        return Sum(self, addend)

    def reduce(self, bank: Bank, to: str) -> Money:
        rate = bank.rate(self._currency, to)
        return Money(self._amount / rate, to)

    @classmethod
    def dollar(cls, amount: int) -> Money:
        return Money(amount, "USD")

    @classmethod
    def franc(cls, amount: int) -> Money:
        return Money(amount, "CHF")


class Sum(Expression):
    def __init__(self, augend: Expression, addend: Expression):
        self.augend = augend
        self.addend = addend

    def reduce(self, bank: Bank, to: str) -> Money:
        amount = (
            self.addend.reduce(bank, to)._amount + self.augend.reduce(bank, to)._amount
        )
        return Money(amount, to)

    def plus(self, addend: Expression) -> Expression:
        pass
