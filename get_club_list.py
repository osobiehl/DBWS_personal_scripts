#!/usr/bin/env python3
import json
print("Content-Type: text/html;charset=utf-8\n\n")
from establish_connection import *

connection = StartConnection()
cursor = connection.cursor()
cursor.execute('SELECT club_id, name FROM club')
dict = {}
for (key, value) in cursor.fetchall():
    dict[key] = value
res = json.dumps(dict)

print(res)
