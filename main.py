from simple_server.server import start, stop, route
from simple_server.http_server import Request


@route("/index", method=["GET", "POST"])
def index(request: Request):
    return "hello world"


@route("/indexClass")
class Index:

    def get(self, request: Request):
        return "get, hello %s" % (request.Args.get("name", "client"))

    def post(self, request):
        return "post"

    def put(self, request):
        return "put"

    def delete(self, request):
        return "delete"


if __name__ == "__main__":
    try:
        start()
    except KeyboardInterrupt:
        stop()
