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
import email
import time
from http import HTTPStatus
import typing
from bframe.server import Request, Response
from bframe.logger import init_logger

logger = init_logger()


class WSGIProxy:

    def __init__(self, application):
        logger.info("run mode: wsgi")
        self.application = application

    def response_status(self, code):
        responses = {
            v: (v.phrase, v.description)
            for v in HTTPStatus.__members__.values()
        }
        if code in responses:
            return "%s %s" % (code, responses[code][0])

    def response_cookies(self, response: Response):
        ret = []
        for cookie in response.Cookies.output():
            ret.append(("Set-Cookie", cookie))
        return ret

    def response_headers(self, response: Response):
        response.Headers['Server'] = self.application.version
        response.Headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)
        ret = [(k, v) for k, v in response.Headers.items()]
        ret.extend(self.response_cookies(response))
        return ret

    def wsgi_app(self,
                 environ: dict,
                 start_response: typing.Callable) -> typing.Any:
        headers = {k[len("HTTP_"):].lower(): v for k,
                   v in environ.items() if k.startswith("HTTP")}
        headers.update({
            "Content-Length": environ.get("CONTENT_LENGTH", 0),
            "Content-Type": environ.get("CONTENT_TYPE"),
        })
        req = Request(
            method=environ.get("REQUEST_METHOD"),
            path="%s?%s" % (environ.get("PATH_INFO"),
                            environ.get("QUERY_STRING")),
            protoc=environ.get("SERVER_PROTOCOL"),
            headers=headers,
        )
        # TODO:解析请求体
        # input = environ["wsgi.input"]
        # d = x.read(int(environ["CONTENT_LENGTH"]))
        if req.method != "GET":
            length = req.Headers.get("Content-Length") or 0
            req.parse_body(environ["wsgi.input"].read(int(length)))   # noqa
        setattr(req, "environ", environ)

        response: Response = self.application(req)
        start_response(self.response_status(response.Code),
                       self.response_headers(response))

        return [response.Body]

    def __call__(self, environ: dict, start_response: typing.Callable) -> typing.Any:   # noqa
        return self.wsgi_app(environ, start_response)
