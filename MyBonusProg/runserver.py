from server.conf import *
from server import app

if __name__ == '__main__':
    HOST = MYBONUSPROG_IP
    PORT = MYBONUSPROG_PORT

    app.run(HOST, PORT, debug=True, threaded=True) 

