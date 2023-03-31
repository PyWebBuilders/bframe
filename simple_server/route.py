from typing import Union, Callable, List, TypeVar
from simple_server.logger import __logger as logger

logger.module = __name__

MethodSenquenceAlias = Union[tuple, list]
AnyPath = TypeVar('AnyPath', int, str)


class Tree:

    def __init__(self, root: str = "", func: Callable = "", children: list = None) -> None:
        self.root = root
        self.func = func
        if children is None:
            self.children = list()
        else:
            self.children = children

    def _split_path(self, path: str = "", split: str = "/"):
        return path.split(split)

    def add(self, path: str = "", func: Callable = ""):
        node = self._split_path(path)
        self.__add(len(node), node, func)

    def find(self, path: str = ""):
        node = self._split_path(path)
        self.__find(len(node), node)

    def __add(self, n: int, nodes: List[AnyPath], func):
        for idx in range(n):
            if nodes[idx] == self.root:
                logger.info("add same node ", idx, self.root, self.func)
                return self.__add(n-1, nodes[1:], func)
            for obj in self.children:
                logger.info("add children node ", idx, obj.root, obj.func)
                if nodes[idx] == obj.root:
                    self = obj
                    return self.__add(n-1, nodes[1:], func)
            _node = Tree(nodes[idx], func)
            logger.info("add add node ", _node.root, _node.func)
            self.children.append(_node)
            self = _node

    def __find(self, n: int, nodes: List[AnyPath]):
        for idx in range(n):
            if nodes[idx] == self.root:
                logger.info("find same node ", idx, self.root, self.func)
                return self.__find(n-1, nodes[1:])
            for obj in self.children:
                logger.info("find children node ", idx, obj.root, obj.func)
                if nodes[idx] == obj.root:
                    self = obj
                    return self.__find(n-1, nodes[1:])
            _node = Tree(nodes[idx])
            logger.info("find add node ", _node.root, _node.func)
            self.children.append(_node)
            self = _node


route_map = Tree()
# route_map.add("/api/v1/index")
# route_map.add("/api/v2/index")
# route_map.add("/api/v2/index")
# route_map.find("/api/v2/index")
# print(1)


def route(url: str, method: MethodSenquenceAlias = None):

    def wrapper(f):
        pass

    return wrapper
