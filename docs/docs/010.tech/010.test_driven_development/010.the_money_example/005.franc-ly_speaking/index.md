# 第 5 章 原則をあえて破るとき

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
    - **5CHF * 2 = 10CHF**

-   Dollar オブジェクトに閉じた計算については、前章までである程度完成した
-   そこで、次は Dollar と同じ機能をフラン(franc)で表現することを考える

    -   Dollar のテストコードをコピーして、Franc のテストを実装する

    ```python
    def test_franc_multiplication():
        five = Franc(5)
        assert five.times(2) == Franc(10)
        assert five.times(3) == Franc(15)
    ```

    -   テストを成功させるための小さなステップとしては、Dollar クラスを丸ごとコピーして、愚直に Dollar を Franc に書き換えることが考えられる
        -   これは綺麗なコードを殺すことに等しいが、TDD において綺麗なコードの作成はテストを通した後のフェーズである
        -   各フェーズにはそれぞれで目的と解決策があり、価値観も異なっている
        -   テストを通すまでは、どのような罪を犯しても良い。設計よりも速度が重要である
        -   最後のフェーズ「重複を除去する」タイミングで正しい設計に修正する
        -   TDD は「動かしてから、正しくする」
    -   最終的に完成した Franc クラスを以下に記載する

    ```python
    class Franc:
        def __init__(self, amount: int):
            self._amount = amount

        def times(self, multiplier: int) -> Franc:
            return Franc(self._amount * multiplier)

        def __eq__(self, o: object) -> bool:
            if type(o) is not Franc:
                return False
            return o._amount == self._amount
    ```

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
    - equalsの一般化
    - timesの一般化

-   愚かな実装をした為、新たに発生した重複を削除しなければならない
-   次章にて、Dollar、Franc クラスの一般化を行っていく
