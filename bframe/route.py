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


class BaseTree:

    def __init__(self,
                 root: str = "",
                 func: Callable = "",
                 children: list = None):
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


class MatchTree():

    def __init__(self):
        """
        <str:name>
        <int:pk>
        <reg:name>
        """
        self.left = "<"
        self.right = ">"
        self.split = ":"
        self.node = None
        self.node_type = None
        self.node_name = None
        self.rule = {
            "str": str,
            "int": int,
            # "reg": "",
        }

    def is_support_match(self, node: str) -> bool:
        """节点是否支持匹配"""
        if node.startswith(self.left) and node.endswith(self.right) and self.split in node:
            self.node = node
            self.initialization()
            if self.node_type not in self.rule.keys():
                return False
            return True
        return False

    def initialization(self):
        """解析node"""
        self.node_type, self.node_name = self.node.removeprefix(self.left).\
            removesuffix(self.right).\
            split(self.split, 1)

    def match(self, _node: str):
        """匹配新节点"""
        v = self.rule.get(self.node_type)(_node)
        return True, {self.node_name: v}


class Tree(BaseTree):

    def __init__(self, root: str = "", func: Callable = "", children: list = None) -> None:
        super().__init__(root, func, children)
        self.match = False
        self.match_tree = MatchTree()

    def add(self, path: str = "", func: Callable = ""):
        node = self.split_path(path)
        self.__match_add(node, func)

    def find(self, call_back: Callable, path: str = "") -> Callable:
        node = self.split_path(path)
        func = self.__match_find(node, call_back)
        if not callable(func):
            raise NoSetControllerException("%s 未配置请求控制器" % "/".join(node))
        return func

    def find_match_node(self, node: str, call_back: Callable = None, open_match=True) -> object:
        for _node in self.children:
            if open_match and _node.match and self.match_tree.is_support_match(_node.root):
                status, value = self.match_tree.match(node)
                if status and call_back:
                    call_back(**value)
                    return _node
            elif _node.root == node:
                return _node
        return None

    def __match_add(self, nodes: List[AnyPath], func: Callable, n: int = 0) -> bool:
        if callable(self.__find_conflict(nodes)):
            raise ReqRepeatException("%s 请求配置重复" % "/".join(nodes))

        if len(nodes) == n:
            self.func = func
            return True

        node = self.find_node(nodes[n])
        if not node:
            node = Tree(nodes[n])
            if node.match_tree.is_support_match(nodes[n]):
                node.match = True
                node.match_tree = MatchTree()   # 需要匹配才配置匹配树
            self.children.append(node)
        return node.__match_add(nodes, func, n+1)

    def __find_conflict(self, nodes: List[AnyPath], n: int = 0):
        if len(nodes) == n:
            return self.func

        # 查找是否出现相同的匹配树
        node = self.find_match_node(nodes[n], open_match=False)
        if not node:
            return ""
        return node.__match_find(nodes, n+1)

    def __match_find(self, nodes: List[AnyPath], call_back: Callable, n: int = 0) -> Callable:
        if len(nodes) == n:
            return self.func

        node = self.find_match_node(nodes[n], call_back)
        if not node:
            return ""
        return node.__match_find(nodes, call_back, n+1)
