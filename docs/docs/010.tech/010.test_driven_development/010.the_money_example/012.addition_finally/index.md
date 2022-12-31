# 第 12 章 設計とメタファー

<!-- prettier-ignore -->
!!! info
    -   $5 + 10CHF = $10 (レートが 2:1 の場合)
    -   **$5 + $5 = $10**

-   前章までで、掛け算の機能が一通り完成した
    -   細かな TODO がまだ残っていたが、本書では扱わないため、一度整理をする
-   足し算について考えていくが、一先ず通貨の違いを意識しない単純な足し算を扱う

    -   これまで通り、まずはテストコードを実装する

        -   当然 plus メソッドは存在しないため、エラーとなるので、Money に plus メソッドを追加する
        -   この処理は明確であるため、一気に重複を排除したメソッドを追加する

        ```python
        def test_simple_addition():
            _sum = Money.dollar(5).plus(Money.dollar(5))
            assert _sum == Money.dollar(10)

        class Money:
            def plus(self, addend: Money) -> Money:
                return Money(self._amount + addend._amount, self._currency)
        ```

-   続いて、異なる通貨間の足し算について考える

    -   当然、複数の通貨を扱っていることほとんど意識しないようなコードにしたい
        -   通貨間の為替レートを簡単に扱えて、かつ計算は計算のように見える方法
    -   そこで今回は、Imposter パターンを使用する
        -   美しい実装パターンを思いつくのに、体系だった方法はない
        -   その為、何故この方法がひらめくかについては言語化が難しい
        -   一方で、TDD のプロセスに沿い、テストによって手入れされたコードは、ひらめきへの備えとなる
            -   ひらめいた設計をコードに落とすのが容易になる
    -   「式(Expression)」というメタファーを使用する

        -   Money は式の最小構成要素であり、様々な操作(sum など)の結果は Expession オブジェクトになる
        -   式のメタファーを使用して、テストを書きなおしていく
            -   一方で、為替レートの管理、換算は Expressioin の責務ではない
                -   現実世界でこの責務を担うのは銀行である
            -   その為、為替管理を行う bank オブジェクトを用意し、そこで通貨間のやり取りをさせる
            ```python
            def test_simple_addition():
                _sum: Expression = Money.dollar(5).plus(Money.dollar(5))
                bank = Bank()
                reduced = bank.reduce(_sum, "USD")
                assert reduced == Money.dollar(10)
            ```
        -   上のテストに従って、まずはランタイムエラーを消す

            ```python
            class Expression:
                pass

            class Bank:
                def reduce(self, source: Expression, to: str) -> Money:
                    return None

            class Money(Expression):
                def plus(self, addend: Money) -> Expression:
                    return Money(self._amount + addend._amount, self._currency)
            ```

        -   これでランタイムエラーは消せるが、当然テストは通らない

            -   Bank の reduce メソッドを正式なものに修正する必要があるが、ここは複雑な機能を実現する必要がある
            -   そのため、本章では仮実装をしておく

            ```python
            class Bank:
                def reduce(self, source: Expression, to: str) -> Money:
                    return Money.dollar(10)
            ```
