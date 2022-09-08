from datetime import datetime
from py.xml import html
import pytest
from common.text_util import *
from common.yaml_util import excel_to_yaml
from common.excel_util import *
from common.log_util import *

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
#    truncate_txt("%s/data/driven_yaml/extract.yaml" % base_dir)
    yield
    print("\n用例运行后置操作：")



@pytest.mark.parametrize
def pytest_configure(config):
    config._metadata["项目名称"] = "vue自动化" # 添加项目名称
    config._metadata["接口地址"] = "http://127.0.0.1:8888/" # 添加接口地址

@pytest.mark.parametrize
def pytest_html_results_summary(prefix,summary,postfix):
    prefix.extend([html.p("所属部门：测试组")])
    prefix.extend([html.p("测试人员：flora")])

@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Description'))
    cells.insert(1, html.th('Time', class_='sortable time', col='time'))
    cells.pop()

@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(report.description))
    cells.insert(1, html.td(datetime.utcnow(), class_='col-time'))
    cells.pop()

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
