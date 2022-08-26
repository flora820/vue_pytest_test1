from functools import wraps
from pathlib import Path
import yaml
from common.excel_util import ExcelUtil

base_dir = Path(__file__).parent.parent

def exception(fun):
    @wraps(fun)
    def wrapped_function(*args,**kwargs):
        try:
            return fun(*args,**kwargs)
        except Exception as e:
            print("操作yaml文件出现异常：", e)

    return wrapped_function

@exception
def read_yaml(yaml_file):
    with open(yaml_file, 'r', encoding='utf-8') as f:
        value = yaml.load(f, Loader=yaml.FullLoader)
        return value 

@exception
def write_yaml(data,yaml_file):
    with open(yaml_file, "w",encoding='utf-8') as f:
        yaml.dump(data=data, stream=f, allow_unicode=True, sort_keys=False, default_flow_style=False)

@exception
def truncate_yaml(yaml_file):
    with open(yaml_file, "w") as f:
         f.truncate()

@exception
def excel_to_yaml(excel_file):
    #"""根据读取excel数据，生成yaml的测试用例数据"""
    value, smoke = ExcelUtil(excel_file).read_excel()
    
    j = 0    
    for v in value:
        for sheetcase,total_case in v.items():
            print("%s模块中用例数：%s" % (sheetcase, len(total_case)))
            j += len(total_case)
            file = '%s/data/yaml/%s.yaml' % (base_dir, sheetcase)
            write_yaml(data=total_case, yaml_file=file)

    # 2.冒烟用例
    smoke_file = '%s/data/yaml/%s.yaml' % (base_dir, 'smoke')
    write_yaml(data=smoke, yaml_file=smoke_file)
    return j

if __name__ == '__main__':
    excel_file='%s/data/excel/vue_testcase.xlsx' % base_dir
    excel_to_yaml(excel_file)


