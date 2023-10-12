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
import inspect
import os
import threading
from typing import Callable, Union

from bframe import __version__
from bframe.config import Config as config
from bframe.logger import Logger as Log
from bframe.logger import init_logger, INFO
from bframe.route import Tree
from bframe.server import HTTP_METHOD
from bframe.server import Request
from bframe.server import SimpleHTTPServer
from bframe.server import SimpleRequestHandler
from bframe.testing import TestClient

MethodSenquenceAlias = Union[tuple, list]


class Scaffold:
    version = "bframe/%s" % __version__

    # http server
    Server: SimpleHTTPServer = None
    ServerLock: threading.Lock = threading.Lock()

    # 路由
    RouteMap: Tree = Tree()
    RouteMapLock: threading.Lock = threading.Lock()

    # 日志
    Logger: Log = init_logger(INFO)

    # 配置文件
    Config: config = config()

     # 会话消息
    SessionID = None
    Session = None

    def __init__(self, name: str = None, static_url="static", static_folder="static"):
        self.app_name = name
        if name is None:
            self.app_name = __name__
        self.root_path = os.path.dirname(os.path.abspath(self.app_name))

        if static_url.startswith("/"):
            static_url = static_url.lstrip("/")
        if static_folder.startswith("/"):
            static_folder = static_folder.lstrip("/")
        self.static_url = static_url
        self.static_folder = os.path.join(self.root_path, static_folder)
        self.init_static = False  # 将静态文件的匹配放置在最后处理

    def make_url(self, method: str, url: str) -> str:
        if url.startswith("/"):
            url = url.lstrip("/")
        return "%s/%s" % (method, url)

    def add_class_route(self, cls, url, method=None):
        meth = [method.lower()
                for method in HTTP_METHOD if hasattr(cls, method.lower())]
        for m in meth:
            _url = self.make_url(m.upper(), url)
            self.RouteMap.add(_url, getattr(cls(), m))

    def add_func_route(self, func, url, method):
        for m in method:
            _url = self.make_url(m.upper(), url)
            self.RouteMap.add(_url, func)

    def add_route(self,
                  url: str,
                  func_or_class: Callable,
                  method: MethodSenquenceAlias = None):
        with self.RouteMapLock:
            handle_method = method or getattr(func_or_class, "method", ("GET", ))
            handle_method = handle_method if isinstance(handle_method, (tuple, list)) else [handle_method]
            if inspect.isclass(func_or_class):
                self.add_class_route(func_or_class, url, handle_method)
            else:
                self.add_func_route(func_or_class, url, handle_method)

    def route(self, url: str, method: MethodSenquenceAlias = None):
        def wrapper(f):
            self.add_route(url, f, method)
            return f

        return wrapper

    def get(self, url: str):
        return self.route(url, "GET")

    def post(self, url: str):
        return self.route(url, "POST")

    def put(self, url: str):
        return self.route(url, "PUT")

    def delete(self, url: str):
        return self.route(url, "DELETE")

    def init_static_url(self):
        url = "%s/<*:x>" % self.static_url
        if self.static_url == "":
            url = "<*:x>"
        self.add_route(url, self.static, "GET")
        self.init_static = True

    def static(self, *args, **kwds):
        raise NotImplementedError

    def run(self, address: str = "127.0.0.1", port: int = 7256):
        self.Logger.info("run mode: no wsgi")
        try:
            if self.Server is None:
                with self.ServerLock:
                    self.Server = SimpleHTTPServer(server_address=(address, port),  # noqa
                                                   RequestHandlerClass=SimpleRequestHandler,  # noqa
                                                   application=self)
            self.Logger.info("start server http://%s:%s" % (address, port))
            self.Server.serve_forever()
        except KeyboardInterrupt:
            self.Logger.info("shutdown server")
            self.Server.shutdown()

    def test_client(self):
        return TestClient(self)

    def dispatch(self, request: Request):
        raise NotImplementedError

    def __call__(self, request: Request):
        if not self.init_static:
            self.init_static_url()
        return self.dispatch(request)
