# 第 17 章 多国通貨の全体振り返り

-   第 1 部の最終章として、プロセスと成果物の両面から振り返りを行う
-   下記項目を振り返る
    -   ここから先はどうなるのか
    -   メタファー：　設計の構造に与える劇的な効果について
    -   JUnit の使用状況：　いつ、どのように使っていたか
    -   コードメトリクス：　出来上がったコードを様々な角度から計測してみる
    -   プロセス：　レッド・グリーン・リファクタリングといったが、それぞれどれくらい作業しているのか
    -   テスト品質：　 TDD のテストは従来の指標から見てどうなのか

## ここから先はどうなるのか

-   多国通貨のコードはまだ書き終わったとは言えない
    -   例えば、Sum と Money の plus メソッドは完全に重複している
    -   Expression をインターフェースからクラスに変更すれば、共通コードの置き場所と出来る
-   そもそも、システム開発において「完了」という状態はないのかもしれない
    -   システムは日々進化していく
    -   コードを批判的に見てみると、新たな修正点が見つかってくるかもしれない
    -   ツール等を使ってコード解析をする事も変更点を見つける助けになる
-   また、「テストは足りているのか」という観点もある
    -   例えば、「こう動いてはならない」という観点でテストを書いたら新たなバグが見つかるかもしれない
-   最後に、TODO リストが空の時は、設計を見直すチャンスである
    -   設計の言葉と概念に齟齬がないのか？
    -   現在の設計では除去が難しい重複はないだろうか？
    -   長く残っている重複は、新たな設計の必要性を示唆していないか？等

## メタファー

-   著者は多国通貨のサンプルをこれまでに 15 回以上作成してきたが、本書にて「式(Expression)」メタファーを初めて導入した
    -   これによって、以前までの実装と大きく異なった
-   式のメタファーは同じ通貨の足し合わせに起因する頭の痛い問題達から解放し、非常にきれいなコードを作り上げた

## JUnit

-   本書のサンプルコードを実装するにあたって、JUnit(本書では Java で実装されている)の実行は、125 回行われた
-   執筆中の実装だったため、実行間隔のデータは正しく取れていないが、純粋に実装中は大抵 1 分に 1 回テストを実行している

## コードメトリクス

-   コードメトリクスを以下に示す

    |               | プロダクトコード | テストコード |
    | :------------ | :--------------- | :----------- |
    | クラス        | 5                | 1            |
    | メソッド      | 22               | 12           |
    | 行数          | 100              | 94           |
    | 循環的複雑度  | 1.05             | 1            |
    | 行数/メソッド | 4.5              | 7.8          |

## プロセス

-   本書では、TDD のサイクルを以下のように表現してきた

    1. 小さいテストを追加する
    1. すべてのテストを実行し、1 つ失敗すること確認する
    1. テストが通るように変更を行う
    1. 再びテストを実行し、全て成功することを確認する
    1. リファクタリングを行い、重複を除去する

-   テストを書くことを一つのステップとして、コンパイル、テスト、リファクタリングまでの一周にどのくらいの変更が必要になるのか
    -   多国通貨にテストを書きながら、開発を行った際の使用量の頻度を確認すると、殆どのサイクルで変更が少ない
    -   大規模プロジェクトではデータを集めた場合には、更に相対的に小さくなるはずである

## テスト品質

-   TDD の過程で作成されるテストは、システムを開発し続けるために有用なものだが、以下の点では代替にならないことに注意する
    -   パフォーマンステスト
    -   負荷テスト
    -   ユーザビリティテスト
-   TDD の中で作成されたテストの品質を評価できる、広く知られた手法を 2 点紹介する
    -   ステートメントカバレッジ
        -   すべての処理のうち、テストコードで動く割合
        -   品質評価のスタート地点として簡単に実施可能だが、十分な評価とはならない
        -   TDD に厳格に従う場合、ステートメントカバレッジは 100%になる
    -   欠陥挿入
        -   「プロダクトコードの任意の行を変更したら、テストは失敗しなければならない」という考え方
        -   手で行ってもよいが、専用のツールも存在する
        -   今回の場合、1 行だけテストを壊さずに変更出来る
            -   Pair クラスの\_\_hash\_\_である
            -   単一の値であれば、0 でない任意の値でテストが通ってしまう
            -   これはテストの欠陥であり、Dollar、Franc 以外の新たな通貨単位が導入されることで顕在化する
-   カバレッジの総量とは、テストの数を、テストすべき側面の数で割ったものである
    -   より多くのテストを書けば、カバレッジが上がるが、もう 1 つカバレッジを上げる方法がある
    -   プロダクトコードをシンプルにして、テストすべき側面を減らすことである
        -   TDD におけるリファクタリングフェーズはこれに該当する
    -   テストを増やすことであらゆる入力の組み合わせをカバーするのではなく、同じテストのままで、コードを減らしてより多くの組み合わせをカバーする

## 最後のふりかえり

-   TDD において、重要な点を 3 つまとめる
    -   テストをきれいに機能させる 3 つのアプローチ
        -   仮実装
        -   三角測量
        -   明白な実装
    -   テストとコードの間の重複除去が、設計を駆動する
    -   テストの間のギャップを制御する能力が重要
        -   路面が滑りやすい(=複雑な機能)ならばグリップを増し、小さな変更を繰り返す
        -   路面がよい(=明確)なら大きく変更を行う
