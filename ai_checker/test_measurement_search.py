"""
快速测试脚本 - 测试测评编号搜索功能
"""
import sys
from main import main

if __name__ == "__main__":
    # 测试用例1：带测评编号参数
    print("=" * 80)
    print("测试1：使用命令行参数")
    print("=" * 80)
    
    if len(sys.argv) > 1:
        test_id = sys.argv[1]
        print(f"使用测试ID: {test_id}")
        main(test_id)
    else:
        print("未提供测试ID，使用示例ID: CP2024001")
        print("\n提示：可以通过 'python test_measurement_search.py <测评编号>' 来指定测试ID\n")
        main("CP2024001")
