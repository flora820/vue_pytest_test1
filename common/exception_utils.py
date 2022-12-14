import traceback
from functools import wraps
from pathlib import Path
base_dir = Path(__file__).parent.parent

def exception_utils(func):
    """处理异常的装饰器"""
    @wraps(func)
    def wraped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print('出现异常，error is %s\n%s' % (e, traceback.extract_stack()))

    return wraped   

"""
def exception_utils(func):
    '''处理异常的装饰器'''
    @wraps(func)
    def wraped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print('出现异常，error is %s\n%s' % (e, traceback.extract_stack()))

    return wraped   
"""

