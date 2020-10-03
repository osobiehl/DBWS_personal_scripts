#!/usr/bin/env python3
import json
import mysql.connector
from mysql.connector import errorcode
import cgitb
import sys
import bcrypt
cgitb.enable()
print("Content-Type: text/html;charset=utf-8\n\n")
f = open('userconfig.json')
config = json.load(f)
try:
    connection = mysql.connector.connect(**config, auth_plugin='mysql_native_password')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    print("successfully connected!")
    '''print("content length is : " + os.environ['CONTENT_LENGTH'])
    if int(os.environ['CONTENT_LENGTH']) > 250:
        print("Status: 400 Bad Request\n")
        exit(0)'''

usr_name = usr_pass = None
# make sure input is valid
try:
    a = sys.stdin.read()
    if not a:
        print("Status: 400 Bad Request\n")
        print("no content body received")
        exit(-1)
    print(a)
    user = json.loads(a)
    usr_name = str.encode(user['username'])
    usr_pass = str.encode(user['password'])
    if not usr_pass or not usr_name:
        print("Status: 400 Bad Request\n")
        print("no user name given: " + a)
        exit(-1)
except json.JSONDecodeError as err:
    print("Status: 400 Bad Request\n")
    print("Invalid json in request: "+a)
    print(err)
    exit(-1)
except KeyError as err:
    print("Status: 400 Bad Request\n")
    print("Invalid json in request: " + a)
    print(err)
    exit(-1)

try:
    cursor = connection.cursor()
    cursor.execute("SELECT u.hash FROM user u where u.name = %s LIMIT 1", (usr_name,))
    usr = cursor.fetchone()
    if usr is None:
        print("user not found!")
        #todo implement this
        exit(-1)
    else:
        usr = str.encode(''.join(usr))
        print(usr)
        if bcrypt.checkpw(usr_pass, usr) is True:
            print("user authenticated!")
        else:
            print("password wrong!")
except mysql.connector.IntegrityError as err:

    print(err)
    print(err.__doc__)
    print(type(err).__name__)
    exit(-1)
# except Exception as err:
#     print(err)
#     print(err.__doc__)
#     print(type(err).__name__)
#     exit(-1)

connection.close()
