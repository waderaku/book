# 第 27 章 テスティングフレームワーク

-   本章では、テストを書くことに焦点を当てたパターンを紹介する

## 小さいテスト

-   あまりに大きな単位で作成したテストが失敗した時には、問題個所を絞り込んで小さいテストを書き、そこに焦点を当てると良い
    -   テストを通すために複数の変更が必要な時や、10 分以上変更をしている時は小さいテストを行う事を考えるべき
-   大きなテストを書いてしまった場合は、そこから学ぶべきである
    -   何故大きなテストを書いてしまったのか
    -   小さく分割するためにはどうすればよかったのか

## Mock Object（模擬オブジェクト）パターン

-   構築処理が重かったり、準備に手間がかかったりするようなリソースに依存したオブジェクトをテストする際には、Mock Object を使用すると良い
-   Mock Object の古典的な例は、データベースである

    -   データベースは処理時間に時間がかかり、中身をきれいにしておくのも難しい
    -   データベースがリモートにある場合、ネットワークに依存したテストにもなる
    -   そのため、多くのテストでは、以下のように定数データを返すようにする

        ```java
        @Test
        public void testOrderLookup() {
            Database db = new MockDatabase();
            db.expectQuery("SELECT order_no FROM Order WHERE cust_no = 123");
            db.returnResult(new String[]{"Order 2", "Order 3"});
        }
        ```

-   Mock Object の価値は速度や信頼性だけではなく、その可読性にもある
    -   上記コードも、何が返ってくるかが自明である
    -   Mock Object を使用すると、必然的にオブジェクトの可視性に留意するようになり、コードの結合度を低く抑えることにつながる
-   Mock Object と実際のプロダクトコードの動きが異なる可能性がある
    -   実際のプロダクトコードが出来上がったタイミングで、改めてテストを流す必要がある

## Self Shunt（自己接続）パターン

-   使用しているオブジェクトのインターフェースが正しいことをテストする時には、Self Shunt パターンを使用すると良い
-   グリーンバーを動的に更新するテスト結果 UI を例にとる

    -   TestResult に登録されたオブジェクトは、個別のテストの終了や失敗、テストスイート全体の開始と終了等の通知を受けられるようにする

    ```python
    def test_notification():
        result = TestResult()
        listener = ResultListener()
        result.add_listener(listener)
        WasRun("test_method").run(result)
        assert 1 == listener.count

    class ResultListener:
        def __init__(self):
            self.count = 0

        def start_test(self):
            self.count += 1
    ```

    -   Self Shunt パターンで記載すると、以下のようになる

    ```python
    def test_notification(self):
        self.count = 0
        result = TestResult()
        result.add_listener(self)
        WasRun("test_method").run(result)
        assert 1 == self.count

    def start_test(self):
        self.count += 1
    ```

    -   これで、テストケース自身が Mock Object のように振舞わせることができる
        -   使用しているオブジェクトのインターフェースが認識と異なる場合、エラーを検知できる

-   Self Shunt パターンを使って書かれたテストは、そうでないテストに比べて可読性が上がる可能性が高い

    -   テストにおいて必要な情報がテストコードの中に全て含まれているからである

-   Self Shunt は、「インターフェースの抽出」を行う必要がある
    -   インターフェースを抽出するのと、既存クラスをブラックボックスでテストするのとで、どちらが簡単かを考慮する

## Log String（記録用文字列）パターン

-   メソッドの呼び出し順序を保証するためには、Log String パターンを使用すると良い
-   Template Method パターンを使用して、メソッドが set_up、テストメソッド、tear_down の順に呼ばれることを例に考える

    ```python
    def test_template_method(self):
        test = WasRun("test_method")
        result = TestResult()
        test.run(result)
        assert "set_up test_method tear_down" == test.log

    def set_up(self):
        self.log = "set_up "

    def test_method(self):
        self.log += "test_method "

    def tear_down(self):
        self.log += "tear_down "
    ```

-   Log String パターンが特に役立つのは、Observer パターンを実装していて、特定の順番で通知が行われていることを検証したいときである
-   通知の種類だけが問題で、順番は問題ないのであれば、文字列を Set に格納すればよい

## Crash Test Dummy（衝突実験ダミー人形）パターン

-   エラー処理部分のコードのテストを行う場合には、Crash Test Dummy パターンを使用すると良い
-   ファイルシステムが限界要領まで達している時にアプリケーションに何が起こるかをテストすることを例に考える

    -   実際に例外が起こるような実装をすると処理が重くなるため、状況をシミュレートするコードを書く

    ```java
    private class FullFile extends File {
        public FullFile(String path){
            super(path);
        }
        public boolean createNewFile() throws IOException {
            throw new IOException();
        }
    }

    @Test
    public void testFileSystemError() {
        File f = new FullFile("foo");
        try {
            saveAs(f);
            fail();
        } catch (IOException e) {
        }
    }
    ```

    -   上記のように例外を発生する特別なオブジェクトを用意することで、エラー発生時の挙動を確認することができる

## 失敗させたままのテスト

-   個人で実装をしている時、コーディングを中断する際には、最新のテストが失敗している状態を推奨する
-   再開する際には、書きかけの内容を確認して、その時何を考えていたかを思い出す手がかりとなる
    -   テストを通すというタスクまで明確な状態で始められる

## きれいなチェックイン

-   「失敗させたままのテスト」は個人開発では適用できるが、チーム開発ではそうはいかない
    -   コードの状態が最後に自身が見た状態とは異なっている可能性が高いからだ
    -   その場合は、自身の理解できない動かないコードがあっては作業ができないため、テストが完全に通るようにして作業を中断することを推奨する
-   チェックイン前に走らせるテストスイートは、手元で常時走らせるテストスイートよりも、周囲との結合部分を考慮するため、広い範囲をカバーするテストスイートとなる
    -   結合テストスイートで失敗した場合は、以下 2 つのルールのどちらかを採用すると良い
        -   一つ目は、手元の作業を捨てて初めからやり直すことである
            -   結合テストで落ちた場合には、これまで書いていたコードにある前提には、何かしらの間違いがあることを証明している
        -   二つ目は、不具合を修正してチェックインする猶予を与える方法である
            -   開発する上で精神衛生上よくなる
            -   結合テストのコスト爆発を避けるために、数分試してダメだった場合は一から捨てる必要がある
