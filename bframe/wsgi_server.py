import email
import time
from http import HTTPStatus
import typing
from bframe.http_server import Request, Response
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
        r = Request(
            method=environ.get("REQUEST_METHOD"),
            path="%s?%s" % (environ.get("PATH_INFO"),
                            environ.get("QUERY_STRING")),
            protoc=environ.get("SERVER_PROTOCOL"),
            headers=headers,
        )
        setattr(r, "environ", environ)

        response: Response = self.application(r)
        start_response(self.response_status(response.Code),
                       self.response_headers(response.Headers))

        return [response.Body]

    def __call__(self, environ: dict, start_response: typing.Callable) -> typing.Any:
        return self.wsgi_app(environ, start_response)
