from simple_server.local import Local, LocalProxy
from simple_server.http_server import Request

__request_ctx: Local = Local()


def set_request(r: Request):
    setattr(__request_ctx, "request", r)


request = LocalProxy(__request_ctx, "request")
