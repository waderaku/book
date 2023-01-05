# 第 21 章 数え上げ

<!-- prettier-ignore -->
!!! info 
    - <s>テストメソッドを呼び出す</s>
    - <s>set_upを呼び出す</s>
    - <s>tear_downを後で呼び出す</s>
    - テストメソッドが失敗したとしてもtear_downを呼び出す
    - 複数のテストを走らせる
    - **収集したテスト結果を出力する**
    - <s>WasRunで文字列をログに記録する</s>

-   テスト結果の出力機能を作成する
-   まずはテストを複数走らせたら以下のようなメッセージが出力される機能を作成する
    -   5 run, 2 failed, TestCaseTest.test_foobar -- ZeroDivideException, MoneyTest.test_negation
-   しかし、フレームワークに自動的に全てのテストケース結果を集めて出力させるのは、第一ステップとしては大きすぎる

    -   TestCase クラスの run メソッドがテストの実行結果を記録した TestResult を返すようにしてみる
    -   一先ずは一つのテストの結果だけを出力するようになるが、テストケースを実装する

    ```python
    class TestCaseTest(TestCase):
        def test_template_method(self):
            test = WasRun("test_method")
            test.run()
            assert "set_up test_method tear_down " == test.log

        def test_result(self):
            test = WasRun("test_method")
            result = test.run()
            assert "1 run, 0 failed" == result.summary()

    TestCaseTest("test_template_method").run()
    TestCaseTest("test_result").run()
    ```

    -   run メソッドは現状何も返さないため、ランタイムエラーとなる。仮実装をしてテストを通す

    ```python
    class TestResult:
        def summary(self):
            return "1 run, 0 failed"

    class TestCase:
        def run(self) -> TestResult:
            self.set_up()
            method = getattr(self, self.name)
            method()
            self.tear_down()
            return TestResult()
    ```

    -   これでテストが通るので、summary メソッドの実装を行える

        -   TestResult 内で実行回数をカウントし、それを出力するように変更する
            -   run メソッド内で TestResult インスタンスを生成し、test_started を呼び出すことでインクリメントさせる

        ```python
        class TestResult:
            def __init__(self):
                self.run_count = 0

            def test_started(self):
                self.run_count += 1

            def summary(self):
                return f"{self.run_count} run, 0 failed"

        class TestCase:
            def run(self) -> TestResult:
                result = TestResult()
                result.test_started()
                self.set_up()
                method = getattr(self, self.name)
                method()
                self.tear_down()
                return result
        ```

    -   テストは正常に通る。次に失敗の数を示す 0 のべた書きを削除したい

        -   三角測量の要領で、もう一つテストを記載する

        ```python
        class TestCaseTest(TestCase):
            def test_failed_result(self):
                test = WasRun("test_broken_method")
                result = test.run()
                assert "1 run, 1 failed" == result.summary()

        TestCaseTest("test_failed_result").run()

        class WasRun(TestCase):
            def test_broken_method(self):
                raise Exception
        ```

        -   しかしこれを動かすと、投げられた例外をキャッチする場所がないため、テストはそこで失敗する
        -   テストが通るように例外をキャッチするようにしたいが、一つのテストで行う変更範囲が大きくなりすぎている
            -   一度現在作成したテストをコメントアウトして、範囲の狭めたテストを次章で行う
