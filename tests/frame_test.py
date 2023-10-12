import os
import sys
import unittest
import json

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

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
    
    def test_login_set_cookie_01(self):
        response = self.client.post("/login", {"user": "admin", "pwd": "admin"})
        self.assertEqual(response.Cookies.get("username").value, "admin", "响应数据异常")
    
    def test_get_admin_01(self):
        response = self.client.get("/admin")
        self.assertEqual(json.loads(response.Body).get("msg"), "小伙子，请登录一下吧", "响应数据异常")

    def test_get_admin_02(self):
        response = self.client.get("/admin?user=tom")
        self.assertEqual(json.loads(response.Body).get("msg"), "获取后台数据成功", "响应数据异常")
    
    def test_get_admin_set_cookie_01(self):
        response = self.client.get("/admin?user=tom", headers={"Cookie": "x-id=1"})
        self.assertEqual(json.loads(response.Body).get("cookie", {}).get("x-id"), "1", "响应数据异常")
    
    def test_get_users_01(self):
        response = self.client.get("/api/user/tom/profile")
        self.assertEqual(json.loads(response.Body).get("data", {}).get("username"), "tom", "响应数据异常")

    def test_get_users_02(self):
        response = self.client.get("/admin/api/users/1/profile")
        self.assertEqual(json.loads(response.Body).get("data", {}).get("user_id"), 1, "响应数据异常")
    
    def test_config_01(self):
        response = self.client.get("/conf")
        body = json.loads(response.Body)
        self.assertEqual(body["HOST"],  "0.0.0.0", "响应数据异常")
        self.assertEqual(body["PORT"], 7256, "响应数据异常")
    
    def test_class_UserInfo_01(self):
        response = self.client.get("/userinfo")
        self.assertEqual(json.loads(response.Body).get("data", {}).get("userinfo"), "get", "响应数据异常")
    
    def test_class_UserInfo_02(self):
        response = self.client.post("/userinfo", {})
        self.assertEqual(json.loads(response.Body).get("data", {}).get("userinfo"), "post", "响应数据异常")
    
    def test_class_UserInfo_03(self):
        response = self.client.put("/userinfo", {})
        self.assertEqual(json.loads(response.Body).get("data", {}).get("userinfo"), "put", "响应数据异常")

    def test_class_UserInfo_04(self):
        response = self.client.delete("/userinfo", {})
        self.assertEqual(json.loads(response.Body).get("data", {}).get("userinfo"), "delete", "响应数据异常")
    

if __name__ == "__main__":
    unittest.main()
