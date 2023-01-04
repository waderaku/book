from __future__ import annotations

from src.test_driven_development.the_money_example.make_it.expressioin import Expression


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
        return Sum(self, addend)

    def reduce(self, to: str) -> Money:
        return self

    @classmethod
    def dollar(cls, amount: int) -> Money:
        return Money(amount, "USD")

    @classmethod
    def franc(cls, amount: int) -> Money:
        return Money(amount, "CHF")


class Sum(Expression):
    def __init__(self, augend: Money, addend: Money):
        self.augend = augend
        self.addend = addend

    def reduce(self, to: str) -> Money:
        amount = self.addend._amount + self.augend._amount
        return Money(amount, to)
