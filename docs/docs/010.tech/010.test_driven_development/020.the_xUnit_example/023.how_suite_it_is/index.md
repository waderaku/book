# 第 23 章 スイートにまとめる

<!-- prettier-ignore -->
!!! info 
    - <s>テストメソッドを呼び出す</s>
    - <s>set_upを呼び出す</s>
    - <s>tear_downを後で呼び出す</s>
    - テストメソッドが失敗したとしてもtear_downを呼び出す
    - **複数のテストを走らせる**
    - <s>収集したテスト結果を出力する</s>
    - <s>WasRunで文字列をログに記録する</s>
    - <s>失敗したテストを出力する</s>
    - set_upのエラーをキャッチして出力する

-   最後に、TestSuite に触れていく
    -   現状は全てのテストがファイルの最後に並んでいる汚いコードである
        -   テストを実行するメソッド以外のコードが重複していることが分かる
    -   重複は常に悪だが、設計に気づきを与えてくれる
        -   仮に一度に一つしかテストが実行されないならば、現状のテストでも問題は発生しなかった
-   TestSuite オブジェクトを作成して、複数のテストをまとめて実行するテストを記載する

    ```python
    class TestCaseTest(TestCase):
        def test_suite(self):
            suite = TestSuite()
            suite.add(WasRun("testMethod"))
            suite.add(WasRun("testBrokenMethod"))
            result = suite.run()
            assert "2 run, 1 failed" == result.summary()

    print(TestCaseTest("test_suite").run().summary())
    ```

    -   テストが通るように、TestSuite クラスを作成する
        -   空のリストをコンストラクタで作成し、add メソッドで受け取った test を追加していく単純な実装とする
        -   ただし、run メソッドでは同じ TestResult インスタンスにテスト回数をカウントしていけるようにする

    ```python
    class TestSuite:
        def __init__(self):
            self.tests: list[TestCase] = []

        def add(self, test: TestCase):
            self.tests.append(test)

        def run(self) -> TestResult:
            result = TestResult()
            for test in self.tests:
                test.run(result)
            return result
    ```

    -   しかし、TestCase は現状 result を受け取るようになっていないためテストは失敗する
        -   run メソッドは TestResult インスタンスを受け取るように変更を加える
        -   単一のテストであろうと、複数のテストであろうと、インターフェースをそろえるために、TestSuite の run メソッドも引数を受け取るようにする

    ```python
    class TestCaseTest(TestCase):
        def test_suite(self):
            suite = TestSuite()
            suite.add(WasRun("test_method"))
            suite.add(WasRun("test_broken_method"))
            result = TestResult()
            suite.run(result)
            assert "2 run, 1 failed" == result.summary()

    class TestSuite:
        def run(self, result: TestResult):
            for test in self.tests:
                test.run(result)

    class TestCase:
        def run(self, result: TestResult):
            result.test_started()
            self.set_up()
            try:
                method = getattr(self, self.name)
                method()
            except Exception:
                result.test_failed()
            self.tear_down()
    ```

    -   この変更によって、まとめたテストが実施できるようになった
        -   最終行にあるテスト実行コードも、TestSuite を使用するように変更する

    ```python
    suite = TestSuite()
    suite.add(TestCaseTest("test_template_method"))
    suite.add(TestCaseTest("test_result"))
    suite.add(TestCaseTest("test_failed_result"))
    suite.add(TestCaseTest("test_failed_result_formatting"))
    suite.add(TestCaseTest("test_suite"))
    result = TestResult()
    suite.run(result)
    print(result.summary())
    ```

    -   3 つのテストで失敗する。これは、引数なしの run メソッドを使用しているテストがあるからである

    ```python
    class TestCaseTest(TestCase):
        def test_template_method(self):
            test = WasRun("test_method")
            result = TestResult()
            test.run(result)
            assert "set_up test_method tear_down " == test.log

        def test_result(self):
            test = WasRun("test_method")
            result = TestResult()
            test.run(result)
            assert "1 run, 0 failed" == result.summary()

        def test_failed_result(self):
            test = WasRun("test_broken_method")
            result = TestResult()
            test.run(result)
            assert "1 run, 1 failed" == result.summary()
    ```

    -   以上にて、全てのテストが通る(「5 run, 0 failed」と出力される)
    -   重複排除として、各々のテストメソッドで TestResult を生成している処理を set_up に寄せる

    ```python
    class TestCaseTest(TestCase):
        def set_up(self):
            self.result = TestResult()

        def test_template_method(self):
            test = WasRun("test_method")
            test.run(self.result)
            assert "set_up test_method tear_down " == test.log

        def test_result(self):
            test = WasRun("test_method")
            test.run(self.result)
            assert "1 run, 0 failed" == self.result.summary()

        def test_failed_result(self):
            test = WasRun("test_broken_method")
            test.run(self.result)
            assert "1 run, 1 failed" == self.result.summary()

        def test_failed_result_formatting(self):
            self.result.test_started()
            self.result.test_failed()
            assert "1 run, 1 failed" == self.result.summary()

        def test_suite(self):
            suite = TestSuite()
            suite.add(WasRun("test_method"))
            suite.add(WasRun("test_broken_method"))
            suite.run(self.result)
            assert "2 run, 1 failed" == self.result.summary()
    ```

-   第 Ⅱ 部の実装としては、以上とする。TODO がいくつか残っているが、そこは読者への宿題とする

<!-- prettier-ignore -->
!!! info 
    - <s>テストメソッドを呼び出す</s>
    - <s>set_upを呼び出す</s>
    - <s>tear_downを後で呼び出す</s>
    - テストメソッドが失敗したとしてもtear_downを呼び出す
    - <s>複数のテストを走らせる</s>
    - <s>収集したテスト結果を出力する</s>
    - <s>WasRunで文字列をログに記録する</s>
    - <s>失敗したテストを出力する</s>
    - set_upのエラーをキャッチして出力する
    - TestCaseクラスからTestSuiteを作る
