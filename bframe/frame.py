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
import os
from typing import Any, Callable

from bframe.scaffold import Scaffold
from bframe.ctx import RequestCtx
from bframe.ctx import request as req
from bframe.server import Request, Response
from bframe._except import NoSetControllerException
from bframe.utils import get_code_desc
from bframe.utils import parse_except_code
from bframe.utils import to_bytes
from bframe.utils import abort
from bframe.sessions import SessionMix
from bframe.sessions import MemorySession


class Frame(Scaffold):

    before_funs_list = list()
    after_funs_list = list()
    error_funs_dict = dict()

    # 会话消息
    Session: SessionMix = MemorySession()

    # 序列化
    Serializer = json

    def static(self, *args, **kwds):
        file_path = req.path.lstrip("/")[len(self.static_url):].lstrip("/")
        file_full_path = os.path.join(self.static_folder, file_path)
        if not (os.path.exists(file_full_path) and os.path.isfile(file_full_path)):
            return abort(404)
        try:
            with open(file_full_path, "rb") as f:
                return f.read()
        except Exception as e:
            return abort(500)

    def match_handle(self) -> Callable:
        url = "%s%s" % (req.Method, req.Path)
        return self.RouteMap.find(req.set_path_args, url)

    def wrapper_response(self, resp: Any) -> Response:
        if isinstance(resp, Response):
            resp.Body = to_bytes(resp.Body)
            return resp
        if isinstance(resp, (str, bytes)):
            return Response(code=200,
                            body=to_bytes(resp))
        if isinstance(resp, (dict, list)):
            return Response(code=200,
                            headers={"Content-Type": "application/json"},
                            body=to_bytes(self.Serializer.dumps(resp)))

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
        for handle in self.before_funs_list:
            rv = handle()
            if rv:
                return rv

    def dispatch_handle(self):
        handle = self.match_handle()
        return self.wrapper_response(handle(**req.Path_Args))

    def error_handle(self, e):
        code = parse_except_code(e)
        if code in self.error_funs_dict:
            response = self.wrapper_response(self.error_funs_dict[code]())
        else:
            response = Response(code, body=get_code_desc(code))
        return response

    def finally_handle(self, response: Response):
        for handle in self.after_funs_list:
            response = handle(response)
        self.Session.save_session(response)
        return response

    def dispatch(self, r: Request):
        ctx = RequestCtx(r, self)
        with ctx:
            self.Logger.debug(req.method, req.full_path)
            # ctx.push()    # 自动push
            self.Session.open_session()
            try:
                response = self.before_handle()
                if response is None:
                    response = self.dispatch_handle()
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
