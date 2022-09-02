import pytest
from common.extract_util import *
from common.request_util import * 
from common.text_util import *
from common.yaml_util import *
import json
#import allure
#from common.log_util import LogUtil


g_idx = 0
g_main_idx = None

class handle_users(object):
   
    idx = 0
    name = ""
    passwd = ""
    def __init__(self,user_config = '%s/data/driven_yaml/user_config.yaml' % base_dir):
        self.name = read_yaml(user_config)['test_user']
        self.passwd = read_yaml(user_config)['test_passwd']

    def add_user(self, url, header, name, passwd):
        payload = '{"username":"%s","password":"%s"}' % (name, passwd)
       # payloads = json.dumps(payload)        
        rep = request_util('post', url, headers=header, payloads=payload)
        
        print(rep)

        temp_id = self.judge_user(url, header, rep, name)
        return temp_id
            

    def requery_user(self,url, header, name):
        temp_id = None
        data = '{"query":"%s","pagenum":1,"pagesize":1}' % (name)
        params = json.loads(data)       
        rep = request_util('get', url, headers=header,  params=params)
        
        for v in json.loads(rep)['data']['users']: #json字符串转化为字典
            if v['username'] == name :
                temp_id = v['id']
        
        self.idx = temp_id
        return temp_id
        

    def delete_user(self,url, header, temp_id):
        
        url = url + "/" + str(temp_id)
        print("deletet_url:",url)
        rep = request_util('delete', url, headers=header)
        print(rep)
   
   #此函数用来判断用户是否已注册，注册就删除，重新执行case
    def judge_user(self, url, header, rep, name):
        temp_id = None 
        if '用户名已存在' in rep:
            temp_id = self.requery_user(url, header, name)
            self.delete_user(url, header, temp_id)
            return None
        if '创建成功' in rep:
            temp_id = json.loads(rep)['data']['id']
            self.idx = temp_id
            return temp_id
        return None


@pytest.fixture(scope="function",autouse=True)
def user_main(user_config = '%s/data/driven_yaml/user_config.yaml' % base_dir, extract_file = "%s/data/driven_yaml/extract.yaml" % base_dir):
    url = read_yaml(user_config)['base_url']+read_yaml(user_config)['test_users_url']
    header = '{"Authorization":"%s","Content-Type":"application/json"}' % read_yaml(extract_file)['token']
    header = eval(header)
    #print(url)
    #print(header)
   ##测试user模块时先注册一个用户 
    test = handle_users()
    temp_id = test.add_user(url, header, test.name, test.passwd)
    
    idx_dict = {}
    idx_dict['id'] = temp_id
   
    g_idx = temp_id
    
    yield idx_dict, test 
   
    g_idx = test.requery_user(url, header, test.name)
    if g_idx != None:
        test.delete_user(url, header, g_idx)


@pytest.mark.users
@pytest.mark.all
@pytest.mark.parametrize('args', extract_util('%s/data/yaml/users.yaml' % base_dir))
def test_users(args, user_main):
    
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
    ret = None
    if name != None:
        ret = user_main[1].judge_user(url, header, rep, name)
        if ret == None:
            rep = request_util(method, url, headers=header, payloads=payloads, params=params, expect=expect, run_result_txt=run_result_txt)

    assert_util(expect, rep, run_result_txt)
    
    print("测试返回:",rep)


if __name__ == '__main__':
    pass

