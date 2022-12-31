#　第 10 章 テストに聞いてみる

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
    -   Dollar と Franc の重複
    -   <s>equals の一般化</s>
    -   **times の一般化**
    -   <s>Franc と Dollar を比較する</s>
    -   <s>通貨の概念</s>
    -  test_franc_multiplicationを削除する？

-   本章で times メソッドを一般化することで、サブクラスを完全に排除する

    ```python
    class Dollar(Money):
        def times(self, multiplier: int) -> Money:
            return Money.dollar(self._amount * multiplier)

    class Franc(Money):
        def times(self, multiplier: int) -> Money:
            return Money.franc(self._amount * multiplier)
    ```

-   それぞれの times メソッドは、前章でそれぞれの FactoryMethod を使用するように変更した

    -   しかし、FactoryMethod を使用する場合は、中々同じメソッドにすることができない
    -   あえて、インライン化に戻す
        -   各オブジェクトにおいて、"USD"と"CHF"はインスタンス変数 currency が常に保証している

    ```python
    class Dollar(Money):
        def times(self, multiplier: int) -> Money:
            return Dollar(self._amount * multiplier, self._currency)

    class Franc(Money):
        def times(self, multiplier: int) -> Money:
            return Franc(self._amount * multiplier, self._currency)
    ```

    -   これでテストが通ることを確認できる
    -   この 2 つのオブジェクトを、Money が返すように変更すると等しいコードになる

        -   この変更は直観的にシステム上誤りである
        -   システム上のどこに問題が発生するかについて、設計から見直す必要はない
        -   一度変更を加えて、テストを通せば、どこに問題が発生するかを、テストが教えてくれる
            -   優秀なソフトウェアエンジニアが 10 分考えて結論を出すことを、テストは 10 秒で教えてくれる！

    -   以下のテストでエラーになる。\_\_eq\_\_にて不具合が発生している事が分かる

        ```python
        def test_franc_multiplication():
            five = Money.franc(5)
        >   assert five.times(2) == Money.franc(10)
        ```

    -   \_\_eq\_\_の現在の実装は以下のようになっている

        ```python
        def __eq__(self, o: object) -> bool:
            if not issubclass(type(o), Money):
                return False
            return o._amount == self._amount and type(self) is type(o)
        ```

    -   本当に調べるべきなのは通貨の等価性であり、型の等価性ではない

        -   テストが通っていないときに新たなテストを追加することは、TDD において基本的に推奨されないが、テストなしでコードを変更することはそれ以上にご法度である
        -   そのため、まずは現在の実装をエラーが出る前の状態に戻して、改めてテストコードを追加する

            ```python
            class Dollar(Money):
                def times(self, multiplier: int) -> Money:
                    return Dollar(self._amount * multiplier, self._currency)

            class Franc(Money):
                def times(self, multiplier: int) -> Money:
                    return Franc(self._amount * multiplier, self._currency)
            ```

        -   これでテストコードが通るようになった。この上で、等価性のテストを追加する

            ```python
            def test_different_class_equality():
                assert Money(10, "CHF") == Franc(10, "CHF")
            ```

        -   当然、テストは失敗するため、\_\_eq\_\_メソッドを、型の比較から currency の比較に変更することでテストが通るようになる

    -   これで、再度 times メソッドが Money を返すようにしてもテストが通ることが確認できる
    -   以上の変更で、2 つのサブクラスの times メソッドの実装は完全に一致したため、親クラスに引き上げることができる

        ```python
        class Money:
            def __init__(self, amount: int, currency: str):
                self._amount = amount
                self._currency = currency

            def times(self, multiplier: int) -> Money:
                return Money(self._amount * multiplier, self._currency)


        class Dollar(Money):
            def __init__(self, amount: int, currency: str):
                super().__init__(amount, currency)


        class Franc(Money):
            def __init__(self, amount: int, currency: str):
                super().__init__(amount, currency)

        ```

    -   ここまでくると、不要なサブクラスを消すことが可能である
