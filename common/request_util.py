import json
import requests
from common.text_util import *


def assert_util(expect,response,run_result_txt):

    print(response)
    for expect_word in expect.split(","):
        assertion = expect_word in response
        if assertion:
            assert assertion
            # 将运行结果写入txt文件保存
            write_txt(text_file=run_result_txt, data=response+"__pass|\n")  # 用"__"符号间隔                    
        else:
            assert assertion
            write_txt(text_file=run_result_txt, data=response+"__fail|\n")        


def request_util(method, url, headers, payloads=None, params=None, expect=None, run_result_txt=None):
    if method == 'get':
        res = requests.request('GET',url, headers=headers, params=params)

    elif method == 'post':
        res = requests.request('POST', url=url, headers=headers, data=payloads)
    
    elif method == 'put':
        res = requests.request('PUT', url=url, headers=headers, data=payloads) 
    
    elif method == 'delete':
        res = requests.request('DELETE', url=url, headers=headers, params=params) 


#    assert_util(expect, res.text, run_result_txt)
    return res.text

