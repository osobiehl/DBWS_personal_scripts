#!/usr/bin/env python3sla

import json
from base64 import b64encode

import mysql.connector
from mysql.connector import errorcode
import cgitb
import sys
import bcrypt
import secrets
import datetime

debug = True


def create_user_session(u_id, cursor):
    print("creating user session . . . ")
    token = secrets.token_bytes()
    token = b64encode(token)
    print(token)
    print(len(token))
    cursor.execute("SELECT s.user_id_fk, s.date, s.session_id from user_session s WHERE s.user_id_fk = %s", (u_id,))
    for (user_id, date, session_id) in cursor.fetchall():
        if date + datetime.timedelta(minutes=30) < datetime.datetime.utcnow():
            if debug:
                print("user session expired: ")
            cursor.execute("DELETE FROM user_session WHERE session_id = %s", (session_id, ))
    #make sure no clashes occur generating a token id, messy but practical solution
    while True:
        try:
            cursor.execute("INSERT INTO user_session (session_id, user_id_fk, date) VALUES (%s, %s, %s)", (token, u_id, datetime.datetime.utcnow()))
            #in case we have a token clash, just try to re-calculate a new token
        except mysql.connector.IntegrityError as err:
            token = secrets.token_bytes()
            continue
        except Exception as err:
            print(err)
            print(err.__doc__)
            print(type(err).__name__)
            exit(-1)
        break
    connection.commit()
    print("operation successful! printing token. . . ")
    print(token);


cgitb.enable()
print("Content-Type: text/html;charset=utf-8\n\n")
f = open('userconfig.json')
config = json.load(f)
try:
    connection = mysql.connector.connect(**config, auth_plugin='mysql_native_password', charset='utf8')
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
    cursor.execute("SELECT u.user_id, u.hash FROM user u where u.name = %s LIMIT 1", (usr_name,))
    usr = cursor.fetchone()
    if usr is None:
        print("user not found!")
        #todo implement this
        exit(-1)
    else:
        (u_id, u_hash) = usr
        u_hash = str.encode(''.join(u_hash))
        print(u_hash)
        if bcrypt.checkpw(usr_pass, u_hash) is True:
            print("user authenticated!")
            create_user_session(u_id, cursor)
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


