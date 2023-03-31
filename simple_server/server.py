import inspect
import threading
from typing import Union

from simple_server.http_server import (HTTP_METHOD, SimpleHTTPServer,
                                       SimpleRequestHandler)
from simple_server.logger import Logger, init_logger
from simple_server.route import Tree

MethodSenquenceAlias = Union[tuple, list]

__server_lock: threading.local = threading.Lock()
__server: SimpleHTTPServer = None
__logger: Logger = init_logger(__name__)
__route_map: Tree = Tree()
__route_map_lock: threading.local = threading.Lock()


# route_map.add("/api/v1/index", lambda x: x+1)
# route_map.add("/api/api/index", lambda x: x+1)
# route_map.add("/api/v2/index", lambda x: x+1)
# route_map.add("/api/v2/index", lambda x: x+1)
# func = route_map.find("/api/v2/index")
# func = route_map.find("/api/v2/indexx")
# print(1, func(1))
def get_route_map():
    return __route_map


def route(url: str, method: MethodSenquenceAlias = None):

    def _add_class_handle(cls):
        meth = [method.lower() for method in HTTP_METHOD if hasattr(cls, method.lower())]
        for m in meth:
            _url = "%s/%s" % (url, m.upper())
            __route_map.add(_url, getattr(cls(), m))

    def wrapper(f):
        with __route_map_lock:
            _methods = method
            if _methods is None:
                _methods = ["GET"]
            if inspect.isclass(f):
                _add_class_handle(f)
                return
            for m in _methods:
                _url = "%s/%s" % (url, m.upper())
                __route_map.add(_url, f)

    return wrapper


def start(address: str = "127.0.0.1", port: int = 7256):
    global __server
    if __server is None:
        with __server_lock:
            __server = SimpleHTTPServer((address, port), SimpleRequestHandler)
    __logger.info("start server http://%s:%s" % (address, port))
    __server.serve_forever()


def stop():
    __logger.info("shutdown server")
    __server.shutdown()
