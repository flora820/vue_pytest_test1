import pytest
from common.extract_util import *
from common.request_util import * 
from common.text_util import *
from common.yaml_util import *
import json
#import allure
#from common.log_util import LogUtil





class handle_users(object):
   
    idx = 0
    name = ""
    passwd = ""
    def __init__(self,user_config = '%s/data/driven_yaml/user_config.yaml' % base_dir):
        self.name = read_yaml(user_config)['test_user']
        self.passwd = read_yaml(user_config)['test_passwd']

    def add_user(self,url,header):
        payload = '{"username":"%s","password":"%s"}' % (self.name, self.passwd)
       # payloads = json.dumps(payload)        
        rep = request_util('post', url, headers=header, payloads=payload)
        
        print(rep)

        self.judge_user(url, header, rep)
            

    def requery_user(self,url, header):
        data = '{"query":"%s","pagenum":1,"pagesize":1}' % (self.name)
        params = json.loads(data)       
        rep = request_util('get', url, headers=header,  params=params)
        
        for v in json.loads(rep)['data']['users']: #json字符串转化为字典
            if v['username'] == self.name :
                self.idx = v['id']
        
        print (self.idx)
        

    def delete_user(self,url, header):
        
        url = url + "/" + str(self.idx)     
        rep = request_util('delete', url, headers=header)
        print(rep)
    
    def judge_user(self, url, header, rep):
        
        if '用户名已存在' in rep:
            self.requery_user(url, header)
            self.delete_user(url, header)
        if '创建成功' in rep:
            self.idx = json.loads(rep)['data']['id']
            return self.idx


def user_main(user_config = '%s/data/driven_yaml/user_config.yaml' % base_dir, extract_file = "%s/data/driven_yaml/extract.yaml" % base_dir):
    url = read_yaml(user_config)['base_url']+read_yaml(user_config)['test_users_url']
    header = '{"Authorization":"%s","Content-Type":"application/json"}' % read_yaml(extract_file)['token']
    header = eval(header)
    print(url)
    print(header)
    
    test = handle_users()
    test.add_user(url, header)
    test.delete_user(url, header)
    
    

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

    assert_util(expect, rep,run_result_txt)
    
    print("测试返回:",rep)


if __name__ == '__main__':
    '''test = users_data()
    url = 'http://127.0.0.1:8888/api/private/v1/users'
    header = {"Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjUwMCwicmlkIjowLCJpYXQiOjE2NjIwMjMyMTMsImV4cCI6MTY2MjEwOTYxM30.vR0pE9tvw_xWrANRG8d1Kdaa8Ol3kpE9hm4XbNWfh7c","Content-Type":"application/json"}
    test.add_user(url, header)
    print(test.name)
    '''
    user_main()


