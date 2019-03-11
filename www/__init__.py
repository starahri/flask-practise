from flask import Flask


print(type(__name__))


"""
每一个 Web 应用都是一个可调用对象
在 Flask 中，这个可调用对象就是 app
"""

app=Flask(__name__,instance_relative_config=True)


@app.route("/")
def hello():
    return "Hello World!"

if __name__=="__main__":
    app.run(port=6001)