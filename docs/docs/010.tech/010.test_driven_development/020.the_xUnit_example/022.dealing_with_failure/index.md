# 第 22 章 失敗の扱い

<!-- prettier-ignore -->
!!! info 
    - <s>テストメソッドを呼び出す</s>
    - <s>set_upを呼び出す</s>
    - <s>tear_downを後で呼び出す</s>
    - テストメソッドが失敗したとしてもtear_downを呼び出す
    - 複数のテストを走らせる
    - <s>収集したテスト結果を出力する</s>
    - <s>WasRunで文字列をログに記録する</s>
    - **失敗したテストを出力する**

-   前章より、もう少し範囲を狭めて、テストが失敗したときに期待した結果が出力されることのテストを記載する

    ```python
    class TestCaseTest(TestCase):
        def test_failed_result_formatting(self):
            result = TestResult()
            result.test_started()
            result.test_failed()
            assert "1 run, 1 failed" == result.summary()

    TestCaseTest("test_failed_result_formatting").run()
    ```

    -   result オブジェクトに対して、テスト開始時と失敗時にメッセージ（メソッド実行）が送られる設計とした
    -   テストが通るように、test_failed が呼び出された際に、失敗回数をインクリメントするような仕組みを実装する

    ```python
    class TestResult:
        def __init__(self):
            self.run_count = 0
            self.error_count = 0

        def test_failed(self):
            self.error_count += 1

        def summary(self):
            return f"{self.run_count} run, {self.error_count} failed"
    ```

    -   これでテストが通った
        -   もっと細かく、出力の代わりにカウントだけをテストすることもできた
        -   この辺りは、自身の脳内のクリアさにあわせて歩幅を調整するべきである
    -   この test_failed メソッドが例外をキャッチするタイミングで呼び出されば、前章のテストが通ることになる
        -   コメントアウトを外して、test_result_failed が通るような実装に再び向きあう

    ```python
    class TestCase:
        def run(self) -> TestResult:
            result = TestResult()
            result.test_started()
            self.set_up()
            try:
                method = getattr(self, self.name)
                method()
            except Exception:
                result.test_failed()
            self.tear_down()
            return result
    ```

    -   これで前章で作成したテストも通るようになる
        -   しかし、この実装には隠れた問題がある
            -   set_up メソッドで問題が起こっても例外がキャッチされず、テストが止まってしまうのだ
            -   これはそれぞれのテストを独立させる意図と異なる実装となっている
        -   一方で、コードを変更するには新たなテストコードの実装が必要となる（TDD の大原則である）
            -   今回は、TODO に追加しておくことにとどめておく

<!-- prettier-ignore -->
!!! info 
    - <s>テストメソッドを呼び出す</s>
    - <s>set_upを呼び出す</s>
    - <s>tear_downを後で呼び出す</s>
    - テストメソッドが失敗したとしてもtear_downを呼び出す
    - 複数のテストを走らせる
    - <s>収集したテスト結果を出力する</s>
    - <s>WasRunで文字列をログに記録する</s>
    - <s>失敗したテストを出力する</s>
    - set_upのエラーをキャッチして出力する
