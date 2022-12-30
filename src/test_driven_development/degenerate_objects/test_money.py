from src.test_driven_development.degenerate_objects.money import Dollar


def test_multiplication():
    five = Dollar(5)
    prouct = five.times(2)
    assert prouct.amount == 10
    product = five.times(3)
    assert product.amount == 15
