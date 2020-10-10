#!/usr/bin/env python3

import json
from base64 import b64encode
import mysql.connector
from mysql.connector import errorcode
import cgitb
import sys
import bcrypt
import secrets
import datetime
import http.cookies as cookie
import os
debug = True

subscriptions_response_dict= {
    "status": 401,
    "description": "session id cookie not found"
}
if 'HTTP_COOKIE' not in os.environ.keys():
    print("Content-Type: text/html;charset=utf-8\n\n")
    print(json.dumps(subscriptions_response_dict))
    exit()



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
    # print("successfully connected!")
    '''print("content length is : " + os.environ['CONTENT_LENGTH'])
    if int(os.environ['CONTENT_LENGTH']) > 250:
        print("Status: 400 Bad Request\n")
        exit(0)'''

usr_name = usr_pass = None
# make sure input is valid
try:
    a = sys.stdin.read()
    if not a:
        authentication_response_dict['description'] = "no body in GET request"
        #print("Status: 400 Bad Request\n")
        #print("no content body received")
        print("Content-Type: text/html;charset=utf-8\n\n")
        print(json.dumps(authentication_response_dict))
        exit()
    user = json.loads(a)
    usr_name = str.encode(user['username'])
    usr_pass = str.encode(user['password'])
    if not usr_pass or not usr_name:
        #print("Status: 400 Bad Request\n")
        authentication_response_dict['description'] = "no user name / password given"
        print("Content-Type: text/html;charset=utf-8\n\n")
        print(json.dumps(authentication_response_dict))
        exit()
except json.JSONDecodeError as err:
    #print("Status: 400 Bad Request\n")
    authentication_response_dict['description'] = "Invalid JSON in request"
    print("Content-Type: text/html;charset=utf-8\n\n")
    print(json.dumps(authentication_response_dict))
    #print(err)
    exit()
except KeyError as err:
    #print("Status: 400 Bad Request\n")
    authentication_response_dict['description'] = "Invalid JSON in request"
    print("Content-Type: text/html;charset=utf-8\n\n")
    print(json.dumps(authentication_response_dict))
    #print(err)
    exit()

try:
    cursor = connection.cursor()
    cursor.execute("SELECT u.user_id, u.hash FROM user u where u.name = %s LIMIT 1", (usr_name,))
    usr = cursor.fetchone()
    if usr is None:
        authentication_response_dict['status'] = 401
        authentication_response_dict['description'] = "username not found"
        print("Content-Type: text/html;charset=utf-8\n\n")
        print(json.dumps(authentication_response_dict))
        #print("user not found!")
        #todo implement this
        exit()
    else:
        (u_id, u_hash) = usr
        u_hash = str.encode(''.join(u_hash))
        if bcrypt.checkpw(usr_pass, u_hash) is True:
            create_user_session(u_id, cursor)
        else:
            authentication_response_dict['status'] = 401
            authentication_response_dict['description'] = "invalid password"
            print("Content-Type: text/html;charset=utf-8\n\n")
            print(json.dumps(authentication_response_dict))
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


