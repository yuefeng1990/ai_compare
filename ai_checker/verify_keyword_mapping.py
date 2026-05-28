"""
验证中英文关键字映射关系的正确性
"""

def verify_keyword_mapping():
    """验证关键字映射是否符合用户要求"""
    
    # 用户提供的标准对照关系
    expected_mapping = {
        'DeviceType': '设备类型',
        'Manufacture': '企业简称（英文）',
        'SecurityPatchTag': '安全补丁标签',
        'BuildRootHash': '版本Hash',
        'MarketName': '设备名称（传播名）',
        'ProductModel': '设备型号',
        'Brand': '品牌英文名',
        'DisplayVersion': '软件版本号',
        'VersionId': '版本Id',
        'OsFullName': '操作系统版本号'
    }
    
    # 当前代码中的映射（从 compare.py 中提取）
    current_mapping = {
        'MarketName': ['设备名称（传播名）', '设备名称', '传播名'],
        'ProductModel': ['设备型号', '产品型号', '型号'],
        'DeviceType': ['设备类型'],
        'Brand': ['品牌英文名', '品牌英文名称', '品牌'],
        'Manufacture': ['企业简称（英文）', '企业简称', '英文简称', 'Manufacturer'],
        'DisplayVersion': ['软件版本号', '显示版本', '软件版本'],
        'SecurityPatchTag': ['安全补丁标签', '安全补丁', '补丁标签'],
        'VersionId': ['版本Id', '版本ID', '版本标识', 'ProdId'],
        'BuildRootHash': ['版本Hash', '版本哈希', '根哈希', 'Hash'],
        'OsFullName': ['操作系统版本号', '系统版本', 'OS版本']
    }
    
    print("=" * 80)
    print("验证中英文关键字映射关系")
    print("=" * 80)
    
    all_correct = True
    
    for keyword, expected_label in expected_mapping.items():
        if keyword in current_mapping:
            labels = current_mapping[keyword]
            
            # 检查期望的标签是否在候选列表中
            if expected_label in labels:
                status = "✓"
            else:
                status = "✗"
                all_correct = False
            
            print(f"\n{status} {keyword:20s}")
            print(f"  期望标签: {expected_label}")
            print(f"  当前映射: {labels}")
            
            if status == "✗":
                print(f"  ⚠️  警告: 期望标签 '{expected_label}' 不在映射列表中！")
        else:
            print(f"\n✗ {keyword:20s}")
            print(f"  期望标签: {expected_label}")
            print(f"  当前映射: [未定义]")
            all_correct = False
    
    print("\n" + "=" * 80)
    if all_correct:
        print("✅ 所有关键字映射关系正确！")
    else:
        print("❌ 发现映射关系错误，请修正！")
    print("=" * 80)
    
    # 额外检查：列表页中存在的字段
    print("\n" + "=" * 80)
    print("列表页中实际存在的字段（从 page_content_debug.txt 分析）")
    print("=" * 80)
    
    list_page_fields = [
        '测评编号', 'ProdId', '测评类型', '操作系统类型', '操作系统版本号',
        '传播名', '设备型号', '芯片型号', '软件版本号', '提交时间',
        '企业名称', '测评状态', '审核人', '操作'
    ]
    
    print("\n列表页字段列表:")
    for field in list_page_fields:
        print(f"  - {field}")
    
    print("\n与关键字映射的对应关系:")
    field_to_keyword = {
        '传播名': 'MarketName',
        '设备型号': 'ProductModel',
        '操作系统版本号': 'OsFullName',
        '软件版本号': 'DisplayVersion',
        'ProdId': 'VersionId',
        '企业名称': '⚠️  注意: 此字段不对应任何关键字（Brand对应的是"品牌英文名"）',
    }
    
    for field, keyword in field_to_keyword.items():
        print(f"  {field:15s} → {keyword}")
    
    print("\n⚠️  重要提示:")
    print("  列表页中没有以下字段（需要从详情页获取）:")
    missing_fields = ['设备类型', '品牌英文名', '企业简称（英文）', '安全补丁标签', '版本Hash']
    for field in missing_fields:
        print(f"    - {field}")

if __name__ == "__main__":
    verify_keyword_mapping()
