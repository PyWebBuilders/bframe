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
import datetime
import inspect
import os
import sys
from typing import TextIO

from bframe.utils import archive_file
from bframe.utils import color_msg, TEXT, BACK, STYLE

INFO = 0x0  # info
DEBUG = 0x1  # debug
WARN = 0x2  # warn


class BaseLogger:

    def __init__(self,
                 level: int = INFO,
                 write_file: bool = False,
                 log_file: str = "log.log",
                 out: TextIO = sys.stdout):
        self.level = level
        self.write_file = write_file
        archive_file(os.getcwd(), log_file)
        if self.write_file:
            self.log = open(log_file, "a", encoding="utf-8")
        self.out = out
        self._prefix = os.path.dirname(os.path.abspath(__file__)) + os.sep

    def write(self, level, *msg):
        stack = inspect.stack()[2]
        _msg = "[%s] - [%s:%d] %s\n" % (str(datetime.datetime.now()),
                                     stack[1][len(self._prefix):], stack[2], " ".join([str(m) for m in msg]))  # noqa
        if level >= self.level:
            if self.write_file:
                self.log.write(_msg)
                self.log.flush()
            if level == INFO:
                _msg = color_msg(_msg, TEXT.WHITE)
            if level == DEBUG:
                _msg = color_msg(_msg, TEXT.YELLOW)
            if level == WARN:
                _msg = color_msg(_msg, TEXT.RED)
            self.out.write(_msg)

    def info(self, *msg):
        self.write(INFO, *msg)

    def debug(self, *msg):
        self.write(DEBUG, *msg)

    def warn(self, *msg):
        self.write(WARN, *msg)


class Logger(BaseLogger):
    pass


def init_logger(level=DEBUG) -> Logger:
    return Logger(level)


# __logger: Logger = init_logger()
