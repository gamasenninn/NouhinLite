from flask import Flask, render_template #追加
import sqlite3

conn = sqlite3.connect('nousei.db')
conn.row_factory = sqlite3.Row

app = Flask(__name__)

@app.route('/nouhin')
def nouhin():
    name = "Hoge"
    #return name

    conn = sqlite3.connect('nousei.db')
    conn.row_factory = sqlite3.Row

    c = conn.cursor()
    c.execute('SELECT * FROM 納品' )    

    nous = c.fetchall()

    c2 = conn.cursor()
    c2.execute('SELECT * FROM 納品明細' )    

    ndtails = c2.fetchall()
    
    return render_template('hello.html', title='flask test', name=name,nous =nous,ndtails=ndtails ) #変更

@app.route('/')
def menu():
    name = "hoge2"
    return render_template('menu.html', title='flask test', name=name ) #変更


## おまじない
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=80)
