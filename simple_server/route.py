from typing import Callable, List, TypeVar, Union

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
        return self.__find(len(node), node)

    def __add(self, n: int, nodes: List[AnyPath], func) -> bool:
        if callable(self.__find(len(nodes), nodes)):
            raise Exception("%s 请求配置重复" % "/".join(nodes))

        for idx in range(n):
            if nodes[idx] == self.root:
                logger.info("add same node ", idx, self.root, self.func)
                return self.__add(n-1, nodes[1:], func)
            for obj in self.children:
                logger.info("add children node ", idx, obj.root, obj.func)
                if nodes[idx] == obj.root:
                    return obj.__add(n-1, nodes[1:], func)
            self.children.append(Tree(nodes[idx], func))
            logger.info("add add node ", self.children[-1])
            self = self.children[-1]
        return True

    def __find(self, n: int, nodes: List[AnyPath]) -> Callable:
        if n == 0 and self:
            return self.func

        for idx in range(n):
            if nodes[idx] == self.root:
                logger.info("find same node ", idx, self.root, self.func)
                return self.__find(n-1, nodes[1:])
            for obj in self.children:
                logger.info("find children node ", idx, obj.root, obj.func)
                if nodes[idx] == obj.root:
                    return obj.__find(n-1, nodes[1:])
        return ""


route_map = Tree()
route_map.add("/api/v1/index", lambda x: x+1)
route_map.add("/api/api/index", lambda x: x+1)
# route_map.add("/api/v2/index", lambda x: x+1)
func = route_map.find("/api/v2/indexx")
print(1, func(1))


def route(url: str, method: MethodSenquenceAlias = None):

    def wrapper(f):
        pass

    return wrapper
