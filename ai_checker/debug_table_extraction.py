"""
调试表格格式提取 - 详细版
"""
import os

def debug_table_extraction_detailed():
    """详细调试表格数据提取过程"""
    
    # 读取页面内容
    content_file = 'page_content_debug.txt'
    if not os.path.exists(content_file):
        print(f"⚠ 文件 {content_file} 不存在")
        return
    
    with open(content_file, 'r', encoding='utf-8') as f:
        web_content = f.read()
    
    lines = web_content.split('\n')
    
    print("=" * 80)
    print("调试垂直表头提取逻辑")
    print("=" * 80)
    
    # 步骤1：收集所有标签行及其索引
    label_to_index = {}
    current_index = 0
    
    known_labels = ['测评编号', 'ProdId', '测评类型', '操作系统类型', '操作系统版本号', 
                   '传播名', '设备型号', '芯片型号', '软件版本号', '提交时间', 
                   '企业名称', '测评状态', '审核人', '操作']
    
    print("\n步骤1: 收集标签行\n")
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        # 跳过空行和包含制表符的行（这些不是标签行）
        if not line_stripped or '\t' in line:
            continue
        
        # 检查这一行是否是已知的标签
        for label in known_labels:
            if label == line_stripped:
                label_to_index[label] = current_index
                print(f"  行{i:2d}: '{label}' -> 索引 {current_index}")
                current_index += 1
                break
    
    print(f"\n总共找到 {len(label_to_index)} 个标签")
    print(f"标签映射: {label_to_index}")
    
    # 步骤2：找到数据行
    print("\n步骤2: 查找数据行\n")
    data_line = None
    data_line_idx = None
    for i, line in enumerate(lines):
        if line.count('\t') >= 10:  # 数据行应该有很多制表符
            data_line = line
            data_line_idx = i
            print(f"  找到数据行 (行{i}): {line[:100]}...")
            break
    
    if not data_line:
        print("  ✗ 未找到数据行")
        return
    
    # 步骤3：解析数据行
    print("\n步骤3: 解析数据行\n")
    data_columns = data_line.split('\t')
    print(f"  列数: {len(data_columns)}")
    for j, col in enumerate(data_columns):
        print(f"    列{j}: '{col}'")
    
    # 步骤4：测试关键字提取
    print("\n步骤4: 测试关键字提取\n")
    
    test_cases = [
        ('MarketName', ['传播名']),
        ('ProductModel', ['设备型号']),
        ('DisplayVersion', ['软件版本号']),
        ('Brand', ['企业名称']),
    ]
    
    for keyword, labels in test_cases:
        print(f"\n关键字: {keyword}")
        print(f"  中文标签: {labels}")
        
        for label in labels:
            if label in label_to_index:
                col_idx = label_to_index[label]
                print(f"  ✓ 标签 '{label}' 对应索引 {col_idx}")
                
                if col_idx < len(data_columns):
                    value = data_columns[col_idx].strip()
                    print(f"  ✓ 提取到值: '{value}'")
                else:
                    print(f"  ✗ 索引 {col_idx} 超出范围 (共{len(data_columns)}列)")
                break
            else:
                print(f"  ✗ 标签 '{label}' 未在映射中找到")

if __name__ == "__main__":
    debug_table_extraction_detailed()
