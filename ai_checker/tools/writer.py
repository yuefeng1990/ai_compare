import pandas as pd
from openpyxl import load_workbook

class ExcelWriter:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def write_results_to_excel(self, results, original_data):
        """将结果写回Excel"""
        try:
            # 创建结果DataFrame
            result_data = []
            
            for i, (url, comparison_result, popup_content, report) in enumerate(results):
                row_data = {
                    'URL': url,
                    '匹配结果': report,
                    '弹窗内容': popup_content,
                    '匹配关键字': ', '.join([k for k, v in comparison_result.items() if v]),
                    '未匹配关键字': ', '.join([k for k, v in comparison_result.items() if not v])
                }
                result_data.append(row_data)
            
            # 创建结果DataFrame
            result_df = pd.DataFrame(result_data)
            
            # 加载原始Excel文件
            book = load_workbook(self.file_path)
            writer = pd.ExcelWriter(self.file_path, engine='openpyxl')
            writer.book = book
            
            # 将结果写入新工作表
            result_df.to_excel(writer, sheet_name='检查结果', index=False)
            
            # 保存文件
            writer.save()
            
            return True
        except Exception as e:
            raise Exception(f"写入Excel失败: {str(e)}")
    
    def append_results_to_existing(self, results):
        """将结果追加到现有Excel文件"""
        try:
            # 读取现有数据
            existing_data = pd.read_excel(self.file_path)
            
            # 准备新数据
            new_data = []
            for result in results:
                new_data.append({
                    'URL': result[0],
                    '匹配结果': result[2],
                    '弹窗内容': result[1],
                    '匹配关键字': ', '.join([k for k, v in result[3].items() if v]),
                    '未匹配关键字': ', '.join([k for k, v in result[3].items() if not v])
                })
            
            new_df = pd.DataFrame(new_data)
            
            # 合并数据
            combined_df = pd.concat([existing_data, new_df], ignore_index=True)
            
            # 保存到新文件
            combined_df.to_excel(self.file_path, index=False)
            
            return True
        except Exception as e:
            raise Exception(f"追加结果到Excel失败: {str(e)}")