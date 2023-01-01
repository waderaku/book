from src.test_driven_development.make_it.expressioin import Expression
from src.test_driven_development.make_it.money import Money


class Bank:
    def reduce(self, source: Expression, to: str) -> Money:
        return source.reduce(to)
