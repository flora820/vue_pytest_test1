import pytest
from common.extract_util import *
from common.request_util import * 
from common.text_util import *
from common.yaml_util import *
from api.api_users import *
import json
#import allure
#from common.log_util import LogUtil


@pytest.fixture(scope="function",autouse=True)
def user_main(user_config = '%s/data/driven_yaml/user_config.yaml' % base_dir, extract_file = "%s/data/driven_yaml/extract.yaml" % base_dir):
    url = read_yaml(user_config)['users']['base_url']+read_yaml(user_config)['users']['test_users_url']
    header = '{"Authorization":"%s","Content-Type":"application/json"}' % read_yaml(extract_file)['token']
    header = eval(header)
    #print(url)
    #print(header)
   ##测试user模块时先注册一个用户 
    test = handle_users()
    temp_id = test.add_user(url, header, test.name, test.passwd)
    
    idx_dict = {}
    idx_dict['id'] = temp_id
   
    
    yield idx_dict, test 
   
    temp_id = test.requery_user(url, header, test.name)
    if temp_id != None:
        test.delete_user(url, header, temp_id)


@pytest.mark.users
@pytest.mark.all
@pytest.mark.parametrize('args', extract_util('%s/data/yaml/users.yaml' % base_dir, user_list=['common','users']))
def test_users(args,user_main):
    test_users.__doc__ = str(args['case_name'])
    log.info("\n\n\n\n\n--------------------------------------------case_name:%s---------------------------------------------------------\n" % str(args['case_name']))
    url = args['url']
    header = eval(args['header'])
    method = args['method']
    payloads = json.dumps(eval(args['body']))
    params = eval(args['body'])
    expect = args['expect_result']  # 断言依据
    run_result_txt = '%s/data/run_result.txt' % base_dir
   
    url = extract_case(url, user_main[0]) 
    
    
    rep = request_util(method, url, headers=header, payloads=payloads, params=params, expect=expect, run_result_txt=run_result_txt)
    

    name = None 
    if 'username' in args['body']:
        name = eval(args['body'])['username']
        user_main[1].name = name
    
    #判断是否是增加用户case,防止用户已存在，误判断
    if name != None:
        ret = user_main[1].judge_user(url, header, rep, name)
        if ret == None:
            rep = request_util(method, url, headers=header, payloads=payloads, params=params, expect=expect, run_result_txt=run_result_txt)

    assert_util(expect, rep, run_result_txt)
    log.info("\n--------------------------------------------case_name:%s end---------------------------------------------------------\n" % str(args['case_name']))
    


if __name__ == '__main__':
    pass

