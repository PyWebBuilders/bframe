from bframe.local import Local, LocalProxy
from bframe.http_server import Request

_request_ctx: Local = Local()
_request_name = "request"


request: Request = LocalProxy(_request_ctx, _request_name)


class RequestCtx():

    __name = _request_name

    def __init__(self, r: Request):
        self.__request = r

    def push(self):
        setattr(_request_ctx, self.__name, self.__request)

    def pop(self):
        delattr(_request_ctx, self.__name)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.pop()
