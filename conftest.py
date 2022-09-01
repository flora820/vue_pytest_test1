import pytest
from common.text_util import *
from common.yaml_util import excel_to_yaml
from common.excel_util import *


@pytest.fixture(scope="function")
def login():
    print("用例运行前，先登录")
    url='http://127.0.0.1:8888/api/private/v1/login'

@pytest.fixture(scope='session', autouse=True)
def my_fixture():
    
    print("同步用例")
    j = excel_to_yaml('%s/data/excel/vue_testcase.xlsx'% base_dir)  # 总用例数
    print("\n用例运行前置操作：")
    print("1.清空run_result.txt文件")
    truncate_txt("%s/data/run_result.txt" % base_dir)
   # print("2.清空extract_save.txt文件")
   # truncate_txt("%s/data/extract_save.txt" % base_dir)
  #  print("3.清空extract_replace.txt文件")
   # truncate_txt("%s/data/extract_replace.txt" % base_dir)
    print("4.清空extract.ymal文件")
    truncate_txt("%s/data/driven_yaml/extract.yaml" % base_dir)
    yield
    print("\n用例运行后置操作：")
