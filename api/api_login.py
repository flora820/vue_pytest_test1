from common.extract_util import *    
from common.request_util import *    
from common.text_util import *    
from common.yaml_util import *    
import json    
#import allure     
#from common.log_util import LogUtil

@exception_utils
class handle_login(object):
    config_key='login'
    
    def __init__(self,config_file="%s/data/driven_yaml/user_config.yaml"% base_dir):
        self.header = read_yaml(config_file)[self.config_key]['login_header']
        self.username = read_yaml(config_file)[self.config_key]['log_user']
        self.passwd = read_yaml(config_file)[self.config_key]['log_passwd']
        self.url = read_yaml(config_file)[self.config_key]['base_url'] + read_yaml(config_file)[self.config_key]['login_url'] 

    @exception_utils
    def login(self, url, header, user, passwd):
        headers = eval(header)
        payloads = '{"username":"%s","password":"%s"}'% (user,passwd)
        rep = request_util('post',url,headers=headers,payloads=payloads)
        
        if "登录成功" in rep:       
            token = json.loads(rep)['data']['token'] 
            save_variable(key='token', value=token)



if __name__ == '__main__':
    pass
