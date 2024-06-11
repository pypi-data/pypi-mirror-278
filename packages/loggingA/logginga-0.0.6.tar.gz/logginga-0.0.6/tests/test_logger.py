#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/5/12
# @Author  : alan
# @File    : test_logger.py
import os
import unittest

import loggingA
from loggingA.logger import get_logger
from unittest import TestCase


class TestLogger(TestCase):

    def setUp(self):
        # 设置测试环境，例如创建临时文件夹或者设置其他必要的资源
        if not os.path.exists("./log"):
            os.mkdir("./log")

    def test_get_logger(self):
        logger = get_logger("./log", log_level=loggingA.DEBUG)
        logger.info("测试")
        logger.debug("测试")


if __name__ == '__main__':
    unittest.main()
