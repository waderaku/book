# 第 19 章 前準備

-   テストを書く際には、以下のような基本ステップがある
    -   準備(Arrange)：オブジェクトを作る
    -   実行(Act)：そのオブジェクトに対して操作を行う
    -   アサート(Assert)：結果の検証を行う

<!-- prettier-ignore -->
!!! info 
    - <s>テストメソッドを呼び出す</s>
    - **set_upを呼び出す**
    - tear_downを後で呼び出す
    - テストメソッドが失敗したとしてもtear_downを呼び出す
    - 複数のテストを走らせる
    - 収集したテスト結果を出力する

-   最初のステップ「準備」は、テスト間で重複しがちである
    -   一方で、「実行」、「アサート」は重複しないことが多い
    -   7 と 9 の四則演算のテストをする際、7 と 9 という値は変わらないが、操作「+, -, \*」とアサート「16, -2, 63」はそれぞれ異なる
-   上記のようなテストに使用する同一のオブジェクトに関して考えると、2 つの相反する制約が生まれる
    -   パフォーマンス：テストは可能な限り早く動作してほしい。その為、生成したオブジェクトを使いまわしたい
    -   独立性：テストの成功/失敗は他のテストの結果に影響してはいけない。テスト間で共有しているオブジェクトが、他のテストの結果に依存してはいけない
-   テスト間の依存関係は避けなければならない
    -   1 つのテストが失敗したら後続のテストが全て失敗してしまえば、明らかに害悪である
    -   テストの実行順序にも依存関係を持たせてはいけない
-   今回はテストごとに新しいオブジェクトを生成する

    -   既に WasRun のテストの形として存在している
        -   テストが走る前にフラグが必ず False に戻っている

    ```python
    class TestCaseTest(TestCase):
        def test_set_up(self):
            test = WasRun("test_method")
            test.run()
            assert test.was_set_up


    TestCaseTest("test_runnning").run()
    TestCaseTest("test_set_up").run()
    ```

    -   was_set_up 属性がないため、設定する一連の処理を追加する

    ```python
    class TestCase:
        def run(self):
            self.set_up()
            method = getattr(self, self.name)
            method()

        def set_up(self):
            pass

    class WasRun(TestCase):
        def set_up(self):
            self.was_set_up = 1
    ```

    -   この変更は、テストが通るまでに 2 つのクラスを変更しなければならなかった
        -   何かを学びながら変更開発するときは、一度に 1 つのメソッドだけを変え、テストがどうなるかを逐次確かめることを推奨する

-   初期化処理を set_up に移管する

    -   まず、was_run フラグを set_up に移動し、不要になったコンストラクタを消す
    -   また、test_running の観点をシンプルにするため、実行前のフラグチェックを削除する
        -   そちらの観点は test_set_up にあるため問題ない

    ```python
    class WasRun(TestCase):
        def set_up(self):
            self.was_run = None
            self.was_set_up = 1

    class TestCaseTest(TestCase):
        def test_runnning(self):
            test = WasRun("test_method")
            test.run()
            assert test.was_run
    ```

-   現状、2 つのテストメソッドがそれぞれで WasRun インスタンスを生成している

    -   これを set_up に共通化する
        -   各々別の TestCaseTest インスタンスで動いているため、それぞれのテストでの独立性は維持している

    ```python
    class TestCaseTest(TestCase):
        def set_up(self):
            self.test = WasRun("test_method")

        def test_runnning(self):
            self.test.run()
            assert self.test.was_run

        def test_set_up(self):
            self.test.run()
            assert self.test.was_set_up
    ```

-   本章では、テストパフォーマンスより依存関係を避けるシンプルな実装を優先した
-   次章では、tear_down メソッドを実装し、各テストメソッドの後に走らせるようにする
