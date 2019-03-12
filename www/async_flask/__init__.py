
from flask import Flask
import time
from  _thread import get_ident

app=Flask(__name__)

@app.route("/")
def hello_world():
    time.sleep(20)
    return "hello world!"+str(get_ident())

@app.route("/index")
def hello():
    time.sleep(1)
    return "Hello"+str(get_ident())

if __name__=="__main__":
    app.run(port=6003)