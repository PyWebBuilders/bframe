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
        del self.storage[id]


class LocalProxy():

    def __init__(self, local: Local, name: str) -> None:
        self.__local = local
        self.__name = name

    def __getattr__(self, name: str):
        obj = getattr(self.__local, self.__name)
        return getattr(obj, name)

    def push(self, value: t.Any):
        setattr(self.__local, self.__name, value)

    def pop(self):
        try:
            delattr(self.__local, self.__name)
        except Exception as e:
            logger.info("local pop: ", e.args)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.pop()
