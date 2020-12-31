import sqlite3
import json

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

conn = sqlite3.connect('nousei.db')
#conn.row_factory = sqlite3.Row
conn.row_factory = dict_factory

c = conn.cursor()
c.execute('SELECT * FROM 納品' )
#nous = json.dumps(c.fetchall())

nous = c.fetchall()

print (nous)
