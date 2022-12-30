from __future__ import annotations


class Dollar:
    def __init__(self, amount: int):
        # Pythonにおいてprivate変数は先頭にアンダースコア2つ付ける事で表現されるが、
        # 慣例としてアンダースコア1つ付けてprivate変数であることを宣言することが多いため、こちらを採用する
        self._amount = amount

    def times(self, multiplier: int) -> Dollar:
        return Dollar(self._amount * multiplier)

    def __eq__(self, o: object) -> bool:
        if type(o) is not Dollar:
            return False
        return o._amount == self._amount
