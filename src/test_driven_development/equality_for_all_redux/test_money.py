from src.test_driven_development.equality_for_all_redux.money import Dollar, Franc


def test_multiplication():
    five = Dollar(5)
    assert five.times(2) == Dollar(10)
    assert five.times(3) == Dollar(15)


def test_equality():
    assert Dollar(5) == Dollar(5)
    assert Dollar(5) != Dollar(6)
    assert Franc(5) == Franc(5)
    assert Franc(5) != Franc(6)


def test_franc_multiplication():
    five = Franc(5)
    assert five.times(2) == Franc(10)
    assert five.times(3) == Franc(15)
