import threading

from simple_server.http_server import SimpleHTTPServer, SimpleRequestHandler
from simple_server.logger import Logger, init_logger


__server_lock: threading.local = threading.Lock()
__server: SimpleHTTPServer = None
__logger: Logger = init_logger(__name__)


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
