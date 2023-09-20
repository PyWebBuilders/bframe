import functools
import os

from bframe import (Frame, MethodView, Redirect, abort, current_app, g,
                    make_response, request, session)
from bframe.server import Response
from bframe.generics import ViewSet

app = Frame(__name__)
# app.Config.from_py("config.py")


@app.get("/favicon.ico")
def index():
    with open("favicon.ico", "rb") as f:
        data = f.read()
    return data


@app.get("/main")
@app.get("/home")
def home():
    print(g.name)
    headers = request.Headers
    headers.update({
        "g_name": g.name,
        "g_url": g.url,
    })
    return headers


@app.route("/api/v1/<int:pk>", method=["GET", "POST"])
def index(pk):
    # print(current_app.Config)
    url = request.Args.get("url")
    if url:
        return Redirect(url)
    return request.Method


@app.route("/index2", method=["GET", "POST"])
@app.route("/index", method=["GET", "POST"])
def index():
    print(request.Method)
    print(request.args)
    print(request.forms)
    print(request.files)
    for name, fileObj in request.files.items():
        print(name)
        path = os.path.join(os.getcwd(), fileObj.filename)
        fileObj.save(path)
    # abort(401)
    # raise
    return "hello world"


# 定义请求钩子
@app.add_before_handle
def before_01():
    name = request.Args.get("name")
    g.name = name
    g.url = request.Path
    # print("req:", request.Method)


# 定义请求钩子
# @app.add_before_handle
# def before_02():
#     if request.Method == "POST":
#         return "disallow method"


# 定义响应钩子
@app.add_after_handle
def after_xx(resp: Response):
    # print("resp:", resp.Code)
    return resp


# 自定义错误响应
@app.add_error_handle(401)
def err_401():
    return "401 error"


@app.route("/indexClass")
class Index:

    def get(self):
        return {"msg": "get, 你好 %s" % (request.Args.get("name", "client"))}

    def post(self):
        return "post"

    def put(self):
        return "put"

    def delete(self):
        return "delete"


class Detail(MethodView):

    def get(self):
        ret = make_response("get detail")
        import time
        print("get session value: ", session["name"])
        session["name"] = f"tom-{str(time.time())}"
        ret.set_cookies("age", "12", path="/detail")
        ret.set_cookies("gender", "nan")
        return ret

    def post(self):
        return "post detail"

    def put(self):
        return "put detail"

    def delete(self):
        return "delete detail"


books = [{
    "id": 1,
    "name": "海底两万里",
    'content': "我是海底两万里"
}, {
    "id": 2,
    "name": "十万个为什么",
    "content": "十万个为什么",
}]


@app.get("/login")
def login():
    username = request.args.get("username")
    if username:
        session["userid"] = username
        return "login successful"
    return "login failed"


@app.get("/logout")
def logout():
    userid = session["userid"]
    if not userid:
        return "logou failed"
    session.clear()
    return "logout successful"


def login_required(f):
    @functools.wraps(f)
    def wrapper(*args, **kwds):
        userid = session["userid"]
        if not userid:
            return "no login"
        return f(*args, **kwds)
    return wrapper


class BookView(MethodView):

    @login_required
    def get(self):
        return books

    @login_required
    def post(self):
        global books
        req = request.forms
        req['id'] = len(books) + 1
        books.append(req)
        return req


class PhoneViewSet(ViewSet):
    pass

   # def list(self):
   #     return "list"

   # def create(self):
   #     return "create"

   # def retrieve(self, pk=None):
   #     return f"retrieve {pk}"

   # def update(self, pk=None):
   #     return f"update {pk}"

   # def partial_update(self, pk=None):
   #     return f"partial_update {pk}"

   # def destroy(self, pk=None):
   #     return f"destroy {pk}"


app.add_route("/detail", Detail.as_view())
app.add_route("/book", BookView.as_view())
app.add_route("/phone", PhoneViewSet.as_view({
    "get": "list",
    "post": "create",
}))
app.add_route("/phone/<int:pk>", PhoneViewSet.as_view({
    "get": "retrieve",
    "post": "update",
    "put": "partial_update",
    "delete": "destroy",
}))


if __name__ == "__main__":
    app.run(address="0.0.0.0")

    # 如果你需要使用wsgi协议,请使用wsgi_proxy对app进行处理
    # from bframe import WSGIProxy
    # from wsgiref.simple_server import make_server
    # with make_server('', 7256, WSGIProxy(app)) as httpd:
    #     print("Serving on port 7256...")
    #     httpd.serve_forever()
