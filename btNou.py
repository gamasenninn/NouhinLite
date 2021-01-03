from bottle import route, run, jinja2_template as template,HTTPResponse,response,request,static_file
import sqlite3
import json
from sqlwrap import *


@route('/')
def index():
    return template('menu.html',title='test',name="AAAA")

@route('/v')
def vue_test():
    return static_file('vue_test.html',root="./views")


@route('/nouhin')
def nouhin():
    name = "Hoge"

    conn = sqlite3.connect('nousei.db')

    j_nous = json_select_all(conn,'納品')
    nous = json.loads(j_nous)

    j_ndtails = json_select_all(conn,'納品明細')
    ndtails = json.loads(j_ndtails)

    conn.close()
    return template('hello.html', title='test', name=name,nous =nous,ndtails=ndtails ) #変更


@route('/api/<table>',method=['GET'])
def api_get_all(table):
    header = {"Content-Type": "application/json"}
    conn = sqlite3.connect('nousei.db')
    res = json_select_all(conn,table)
    conn.close()
    return HTTPResponse(status=200, body=res, headers=header)

@route('/api/<table>/<pkey>',method=['GET'])
def api_get_one(table,pkey):
    header = {"Content-Type": "application/json"}
    conn = sqlite3.connect('nousei.db')
    sel_key = {'ID':pkey}
    res = json_select_one(conn,table,sel_key,'ID')
    conn.close()
    return HTTPResponse(status=200, body=res, headers=header)

@route('/api/<table>',method=['POST'])
def api_get_post(table):
    header = {"Content-Type": "application/json"}
    conn = sqlite3.connect('nousei.db')
    res = dict_insert(conn,table,request.json)
    conn.commit()
    conn.close()
    return HTTPResponse(status=200, body=res, headers=header)

@route('/api/<table>',method=['PUT'])
def api_put_del(table):
    header = {"Content-Type": "application/json"}
    conn = sqlite3.connect('nousei.db')
    res = dict_update(conn,table,request.json,'ID')
    conn.commit()
    conn.close()
    return HTTPResponse(status=200, body=res, headers=header)

@route('/api/<table>/<pkey>',method=['DELETE'])
def api_put_del(table,pkey):
    header = {"Content-Type": "application/json"}
    conn = sqlite3.connect('nousei.db')

    del_key = {'ID':pkey }
    res = dict_delete(conn,table,del_key,'ID')
    conn.commit()
    conn.close()
    return HTTPResponse(status=200, body=res, headers=header)


run(host='localhost', port=8080, reload=True, debug=True)
