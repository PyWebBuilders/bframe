import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bframe.route import Tree


class TreeTestCase(unittest.TestCase):

    def setUp(self):
        self.tree = Tree()
        self.tree.add("/api/v1/add", lambda x,y: x+y)
        self.tree.add("/api/v1/sub", lambda x,y: x-y)
    
    def test_add_01(self):
        func = self.tree.find("/api/v1/add")
        self.assertIsNotNone(func)
        self.assertEqual(func(1, 3), 4, "执行异常")

    def test_sub_01(self):
        func = self.tree.find("/api/v1/sub")
        self.assertIsNotNone(func)
        self.assertEqual(func(10, 2), 8, "执行异常")



if __name__ == "__main__":
    unittest.main()
