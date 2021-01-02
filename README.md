# NouhinLite
easy CRUD System and to output with PDF for Nouhinsho &amp; Seikyuusho

# 現在の開発状況
このプロジェクトの状況はドラフトです。  
まずは私ともう一人の開発者ががgithub上で共同開発ができるように試験的な段階からスタートすることにしました。  
現在のところほとんどファイルはありません。これから少しずつ実装していく予定です。
Bottleによるルーティングロジックとテンプレート回り、DBからの読み取りなどをテストしている段階です。  
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
最終的には基本的で簡素なアプリモデルを作成します。個別の仕様や特殊な処理が必要な場合、
プロジェクトをforkして開発するとよいと思います。

# どのように動くか

基本言語はPythonです。
Bottleによるアプリをローカル上のマイクロサーバーとします。
ブラウザで指定のアドレスにアクセスすることで処理画面が表示され、データの入力と帳票出力が行えます。
ルーティングはBottleでい、コントロールはVue.jsが担当します。  
ローカルでシステムが動くことで完結しますが、もちろん外部サーバーにデプロイすることも可能です。
デプロイする方法なども記載する予定です。

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

Q. 基本モデルのみの提供ということですが、個別の客先案件に対応するためのカスタマイズは簡単にできますか？
>A. 初歩レベルのSQLの知識と、Vue.jsの知識があれば簡単にカスタマイズ可能だと思います。

Q. 帳票のカスタマイズは自由にできますか？
>A. エクセルなどで帳票のベースをPDFとして作成すれば、
任意の位置にデータをポイントすればよいだけなので比較的簡単で自由な帳票設計が可能かと思います。



# Tips集
開発時に気づいたこと。ちょっとしたテクニックなどをメモしておきます。

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

nous = c.fetchall()

print (nous)
```

## DBへのアクセスの方針
DBへのアクセスはなるべく生のSQLを書かないようにしたいと思っています。  
SQLインジェクション防止とプログラムのメンテナンス性向上のためです。SQLite以外のDBMSでも簡単に移行が可能となります。    
とはいえORMなどを導入するまではいかないのでDBアクセスのためのラッパーを用意したいと思います。  
一方フロントからのデータ入出力はすべてajax通信によるものなのでJsonでのやり取りになります。  
次のような関数群を想定しています。  
```
import sqlite3
import json

def sqlify_for_insert(string_iterable):
    return f'({",".join(string_iterable)})'

def sqlify_for_update(string_iterable):
    return f'{"=?,".join(string_iterable)+"=?"}'

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#----- Insert operation

def dict_insert(conn, table_name, d):
    conn.execute(
        'insert into {table_name} {keys} values {replacement_fields}'.format(
            table_name=table_name,
            keys=sqlify_for_insert(d), 
            replacement_fields=sqlify_for_insert('?'*len(d)) 
        ),
        tuple(d.values())
    )

def json_insert(conn,table_name,j):
    dic_d = json.loads(j)
    return dict_insert(conn,table_name,dic_d)

#------ Update operation

def dict_update(conn,table_name,d,key_name):
    v = d.pop(key_name)
    vl=[]
    vl.append(v)
    
    conn.execute(
        'update {table_name} set {key_values} where {key_name} = ? '.format(
            table_name=table_name,
            key_values=sqlify_for_update(d),
            key_name = key_name
        ),
        tuple(d.values())+tuple(vl)
    )

def json_update(conn,table_name,j,key_name):
    dic_j = json.loads(j)
    return dict_update(conn,table_name,dic_j,key_name)

#----- delete operation

def dict_delete(conn, table_name, d, key_name):
    v = d.pop(key_name)
    vl=[]
    vl.append(v)
    conn.execute(
        'delete from {table_name} where {keys} = ?'.format(
            table_name=table_name,
            keys=key_name
        ),
        tuple(vl)
    )

def json_delete(conn,table_name,j,key_name):
    dic_j = json.loads(j)
    return dict_delete(conn,table_name,dic_j,key_name)


#------ select operation

def json_select_all(conn, table_name):
    conn.row_factory = dict_factory

    c = conn.cursor()
    c.execute('SELECT * FROM '+table_name )

    nous = c.fetchall()

    return nous

```






