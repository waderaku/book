# 第 16 章 将来の読み手を考えたテスト

<!-- prettier-ignore -->
!!! info
    -   <s>$5 + 10CHF = $10 (レートが 2:1 の場合)</s>
    -   <s>$5 + $5 = $10</s>
    -   <s>$5 + $5がMoneyを返す</s>
    -   <s>Bank.reduce(Money)</s>
    -   <s>Moneyを変換して換算を行う</s>
    -   <s>reduce(Bank, str)</s>
    -   **Sum.plus**
    -   Expression.times

-   前章で空実装だけを行った Sum の plus メソッドをきちんと実装していく

    -   まずはテストコードを実装する

    ```python
    def test_sum_plus_money():
        five_bucks: Expression = Money.dollar(5)
        ten_francs: Expression = Money.franc(10)
        bank = Bank()
        bank.add_rate("CHF", "USD", 2)
        _sum = Sum(five_bucks, ten_francs).plus(five_bucks)
        result = bank.reduce(_sum, "USD")
        assert result == Money.dollar(15)
    ```

    -   five_bucks.plus(ten_francs)と書くことで間接的に Sum を作成することもできるが、意図を明確にするために Sum をインスタンスから作成している
        -   テストコードが仕様となり、現在考えていることを将来の開発者に伝える役割を兼ねられる
    -   Sum の plus メソッドは Null を返しているため、テストは通らない

        -   自身と addend を組み合わせた Sum クラスを返すように変更して、テストを通す

        ```python
        class Sum(Expression):
            def plus(self, addend: Expression) -> Expression:
                return Sum(self, addend)
        ```

-   TDD を行うと、必ず各機能に対してテストコードを書くことになるため、テストコードとプロタクトコードの行数が同じ程度になる事が多い

    -   つまり、これまでの 2 倍の生産性で実装するか、半分のコードで同じ機能を実現できなければ、TDD のメリットを受けることができない
    -   ただし、実装だけでなく、デバッグやインテグレーション、他の開発者への説明にかかる時間も考慮するべきである

<!-- prettier-ignore -->
!!! info
    -   <s>$5 + 10CHF = $10 (レートが 2:1 の場合)</s>
    -   <s>$5 + $5 = $10</s>
    -   <s>Bank.reduce(Money)</s>
    -   <s>Moneyを変換して換算を行う</s>
    -   <s>reduce(Bank, str)</s>
    -   <s>Sum.plus</s>
    -   **Expression.times**

-   続いて、Expression に times メソッドを宣言する

    ```python
    def test_sum_times():
        five_bucks: Expression = Money.dollar(5)
        ten_francs: Expression = Money.franc(10)
        bank = Bank()
        bank.add_rate("CHF", "USD", 2)
        _sum = Sum(five_bucks, ten_francs).times(2)
        result = bank.reduce(_sum, "USD")
        assert result == Money.dollar(20)
    ```

    -   テストが通るように、Expression インターフェース及び Sum クラスに times メソッドを実装する

    ```python
    class Expression(ABC):
        @abstractmethod
        def times(self, multiplier: int) -> Expression:
            raise NotImplementedError()

    class Sum(Expression):
        def times(self, multiplier: int) -> Expression:
            return Sum(self.augend.times(multiplier), self.addend.times(multiplier))
    ```

-   これにて、一通りのタスクが完了した
