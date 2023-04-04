import json
from typing import Any, Callable, Union

from bframe._frame import _Frame
from bframe.ctx import request
from bframe.http_server import Request, Response
from bframe.route import NoSetControllerException
from bframe.utils import to_bytes

MethodSenquenceAlias = Union[tuple, list]


class Frame(_Frame):

    def match_handle(self, request: Request) -> Callable:
        url = "%s/%s" % (request.Path, request.Method)
        return self.RouteMap.find(url)

    def wrapper_response(self, resp: Any) -> Response:
        self.Logger.info("wrapper_response:", str(resp)[:20])
        if isinstance(resp, Response):
            resp.Body = to_bytes(resp.Body)
            return resp
        if isinstance(resp, (str, bytes)):
            return Response(code=200,
                            body=to_bytes(resp))
        if isinstance(resp, dict):
            return Response(code=200,
                            headers={"Content-Type": "application/json"},
                            body=to_bytes(json.dumps(resp)))

    def before_handle(self, request: Request):
        self.Logger.info("before_handle")

    def dispatch_handle(self, request: Request):
        handle = self.match_handle(request)
        return self.wrapper_response(handle())

    def error_handle(self, e):
        self.Logger.info("error_handle")

    def finally_handle(self, response: Response):
        self.Logger.info("finally_handle")
        return response

    def dispatch(self, r: Request):
        # self.Logger.info("thread:", threading.enumerate())
        with request:
            request.push(r)
            try:
                response = self.before_handle(r)
                if response is None:
                    response = self.dispatch_handle(r)
            except NoSetControllerException as e:
                self.Logger.debug(e.args)
                response = Response(code=404)
            except Exception as e:
                self.Logger.debug(e.args)
                # response = self.error_handle(e)
            finally:
                response = self.finally_handle(response)
                return response
