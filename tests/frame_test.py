import os
import sys
import unittest
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _frame_demo import app


class FrameTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_index_01(self):
        response = self.client.get("/")
        self.assertEqual(response.Body, b"hello world", "响应数据异常")
        response = self.client.get("/index")
        self.assertEqual(response.Body, b"hello world", "响应数据异常")
    
    def test_login_01(self):
        response = self.client.post("/login", {"user": "admin"})
        self.assertEqual(json.loads(response.Body).get("msg"), "数据不完整", "响应数据异常")

    def test_login_02(self):
        response = self.client.post("/login", {"user": "admin", "pwd": "xxx"})
        self.assertEqual(json.loads(response.Body).get("msg"), "账号密码异常", "响应数据异常")

    def test_login_03(self):
        response = self.client.post("/login", {"user": "admin", "pwd": "admin"})
        self.assertEqual(json.loads(response.Body).get("msg"), "登录成功", "响应数据异常")
    
    def test_get_admin_01(self):
        response = self.client.get("/admin")
        self.assertEqual(json.loads(response.Body).get("msg"), "小伙子，请登录一下吧", "响应数据异常")

    def test_get_admin_02(self):
        response = self.client.get("/admin?user=tom")
        self.assertEqual(json.loads(response.Body).get("msg"), "获取后台数据成功", "响应数据异常")


if __name__ == "__main__":
    unittest.main()
