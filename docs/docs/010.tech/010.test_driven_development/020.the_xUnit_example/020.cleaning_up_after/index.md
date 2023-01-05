# 第 20 章 後片付け

-   テストには、set_up メソッドで外部リソースを用意するものもある
    -   その場合、テストの独立性を保つためには、外部リソースを終了時に開放しなければならない
-   上記機能を実現する tear_down メソッドを実装する
    -   単純に実装するならフラグを追加するが、既にフラグが複数あり、複雑なフラグ管理が必要になってしまう
    -   そこで、テスト戦略を変更し、ログを保持する処理方式にする

<!-- prettier-ignore -->
!!! info 
    - <s>テストメソッドを呼び出す</s>
    - <s>set_upを呼び出す</s>
    - tear_downを後で呼び出す
    - テストメソッドが失敗したとしてもtear_downを呼び出す
    - 複数のテストを走らせる
    - 収集したテスト結果を出力する
    - **WasRunで文字列をログに記録する**

-   tear_down を実装する前に、他のフラグもログに変更していく

    -   まずは set_up を変更する
    -   テストコードでのチェックをログの確認に変更し、set_up メソッドでログを追記する

    ```python
    class TestCaseTest(TestCase):
        def test_set_up(self):
            self.test.run()
            assert "set_up " == self.test.log

    class WasRun(TestCase):
        def set_up(self):
            self.was_run = None
            self.was_set_up = 1
            self.log = "set_up "
    ```

    -   テストが通ったので、was_set_up フラグを削除する事ができる
    -   同様にして、test_method 時にログを追記するようにし、テストコードを変更する

    ```python
    class WasRun(TestCase):
        def test_method(self):
            self.was_run = 1
            self.log += "test_method "

    class TestCaseTest(TestCase):
        def test_runnning(self):
            self.test.run()
            assert "set_up test_method " == self.test.log
    ```

    -   test_method は通ったが、test_set_up で失敗するようになった

        -   ここまでの変更でログには「set_up test_method 」が残るようになったからである
        -   テストコードを修正する

        ```python
        class TestCaseTest(TestCase):
            def test_set_up(self):
                self.test.run()
                assert "set_up test_method " == self.test.log
        ```

    -   上記変更によって、test_set_up は 2 つのテスト内容を併せ持つようになった

        -   test_running を削除し、test_set_up を観点に合う名前(test_template_method)に変更する
        -   また、不要になった was_run フラグを削除する

        ```python
        class WasRun(TestCase):
            def test_method(self):
                self.log += "test_method "

            def set_up(self):
                self.log = "set_up "

        class TestCaseTest(TestCase):
            def set_up(self):
                self.test = WasRun("test_method")

            def test_template_method(self):
                self.test.run()
                assert "set_up test_method " == self.test.log

        TestCaseTest("test_template_method").run()
        ```

        -   前章で WasRun クラスのインスタンス化を共通化したが、呼び出し元が一つになったため、test_template_method に戻す

        ```python
        class TestCaseTest(TestCase):
            def test_template_method(self):
                test = WasRun("test_method")
                test.run()
                assert "set_up test_method " == test.log
        ```

        -   今回のように、重複が発生したためリファクタリングを行ったものの、直後に元の形に戻さなければならなくなることがしばしばある
            -   このような手戻りを嫌って、重複をしばらく放置する事は推奨しない
            -   思考サイクルを設計に集中できるように、反射的にリファクタリングをした方が結果的に良くなることが多い

-   これで tear_down のテストコードを実装することができる

    ```python
    class TestCaseTest(TestCase):
        def test_template_method(self):
            test = WasRun("test_method")
            test.run()
            assert "set_up test_method tear_down " == test.log
    ```

    -   当然テストは失敗する。set_up や test_method と同じように、tear_down の機能を実装する

    ```python
    class TestCase:
        def run(self):
            self.set_up()
            method = getattr(self, self.name)
            method()
            self.tear_down()

    class WasRun(TestCase):
        def tear_down(self):
            self.log += "tear_down "
    ```

    -   しかし、テストは失敗する。エラーの箇所は WasRun ではなく、TestCaseTest からエラーが出ている
        -   TestCase クラスに tear_down メソッドがない事が原因である
            -   現在開発しているテスティングフレームワークが機能して原因究明ができた
        -   修正自体は TestCase に空の tear_down メソッドを追加すればよい

-   次章では、テスト結果のレポート機能に着手する
