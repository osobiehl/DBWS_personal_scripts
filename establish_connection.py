def StartConnection():
    import json
    import mysql.connector
    from mysql.connector import errorcode
    f = open('userconfig.json')
    config = json.load(f)
    try:
        connection = mysql.connector.connect(**config, auth_plugin='mysql_native_password')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print(err)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(err)
        else:
            print(err)
        return None
    return connection
