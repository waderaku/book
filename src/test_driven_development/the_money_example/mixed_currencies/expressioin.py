from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.test_driven_development.the_money_example.mixed_currencies.bank import Bank
    from src.test_driven_development.the_money_example.mixed_currencies.money import (
        Money,
    )


class Expression(ABC):
    @abstractmethod
    def reduce(self, bank: Bank, to: str) -> Money:
        raise NotImplementedError()

    @abstractmethod
    def plus(self, addend: Expression) -> Expression:
        raise NotImplementedError()
