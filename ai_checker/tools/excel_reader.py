import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows

class ExcelReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
    
    def read_excel(self, sheet_name=0):
        """读取Excel文件"""
        try:
            # skiprows=4 跳过前4行（从第5行开始读取）
            # sheet_name=0 默认读取第一个工作表
            self.data = pd.read_excel(self.file_path, sheet_name=sheet_name, skiprows=4)
            return self.data
        except Exception as e:
            raise Exception(f"读取Excel文件失败: {str(e)}")
    
    def get_column_data(self, column_index):
        """获取指定列的数据（使用列索引）"""
        if self.data is None:
            raise Exception("Excel数据未加载")
        
        # 使用iloc通过列索引获取数据
        return self.data.iloc[:, column_index].tolist()
    
    def get_description_column(self):
        """获取E列描述内容（第5列，索引为4）"""
        if self.data is None:
            raise Exception("Excel数据未加载")
        
        # E列是第5列，索引为4
        return self.get_column_data(4)
    
    def get_url_column(self):
        """获取URL列（第6列，索引为5）"""
        if self.data is None:
            raise Exception("Excel数据未加载")
        
        # F列是第6列，索引为5
        return self.get_column_data(5)
    
    def get_test_data(self):
        """获取测试数据"""
        if self.data is None:
            raise Exception("Excel数据未加载")
        
        return self.data.to_dict('records')