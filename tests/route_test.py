import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bframe.route import Tree
from bframe.wrappers import Request


class TreeTestCase(unittest.TestCase):

    def setUp(self):
        self.tree = Tree()
        self.tree.add("/api/v1/sub", lambda x, y: x-y)
        self.tree.add("/api/v3/sub/<int:pk>", lambda x, y: x-y)
        self.tree.add("/api/v4/sub/<str:name>", lambda x, y: x-y)

    def test_sub_01(self):
        self.req_1 = Request()
        func = self.tree.find(self.req_1.set_path_args, "/api/v1/sub")
        self.assertIsNotNone(func)
        self.assertEqual(func(10, 2), 8, "执行异常")

    def test_sub_02(self):
        self.req_2 = Request()
        func = self.tree.find(self.req_2.set_path_args, "/api/v3/sub/1")
        self.assertIsNotNone(func)
        self.assertEqual(func(10, 2), 8, "执行异常")
        self.assertEqual(self.req_2.Path_Args, {'pk': 1}, "执行异常")

    def test_sub_03(self):
        self.req_3 = Request()
        func = self.tree.find(self.req_3.set_path_args, "/api/v4/sub/tom")
        self.assertIsNotNone(func)
        self.assertEqual(func(10, 2), 8, "执行异常")
        self.assertEqual(self.req_3.Path_Args, {'name': "tom"}, "执行异常")


if __name__ == "__main__":
    unittest.main()
