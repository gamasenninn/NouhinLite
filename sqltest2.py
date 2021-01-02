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


#----------- main block -----------

conn = sqlite3.connect(':memory:')

#---Make Model -----

sql = '''
CREATE TABLE "納品" (
	"ID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"納品日"	TEXT,
	"納品先"	TEXT,
	"担当者"	TEXT,
	"摘要"	TEXT
)
'''
conn.execute(sql)

print("\n-----Created Table------")

#-----Insert data------
print("\n-----insert into Table------")

data = {'納品日': "2020/11/01",'納品先': "ABC商店",'担当者': "小野",'摘要': "特別注文"}
dict_insert(conn, '納品', data)

data = {'納品日': "2020/11/02",'納品先': "DEF商店",'担当者': "小野",'摘要': "特別注文"}
j_data = json.dumps(data)
json_insert(conn, '納品', j_data)


#----Select data ------
print("\n-----select from Table------")
c = conn.cursor()
c.execute('SELECT * FROM 納品' )
nous = c.fetchall()
print (nous)

#-----Update data------
print("\n-----Update Table------")
data = {'ID': 2,'納品日': "2020/11/02",'納品先': "更新テスト",'担当者': "小野",'摘要': "特別注文"}
dict_update(conn,'納品',data,'ID')

data = {'納品日': "2020/11/02",'担当者': "小野",'摘要': "更新テスト"}
j_data = json.dumps(data)
json_update(conn,'納品',j_data,'担当者')

#----Select data ------
print("\n-----select from Table------")
c.execute('SELECT * FROM 納品' )
nous = c.fetchall()
print (nous)

#----Select data JSON Format------
print("\n-----select data JSON ------")
nous = json_select_all(conn,'納品')
print(nous)

#-----Delete data------
print("\n-----Delete Table------")
data = {'ID': 2}
dict_delete(conn,'納品',data,'ID')

data = {'ID': 1}
j_data = json.dumps(data)
json_delete(conn,'納品',j_data,'ID')

#----Select data ------
print("\n-----select from Table------")
c.execute('SELECT * FROM 納品' )
nous = c.fetchall()
print (nous)

