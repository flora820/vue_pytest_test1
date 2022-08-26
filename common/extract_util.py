import re
from common.exception_utils import exception_utils
from common.text_util import *
from common.yaml_util import *



@exception_utils
def extract_util(case_file, extract_file='%s/data/driven_yaml/extract.yaml'%s base_dir, \
        user_yamlfile='%s/data/driven_yaml/user_config.yaml')
    
    """
    数据关联的公共方法
    思路:
    1.运行用例前，检查用例yaml中是否有${}
    2.有，则检查${}中的变量是否存在于extract.yaml中
    3.有，则替换；无，则不变，或设置默认值
    4.内存中覆盖yaml中读取的值
    5.再进行数据驱动

    返回——>替换${变量}后的数据
    """

 # 运行用例
    text_file = '%s/data/extract_replace.txt' % base_dir



    
