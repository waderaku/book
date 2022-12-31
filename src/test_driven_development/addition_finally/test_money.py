from src.test_driven_development.addition_finally.bank import Bank
from src.test_driven_development.addition_finally.expressioin import Expression
from src.test_driven_development.addition_finally.money import Money


def test_multiplication():
    five = Money.dollar(5)
    assert five.times(2) == Money.dollar(10)
    assert five.times(3) == Money.dollar(15)


def test_equality():
    assert Money.dollar(5) == Money.dollar(5)
    assert Money.dollar(5) != Money.dollar(6)
    assert Money.dollar(5) != Money.franc(5)


def test_currency():
    assert "USD" == Money.dollar(1).currency()
    assert "CHF" == Money.franc(1).currency()


def test_simple_addition():
    _sum: Expression = Money.dollar(5).plus(Money.dollar(5))
    bank = Bank()
    reduced = bank.reduce(_sum, "USD")
    assert reduced == Money.dollar(10)
