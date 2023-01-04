class Pair:
    def __init__(self, _from: str, to: str):
        self._from = _from
        self._to = to

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Pair):
            return False
        return __o._from == self._from and __o._to == self._to

    def __hash__(self) -> int:
        return 0
