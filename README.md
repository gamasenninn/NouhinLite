# NouhinLite
easy CRUD System and to output with PDF for Nouhinsho &amp; Seikyuusho

# 現在の開発状況
このプロジェクトの状況はドラフトです。  
まずは私ともう一人の開発者ががgithub上で共同開発ができるように試験的な段階からスタートすることにしました。  
現在のところほとんどファイルはありません。  
Bottleによるルーティングロジックとテンプレート回り、DBからの読み取りテストなどをテストしている段階です。  
PDF出力回りは未実装です。

# このプロジェクトについて
できるだけ手軽に納品書や請求書を発行できるシステムです。  
納品書や請求書はMS EXELで作ることが現場で普通に行われているものですが、
運用していくにつれファイルが散在してあとから参照しづらいといった問題が発生します。
また、MS ACCESSなどを使い専用のアプリを作成する場合、
フロントエンドのアプリを動かすためにランタイムが必要となり、配布時に面倒なインストール作業が発生します。  
一方で、Webシステムを組んでクラウド上で書類を発行できるようにするというアイディアが浮かびます。  
理想的ではありますが、作成コストやデプロイのためのコストがかかるという問題があります。  
  
こういった問題を解決する一つのアイディアとしては
ローカル環境でサクッとWebサービスを起動させ、フロントエンドをブラウザとして
データを入力し、書類をPDFで出力するという運用はどうでしょうか。  
ファイルの散在問題も解決し、アプリのためのランタイム環境設定なども必要もなくなります。
Webシステムを構築するコストも手間もかかりません。
使い慣れたブラウザでデータを入力すればすぐに納品書が発行できる。  
そんなイメージでこのシステムを作成しようとしています。 

# どのように動くか

基本言語はPythonです。
Bottleを起動しアプリをマイクロサーバーとします。




# システムのインストール（開発環境と実行環境）

最初にプロジェクトをcloneします。
```
$git clone https://github.com/gamasenninn/NouhinLite
```
cloneしたローカル環境にはすでにpythonがインストールされていることが前提としてます。 
bottle,他XXX、XXXのライブラリーを使用しますので
あらかじめpipでインストールしてください。

```
pip install bottle
```
準備ができたら 
次のファイルを実行します。
```
$python btNou.py
```
すると次のような画面が表示されます。
```
Bottle v0.12.19 server starting up (using WSGIRefServer(reload=True))...
Listening on http://localhost:8080/
Hit Ctrl-C to quit.
```
お使いのブラウザで次のURLにアクセスします。

```
http://localhost:8080
```
メニューが表示されたらインストールは成功です。
あとは、お好きなデータを入力し、印刷をしてみてください。

# システムのインストール（実行環境のみ）

windowsのEXEファイルを用意する予定です。
Pyinstallで必要なライブラリーを同梱したものをダウンロードし、exeファイルをクリックするだけで動くようにする予定です。


# FAQ
Q. なぜFlaskではなくBottleを使うのですか？
>A. Bottleは1ファイルで完結するため、pipが動かないサーバーにもインストールできるからです。

# Tips集
## SQLiteのDBから取得したデータをJson化するには
SQLiteでデータを取得するfetchはデフォルトでは配列を返すだけです。通常はそれで問題ありませんが、
APIを作成する場合著しく汎用性に欠けるものになってしまいます。  
そのためには少々工夫が必要です。幸いSQLiteのConnectionオブジェクトにはrow_factoryという便利な属性があります。  
この属性に返却値のロジックを与えることで目的のデータフォーマットを出力することができます。 
本プログラムではAPIルーターでこの処理をJSON出力として利用します。  
次に示す簡単なサンプルプログラムを見れば理解が早いと思います。  
sqltest.py  
```
import sqlite3
import json

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

conn = sqlite3.connect('nousei.db')
#conn.row_factory = sqlite3.Row
conn.row_factory = dict_factory

c = conn.cursor()
c.execute('SELECT * FROM 納品' )
#nous = json.dumps(c.fetchall())

nous = c.fetchall()

print (nous)
```


