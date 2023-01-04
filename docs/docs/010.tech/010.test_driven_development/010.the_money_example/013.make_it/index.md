# 第 13 章 実装を導くテスト

-   前章の段階ではまだ仮実装の段階なので、「$5 + $5」は完了にできない
-   本章にて、一般性を持たせた実装にリファクタリングをする
-   まず、Money の plus メソッドは Money の代わりに Expression のインスタンス(Sum クラスとする)を返す必要がある

    -   TODO に追加しておく

    <!-- prettier-ignore -->
    !!! info
        -   $5 + 10CHF = $10 (レートが 2:1 の場合)
        -   **$5 + $5 = $10**
        -   $5 + $5がMoneyを返す

    -   一時的ではあるが、Sum が返却することを保証するテストを新規に追加する

    ```python
    def test_plus_returns_sum():
        five = Money.dollar(5)
        _sum = five.plus(five)
        assert _sum.augend == five
        assert _sum.addend == five
    ```

    -   まずはランタイムエラーを消すため、以下の変更を行う

        -   Sum クラスの作成
        -   plus メソッドの返却を Sum クラスにする

        ```python
        class Money(Expression):
            def plus(self, addend: Money) -> Expression:
                return Sum(self, addend)

        class Sum(Expression):
            def __init__(self, augend: Money, addend: Money):
                self.augend = augend
                self.addend = addend
        ```

    -   今回のテストは Sum クラスが返ってくることだけのテストなので、この段階でテストも通る

    -   次のステップに進む

        -   Bank の reduce メソッドは Sum を引数に取る
        -   Sum の通貨が同じ通貨ならば、足し算の結果も同じ通貨であり、足した結果の Money になる
        -   以下にそのテストを追加する
            ```python
            def test_reduce_sum():
                _sum = Sum(Money.dollar(3), Money.dollar(4))
                bank = Bank()
                result = bank.reduce(_sum, "USD")
                assert result == Money.dollar(7)
            ```
        -   現在は足し算の機能は存在しないため、エラーとなる
        -   reduce メソッドは Sum の内部の変数を足し算した結果が返ってくるはずである

            ```python
            class Bank:
                def reduce(self, source: Expression, to: str) -> Money:
                    amount = source.augend._amount + source.addend._amount
                    return Money(amount, to)
            ```

    -   これで同一通貨に対しての足し算に対しては一般性が保てた
    -   しかし、現在のコードは、Bank クラスが合計の計算の責務を担ってしまっている
    -   本来であれば、合計の計算を行うのは Sum クラスの責務である

        -   Bank が担ってしまっていることで、Sum 以外の計算が出来なくなってしまっている
        -   Sum クラスに reduce メソッドを追加し、そこで足し算の計算を行うように変更する

            ```python
            class Bank:
                def reduce(self, source: Expression, to: str) -> Money:
                    return source.reduce(to)

            class Sum(Expression):
                def reduce(self, to: str) -> Money:
                    amount = self.addend._amount + self.augend._amount
                    return Money(amount, to)
            ```

    -   現段階ではまだ Sum クラスが返ってくることが前提となっている

        -   あらゆる Expression クラス(現在は他に Money クラスしかない)が返ってきても問題がないように変更を加える
        -   まずは、Money クラスに対しての reduce のテストを記載する

            ```python
            def test_reduce_money():
                bank = Bank()
                result = bank.reduce(Money.dollar(1), "USD")
                assert result == Money.dollar(1)
            ```

        -   現在は Money クラスに reduce メソッドは実装されていないため、エラーとなる

            -   しかし、あらゆる式メタファーには reduce の実装が必要である

                -   Expression を ABC クラスとし、reduce メソッドを実装することで、継承先に reduce メソッドの実装を強制する

                -   その上で、Money クラスの reduce メソッドを追加する

            ```python
            class Expression(ABC):
                @abstractmethod
                def reduce(self, to: str) -> Money:
                    raise NotImplementedError()

            class Money(Expression):
                def reduce(self, to: str) -> Money:
                    return self
            ```

-   以上にて、同一通貨での足し算の機能は完了した
-   次章ではいよいよ通貨の変換に取り組む
-   一方で、上記のコードは、Expression と Bank の reduce メソッドのインターフェースが異なるのに、同じ名称を使用していることが気になる
-   その点も含めて、TODO に記しておく

<!-- prettier-ignore -->
!!! info
    -   $5 + 10CHF = $10 (レートが 2:1 の場合)
    -   <s>$5 + $5 = $10</s>
    -   <s>$5 + $5がMoneyを返す</s>
    -   <s>Bank.reduce(Money)</s>
    -   Moneyを変換して換算を行う
    -   reduce(Bank, str)
