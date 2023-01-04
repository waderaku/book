from src.test_driven_development.the_money_example.muiti_currency_money.money import (
    Dollar,
)


def test_multiplication():
    five = Dollar(5)
    five.times(2)
    assert five.amount == 10
