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
        self.tree.add("/admin/api/<reg:(?P<version>v\d+$)>/tom", lambda x, y: x-y)
        self.tree.add("/admin/<reg:(?P<xxx>ap[a-z]{1}$)>/<reg:(?P<version>v\d+$)>/tom", lambda x, y: x-y)
        self.tree.add("/static/<*:xxxx>", lambda x, y: x-y)

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
    
    def test_admin_api_1(self):
        self.req_4 = Request()
        func = self.tree.find(self.req_4.set_path_args, "/admin/api/v1/tom")
        self.assertIsNotNone(func)
        self.assertEqual(func(10, 2), 8, "执行异常")
        self.assertEqual(self.req_4.Path_Args, {'version': "v1"}, "执行异常")

    def test_admin_api_2(self):
        self.req_5 = Request()
        func = self.tree.find(self.req_5.set_path_args, "/admin/api/v2/tom")
        self.assertIsNotNone(func)
        self.assertEqual(func(10, 2), 8, "执行异常")
        self.assertEqual(self.req_5.Path_Args, {'version': "v2"}, "执行异常")
    
    def test_admin_apa_1(self):
        self.req_6 = Request()
        func = self.tree.find(self.req_6.set_path_args, "/admin/apa/v2/tom")
        self.assertIsNotNone(func)
        self.assertEqual(func(10, 2), 8, "执行异常")
        self.assertEqual(self.req_6.Path_Args, {'xxx': "apa",'version': "v2"}, "执行异常")
   
    def test_static_1(self):
        self.req_7 = Request()
        func = self.tree.find(self.req_7.set_path_args, "/static/main.css")
        self.assertIsNotNone(func)
        self.assertEqual(func(10, 2), 8, "执行异常")
    
    def test_static_2(self):
        self.req_8 = Request()
        func = self.tree.find(self.req_8.set_path_args, "/static/css/main.css")
        self.assertIsNotNone(func)
        self.assertEqual(func(10, 2), 8, "执行异常")


if __name__ == "__main__":
    unittest.main()
