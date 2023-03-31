import datetime
import sys
from typing import TextIO

INFO = 0x0  # info
DEBUG = 0x1  # debug
WARN = 0x2  # warn


class BaseLogger():

    def __init__(self, module, level: int = INFO, log_file: str = "log.log", out: TextIO = sys.stdout):
        self.__module = module
        self.level = level
        self.log = open(log_file, "a", encoding="utf-8")
        self.out = out

    @property
    def module(self):
        return self.__module

    @module.setter
    def module(self, module):
        self.__module = module

    def write(self, level, *msg):
        _msg = "[%s] - [%s] %s\n" % (str(datetime.datetime.now()), self.module, " ".join([str(m) for m in msg]))
        if level >= self.level:
            self.log.write(_msg)
            self.log.flush()
        self.out.write(_msg)

    def info(self, *msg):
        self.write(INFO, *msg)

    def debug(self, *msg):
        self.write(DEBUG, *msg)

    def warn(self, *msg):
        self.write(WARN, *msg)


class Logger(BaseLogger):
    pass


def init_logger(module) -> Logger:
    return Logger(module)


__logger: Logger = init_logger(__name__)
