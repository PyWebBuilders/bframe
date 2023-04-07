import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bframe.ctx import RequestCtx, g, request
from bframe.server import Request



class CtxTestCase(unittest.TestCase):

    def setUp(self):
        self.req = Request(method="GET", path="/api/xxx/dddd", headers={"location": "www.python.org"})
        self.req_ctx = RequestCtx(self.req)
        

    def test_request(self):
        self.req_ctx.push()
        self.assertEqual(request.method, self.req.method, "请求method数据和封装的request数据不一致")
        self.assertEqual(request.path, self.req.path, "请求path数据和封装的request数据不一致")
        self.assertEqual(request.headers, self.req.headers, "请求headers数据和封装的request数据不一致")
        self.req_ctx.pop()
        try:
            request.method
        except Exception as e:
            self.assertIsInstance(e, KeyError)

    def test_g(self):
        self.req_ctx.push()
        g.test = 666
        self.assertEqual(g.test, 666, "请求method数据和封装的request数据不一致")
        self.req_ctx.pop()


if __name__ == "__main__":
    unittest.main()
