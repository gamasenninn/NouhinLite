import sqlite3
import json


def sqlify_list(string_iterable):
    return f'({",".join(string_iterable)})'

def sqlify_list2(string_iterable):
    return f'({"=?,".join(string_iterable)})'

#    return ','.join([f'{key} = {value}' for key, value in string_iterable.items()])

#----- Insert operation

def json_insert(conn, table_name, d):
    conn.execute(
        'insert into {table_name} {keys} values {replacement_fields}'.format(
            table_name=table_name,
            keys=sqlify_list(d), 
            replacement_fields=sqlify_list('?'*len(d)) 
        ),
        tuple(d.values())
    )

#------ Update operation

def json_update(conn,table_name,d,key_name):
    print("key_nmae="+key_name)
    v = [v for k,v in data.items() if k == key_name]
    #key_value = v[0] if len(v) else ''
    #print("key_value="+v)
    print(
        'update {table_name} set {key_values} where {key_name} = ? '.format(
            table_name=table_name,
            key_values=sqlify_list2(d),
            key_name = key_name
        ),
        tuple(d.values())+tuple(v)
    )


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

print("Created Table")

#-----Insert data------

#data = {'ID': 1,'納品日': "2020/11/01",'納品先': "ABC商店",'担当者': "小野",'摘要': "特別注文"}
data = {'納品日': "2020/11/01",'納品先': "ABC商店",'担当者': "小野",'摘要': "特別注文"}
#d = {'a': 1, 'b': 2, 'c': 3}
json_insert(conn, '納品', data)

#data = {'ID': 3,'納品日': "2020/11/02",'納品先': "DEF商店",'担当者': "小野",'摘要': "特別注文"}
data = {'納品日': "2020/11/02",'納品先': "DEF商店",'担当者': "小野",'摘要': "特別注文"}
json_insert(conn, '納品', data)


#----Select adta ------
c = conn.cursor()
c.execute('SELECT * FROM 納品' )

nous = c.fetchall()

print (nous)

#-----Update data------
data = {'ID': 3,'納品日': "2020/11/02",'納品先': "DEF商店",'担当者': "小野",'摘要': "特別注文"}
json_update(conn,'納品',data,'担当者')
