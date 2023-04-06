import os
import sys
import time
import unittest

import HtmlTestRunner

# 获取当前路径
curren_path = os.path.dirname(__file__)
# 获取测试用例目录的路径
case_path = os.path.join(curren_path, "tests")


# 使用discover()来实现添加执行整个目录下所有的测试用例
# 匹配测试用例路径下的所有的测试方法
discover = unittest.defaultTestLoader.discover(start_dir=case_path,  # 用例路径
                                               pattern="*_test.py",
                                               top_level_dir=None)   # 文件类型
# 创建主套件
main_suite = unittest.TestSuite()
# 把测试用例路径添加到主套件中
main_suite.addTest(discover)
# 执行并生成测试报告
now = time.strftime("%y-%m_%d_%H_%M_%S_", time.localtime(time.time()))
# 创建配置html测试报告的相关信息的对象
runner = HtmlTestRunner.HTMLTestRunner(stream=sys.stdout)
# 生成html测试报告
runner.run(main_suite)
