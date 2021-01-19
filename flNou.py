from flask import Flask, render_template, request, json, jsonify
import sqlite3
import json
from sqlwrap import *
#from mkpdf import make_pdf
import subprocess

app = Flask(__name__)

#------各処理ページの基本的なルーティング-------

@app.route('/')
def menu():
    return render_template('menu.html', title='メニュー', name="TEST") 

@app.route('/<f>')
def proc(f):
    return app.send_static_file('./'+f)

@app.route('/<dirname>/<f>')
def dir_file(dirname,f):
    return app.send_static_file(f'./{dirname}/{f}')


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r



#------- TEST用ルーティング-------
'''
@app.route('/v/<f>')
def bv(f):
    return app.send_static_file('./Vue_test/'+f)

@app.route('/nouhin')
def nouhin():
    return app.send_static_file('nouhin.html')

@app.route('/compo/<f>')
def compof(f):
    return app.send_static_file('./Vue_test/'+f)
'''
#--------印刷 ブロック -------------

@app.route('/print/<conf>/<ID>')
def print(conf,ID):
    try:
        #make_pdf(table,'test','14')
        cmd = "python ./mkpdf.py "+conf+" "+ID
        subprocess.run(cmd)
        return app.send_static_file('./pdf/output.pdf')
    except:
        print ("Print Error")
        return "Print Error"


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
