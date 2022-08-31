import pytest
from common.extract_util import *
from common.request_util import request_util 
from common.text_util import *
from common.yaml_util import *
import json
#import allure
#from common.log_util import LogUtil





class users_data(object):
    
    def __init__(self, config_path='%s/data/driven_yaml/user_config.yaml' % Path(__file__).parent.parent):
        self.idx = idx
        self.users = users

    def add_user(self):
                 

    def requery_user(self):

    def delete_user(self):





@pytest.mark.users
@pytest.mark.all
@pytest.mark.parametrize('args', extract_util('%s/data/yaml/users.yaml' % base_dir))
def test_users(args):
    url = args['url']
    header = eval(args['header'])
    method = args['method']
    payloads = json.dumps(eval(args['body']))
    params = eval(args['body'])
    expect = args['expect_result']  # 断言依据
    run_result_txt = '%s/data/run_result.txt' % base_dir

    rep = request_util(method, url, headers=header, payloads=payloads, params=params, expect=expect, run_result_txt=run_result_txt)

    assert_util(expect, response,run_result_txt)
    
    print("测试返回:",rep)

