# 第 8 章 実装を隠す

<!-- prettier-ignore -->
!!! info
    -   $5 + 10CHF = $10 (レートが 2:1 の場合)
    -   <s>$5 \* 2 = $10</s>
    -   <s>amount を private にする</s>
    -   <s>Dollar の副作用どうする？</s>
    -   Money の丸め処理どうする？
    -   <s>\_\_eq\_\_メソッド</s>
    -   \_\_hash\_\_メソッド
    -   null との等価性比較
    -   他のオブジェクトとの等価性比較
    -   <s>5CHF \* 2 = 10CHF</s>
    -   **Dollar と Franc の重複**
    -   <s>equals の一般化</s>
    -   times の一般化
    -   <s>Franc と Dollar を比較する</s>
    -   通貨の概念

-   現時点で、Franc と Dollar の times メソッドは似通っている
-   そこで、本章では、Franc と Dollar の重複を排除し、Money オブジェクトに責務を移管していく
-   Dollar、Franc は大した仕事をしていないので、この際消してしまいたいため、小さなステップを繰り返してそれを実現していく

    -   まず、Dollar、Franc の times メソッドの戻り値を Money に変更する
        -   Python においては特段意味のある変更ではない（type hinting の変更）が、本文では Java コードであるため記載
    -   コンシューマが Dollar、Franc への依存箇所を減らしていくため、まずは Money に FactorMethod を用意する

    ```python
    def test_multiplication():
        five = Money.dollar(5)
        assert five.times(2) == Money.dollar(10)
        assert five.times(3) == Money.dollar(15)


    class Money:
        def __init__(self, amount: int):
            self._amount = amount

        def __eq__(self, o: object) -> bool:
            if not issubclass(type(o), Money):
                return False
            return o._amount == self._amount and type(self) is type(o)

        @classmethod
        def dollar(cls, amount: int) -> Money:
            return Dollar(amount)

        @abstractmethod
        def times(self, amount: int) -> Money:
            raise NotImplementedError()
    ```

    -   また、Money 側に times インターフェースがないため、追加で times メソッドを abstract メソッドとして追加している
    -   これを使用して、全てのテストコードから dollar への依存を弾くことができる

    ```python
    def test_multiplication():
        five = Money.dollar(5)
        assert five.times(2) == Money.dollar(10)
        assert five.times(3) == Money.dollar(15)


    def test_equality():
        assert Money.dollar(5) == Money.dollar(5)
        assert Money.dollar(5) != Money.dollar(6)
        assert Franc(5) == Franc(5)
        assert Franc(5) != Franc(6)
        assert Money.dollar(5) != Franc(5)


    def test_franc_multiplication():
        five = Franc(5)
        assert five.times(2) == Franc(10)
        assert five.times(3) == Franc(15)
    ```

    -   テストからサブクラスの存在が切り離されたので、既存のコードの影響を及ぼさずに継承構造を変更する権利を手に入れた
    -   同じことを Franc にも適用したい

        -   しかし、test_franc_multiplication から Franc への依存を弾いた時、そこでテストしようとしているロジックは既に test_multiplication によって全てテストされていることに気が付く
        -   今後削除される可能性も考慮しつつ、一先ず同様の作業を行う

        ```python
        def test_multiplication():
            five = Money.dollar(5)
            assert five.times(2) == Money.dollar(10)
            assert five.times(3) == Money.dollar(15)


        def test_equality():
            assert Money.dollar(5) == Money.dollar(5)
            assert Money.dollar(5) != Money.dollar(6)
            assert Money.franc(5) == Money.franc(5)
            assert Money.franc(5) != Money.franc(6)
            assert Money.dollar(5) != Money.franc(5)


        def test_franc_multiplication():
            five = Money.franc(5)
            assert five.times(2) == Money.franc(10)
            assert five.times(3) == Money.franc(15)


        class Money:
            def __init__(self, amount: int):
                self._amount = amount

            def __eq__(self, o: object) -> bool:
                if not issubclass(type(o), Money):
                    return False
                return o._amount == self._amount and type(self) is type(o)

            @classmethod
            def dollar(cls, amount: int) -> Money:
                return Dollar(amount)

            @classmethod
            def franc(cls, amount: int) -> Money:
                return Franc(amount)

            @abstractmethod
            def times(self, amount: int) -> Money:
                raise NotImplementedError()
        ```

-   ここまでの一連作業で、外部からの Dollar、Franc への依存性を完全に排除することができた
-   ただし、times メソッドはいまだそれぞれのクラスに存在している。ここについては、次章移行で解決していく
