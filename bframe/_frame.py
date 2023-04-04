import inspect
import threading
from typing import Callable, Union

from bframe import __version__
from bframe.http_server import HTTP_METHOD, Request, SimpleHTTPServer, SimpleRequestHandler
from bframe.logger import Logger as Log
from bframe.logger import init_logger
from bframe.route import Tree

MethodSenquenceAlias = Union[tuple, list]


class _Frame():

    version = "bframe/%s" % __version__

    # http server
    Server: SimpleHTTPServer = None
    ServerLock: threading.Lock = threading.Lock()

    # 路由
    RouteMap: Tree = Tree()
    RouteMapLock: threading.Lock = threading.Lock()

    # 日志
    Logger: Log = init_logger(__name__)

    def __init__(self, name: str = None) -> None:
        self.app_name = name
        if name is None:
            self.app_name = __name__

    def add_route(self, url: str, func_or_class: Callable, method: MethodSenquenceAlias = None):
        def _add_class_handle(cls):
            meth = [method.lower()
                    for method in HTTP_METHOD if hasattr(cls, method.lower())]
            for m in meth:
                _url = "%s/%s" % (url, m.upper())
                self.RouteMap.add(_url, getattr(cls(), m))

        with self.RouteMapLock:
            _methods = method
            if _methods is None:
                _methods = ["GET"]
            if not isinstance(_methods, (tuple, list)):
                _methods = [_methods]

            if inspect.isclass(func_or_class):
                _add_class_handle(func_or_class)
                return
            for m in _methods:
                _url = "%s/%s" % (url, m.upper())
                self.RouteMap.add(_url, func_or_class)

    def get(self, url: str):
        def wrapper(f):
            self.add_route(url, f, "GET")
            return f
        return wrapper

    def post(self, url: str):
        def wrapper(f):
            self.add_route(url, f, "POST")
            return f
        return wrapper

    def put(self, url: str):
        def wrapper(f):
            self.add_route(url, f, "PUT")
            return f
        return wrapper

    def delete(self, url: str):
        def wrapper(f):
            self.add_route(url, f, "DELETE")
            return f
        return wrapper

    def route(self, url: str, method: MethodSenquenceAlias = None):
        def wrapper(f):
            self.add_route(url, f, method)
            return f
        return wrapper

    def run(self, address: str = "127.0.0.1", port: int = 7256):
        self.Logger.info("run mode: no wsgi")
        try:
            if self.Server is None:
                with self.ServerLock:
                    self.Server = SimpleHTTPServer(server_address=(address, port),
                                                   RequestHandlerClass=SimpleRequestHandler,
                                                   application=self)
            self.Logger.info("start server http://%s:%s" % (address, port))
            self.Server.serve_forever()
        except KeyboardInterrupt:
            self.Logger.info("shutdown server")
            self.Server.shutdown()

    def dispatch(self, request: Request):
        raise NotImplemented

    def __call__(self, request: Request):
        return self.dispatch(request)