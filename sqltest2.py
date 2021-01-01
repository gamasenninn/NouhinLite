import sqlite3
import json


def sqlify_list(string_iterable):
    """ ('a', 'b', 'c') -> '(a, b, c)' """
    return f'({",".join(string_iterable)})'

def sqlify_list2(string_iterable):
    """ ('a', 'b', 'c') -> '(a, b, c)' """
    return f'({"=?,".join(string_iterable)})'

#    return ','.join([f'{key} = {value}' for key, value in string_iterable.items()])

#----- Insert operation

def json_insert(conn, table_name, d):
    conn.execute(
        'insert into {table_name} {keys} values {replacement_fields}'.format(
            table_name=table_name,
            keys=sqlify_list(d), # dict.__iter__ yields the keys, so .keys() isn't necessary
            replacement_fields=sqlify_list('?'*len(d)) # str.__iter__ yields characters, so ','.join('?'*5) is equivalent to ','.join(['?']*5)
        ),
        tuple(d.values())
    )

#------ Update operation

def json_update(conn,table_name,d,rkey,rvalue):
    print(
        'update {table_name} set {key_values} where {rkey} = {rvalue}'.format(
            table_name=table_name,
            key_values=sqlify_list2(d),
            rkey = rkey,
            rvalue = rvalue
        ),
        tuple(d.values())
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
data = {'納品日': "2020/11/02",'納品先': "DEF商店",'担当者': "小野",'摘要': "特別注文"}
json_update(conn,'納品',data,rkey='ID',rvalue='3')
