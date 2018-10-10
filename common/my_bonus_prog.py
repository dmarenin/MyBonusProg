from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
#import _thread

from common import api_func, path_list

class MyBonusProgException(Exception):
    pass

class MyBonusProgHandler(BaseHTTPRequestHandler):
    callback = None

    def smart_response(self, code, message, headers = []):
        self.send_response(code)
        for h, v in headers:
            self.send_header(h, v)

        self.send_header("Content-type", "text/plain; charset=utf-8")

        self.end_headers()
        if (code != 200):
            print(message)
            message = message

        return self.wfile.write(message.encode())

    def do_GET(self):
        path = urlparse(self.path).path
        qs = urlparse(self.path).query
        qs = parse_qs(qs)
        
        res = self.callback(path, qs, self)

class MyBonusProg():
    server = None
    handler = MyBonusProgHandler

    pathmap = {}
    
    def __init__(self, caller = None):
        self.init_pathmap()
        self.handler.callback = self.callback
        #_thread.start_new_thread(self.upd_loop, ())

    def register(self, method, path, function):
        self.pathmap[path] = function       
    def callback(self, path, qs, handler):
        while path and path[0] == '/':

            func = self.pathmap.get(path)
            if func is None:
                return handler.smart_response(404, "Не найден метод: "+str(path))

            try:
                res = func(qs)
            except KeyError as e:
                return handler.smart_response(500, "Не задано значение параметра: %s" % e)
            except ValueError as e:
                return handler.smart_response(500, "Ошибка в значении параметра: %s" % e)
            except MyBonusProgException as e:
                return handler.smart_response(500, "%s" % e)
            except Exception as e:
                return handler.smart_response(500, "Неожиданная ошибка: %s" % e)

            if not res:
                res = []

            res = json.dumps(res, default=common.json_serial)
            content_type = "application/json"

            try:
                handler.smart_response(200, res, [
                    ("Content-type", content_type),
                    ("Access-Control-Allow-Origin", "*"),
                    ("Access-Control-Expose-Headers", "Access-Control-Allow-Origin"),
                    ("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept"),
                ])
            except socket.error as e:
                pass

            return
        else:
            handler.smart_response(401, "Unauthorized call: %s from %s" % (path, client_address))
  
    def init_pathmap(self):
        for x in path_list.get():
            self.register(x['method'], x['func'], x['handler'])

