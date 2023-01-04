from src.test_driven_development.the_money_example.make_it.bank import Bank
from src.test_driven_development.the_money_example.make_it.money import Money, Sum


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
    _sum = Money.dollar(5).plus(Money.dollar(5))
    bank = Bank()
    reduced = bank.reduce(_sum, "USD")
    assert reduced == Money.dollar(10)


def test_plus_returns_sum():
    five = Money.dollar(5)
    _sum = five.plus(five)
    assert _sum.augend == five
    assert _sum.addend == five


def test_reduce_sum():
    _sum = Sum(Money.dollar(3), Money.dollar(4))
    bank = Bank()
    result = bank.reduce(_sum, "USD")
    assert result == Money.dollar(7)


def test_reduce_money():
    bank = Bank()
    result = bank.reduce(Money.dollar(1), "USD")
    assert result == Money.dollar(1)
