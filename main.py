from simple_server.server import start, stop, route
from simple_server.http_server import Request


@route("/index", method=["GET", "POST"])
def index(request: Request):
    return "hello world"


if __name__ == "__main__":
    try:
        start()
    except KeyboardInterrupt:
        stop()
