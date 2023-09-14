from typing import Callable, List, TypeVar

from bframe.logger import __logger as logger

logger.module = __name__


AnyPath = TypeVar('AnyPath', int, str)


class ReqRepeatException(Exception):
    """请求路径配置重复"""
    pass


class NoSetControllerException(Exception):
    """未配置请求控制器"""
    pass


class Tree:

    def __init__(self, root: str = "", func: Callable = "", children: list = None) -> None:
        self.root = root
        self.func = func
        if children is None:
            self.children = list()
        else:
            self.children = children

    def split_path(self, path: str = "", split: str = "/"):
        return path.lstrip(split).split(split)

    def add(self, path: str = "", func: Callable = ""):
        node = self.split_path(path)
        self.__add(node, func)

    def find(self, path: str = "") -> Callable:
        node = self.split_path(path)
        func = self.__find(node)
        if not callable(func):
            raise NoSetControllerException("%s 未配置请求控制器" % "/".join(node))
        return func

    def find_node(self, node: str) -> object:
        for _node in self.children:
            if _node.root == node:
                return _node
        return None

    def __add(self, nodes: List[AnyPath], func: Callable, n: int = 0) -> bool:
        if callable(self.__find(nodes)):
            raise ReqRepeatException("%s 请求配置重复" % "/".join(nodes))

        if len(nodes) == n:
            self.func = func
            return True

        node = self.find_node(nodes[n])
        if not node:
            node = Tree(nodes[n])
            self.children.append(node)
        return node.__add(nodes, func, n+1)

    def __find(self, nodes: List[AnyPath], n: int = 0) -> Callable:
        if len(nodes) == n:
            return self.func

        node = self.find_node(nodes[n])
        if not node:
            return ""
        return node.__find(nodes, n+1)
