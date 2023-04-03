from simple_server.frame import Frame
from simple_server.http_server import Request

app = Frame(__name__)


@app.get("/favicon.ico")
def index(request: Request):
    with open("favicon.ico", "rb") as f:
        data = f.read()
    return data


@app.get("/main")
@app.get("/home")
def home(request: Request):
    return request.Headers


@app.route("/", method=["GET", "POST"])
def index(request: Request):
    return "index"


@app.route("/index2", method=["GET", "POST"])
@app.route("/index", method=["GET", "POST"])
def index(request: Request):
    return "hello world"


@app.route("/indexClass")
class Index:

    def get(self, request: Request):
        return {"msg": "get, 你好 %s" % (request.Args.get("name", "client"))}

    def post(self, request):
        return "post"

    def put(self, request):
        return "put"

    def delete(self, request):
        return "delete"


if __name__ == "__main__":
    app.run(address="0.0.0.0")
