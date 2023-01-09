# 第 2 章 明白な実装

-   TDD においての最終ゴールは、動作する綺麗なコードである
    -   そのために、まずは「動作する」に取り組み、その後で「綺麗な」に取り組む
    -   これは、アーキテクチャ駆動とは正反対である
    -   アーキテクチャ駆動では、「綺麗な」に最初に取り組み、そのうえで苦心して設計の辻褄を合わせながらどうにか「動作する」を実現する

<!-- prettier-ignore -->
!!! info 
    - $5 + 10CHF = $10 (レートが2:1の場合)
    - <s>$5 * 2 = $10</s>
    - amountをprivateにする
    - **Dollarの副作用どうする？**
    - Moneyの丸め処理どうする？

-   現状、Dollar オブジェクトを操作すると、Dollar オブジェクトの状態が変化してしまっている
-   以下のようなテストコードが通ることを目的とする

    ```python
    def test_multiplication():
        five = Dollar(5)
        prouct = five.times(2)
        assert prouct.amount == 10
        product = five.times(3)
        assert product.amount == 15
    ```

-   まずはテストコードのコンパイルが通るように修正を加える

    ```python
    class Dollar:
        def __init__(self, amount: int):
            self.amount = amount

        def times(self, multiplier: int) -> Dollar:
            self.amount *= multiplier
            return self
    ```

-   この段階ではコンパイルは通るが、テストは失敗する
-   テストの値が通るように、新たな Dollar オブジェクトを返却するように以下のように変更を加える

    ```python
    class Dollar:
        def __init__(self, amount: int):
            self.amount = amount

        def times(self, multiplier: int) -> Dollar:
            return Dollar(self.amount * multiplier)
    ```

-   TDD には 3 つの実装方法がある。以下に、そのうちの 2 つを記す

    -   仮実装（第 1 章）: まずべた書きの値を使い、徐々に変数に置き換えていく
    -   明白な実装（第 2 章）: すぐに頭の中の実装をコードに落とす
        -   本章では、第 1 章と比較して大きなステップで実装をした（べた書きでテストを通さなかった）

-   筆者は普段 TDD を行うときには、上記 2 つの実装モードを揺れ動く
    -   実装方法が明らかな場合は、明白な実装を行う
    -   その間、テストを動かし続け、自身が明白だと思っていることをマシンも明白だと示してくれるのを確かめ続けている
    -   予期しないエラーが発生したら、すぐに仮実装にシフトし、リファクタリングによって正しい実装に近づけていく
-   尚、TDD の 3 つ目の戦略である三角測量は、次章で解説する
-   副作用への不快感など、感情をテストに翻訳することは、TDD において大きなテーマである
    -   システムがどう振る舞うべきかを考えるプロセスを繰り返していくことで、より洗練されていく
