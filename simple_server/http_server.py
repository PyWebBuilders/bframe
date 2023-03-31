from http.server import BaseHTTPRequestHandler, HTTPServer

from simple_server.logger import __logger as logger

logger.module = __name__


class Request:

    Method: str = ""
    Path: str = ""
    Protoc: str = ""
    Headers: str = {}

    def __init__(self, method: str = "", path: str = "", protoc: str = "", headers: dict = ""):
        self.Method = method
        self.Path = path
        self.Protoc = protoc
        self.Headers = headers


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
        # 0x2 match handle
        # 0x3 execute handle
        # 0x4 solve except
        # 0x5 set response
        res = Response(body=">>>>?????<<<<<")
        logger.info(str(self))
        self.__send_response(res)

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
