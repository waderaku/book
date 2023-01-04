# 第 18 章 xUnit へ向かう小さな一歩

-   まず、テストケースを作り、テストメソッドを実行できるようにしたい
    -   例えば、TestCase("TestMethod").run()のように動くようにしたい
    -   しかし、テストのフレームワークを作る瞬間には、テストのフレームワークはない
    -   つまり、テストケースを書くために使うフレームワークの為のテストケースを書く必要がある
    -   最初の小さな一歩は手作業で進めるしかない
    -   そこで、きわめて小さなステップを刻みながら、細かく確認をしながら進める必要がある
-   TODO リストは以下になる

<!-- prettier-ignore -->
!!! info 
    - **テストメソッドを呼び出す**
    - setUpを呼び出す
    - tearDownを後で呼び出す
    - テストメソッドが失敗したとしてもtearDownを呼び出す
    - 複数のテストを走らせる
    - 収集したテスト結果を出力する

-   TDD に従って実装を行っていく
-   まずはテストメソッドが呼ばれたら true を出力し、呼ばれなかったら false を出力する小さなプログラムを実装する

    -   呼ばれたかどうかのフラグをテストメソッドの中で設定すれば、実行後にフラグの値を出力し、その値が正しいかどうかを確かめられる
    -   最初のステップとして、テスト対象クラスとして WasRun クラス、フラグに was_run を用意し、メソッドを走らせてみる

        ```python
        test = WasRun("test_method")
        print(test.was_run)
        test.testMethod()
        print(test.was_run)
        ```

        -   ランタイムエラーが発生しないように、最低限の修正を行う

        ```python
        class WasRun:
            def __init__(self, name: str):
                self.was_run = None

            def test_method(self):
                self.was_run = 1
        ```

        -   テストメソッドが実行される前には None が出力され、実行後には 1 が出力されることを期待したが、実際には None が 2 度出力される
        -   想定通りに出力されるように変更を加える

        ```python
        class WasRun:
            def test_method(self):
                self.was_run = 1
        ```

    -   次のステップとして、インターフェースを修正する

        -   テストメソッドを直接呼ぶのではなく、run メソッドを呼び出せば間接的に呼び出すように変更する

        ```python
        class WasRun:
            def run(self):
                self.test_method()

        test = WasRun("test_method")
        print(test.was_run)
        test.run()
        print(test.was_run)
        ```

        -   都度 Python ファイルを実行し、結果が想定通りであることを確認する

    -   次は test_method の動的な呼び出しに取り組む

        -   Python ではクラス名やメソッド名を関数のように扱える
            -   テストケース名を示す属性を問い合わせ、返ってきたオブジェクトを関数のように呼び出せば、メソッドを呼び出すことができる

        ```python
        class WasRun:
            def __init__(self, name: str):
                self.was_run = None
                self.name = name

            def run(self):
                method = getattr(self, self.name)
                method()
        ```

    -   ここでもう 1 つのリファクタリングのパターンが出てきた
        -   まずとある状況で動くコードを書き、その後他の様々な場合にも動くようにべた書きの値を変数に変えながら一般化していく
        -   TDD には、一般化対象の動作を実際に確かめながら進めるため、頭の中だけで悩まずに済む強みがある
    -   WasRun クラスの責務が以下の 2 つになってしまっている
        -   メソッドが起動されたかどうかを記録する仕事
        -   テストメソッドを動的に呼び出す仕事
    -   後者の機能である run メソッドに関わる部分をを親クラス TestCase に移行する

    ```python
    class TestCase:
        def __init__(self, name: str):
            self.name = name

        def run(self):
            method = getattr(self, self.name)
            method()


    class WasRun(TestCase):
        def __init__(self, name: str):
            self.was_run = None
            super().__init__(name)
    ```

    -   ここまでのステップで、都度 Python ファイルを実行し、None と 1 が出力されることを確認し続けてきた

        -   本章で作成した機能を利用して、以下のように変更することで、以降は問題があった場合のみスタックトレースが出るようになる

        ```python
        class TestCaseTest(TestCase):
            def test_runnning(self):
                test = WasRun("test_method")
                assert not test.was_run
                test.run()
                assert test.was_run


        TestCaseTest("test_runnning").run()
        ```

-   本章では、非常に小さなステップで進めてきた

    -   しかし、著者は当初、もっと大きな手順を試した際に 6 時間もかかった
    -   最初の小さなステップを飛ばしたばかりに結果的に高くついてしまったのだ
    -   TDD を習得したら、より大きな機能追加をテストを書きながら行えるようになる
        -   しかし TDD をマスターするためには、いつでも必要にお応じて小さなステップに戻せるようにならなければならない

-   次章では、テスト前に setUp メソッドを呼ぶ機能に取り組んでいく
