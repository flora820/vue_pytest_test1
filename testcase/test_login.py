import pytest
from common.extract_util import extract_util
from common.request_util import request_util 
from common.text_util import *
from common.yaml_util import *
import json
#import allure
#from common.log_util import LogUtil



@pytest.mark.run(order=1)
@pytest.mark.all
@pytest.mark.parametrize('args', extract_util('%s/data/yaml/login.yaml' % base_dir))

def test_login():
    url = args[url]
