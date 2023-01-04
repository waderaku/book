from __future__ import annotations

from abc import ABC, abstractmethod


class Expression(ABC):
    @abstractmethod
    def reduce(self, to: str) -> Expression:
        raise NotImplementedError()
