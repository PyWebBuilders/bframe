from bframe.local import Local, LocalProxy
from bframe.http_server import Request

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
