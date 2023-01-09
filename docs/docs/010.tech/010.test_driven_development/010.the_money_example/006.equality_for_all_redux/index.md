# 第 6 章 テスト不足に気づいたら

-   第 5 章では準備に長い時間をかけるのを避けて、新しいテストが通るところまですぐに持ってきたが、その代償に多くの罪を犯した
    -   Dollar クラスと Franc クラスには沢山の重複が発生した
-   本章ではこの愚かなコードをリファクタリングしていく
-   各クラスの重複を排除するために、2 つのクラスの共通の親クラス(Money)を作成する

    -   例によって小さなステップを繰り返していく
    -   第一ステップとして、空の Money クラスを作成する
    -   テストは引き続き通る事を確認する（テストコードには一切影響していないため当然ではあるが）
        -   このような破壊的なリファクタリングは、テストを頻繁に動かして都度確認することが推奨される
    -   次に、Dollar が Money を継承するようにする
    -   そして、amount フィールドを Money クラスに移動し、\_\_eq\_\_ メソッドを Money クラスに実装する(issubclass による確認に変更)

    ```python
    class Money:
        def __init__(self, amount: int):
            self._amount = amount

        def __eq__(self, o: object) -> bool:
            if not issubclass(type(o), Money):
                return False
            return o._amount == self._amount


    class Dollar(Money):
        def __init__(self, amount: int):
            super().__init__(amount)

        def times(self, multiplier: int) -> Dollar:
            return Dollar(self._amount * multiplier)
    ```

-   これによって、Dollar クラスの\_\_eq\_\_ メソッドを消すことができた。同様にして、Franc クラスの\_\_eq\_\_メソッドを排除する

    -   しかし、現時点で Franc クラスの等価性比較を保証するテストが存在しない

        -   テストによって守られていないコードをリファクタリングすると、テストは通るのにバグを潜めてしまう危険性がある
            -   そういった場合には、あるべきテストを追加していく事が推奨される

        ```python
        def test_equality():
            assert Dollar(5) == Dollar(5)
            assert Dollar(5) != Dollar(6)
            assert Franc(5) == Franc(5)
            assert Franc(5) != Franc(6)
        ```

    -   テストコードに重複が生まれてしまったが、一先ず Franc の機能を保証することができた
    -   これで、Dollar と同様にして、Money クラスの継承、amount フィールドの移行、\_\_eq\_\_ メソッドの排除ができる

    ```python
    class Franc(Money):
        def __init__(self, amount: int):
            super().__init__(amount)

        def times(self, multiplier: int) -> Franc:
            return Franc(self._amount * multiplier)
    ```

-   重複を統一したことによって Franc と Dollar の比較について考慮しなければならなくなったため、第 7 章にて解決する

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
    - **FrancとDollarを比較する**
