from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Callable
from simple_server.logger import __logger as logger
from simple_server.route import NoSetControllerException, ReqRepeatException

logger.module = __name__

HTTP_METHOD = ["GET", "POST", "PUT", "DELETE"]


class Request:

    Method: str = ""
    Path: str = ""
    Args: dict = {}
    Protoc: str = ""
    Headers: str = {}

    def __init__(self, method: str = "", path: str = "", protoc: str = "", headers: dict = ""):
        self.Method = method
        if "?" in path:
            self.Path, self.Args = self.initializa_path(path)
        else:
            self.Path = path
        self.Protoc = protoc
        self.Headers = headers

    def initializa_path(self, path):
        path, args_str = path.split("?")
        args = dict()
        for kv_item in args_str.split("&"):
            item = kv_item.split("=")
            args.update({item[0]: item[1]})
        return path, args


class Response:

    Code: int = 200
    Headers: dict = {}
    Body: str = ""

    def __init__(self, code: int = 200, headers: dict = dict(), body: str = "") -> None:
        self.Code = code
        self.Headers = headers
        self.Body = body


class SimpleHTTPServer(HTTPServer):
    pass


class HTTPHandleMix:

    def do_GET(self):
        self.do_handle()

    def do_POST(self):
        self.do_handle()

    def do_PUT(self):
        self.do_handle()

    def do_DELETE(self):
        self.do_handle()


class SimpleRequestHandler(HTTPHandleMix, BaseHTTPRequestHandler):

    def do_handle(self):
        # 0x1 package request
        req = Request(self.command,
                      self.path,
                      self.protocol_version,
                      dict(self.headers))
        try:
            ret = self.dispatch(req)
        except Exception as e:
            # 0x5 set response
            res = Response(body=e.args[0])
        else:
            # 0x5 set response
            res = Response(body=ret)

        logger.info(str(self))
        self.__send_response(res)

    def dispatch(self, request: Request):
        try:
            # 0x2 match handle
            handle = self.match_handle(request)
            # 0x3 execute handle
            ret = handle(request)
            # 0x4 solve except
        except (ReqRepeatException, NoSetControllerException) as e:
            logger.debug(e.args)
            raise Exception("match handle error", e.args[0])
        except Exception as e:
            logger.debug(e.args)
            raise Exception("execute handle error", e.args[0])
        return ret

    def match_handle(self, request: Request) -> Callable:
        from simple_server.server import get_route_map
        url = "%s/%s" % (request.Path, request.Method)
        return get_route_map().find(url)

    def __send_response(self, r: Response):
        self.send_response_only(r.Code)
        self.send_header('Server', self.version_string())
        self.send_header('Date', self.date_time_string())
        for head, val in r.Headers:
            self.send_header(head, val)

        if r.Body:
            self.send_header("Content-Length", len(r.Body))
        self.end_headers()
        self.wfile.write(r.Body.encode())
