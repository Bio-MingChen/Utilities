#!/usr/bin/env python
# -*- coding=utf-8 -*-

# this script is used to test ../functions/mk_logging.py
import sys
sys.path.append('../')

import pytest
from func.mk_logging import *

def test_basic_log():
    logger1 = basic_log('test')
    logger2 = basic_log('test.test1')
    logger1.info("Let\'s do something!")
    logger2.warning("This is a Warning!")
    logger1.error("Something goes wrong...")

def test_multi_log():
    logger = multi_logger('test')
    logger.info('good')

if __name__ == "__main__":
    test_basic_log()
    test_multi_log()