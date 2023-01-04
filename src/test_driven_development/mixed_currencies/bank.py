from src.test_driven_development.change.expressioin import Expression
from src.test_driven_development.change.money import Money
from src.test_driven_development.change.pair import Pair


class Bank:
    def __init__(self):
        self._rates = {}

    def reduce(self, source: Expression, to: str) -> Money:
        return source.reduce(self, to)

    def add_rate(self, _from: str, to: str, rate: int):
        pair = Pair(_from, to)
        self._rates[pair] = rate

    def rate(self, _from: str, to: str) -> int:
        if _from == to:
            return 1
        return self._rates[Pair(_from, to)]
