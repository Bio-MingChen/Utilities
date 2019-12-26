#!/usr/bin/env python
# -*- coding=utf-8 -*-

#This scripts was used to store variety of decorators


#==================================================================
# runtime decorator is used to figure out the function running time
#==================================================================
def runtime(func):
    """
    decorator for recording time eclipse of function running
    """
    def wrapper(*args,**kwargs):
        start = time()
        result = func()
        eclipse = time() -start
        print('{func} running time: {eclipse}'.format(func=func,eclipse=eclipse))
        return result
    return wrapper
