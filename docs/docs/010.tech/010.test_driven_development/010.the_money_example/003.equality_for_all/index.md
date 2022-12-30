# 第 3 章 三角測量

-   Dollar オブジェクトは Value Object である
    -   ある整数に 1 を足すとき、一般的に元の整数が変更されるとは考えず、新しい値が得られると考える
    -   一方で、保険契約オブジェクトがあり、そこに契約条項を 1 つ追加する場合、元の保険契約オブジェクトが変更されると考えるだろう
    -   Dollar オブジェクトのように、オブジェクトとして定義をしつつも、値として扱いたいオブジェクトには、Value Object パターンが適用される
-   Value Object を使う大きなメリットは、別名参照を気にする必要がなくなることである
    -   例えば、2 つの小切手オブジェクトがそれぞれ同じ Dollar オブジェクトを持っており、片方のオブジェクトが自身の Dollar オブジェクトに操作を加えた際、もう片方のオブジェクトにも影響を及ぼしてしまう危険がある
    -   Value Object を使用すると、一度発行されたオブジェクトに対して操作が行われた場合、新たな Value Object を発行するため、上記のような問題を避けることができる
-   オブジェクトが Value Object であるためには、操作は全て新しいオブジェクトを返さなければならなく、\_\_eq\_\_メソッド(原文では equals メソッドと記載されているが、Python では\_\_eq\_\_メソッドの実装となる)を提供しなければならない
-   また、Dollar オブジェクトをハッシュテーブルのキーとして扱うなら、\_\_hash\_\_メソッドも実装しなければならない

<!-- prettier-ignore -->
!!! info 
    - $5 + 10CHF = $10 (レートが2:1の場合)
    - <s>$5 * 2 = $10</s>
    - amountをprivateにする
    - <s>Dollarの副作用どうする？</s>
    - Moneyの丸め処理どうする？
    - **\__eq__メソッド**
    - \__hash__メソッド

-   等価性のテスト方法を考える

    -   まず、5 ドルは他の 5 ドルと等価でなければならない
    -   しかし、上記だけのテストコードでは、必ず True を返却するコードが、重複性のなく、そして一般化されていないコードが成立してしまう
    -   そこで、三角測量[^1]の概念を真似て、コードを一般化するために、2 つ以上の実例を用いることが効果的である
    -   ここでは、「$5 != $6」のテストを追加する

    ```python
    def test_equality():
        assert Dollar(5) == Dollar(5)
        assert Dollar(5) != Dollar(6)

    class Dollar:
        def __init__(self, amount: int):
            self.amount = amount

        def times(self, multiplier: int) -> Dollar:
            return Dollar(self.amount * multiplier)

        def __eq__(self, o: object) -> bool:
            if type(o) is not Dollar:
                return False
            return o.amount == self.amount
    ```

-   times メソッドにおいても、「$5 \* 2 = $10」と、「$5 \* 3 = $15」の 2 種類のテストを実行することによって、三角測量を利用した一般化を図っている
-   筆者は、基本的には重複を除去するプロセスを進めている
    -   最終的に設計のアイデアが浮かばない場合、三角測量によるテストコードを実装する
    -   これによって、異なった角度からの視点をテストに取り入れることができる

<!-- prettier-ignore -->
!!! info 
    - $5 + 10CHF = $10 (レートが2:1の場合)
    - <s>$5 * 2 = $10</s>
    - amountをprivateにする
    - <s>Dollarの副作用どうする？</s>
    - Moneyの丸め処理どうする？
    - <s>\__eq__メソッド</s>
    - \__hash__メソッド
    - nullとの等価性比較
    - 他のオブジェクトとの等価性比較

-   この変更によって、等価性を比較できるようになった
    -   ただ、null との比較や、他のクラスのオブジェクトの比較は考慮されていない
    -   こうした比較も今後必要になる可能性があるため、TODO リストに追加しておく

[^1]: 2 つの地点とその距離が分かっている時、その他の任意の地点について、2 地点からの角度さえ分かれば、その場所を特定できる性質。ここでは、複数のテストを用意することで、任意のテストを表現するのに十分な情報を満たすことを示している