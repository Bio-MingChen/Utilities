# -*- coding=utf-8 -*-

#This script is used to test functions/file_operation.py 
import sys
sys.path.append('../') #used for import modules from upper directory

import pytest
from func import file_operation

def test_titleparser():
    """
    test fo TitleParser class
    """
    title = 'ColA\tColB\tColC\n'
    tp = file_operation.TitleParser(title)

    first_line = '1\t2\t3\n'
    # test get_filed method
    col_a = tp.get_field(first_line.split('\t'),"cola")
    print(col_a)
    assert col_a == '1'

    # test get_idx method
    col_b_idx = tp.get_idx('colb')
    assert col_b_idx == 1

    # test have_title
    assert tp.have_title('colc') 
