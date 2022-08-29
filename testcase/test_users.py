import pytest
from common.extract_util import *
from common.request_util import request_util 
from common.text_util import *
from common.yaml_util import *
import json
#import allure
#from common.log_util import LogUtil



@pytest.mark.run(order=1)
@pytest.mark.all
@pytest.mark.parametrize('args', extract_util('%s/data/yaml/users.yaml' % base_dir))
def test_users(args):
    url = args['url']
    header = eval(args['header'])
    method = args['method']
    payload = json.dumps(eval(args['body']))
    params = eval(args['body'])
    expect = args['expect_result']  # 断言依据
    run_result_txt = '%s/data/run_result.txt' % base_dir

    rep = request_util(method, url, headers=header, payloads=payload, params=params, expect=expect, run_result_txt=run_result_txt)
    print("测试返回:",rep)

