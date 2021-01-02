from bottle import route, run, jinja2_template as template,HTTPResponse,response,request
import sqlite3
import json
from sqlwrap import *


@route('/')
def index():
    return template('menu.html',title='test',name="AAAA")

@route('/nouhin')
def nouhin():
    name = "Hoge"

    conn = sqlite3.connect('nousei.db')

    j_nous = json_select_all(conn,'納品')
    nous = json.loads(j_nous)

    j_ndtails = json_select_all(conn,'納品明細')
    ndtails = json.loads(j_ndtails)
    
    return template('hello.html', title='test', name=name,nous =nous,ndtails=ndtails ) #変更


@route('/api/<table>',method=['GET','POST'])
def api(table):
    header = {"Content-Type": "application/json"}
    conn = sqlite3.connect('nousei.db')

    if request.method == 'GET':
        res = json_select_all(conn,table)
    else:
        res = dict_insert(conn,table,request.json)
        conn.commit()
    conn.close()
    return HTTPResponse(status=200, body=res, headers=header)



run(host='localhost', port=8080, reload=True, debug=True)
