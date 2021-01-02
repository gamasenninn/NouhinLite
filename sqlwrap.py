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
    try:
        sql = 'insert into {table_name} {keys} values {replacement_fields}'.format(
                table_name=table_name,
                keys=sqlify_for_insert(d), 
                replacement_fields=sqlify_for_insert('?'*len(d)) 
            )
        conn.execute(
            sql,
            tuple(d.values())
        )
        return "OK:"+sql
    except:
        return "SQL ERROE"

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

    return json.dumps(nous)


