#!/usr/bin/env python3
import os
import http.cookies as Cookie
import datetime
import mysql.connector
import json
from base64 import b64encode
from base64 import b64decode
import sys
import cgitb
import imghdr
from email import message
from email.mime import multipart
from email.mime import nonmultipart
from email.mime import text

cgitb.enable()
print("Content-Type: text/html;charset=utf-8\n\n")
a = sys.stdin.read()
req_content = json.loads(a)
img_b64 = req_content['image']
img = b64decode(img_b64)
req_content['image'] = None
print (req_content)

f = open('test.jpeg', 'wb+')
f.write(img)

f.close()

