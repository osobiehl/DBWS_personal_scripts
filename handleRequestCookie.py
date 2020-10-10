import os
import http.cookies as Cookie
def handleRequestCookie():
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
            req_response['description'] = "invalid cookie name"
            return req_response

    
    except Exception as err:
        print("Content-Type: text/html;charset=utf-8\n\n")
        print(err);
