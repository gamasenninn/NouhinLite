from flask import Flask, render_template, request, json, jsonify
import sqlite3
import json
from sqlwrap import *

app = Flask(__name__)

#------各処理ページの基本的なルーティング-------

@app.route('/')
def hello():
    return render_template('menu.html', title='メニュー', name="TEST") 

@app.route('/v')
def vue():
    return app.send_static_file('vue_test.html')

@app.route('/bv')
def bv():
    return app.send_static_file('bv_test.html')

@app.route('/nouhin')
def nouhin():
    return app.send_static_file('nouhin.html')

@app.route('/compo')
def compo():
    return app.send_static_file('./Vue_test/nouhin.html')

@app.route('/compo/<f>')
def compof(f):
    return app.send_static_file('./Vue_test/'+f)

#--------API ブロック -------------
@app.route('/api/<table>',methods=['GET'])
def api_get_all(table):
    conn = sqlite3.connect('nousei.db')
    res = json_select_all(conn,table)
    conn.close()
    return res

@app.route('/api/<table>/<pkey>',methods=['GET'])
def api_get_one(table,pkey):
    conn = sqlite3.connect('nousei.db')
    sel_key = {'ID':pkey}
    res = json_select_one(conn,table,sel_key,'ID')
    conn.close()
    return res

@app.route('/api/<table>/<item>/<key>',methods=['GET'])
def api_get_byKey(table,item,key):
    conn = sqlite3.connect('nousei.db')
    sel_key = {item:key}
    res = json_select_all_key(conn,table,sel_key,item)
    conn.close()
    return res

@app.route('/api/<table>',methods=['POST'])
def api_get_post(table):
    conn = sqlite3.connect('nousei.db')
    res = dict_insert(conn,table,request.json)
    conn.commit()
    conn.close()
    return res

@app.route('/api/<table>',methods=['PUT'])
def api_put(table):
    conn = sqlite3.connect('nousei.db')
    res = dict_update(conn,table,request.json,'ID')
    conn.commit()
    conn.close()
    return res

@app.route('/api/<table>/<pkey>',methods=['DELETE'])
def api_del(table,pkey):
    conn = sqlite3.connect('nousei.db')

    del_key = {'ID':pkey }
    res = dict_delete(conn,table,del_key,'ID')
    conn.commit()
    conn.close()
    return res


#------Main-----
if __name__ == "__main__":
    app.run(debug=True)
