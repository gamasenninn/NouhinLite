from flask import Flask, render_template, request, json, jsonify
import sqlite3
import json
from sqlwrap import *

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('menu.html', title='メニュー', name="TEST") #変更

@app.route('/v')
def vue():
    return app.send_static_file('vue_test.html')

@app.route('/nouhin')
def nouhin():
    name = "Hoge"

    conn = sqlite3.connect('nousei.db')

    j_nous = json_select_all(conn,'納品')
    nous = json.loads(j_nous)

    j_ndtails = json_select_all(conn,'納品明細')
    ndtails = json.loads(j_ndtails)

    conn.close()
    return render_template('hello.html', title='test', name=name,nous =nous,ndtails=ndtails ) #変更

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