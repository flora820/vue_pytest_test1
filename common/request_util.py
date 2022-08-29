import json
import requests
from common.text_util import *


def request_util(method, url, headers, payloads=None, params=None, expect=None, run_result_txt=None):
    if method == 'get':
        res = requests.request('GET',url, headers=headers, params=params)
        print(res.text)
        for expect_word in expect.split(","):
            assertion = expect_word in res.text
            if assertion:
                assert assertion
                # 将运行结果写入txt文件保存
                write_txt(text_file=run_result_txt, data=res.text+"__pass|")  # 用"__"符号间隔                    
            else:
                assert assertion
                write_txt(text_file=run_result_txt, data=res.text+"__fail|")        
        return res.text

    elif method == 'post':
        res = requests.request('POST', url=url, headers=headers, data=payloads)
        print(res.text)
        for expect_word in expect.split(","):
            assertion = expect_word in res.text
            # print("断言是：", assertion)
            if assertion:
                assert assertion
                write_txt(text_file=run_result_txt, data=res.text+"__pass|")
            else:
                assert assertion
                write_txt(text_file=run_result_txt, data=res.text+"__fail|")
        return res.text
    elif method == 'put':
        pass
    
    elif method == 'delete':
        pass

