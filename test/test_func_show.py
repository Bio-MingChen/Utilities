# -*- coding=utf-8 -*-

import sys
sys.path.append('../')

import pytest

from functions.show import *

def test_colors():
    """
    test for make_colors
    """
    colors = make_colors()
    print('{green}Using colorama to print {red}colorful {back}'.format(**colors))

