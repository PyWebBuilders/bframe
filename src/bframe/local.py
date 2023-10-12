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
from bframe.logger import init_logger

logger = init_logger()


class Local:

    def __init__(self):
        super().__setattr__("storage", {})

    def __setattr__(self, name: str, value: str):
        pk = get_ident()
        if pk in self.storage:
            self.storage[pk][name] = value
        else:
            self.storage[pk] = {name: value}

    def __getattr__(self, name: str):
        pk = get_ident()
        return self.storage[pk][name]

    def __delattr__(self, name: str):
        pk = get_ident()
        try:
            del self.storage[pk]
        except KeyError:
            pass


class LocalProxy:

    def __init__(self, local: Local, name: str) -> None:
        self.__local = local
        self.__name = name

    def __getattr__(self, name: str):
        if callable(self.__local):
            obj = self.__local(self.__name)
        else:
            obj = getattr(self.__local, self.__name)
        return getattr(obj, name)

    def __setitem__(self, key, value):
        if callable(self.__local):
            obj = self.__local(self.__name)
            obj[key] = value
            return
        self.__local[key] = value

    def __getitem__(self, key):
        if callable(self.__local):
            obj = self.__local(self.__name)
            return obj[key]
        return self.__local[key]
