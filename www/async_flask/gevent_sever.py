
from flask import Flask

from gevent.pywsgi import WSGIServer

from gevent import monkey
# from _thread import get_ident
from greenlet import getcurrent as get_ident
import time


monkey.patch_all()
app=Flask(__name__)

@app.route("/")
def hello_world():
    print(get_ident())
    time.sleep(10)
    return "hello world"

@app.route("/index")
def hello():
    print(get_ident())
    return "hello"

if __name__=="__main__":
    http_server=WSGIServer(("127.0.0.1",6005),app)
    http_server.serve_forever()