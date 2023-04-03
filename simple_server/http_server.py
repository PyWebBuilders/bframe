from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote

from simple_server.logger import __logger as logger

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
        
        if args_str == "":
            return path, args
        for kv_item in args_str.split("&"):
            item = kv_item.split("=")
            args.update({unquote(item[0]): unquote(item[1])})
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

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, application=None):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        self.application = application

    def set_app(self, application):
        self.application = application


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
            logger.info(req.Method, req.Path)
            res = self.server.application(req)
        except Exception as e:
            logger.info(e.args)
            res = Response(code=500,
                           body=e.args[0])

        self.__send_response(res)

    def write(self, content):
        if isinstance(content, bytes):
            self.wfile.write(content)
        elif isinstance(content, str):
            self.wfile.write(content.encode())
        else:
            self.wfile.write(str(content).encode())

    def __send_response(self, r: Response):
        self.send_response_only(r.Code)
        self.send_header('Server', self.version_string())
        self.send_header('Date', self.date_time_string())
        for head, val in r.Headers.items():
            self.send_header(head, val)

        if r.Body:
            self.send_header("Content-Length", len(r.Body))
        self.end_headers()
        self.write(r.Body)
