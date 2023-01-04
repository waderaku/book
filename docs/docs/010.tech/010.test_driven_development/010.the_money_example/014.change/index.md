# 第 14 章 学習用テストと回帰テスト

<!-- prettier-ignore -->
!!! info
    -   $5 + 10CHF = $10 (レートが 2:1 の場合)
    -   <s>$5 + $5 = $10</s>
    -   <s>$5 + $5がMoneyを返す</s>
    -   <s>Bank.reduce(Money)</s>
    -   **Moneyを変換して換算を行う**
    -   reduce(Bank, str)

-   本章では、通貨の変換機能の実装をしていく
-   まずは、2 フランを 1 ドルに換算出来るようなテストコードを記載する

    ```python
    def test_reduce_money_different_currency():
        bank = Bank()
        bank.add_rate("CHF", "USD", 2)
        result = bank.reduce(Money.franc(2), "USD")
        assert Money.dollar(1) == result
    ```

    -   テストを通すため、add_rate のインターフェースを用意し、Money の reduce に仮実装をする

    ```python
    class Money(Expression):
        def reduce(self, to: str) -> Money:
            rate = 2 if self._currency == "CHF" and to == "USD" else 1
            return Money(self._amount / rate, to)

    class Bank:
        def add_rate(self, _from: str, to: str, rate: int):
            pass
    ```

-   これでテストは通るが、Money が為替レートを知っていることになってしまっている
    -   この責務は Bank が担うはずである
-   Expression とそのサブクラス の reduce メソッドに Bank インスタンスを渡すように変更し、レート換算は Bank で行うように変更する

    ```python
    class Expression(ABC):
        @abstractmethod
        def reduce(self, bank: Bank, to: str) -> Money:
            raise NotImplementedError()

    class Money(Expression):
        def reduce(self, bank: Bank, to: str) -> Money:
            rate = bank.rate(self._currency, to)
            return Money(self._amount / rate, to)

    class Bank:
        def rate(self, _from: str, to: str) -> int:
            return 2 if _from == "CHF" and to == "USD" else 1
    ```

-   責務の移管は出来たが、レート値がコード上にべた書きされている

    -   Bank の中でハッシュテーブルを使用し、検索可能な構造にする
    -   ハッシュテーブルは 2 つの通貨名が入ったリストをキーに使いたい

        -   これがハッシュキーに使用出来るかを確認する
        -   外部ライブラリ（今回は Python 組み込みのリスト）等の機能を確認する際も、**限定的な仕様であるならばテストを書いてしまえば効率的である**

        ```python
        def test_array_equals():
            _dict = {["abc"]: 1}
            assert _dict[["abc"]] == 1
        ```

        -   テストは通らない。エラーメッセージから、Python の list は hash 化する機能がないことが分かる

            -   通貨名を管理する Pair クラスを作成する（上記のテストコードはもう不要なため削除する）

            ```python
            class Pair:
                def __init__(self, _from: str, to: str):
                    self._from = _from
                    self._to = to

                def __eq__(self, __o: object) -> bool:
                    if not isinstance(__o, Pair):
                        return False
                    return __o._from == self._from and __o._to == self._to

                def __hash__(self) -> int:
                    return 0
            ```

            -   hash 値が必ず 0 を返すのは非常に良くないが、そこは後ほどまたテストを書くことにする

        -   これでハッシュ管理ができるようになっているので、為替レートを Bank で管理するように変更を加える

        ```python
        class Bank:
            def __init__(self):
                self._rates = {}

            def add_rate(self, _from: str, to: str, rate: int):
                pair = Pair(_from, to)
                self._rates[pair] = rate

            def rate(self, _from: str, to: str) -> int:
                return self._rates[Pair(_from, to)]
        ```

        -   この変更で為替レートの管理が出来るようになったと思ったが、テストでエラーが発生した
            -   エラーの箇所は USD から USD への為替レートの変換で起こっている
            -   **予想できていなかったバグであるため、改めて状況を再現する回帰テストを用意する**
            ```python
            def test_identity_rate():
                assert 1 == Bank().rate("USD", "USD")
            ```
            -   予想通りエラーになるが、簡単に修正可能である
            ```python
            class Bank:
                def rate(self, _from: str, to: str) -> int:
                    if _from == to:
                        return 1
                    return self._rates[Pair(_from, to)]
            ```
            -   これで全てのテストが通る

    -   本章では、仕様確認のテスト（学習用テスト）と、リファクタリング時のミスを再現するテスト（回帰テスト）を紹介した
        -   これらを使用することで、より着実にコードを変更していくことができる
