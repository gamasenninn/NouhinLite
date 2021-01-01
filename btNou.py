from bottle import route, run, jinja2_template as template, HTTPResponse
import sqlite3
import json

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@route('/')
def index():
    return template('menu.html',title='test',name="AAAA")


@route('/nouhin')
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
    
    return template('hello.html', title='test', name=name,nous =nous,ndtails=ndtails ) #変更


@route('/api/<table>')
def api(table='納品'):
    header = {"Content-Type": "application/json"}

    conn = sqlite3.connect('nousei.db')
    conn.row_factory = dict_factory

    c = conn.cursor()
    c.execute('SELECT * FROM '+table )
    nous = json.dumps(c.fetchall())
   
    res = HTTPResponse(status=200, body=nous, headers=header)
    return res

##

run(host='localhost', port=8080, reload=True, debug=True)
