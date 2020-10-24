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
# TODO add error handling on input JSON



cgitb.enable()
print("Content-Type: text/html;charset=utf-8\n\n")
a = sys.stdin.read()
req_content = json.loads(a)

if 'title' and 'content' and 'image-type' and 'image' not in req_content:
    print("invalid! ")

img_b64 = req_content['image']
img = b64decode(img_b64)
req_content['image'] = None
options = {
    "image/gif": "gif",
    "image/jpeg": "jpeg",
    "image/png": "png"
}
if req_content['image-type'] not in options:
    print("type not supported!")
print(req_content)
# make proper file w/ proper format
f = open('test.' + options[req_content['image-type']], 'wb+')
f.write(img)

f.close()

