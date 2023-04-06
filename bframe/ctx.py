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
from bframe.local import Local, LocalProxy
from bframe.server import Request

_request_ctx: Local = Local()
_app_ctx: Local = Local()
_request_name = "request"
_app_name = "g"


class RequestCtx():

    __name = _request_name

    def __init__(self, r: Request):
        self.__request = r
        self.__appctx = AppCtx()

    def push(self):
        setattr(_request_ctx, self.__name, self.__request)
        self.__appctx._AppCtx__push()

    def pop(self):
        delattr(_request_ctx, self.__name)
        self.__appctx._AppCtx__pop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.pop()


class AppCtx():

    __name = _app_name

    def __push(self):
        setattr(_app_ctx, self.__name, dict())

    def __pop(self):
        delattr(_app_ctx, self.__name)

    def __setattr__(self, name: str, value: str):
        g_value: dict = getattr(_app_ctx, self.__name)
        g_value.update({name: value})
        setattr(_app_ctx, self.__name, g_value)

    def __getattr__(self, name: str):
        return getattr(_app_ctx, self.__name).get(name)


request: Request = LocalProxy(_request_ctx, _request_name)
g = AppCtx()
