# 第 9 章 歩幅の調整

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
    -   times の一般化
    -   <s>Franc と Dollar を比較する</s>
    -   **通貨の概念**
    -  test_franc_multiplicationを削除する？

-   Franc と Dollar を消すために、本章では通貨の概念について考える
-   まず、どのように通貨をテストするか考える
    -   TDD においては、必ずテストから考える事を意識する
    -   決して実装内容について考えてはいけない！
-   まずは単純に、通貨の概念を文字列で表現することを考える

    ```python
    def test_currency():
        assert "USD" == Money.dollar(1).currency()
        assert "CHF" == Money.franc(1).currency()
    ```

    -   Money クラスに abstruct メソッドを定義し、サブクラスに実装する

    ```python
    class Money:
        @abstractmethod
        def currency(self) -> str:
            raise NotImplementedError()


    class Dollar(Money):
        def currency(self) -> str:
            return "USD"


    class Franc(Money):
        def currency(self) -> str:
            return "CHF"
    ```

    -   続いて、2 つのサブクラスの実装を近づけていって、同じものにする
        -   インスタンス変数に通貨名を格納して、それを返すだけの実装に変更する

    ```python
    class Dollar(Money):
        def __init__(self, amount: int):
            super().__init__(amount)
            self._currency = "USD"

        def currency(self) -> str:
            return self._currency


    class Franc(Money):
        def __init__(self, amount: int):
            super().__init__(amount)
            self._currency = "CHF"

        def currency(self) -> str:
            return self._currency
    ```

    -   これで currency メソッドが同一になったので、インスタンス変数と currency メソッドを親クラスに引き上げる

    ```python
    class Money:
        def __init__(self, amount: int):
            self._amount = amount
            self._currency = ""

        def currency(self) -> str:
            return self._currency
    ```

    -   更に、文字列"USD"や"CHF"を FactoryMethod に移動すれば、2 つのサブクラスは完全に一致し、共通の実装を導くことができる
        -   コンストラクタ呼び出しでエラーが出るので、一先ず None を渡して通す

    ```python
    class Money:
        @classmethod
        def franc(cls, amount: int) -> Money:
            return Franc(amount, None)

    class Franc(Money):
        def __init__(self, amount: int, currency: str):
            super().__init__(amount)
            self._currency = "CHF"

        def times(self, multiplier: int) -> Money:
            return Franc(self._amount * multiplier, None)
    ```

    -   現在の変更とは無関係だが、Franc の times メソッドが FactoryMethod を呼び出していることに気づく
        -   教科書的には「今行っている作業を止めないために、修正を待つべき」となる
        -   しかし、著者は、簡易的な修正割込みなら問題ないとしている
        -   ただし、割込みを更に割り込むことはしないようにしている
    -   今回は、times メソッドの内部処理も修正しておく
    -   最後に、Factory メソッドに currency の知識を組み込み、コンストラクタのパラメータをインスタンス変数に代入するようにすれば、共通化ができる

    ```python
    class Money:
        @classmethod
        def franc(cls, amount: int) -> Money:
            return Franc(amount, "CHF")

    class Franc(Money):
        def __init__(self, amount: int, currency: str):
            super().__init__(amount)
            self._currency = currency

        def times(self, multiplier: int) -> Money:
            return Money.franc(self._amount * multiplier)
    ```

-   本章では、あえて非常に小さい手順に分けて説明をした
    -   実際に作業をする際には、ここまで細かく分けて作業をする必要はない
    -   大切なことは、小さなステップを繰り返し、都度テストを行っていく事も可能である、ということだ
-   同じように Dollar についても変更を行う。今度は一度で全ての変更を行う

    ```python
    class Money:
        @classmethod
        def dollar(cls, amount: int) -> Money:
            return Dollar(amount, "USD")

    class Dollar(Money):
        def __init__(self, amount: int, currency: str):
            super().__init__(amount)
            self._currency = currency

        def times(self, multiplier: int) -> Money:
            return Money.dollar(self._amount * multiplier)
    ```

-   TDD を行う際には、常に今回のような微調整を行う

    -   小さいステップでは窮屈に感じるならば、歩幅を大きくしていく
    -   変更の正しさに不安を感じるならば、歩幅を小さくする

-   最後に、2 つのサブクラスのコンストラクタは完全に一致したので、親クラスに引き上げる

    ```python
    class Money:
        def __init__(self, amount: int, currency: str):
            self._amount = amount
            self._currency = currency

    class Dollar(Money):
        def __init__(self, amount: int, currency: str):
            super().__init__(amount, currency)

    class Franc(Money):
        def __init__(self, amount: int, currency: str):
            super().__init__(amount, currency)
    ```
