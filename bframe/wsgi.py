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
from bframe.logger import __logger as logger

logger.module = __name__


class WSGIProxy:

    def __init__(self, application):
        self.application = application

    def response_status(self, code):
        responses = {
            v: (v.phrase, v.description)
            for v in HTTPStatus.__members__.values()
        }
        if code in responses:
            return "%s %s" % (code, responses[code][0])

    def response_headers(self, headers):
        headers['Server'] = self.application.version
        headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)
        ret = [(k, v) for k, v in headers.items()]
        return ret

    def wsgi_app(self, environ: dict, start_response: typing.Callable) -> typing.Any:
        logger.info("run mode: wsgi")
        headers = {k[len("HTTP_"):].lower(): v for k,
                   v in environ.items() if k.startswith("HTTP")}
        headers.update({
            "content-type": environ["CONTENT_TYPE"],
            "content-length": environ["CONTENT_LENGTH"],
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
            length = req.Headers.get("content-length") or 0
            req._BaseRequest__parse_body(environ["wsgi.input"].read(int(length)))
        setattr(req, "environ", environ)

        response: Response = self.application(req)
        start_response(self.response_status(response.Code),
                       self.response_headers(response.Headers))

        return [response.Body]

    def __call__(self, environ: dict, start_response: typing.Callable) -> typing.Any:
        return self.wsgi_app(environ, start_response)
