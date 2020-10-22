#!/usr/bin/env python3
import os
import http.cookies as Cookie
import datetime
import mysql.connector
import json
from base64 import b64encode
'''
WARNING: CONNECTION MUST STILLBE COMMITTED BEFORE DOING ANYTHING ELSE!
status return types:
440: user session expired
400: missing cookie, cookie not found, no user session in database




'''
def handleRequestCookie(mysql_connection):
    print("Content-Type: text/html;charset=utf-8\n\n")
    req_response = {
        "status": 401,
        "description": "default_description"
    }
    if 'HTTP_COOKIE' not in os.environ:
        req_response['status'] = 400
        req_response['description'] = "missing Cookie"
        return req_response
    try:
        cookie_string = os.environ.get('HTTP_COOKIE')
        C = Cookie.SimpleCookie()

        C.load(cookie_string)
        if 'DBWS-g3-auth' not in C:
            req_response['description'] = "cookie not found"
            return req_response
        auth_cookie = C['DBWS-g3-auth']
        print("printing auth cookie value . . .")
        print(auth_cookie.value)
        print('<br>')
    except Exception as err:
        print("Content-Type: text/html;charset=utf-8\n\n")
        print(err)
    #try to see if user session is authenticated
    try:
        cursor = mysql_connection.cursor()
        row_count = cursor.execute('SELECT s.user_id_fk, s.date, s.session_id FROM user_session s WHERE s.session_id = %s', (auth_cookie.value,))

        if row_count is 0:
            req_response['description'] = "no user session found in database"
            return req_response
        user_id, date, session_id = cursor.fetchone()

        print((user_id, date, session_id))
        print('<br>')

        #case: user session has expired
        if date + datetime.timedelta(minutes=30) < datetime.datetime.utcnow():
            req_response['description'] = "user session expired"
            req_response['status'] = 440
            #delete current user session since it expired
            cursor.execute("DELETE FROM user_session WHERE session_id = %s ", (session_id, ))
            return req_response
        #update our date in cookie / request
        curdate = datetime.datetime.utcnow()
        auth_cookie['expires'] = curdate.strftime("%a, %d %b %Y %H:%M:%S UTC")
        #set our new cookie for the browser
        print(auth_cookie)
        cursor.execute("UPDATE user_session SET date =%s WHERE session_id = %s", (curdate, session_id))
        req_response['status'] = 200
        req_response['description'] = "successfully authenticated!"
        return req_response

    except Exception as err:
        print(err)
        return req_response

f = open('userconfig.json')
config = json.load(f)
connection = mysql.connector.connect(**config, auth_plugin='mysql_native_password', charset='utf8')
print(handleRequestCookie(connection))
connection.commit();
