from __future__ import annotations


class Dollar:
    def __init__(self, amount: int):
        self.amount = amount

    def times(self, multiplier: int) -> Dollar:
        return Dollar(self.amount * multiplier)

    def __eq__(self, o: object) -> bool:
        if type(o) is not Dollar:
            return False
        return o.amount == self.amount
