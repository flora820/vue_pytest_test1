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
    config_key='users'

    def __init__(self,user_config = '%s/data/driven_yaml/user_config.yaml' % base_dir):
        self.name = read_yaml(user_config)[self.config_key]['test_user']
        self.passwd = read_yaml(user_config)[self.config_key]['test_passwd']

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
