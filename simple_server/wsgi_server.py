import email
import time
from http import HTTPStatus

from simple_server.http_server import Request, Response
from simple_server.logger import __logger as logger

logger.module = __name__


def wsgi_proxy(app):
    def response_status(code):
        responses = {
            v: (v.phrase, v.description)
            for v in HTTPStatus.__members__.values()
        }
        if code in responses:
            return "%s %s" % (code, responses[code][0])

    def response_headers(headers):
        headers['Server'] = "simple server"
        headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)
        ret = [(k, v) for k, v in headers.items()]
        return ret

    def wsgi(environ, start_response):
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

        response: Response = app(r)
        start_response(response_status(response.Code),
                       response_headers(response.Headers))

        return [response.Body]

    return wsgi
