"""
MIT License

Copyright (c) 2023 Bean-jun

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from http.server import BaseHTTPRequestHandler, HTTPServer

from bframe.logger import init_logger
from bframe.wrappers import Cookie, Request, Response

logger = init_logger()


HTTP_METHOD = ["HEAD", "GET", "POST", "PUT", "DELETE"]


class SimpleHTTPServer(HTTPServer):

    def __init__(self,
                 server_address,
                 RequestHandlerClass,   # noqa
                 bind_and_activate=True,
                 application=None):
        super().__init__(server_address,
                         RequestHandlerClass,
                         bind_and_activate)
        self.application = application

    def set_app(self, application):
        self.application = application


class HTTPHandleMix:

    def do_HEAD(self):
        self.do_handle()

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
        # TODO:解析请求体
        req = Request(self.command,
                      self.path,
                      self.protocol_version,
                      dict(self.headers))
        if req.method != "GET":
            length = req.Headers.get("Content-Length") or 0
            req.parse_body(self.rfile.read(int(length)))
        try:
            res = self.server.application(req)
        except Exception as e:   # noqa
            logger.warn("[do handle error]", e.args)
            res = Response(code=500,
                           body="Internal Server Error")

        self.__send_response(res)

    def write(self, content):
        if isinstance(content, bytes):
            self.wfile.write(content)
        elif isinstance(content, str):
            self.wfile.write(content.encode())
        else:
            self.wfile.write(str(content).encode())

    def send_cookies(self, m: Cookie):
        for cookie in m.output():
            self.send_header("Set-Cookie", cookie)

    def __send_response(self, r: Response):
        self.send_response_only(r.Code)
        self.send_header('Server', self.server.application.version)
        self.send_header('Date', self.date_time_string())
        for head, val in r.Headers.items():
            self.send_header(head, val)

        self.send_cookies(r.Cookies)

        if r.Body:
            self.send_header("Content-Length", len(r.Body))
        self.end_headers()
        self.write(r.Body)
