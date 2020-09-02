from flask import Flask
from flask import session, request
from flask import abort

"""
每一个 Web 应用都是一个可调用对象
在 Flask 中，这个可调用对象就是 app
"""

app = Flask(__name__)
app.secret_key = "dev"
# To make ipdb more easy
app.debug = False


@app.route("/")
def hello():
    if "username" in session:
        session["session_id"] = 123
        return f"Hello  {session['username']} \n"

    # Test `abort` logic
    import ipdb;ipdb.set_trace()
    abort(404)
    return "Hello World!\n"


@app.route("/response")
def resp():
    return "RESPONSE SUCCESS!", 201, {"X-Foo": "BAR"}
    # return None  # Type Error


"""
http -v -f --session=mysession POST http://127.0.0.1:5000/login username=Ahri
-v 打印请求 
-f 请求为表单数据
-session  将返回的 cookie 保存在变量中，后面可以通过变量来指定 session

zhanghuadeMacBook-Pro:PycharmProjects zhanghua$ http -v -f --session=mysession POST 127.0.0.1:6001/login username=Ahri
POST /login HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 13
Content-Type: application/x-www-form-urlencoded; charset=utf-8
Cookie: session=eyJ1c2VybmFtZSI6Ilx1Njc5N1x1NTk5OVx1NTNlZiJ9.XIn01g.ELyVbL7OaVVaZJI_gs48wf9tAqA
Host: 127.0.0.1:6001
User-Agent: HTTPie/1.0.2

username=Ahri

HTTP/1.0 200 OK
Content-Length: 14
Content-Type: text/html; charset=utf-8
Date: Thu, 14 Mar 2019 06:31:03 GMT
Server: Werkzeug/0.14.1 Python/3.6.8
Set-Cookie: session=eyJ1c2VybmFtZSI6IkFocmkifQ.XIn1Jw.g1fYoD7agMZTDAaSeujUJU63S0c; HttpOnly; Path=/
Vary: Cookie

Login Success

Cookie 的是保存的 key-value 

"""


@app.route("/login", methods=["POST"])
def login():
    session["username"] = request.form["username"]
    return "Login Success\n"


if __name__ == "__main__":
    app.run(port=5001)
