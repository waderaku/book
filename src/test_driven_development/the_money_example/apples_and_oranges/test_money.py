from src.test_driven_development.the_money_example.apples_and_oranges.money import (
    Dollar,
    Franc,
)


def test_multiplication():
    five = Dollar(5)
    assert five.times(2) == Dollar(10)
    assert five.times(3) == Dollar(15)


def test_equality():
    assert Dollar(5) == Dollar(5)
    assert Dollar(5) != Dollar(6)
    assert Franc(5) == Franc(5)
    assert Franc(5) != Franc(6)
    assert Dollar(5) != Franc(5)


def test_franc_multiplication():
    five = Franc(5)
    assert five.times(2) == Franc(10)
    assert five.times(3) == Franc(15)
