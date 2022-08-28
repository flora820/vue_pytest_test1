import re
from common.exception_utils import exception_utils
from common.text_util import *
from common.yaml_util import *



@exception_utils
def extract_util(case_file, extract_file='%s/data/driven_yaml/extract.yaml' % base_dir, \
        user_yamlfile='%s/data/driven_yaml/user_config.yaml' % base_dir):
    
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
    
    value_cases = str(read_yaml(case_file))
    print(value_cases)

#匹配表达式${}
    p = r'\$\{(.*?)\}'
    match_list = list(set(re.findall(p, value_cases)))
    print (match_list)

    global value_extract_keys, value_extract, total_extract
    total_extract = {}

    value_extract = read_yaml(extract_file)
    value_user = read_yaml(user_yamlfile)
    print(value_extract)
    print(value_user)

    if  value_extract:
        total_extract.update(value_extract)
    
    if value_user:
        total_extract.update(value_user)
    print (total_extract)

    for m in match_list:
        if m in list(total_extract.keys()):
           print(m) 


if __name__ == '__main__':
    case_file = '%s/data/yaml/user.yaml' % base_dir
    extract_file = '%s/data/driven_yaml/extract.yaml' % base_dir
    rep = extract_util(case_file,extract_file)
    print(rep)

    
