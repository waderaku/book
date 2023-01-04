# 第 15 章 テスト任せとコンパイラ任せ

<!-- prettier-ignore -->
!!! info
    -   **$5 + 10CHF = $10 (レートが 2:1 の場合)**
    -   <s>$5 + $5 = $10</s>
    -   <s>$5 + $5がMoneyを返す</s>
    -   <s>Bank.reduce(Money)</s>
    -   <s>Moneyを変換して換算を行う</s>
    -   <s>reduce(Bank, str)</s>

-   本章にてついに別レートの足し算の計算を実装する
-   まずはこれまで通り、仕様に従うテストを実装する

    ```python
    def test_mixed_addition():
        five_bucks = Money.dollar(5)
        ten_francs = Money.franc(10)
        bank = Bank()
        bank.add_rate("CHF", "USD", 2)
        result = bank.reduce(five_bucks.plus(ten_francs), "USD")
        assert result == Money.dollar(10)
    ```

    -   テストは通らない。10USD ではなく 15USD が返ってきている
    -   Sum の reduce メソッドが引数を換算していないからである
    -   足し算をする前に、addend と augend の両方を換算するように変更する

    ```python
    class Sum(Expression):
        def reduce(self, bank: Bank, to: str) -> Money:
            amount = (
                self.addend.reduce(bank, to)._amount + self.augend.reduce(bank, to)._amount
            )
            return Money(amount, to)
    ```

    -   ここからは抽象化に取り組んでいく。変更ごとにテストを動かし、通ることを確認しながら進める
    -   まずは Sum の augend と addend を Expression に変更し、Money の plus メソッドの引数と times メソッドの戻り値を Expression に変更する

    ```python
    class Sum(Expression):
        def __init__(self, augend: Expression, addend: Expression):
            self.augend = augend
            self.addend = addend

    class Money(Expression):
        def plus(self, addend: Expression) -> Expression:
            return Sum(self, addend)
    ```

    -   問題なくテストは通る。続いて、テストケースで plus に渡している引数の型を Expression に変更してみる

    ```python
    def test_mixed_addition():
        five_bucks: Expression = Money.dollar(5)
        ten_francs: Expression = Money.franc(10)
        bank = Bank()
        bank.add_rate("CHF", "USD", 2)
        result = bank.reduce(five_bucks.plus(ten_francs), "USD")
        assert result == Money.dollar(10)
    ```

    -   コンパイラ（Python の場合は VSCode の拡張機能）が Expression に plus メソッドが存在しないことを教えてくれる
        -   コンパイラに素直に従い変更していく

    ```python
    class Expression(ABC):
        @abstractmethod
        def reduce(self, bank: Bank, to: str) -> Money:
            raise NotImplementedError()
        @abstractmethod
        def plus(self, addend: Expression) -> Expression:
            raise NotImplementedError()
    ```

    -   今度は Sum に plus メソッドを追加しなければならなくなった。一先ず空実装を追加しておく

    ```python
    class Sum(Expression):
        def plus(self, addend: Expression) -> Expression:
            pass
    ```

<!-- prettier-ignore -->
!!! info
    -   <s>$5 + 10CHF = $10 (レートが 2:1 の場合)</s>
    -   <s>$5 + $5 = $10</s>
    -   <s>$5 + $5がMoneyを返す</s>
    -   <s>Bank.reduce(Money)</s>
    -   <s>Moneyを変換して換算を行う</s>
    -   <s>reduce(Bank, str)</s>
    -   Sum.plus
    -   Expression.times

-   抽象化することで何点か問題が出てきてしまったが、それは次章で解決する
