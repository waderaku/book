# 第 24 章 xUnit 全体ふりかえり

-   もしテスティングフレームワークを実装する時が来たなら、第 Ⅱ 部の手順は良いガイドになるだろう
    -   ここでは実装の詳細よりもテストケースが重要である
    -   テストを独立で動かし、それらをまとめて評価できるようにする
-   現在殆どのプログラミング言語には、xUnit が移植されているが、あえて自身で作ることにも以下の意義がある

    -   熟達：自分自身でフレームワーク実装をすることで、使用するうえでも内部の作りや思想の理解を十分したうえで扱うことができる
    -   探索：新言語を学ぶ上で、よい入門となる。8 個から 10 個のテストが通るころには、日々の実装で使用する機能はほとんど登場している可能性が高い

-   テストを行う際、アサーションの失敗と、テスト実行中に起こる他のエラーとの大きな違いに気づく

    -   アサーションの失敗は、デバッグに大きな時間がかかる
    -   その為、普通はアサーションの失敗とエラーを UI 上分ける
