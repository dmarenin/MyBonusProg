from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from common import my_bonus_prog

MYBONUSPROG_IP = '0.0.0.0' 
MYBONUSPROG_PORT = 13000

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    my_bonus_prog_server = my_bonus_prog.MyBonusProg()
    server = ThreadedHTTPServer((MYBONUSPROG_IP, MYBONUSPROG_PORT), my_bonus_prog.MyBonusProgHandler)
    print('starting MyBonusProg server '+str(MYBONUSPROG_IP)+':'+str(MYBONUSPROG_PORT)+' (use <Ctrl-C> to stop)')
    server.serve_forever()

