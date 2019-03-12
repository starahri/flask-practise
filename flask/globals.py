# -*- coding: utf-8 -*-
"""
    flask.globals
    ~~~~~~~~~~~~~

    Defines all the global objects that are proxies to the current
    active context.

    定义全局对象，这些全局对象是现在活动上下文的代理。

    :copyright: © 2010 by the Pallets team.
    :license: BSD, see LICENSE for more details.
"""
"""
每一段程序都有很多外部变量。只有像Add这种简单的函数才是没有外部变量的。
一旦你的一段程序有了外部变量，这段程序就不完整，不能独立运行。
你为了使他们运行，就要给所有的外部变量一个一个写一些值进去。这些值的集合就叫上下文。

比如在 flask 中，视图函数需要知道它执行情况的请求信息，以及应用信息（应用中初始化的数据库等），才能够正确运行


最直观地做法是把这些信息封装成一个对象，作为参数传递给视图函数。
但是这样的话，所有的视图函数都需要添加对应的参数，即使该函数内部并没有使用到它
比如我只返回一个 "Hello World"。

flask 的做法是把这些信息作为类似全局变量的东西，视图函数需要的时候，可以使用 from flask import request 获取。
但是这些对象和全局变量不同的是——它们必须是动态的，因为在多线程或者多协程的情况下，
每个线程或者协程获取的都是自己独特的对象，不会互相干扰

多线程中有个非常类似的概念 threading.local，可以实现多线程访问某个变量的时候只看到自己的数据。
内部的原理说起来也很简单，这个对象有一个字典，保存了线程 id 对应的数据，读取该对象的时候，它动态地查询当前线程 id 对应的数据。
flaskpython 上下文的实现也类似。

"""

from functools import partial
from werkzeug.local import LocalStack, LocalProxy


_request_ctx_err_msg = '''\
Working outside of request context.

This typically means that you attempted to use functionality that needed
an active HTTP request.  Consult the documentation on testing for
information about how to avoid this problem.\
'''
_app_ctx_err_msg = '''\
Working outside of application context.

This typically means that you attempted to use functionality that needed
to interface with the current application object in some way. To solve
this, set up an application context with app.app_context().  See the
documentation for more information.\
'''

"""
返回 _request_ctx_stack 的栈顶的 ele.name 属性
"""

def _lookup_req_object(name):
    top = _request_ctx_stack.top
    if top is None:
        raise RuntimeError(_request_ctx_err_msg)
    return getattr(top, name)


"""
返回 _app_ctx_stack 的栈顶 ele.name 属性
"""
def _lookup_app_object(name):
    top = _app_ctx_stack.top
    if top is None:
        raise RuntimeError(_app_ctx_err_msg)
    return getattr(top, name)


"""
返回 _app_ctx_stack 的栈顶 ele.app 
"""

def _find_app():
    top = _app_ctx_stack.top
    if top is None:
        raise RuntimeError(_app_ctx_err_msg)
    return top.app

"""
flask 有两种上下文：application context 和 request context。
application context -> current_app 和 g
request context -> request 和 session

context 都是 LocalStack 栈结构
current_app /g /request /session 都是 LocalProxy

LocalStack 和 LocalProxy 可以让我们动态的获取两个上下文的内容，在并发程序中每个视图函数都只看到自己的上下文
LocalStack 和 LocalProxy 是由 werkzeug 提供

"""
# context locals
_request_ctx_stack = LocalStack()
_app_ctx_stack = LocalStack()

"""

partial 会实现函数的参数绑定，并且返回的依然是个function
_lookup_req_object("request") 那么返回的是一个已经处理的结果
不然必须传入两个参数进去 _lookup_req_object ,"request"

"""
current_app = LocalProxy(_find_app)
request = LocalProxy(partial(_lookup_req_object, 'request'))
session = LocalProxy(partial(_lookup_req_object, 'session'))
g = LocalProxy(partial(_lookup_app_object, 'g'))
