from bframe import request
from bframe import Frame

app = Frame(__name__)


@app.get("/favicon.ico")
def index():
    with open("favicon.ico", "rb") as f:
        data = f.read()
    return data


@app.get("/main")
@app.get("/home")
def home():
    return request.Headers


@app.route("/", method=["GET", "POST"])
def index():
    return request.Method


@app.route("/index2", method=["GET", "POST"])
@app.route("/index", method=["GET", "POST"])
def index():
    print(request.Method)
    return "hello world"


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
