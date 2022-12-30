# 第 4 章 意図を語るテスト

-   前章で等価性が定義出来たので、テストがより「雄弁」になった
-   しかし、ここまでのテストでは、Dollar のメソッドが新たな Dollar を返すことが伝わりにくい

    ```python
    def test_multiplication():
        five = Dollar(5)
        prouct = five.times(2)
        assert prouct.amount == 10
        product = five.times(3)
        assert product.amount == 15
    ```

    -   そこで、アサーションを修正して、Dollar 同士を直接比較する
    -   更に、一時変数 product も不要になったため、インライン化する

    ```python
    def test_multiplication():
        five = Dollar(5)
        assert five.times(2) == Dollar(10)
        assert five.times(3) == Dollar(15)
    ```

-   上記変更によって、明確に意図を語るようになった。そして、操作の連なりではなく、まるで真実の証明であるかのように読める
-   また、これによって、amount フィールドを直接使用するのは Dollar クラスのみになったため、フィールドを隠ぺいすることができる

    ```python
    class Dollar:
    def __init__(self, amount: int):
        # Pythonにおいてprivate変数は先頭にアンダースコア2つ付ける事で表現されるが、
        # 慣例としてアンダースコア1つ付けてprivate変数であることを宣言することが多いため、こちらを採用する
        self._amount = amount

    def times(self, multiplier: int) -> Dollar:
        return Dollar(self._amount * multiplier)

    def __eq__(self, o: object) -> bool:
        if type(o) is not Dollar:
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

-   これで TODO リストの項目がまた 1 つ「済」になった
-   ただし、この変更によって、あるリスクを受け入れたことを理解しなければならない
    -   掛け算のテストには、等価性比較の機能を利用している
    -   そのため、もしも等価性比較のテストが正常に検証出来ていなかったら、掛け算のテストも正常に検証出来ていないということになる
    -   注意しなければならないのは、TDD は完璧を求めているのではない
        -   全てのものをコードとテスト両方の視点から捉えることによって欠陥を減らし、自信を持って進めるようになることを求めている
-   仮に自分の思惑がはずれ、上記のようなリスクが顕在化してしまった時には、どのようなテストが正しかったのかを都度考え、それを教訓とする
