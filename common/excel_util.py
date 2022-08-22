from pathlib import path
from openpyxl import load_workbook
from commom.exception_utils import exception_utils
import time

class ExcelUtil():
    def __init__(self, excel_path='%s/data/case_excel/接口测试框架实践用例.xlsx' % Path(__file__).parent.parent):
        self.wb = load_workbook(excel_path)

