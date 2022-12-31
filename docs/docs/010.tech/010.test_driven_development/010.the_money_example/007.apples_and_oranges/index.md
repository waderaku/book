# 第 7 章 疑念をテストに翻訳する

-   第 6 章の最後で、Dollar と Franc を比較したらどうなるかという疑念にかられた
-   頭の中にある疑念をテストに落としてみれば、それに対しての現状が明らかになる

    ```python
    def test_equality():
        assert Dollar(5) == Dollar(5)
        assert Dollar(5) != Dollar(6)
        assert Franc(5) == Franc(5)
        assert Franc(5) != Franc(6)
        assert Dollar(5) != Franc(5)
    ```

    -   等価性比較の最終行に、$5 と 5CHF の比較を追加した。
    -   当然、この 2 つは異なる通貨であり、等しくないはずである
    -   しかし、テストの結果は失敗する

-   現時点で簡単にチェックを行いたいのであれば、2 つのオブジェクトの type を確認すればよい

    ```python
    class Money:
        def __init__(self, amount: int):
            self._amount = amount

        def __eq__(self, o: object) -> bool:
            if not issubclass(type(o), Money):
                return False
            return o._amount == self._amount and type(self) is type(o)
    ```

    -   本来であれば、比較は Python オブジェクトの世界ではなく、財務の世界の言語で行いたい
    -   しかし、現段階では通貨の概念を取り入れることができていないため、一先ず上記のような対処をしておく

-   大切なことは、現状の設計に疑念があるのであれば、それをテストに落とし込み、その疑念を晴らすことである

<!-- prettier-ignore -->
!!! info 
    - $5 + 10CHF = $10 (レートが2:1の場合)
    - <s>$5 * 2 = $10</s>
    - <s>amountをprivateにする</s>
    - <s>Dollarの副作用どうする？</s>
    - Moneyの丸め処理どうする？
    - <s>\__eq__メソッド</s>
    - \__hash__メソッド
    - nullとの等価性比較
    - 他のオブジェクトとの等価性比較
    - <s>5CHF * 2 = 10CHF</s>
    - DollarとFrancの重複
    - <s>equalsの一般化</s>
    - timesの一般化
    - <s>FrancとDollarを比較する</s>
    - 通貨の概念
