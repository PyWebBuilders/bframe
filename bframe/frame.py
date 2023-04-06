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
import json
from typing import Any, Callable, Union

from bframe._frame import _Frame
from bframe.ctx import RequestCtx
from bframe.server import Request, Response
from bframe.route import NoSetControllerException
from bframe.utils import get_code_desc, parse_execept_code, to_bytes

MethodSenquenceAlias = Union[tuple, list]


class Frame(_Frame):

    before_funs_list = list()
    after_funs_list = list()
    error_funs_dict = dict()

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

    def add_before_handle(self, f):
        self.before_funs_list.append(f)
        return f

    def add_after_handle(self, f):
        self.after_funs_list.append(f)
        return f

    def add_error_handle(self, code):
        def wrapper(f):
            self.error_funs_dict[code] = f
            return f
        return wrapper

    def before_handle(self):
        self.Logger.info("before_handle")
        for handle in self.before_funs_list:
            rv = handle()
            if rv:
                return rv

    def dispatch_handle(self, request: Request):
        handle = self.match_handle(request)
        return self.wrapper_response(handle())

    def error_handle(self, e):
        self.Logger.info("error_handle")
        code = parse_execept_code(e)
        if code in self.error_funs_dict:
            response = self.wrapper_response(self.error_funs_dict[code]())
        else:
            response = Response(code, body=get_code_desc(code))
        return response

    def finally_handle(self, response: Response):
        self.Logger.info("finally_handle")
        for handle in self.after_funs_list:
            response = handle(response)
        return response

    def dispatch(self, r: Request):
        # self.Logger.info("thread:", threading.enumerate())
        ctx = RequestCtx(r)
        with ctx:
            ctx.push()
            try:
                response = self.before_handle()
                if response is None:
                    response = self.dispatch_handle(r)
                response = self.wrapper_response(response)
            except NoSetControllerException as e:
                self.Logger.debug(e.args)
                response = Response(code=404)
            except Exception as e:
                self.Logger.debug(e.args)
                response = self.error_handle(e)
            finally:
                response = self.finally_handle(response)
                return response
