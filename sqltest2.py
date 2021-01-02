import sqlite3
import json
from sqlwrap import *

#
#  Test for sqlwrap.py
#

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

