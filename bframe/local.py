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
from threading import get_ident
from bframe.logger import __logger as logger
import typing as t

logger.module = __name__


class Local():

    def __init__(self):
        super().__setattr__("storage", {})

    def __setattr__(self, name: str, value: str):
        id = get_ident()
        if id in self.storage:
            self.storage[id][name] = value
        else:
            self.storage[id] = {name: value}

    def __getattr__(self, name: str):
        id = get_ident()
        return self.storage[id][name]

    def __delattr__(self, name: str):
        id = get_ident()
        try:
            del self.storage[id]
        except KeyError:
            pass


class LocalProxy():

    def __init__(self, local: Local, name: str) -> None:
        self.__local = local
        self.__name = name

    def __getattr__(self, name: str):
        obj = getattr(self.__local, self.__name)
        return getattr(obj, name)
