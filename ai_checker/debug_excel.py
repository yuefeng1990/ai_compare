"""
调试Excel文件结构，查看列名和数据
"""
import pandas as pd
import os

def debug_excel_structure():
    """检查Excel文件的结构"""
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(current_dir, 'data', 'checklist.xlsx')
    
    print("=" * 80)
    print("调试Excel文件结构")
    print("=" * 80)
    
    # 读取完整的Excel文件（不跳过任何行）
    print("\n1. 读取完整Excel文件（前5行）...")
    df_full = pd.read_excel(excel_path, sheet_name=0)
    print(f"总行数: {len(df_full)}")
    print(f"总列数: {len(df_full.columns)}")
    print(f"\n列名列表:")
    for i, col in enumerate(df_full.columns):
        print(f"  列{i}: '{col}'")
    
    print(f"\n前5行数据:")
    print(df_full.head().to_string())
    
    # 读取从第5行开始的数据
    print("\n\n2. 读取从第5行开始的数据（skiprows=4）...")
    df_skip = pd.read_excel(excel_path, sheet_name=0, skiprows=4)
    print(f"总行数: {len(df_skip)}")
    print(f"总列数: {len(df_skip.columns)}")
    print(f"\n列名列表:")
    for i, col in enumerate(df_skip.columns):
        print(f"  列{i}: '{col}'")
    
    print(f"\n前5行数据:")
    print(df_skip.head().to_string())
    
    # 检查测评编号列
    print("\n\n3. 检查测评编号列...")
    possible_columns = ['测评编号', 'certificationNumber', 'CertificationNumber', 'ID', '编号']
    
    for col_name in possible_columns:
        if col_name in df_skip.columns:
            print(f"✓ 找到列: '{col_name}'")
            print(f"  前5个值:")
            for i, val in enumerate(df_skip[col_name].head()):
                print(f"    行{i+1}: '{val}' (类型: {type(val).__name__})")
            break
    else:
        print("✗ 未找到可能的测评编号列")
        print(f"  所有列名: {list(df_skip.columns)}")

if __name__ == "__main__":
    debug_excel_structure()
