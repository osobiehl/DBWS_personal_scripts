import json
import mysql.connector
from mysql.connector import errorcode
import cgitb
import sys
import random
import bcrypt
import datetime
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

cursor = connection.cursor();
clubs = open('CLUB_NAMES')
lines = clubs.readlines()

for line in lines:
    club_info = line.split(' ', 1)
    cursor.execute("INSERT INTO club (name, description) VALUES (%s, %s)", (club_info[0], club_info[1]))
connection.commit()

for i in range(0, 16):
    for d in range(1, 5):
        try:
            cursor.execute("INSERT INTO subscription (user_id, club_id) VALUES (%s, %s)", (i, random.randint(0,7)))
        except Exception:
            continue

for i in range(1, 18):
    try:
        cursor.execute(
            "SELECT u.name, c.name, s.club_id from subscription s "
            "INNER JOIN club c on s.user_id = %s AND c.club_id = s.club_id "
            "INNER JOIN user u ON u.user_id = s.user_id",
            (i, ))
        res = cursor.fetchall()

        for (user_name, club_name, club_id) in res:
            cursor.execute("INSERT INTO post (user_id, club_id, date, likes, title, content) VALUES (%s, %s, %s, %s, %s, %s)",
                           (
                               i,
                               club_id,
                               datetime.datetime.utcnow() - datetime.timedelta(hours=random.randint(1,6), minutes=random.randint(0,60)),
                               random.randint(0,17),
                               "USER: "+user_name+", title!",
                               "This is "+club_name+" this is my content, in club: "+club_name)

                           )
    except Exception as err:
        print(err)
        print(err.__doc__)
        continue

        #user id: 5, club id: 3Error Code: 1055. Error Code: 1305. FUNCTION dbws.DATEADD does not exist



for i in range(1, 18):
    try:
        cursor.execute(
            '''SELECT u.name, c.name, p.post_id from subscription s
            INNER JOIN club c on s.user_id = %s AND c.club_id = s.club_id 
            INNER JOIN user u ON u.user_id = s.user_id 
            INNER JOIN post p on p.club_id = s.club_id ''',
            (i, ))
        res = cursor.fetchall()

        for (user_name, club_name, post_id) in res:
            cursor.execute("INSERT INTO comments (user_id, post_id, date, likes,  content) VALUES (%s, %s, %s, %s, %s)",
                           (
                               i,
                               post_id,
                               datetime.datetime.utcnow() - datetime.timedelta(hours=random.randint(1,2), minutes=random.randint(0,60)),
                               random.randint(0,17),
                               "hello! I am "+user_name+", commenting on this post from club:" + club_name)

                           )
    except Exception as err:
        print(err)
        print(err.__doc__)
        continue

        #user id: 5, club id: 3Error Code: 1055. Error Code: 1305. FUNCTION dbws.DATEADD does not exist


connection.commit()