import re
from common.exception_utils import exception_utils
from common.text_util import *
from common.yaml_util import *
import json



@exception_utils
def extract_util(case_file, extract_file='%s/data/driven_yaml/extract.yaml' % base_dir, \
        user_yamlfile='%s/data/driven_yaml/user_config.yaml' % base_dir, user_list=None):
    
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
    excel_to_yaml('%s/data/excel/vue_testcase.xlsx'% base_dir)

 # 运行用例
    value_cases = str(read_yaml(case_file))

#匹配表达式${}
    p = r'\$\{(.*?)\}'
    match_list = list(set(re.findall(p, value_cases)))

    global value_extract_keys, value_extract, total_extract
    total_extract = {}
    total_user = {}

    value_extract = read_yaml(extract_file)
    value_user = read_yaml(user_yamlfile)
    for i in range(len(user_list)):
        if (value_user[user_list[i]]):
            total_user.update(value_user[user_list[i]]) 
    #print(value_extract)
    #print(value_user)

    if  value_extract:
        total_extract.update(value_extract)
    
    if value_user:
        total_extract.update(total_user)


    for m in match_list:
        if m in list(total_extract.keys()):
            p1 = r'\${%s}' % m
            value_cases = re.sub(p1, total_extract[m], value_cases)
    
    return list(eval(value_cases).values())[0]

@exception_utils
def save_variable(key, value):
    extract_file='%s/data/driven_yaml/extract.yaml' % base_dir
    set_dict = {}
    set_dict[key] = value
    write_yaml(set_dict, extract_file)


@exception_utils
def extract_case(case, config_dict=None, config_file=None):
    
    p = r'\$\{(.*?)\}'
    match_list = list(set(re.findall(p, json.dumps(case))))
    print (match_list)
    
    total_extract = {}
    value_user = None
    if config_file : 
        value_user = read_yaml(config_file)
        
    if value_user:
        total_extract.update(value_user)
    if config_dict:
        total_extract.update(config_dict)

    
    for m in match_list:
        if m in list(total_extract.keys()):
            p1 = r'\${%s}' % m
            case = re.sub(p1, str(total_extract[m]), case)
    
    return case


if __name__ == '__main__':
    
    case_file = '%s/data/yaml/user.yaml' % base_dir
    extract_file = '%s/data/driven_yaml/extract_bk.yaml' % base_dir
    rep = extract_util(case_file,extract_file)
    print(rep)
    
    #set_variable('test_qw', 'happyeveryday') 
