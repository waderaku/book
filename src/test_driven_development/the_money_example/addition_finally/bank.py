from src.test_driven_development.the_money_example.addition_finally.expressioin import (
    Expression,
)
from src.test_driven_development.the_money_example.addition_finally.money import Money


class Bank:
    def reduce(self, source: Expression, to: str) -> Money:
        return Money.dollar(10)
