from __future__ import annotations


class Dollar:
    def __init__(self, amount: int):
        self._amount = amount

    def times(self, multiplier: int) -> Dollar:
        return Dollar(self._amount * multiplier)

    def __eq__(self, o: object) -> bool:
        if type(o) is not Dollar:
            return False
        return o._amount == self._amount


class Franc:
    def __init__(self, amount: int):
        self._amount = amount

    def times(self, multiplier: int) -> Franc:
        return Franc(self._amount * multiplier)

    def __eq__(self, o: object) -> bool:
        if type(o) is not Franc:
            return False
        return o._amount == self._amount
