from __future__ import annotations


class Money:
    def __init__(self, amount: int):
        self._amount = amount

    def __eq__(self, o: object) -> bool:
        if not issubclass(type(o), Money):
            return False
        return o._amount == self._amount


class Dollar(Money):
    def __init__(self, amount: int):
        super().__init__(amount)

    def times(self, multiplier: int) -> Dollar:
        return Dollar(self._amount * multiplier)


class Franc(Money):
    def __init__(self, amount: int):
        super().__init__(amount)

    def times(self, multiplier: int) -> Franc:
        return Franc(self._amount * multiplier)
