# 第 11 章 不要になったら消す

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
    -   <s>times の一般化</s>
    -   <s>Franc と Dollar を比較する</s>
    -   <s>通貨の概念</s>
    -  test_franc_multiplicationを削除する？

-   2 つのサブクラスを消すことを考える

    -   すでにこのサブクラスは、何の役割も持っていないため、参照先をすべて Money に置き換えても、コードの意味は変わらない

        ```python
        class Money:
            @classmethod
            def dollar(cls, amount: int) -> Money:
                return Money(amount, "USD")

            @classmethod
            def franc(cls, amount: int) -> Money:
                return Money(amount, "CHF")
        ```

    -   この変更によって、各サブクラスを参照する処理はすべてなくなったが、前章で追加した等価性のテストコード(test_different_class_equality)に Franc の参照が残っている

        -   等価性のテストは、他のテスト(test_equality)で十分満たされている

            -   むしろ test_equality にあるテスト自体も、Dollar と Franc それぞれに\_\_eq\_\_メソッドが実装されていた名残りがあるため、そこも削減することが可能である

                ```python
                def test_equality():
                    assert Money.dollar(5) == Money.dollar(5)
                    assert Money.dollar(5) != Money.dollar(6)
                    assert Money.dollar(5) != Money.franc(5)
                ```

    -   以上で、2 つのサブクラスを完全に排除することを実現した
    -   また、Franc と Dollar それぞれの掛け算のテストがあるが、こちらも Money に移管したことによって同一のテストになっているため、片方(test_franc_multiplication)を削除する

-   TDD に沿って変更を行っていくと、しばしば不要なテストコードが生まれる
    -   コードの変更に併せて、不要なテストコードも都度削除していく
