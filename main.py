import os

from bframe import Frame, Redirect, abort, g, request
from bframe.server import Response


app = Frame(__name__)


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


@app.route("/", method=["GET", "POST"])
def index():
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
    print("req:", request.Method)


# 定义请求钩子
# @app.add_before_handle
# def before_02():
#     if request.Method == "POST":
#         return "disallow method"


# 定义响应钩子
@app.add_after_handle
def after_xx(resp: Response):
    print("resp:", resp.Code)
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


if __name__ == "__main__":
    app.run(address="0.0.0.0")

    # 如果你需要使用wsgi协议,请使用wsgi_proxy对app进行处理
    # from bframe import WSGIProxy
    # from wsgiref.simple_server import make_server
    # with make_server('', 7256, WSGIProxy(app)) as httpd:
    #     print("Serving on port 7256...")
    #     httpd.serve_forever()
