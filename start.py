from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from common import my_bonus_prog, conf

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    my_bonus_prog_server = my_bonus_prog.MyBonusProg()
    server = ThreadedHTTPServer((conf.MYBONUSPROG_IP, conf.MYBONUSPROG_PORT), my_bonus_prog.MyBonusProgHandler)
    print('starting MyBonusProg server '+str(conf.MYBONUSPROG_IP)+':'+str(conf.MYBONUSPROG_PORT)+' (use <Ctrl-C> to stop)')
    server.serve_forever()

