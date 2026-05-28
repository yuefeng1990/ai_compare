"""
完整流程测试 - 包含真实网页内容
"""
from tools.compare import CompareTool
import os

def test_with_real_content():
    """使用真实的页面内容进行测试"""
    
    # 读取之前保存的页面内容
    content_file = 'page_content_debug.txt'
    if not os.path.exists(content_file):
        print(f"⚠ 文件 {content_file} 不存在，请先运行自动化脚本生成")
        return
    
    with open(content_file, 'r', encoding='utf-8') as f:
        web_content = f.read()
    
    print("=" * 80)
    print("使用真实页面内容测试关键字提取")
    print("=" * 80)
    print(f"\n页面内容长度: {len(web_content)} 字符\n")
    
    # 显示前500字符预览
    preview = web_content[:500] if len(web_content) > 500 else web_content
    print(f"内容预览:\n{preview}\n")
    print("-" * 80)
    
    # 初始化对比工具
    compare_tool = CompareTool()
    
    # 建立英文关键字到中文标签的映射（与compare.py中保持一致）
    keyword_mapping = {
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
    
    # 测试所有关键字
    test_keywords = list(keyword_mapping.keys())
    
    results = {}
    success_count = 0
    
    print("\n开始提取关键字...\n")
    
    for keyword in test_keywords:
        chinese_labels = keyword_mapping[keyword]
        print(f"关键字: {keyword}")
        print(f"  中文标签: {', '.join(chinese_labels)}")
        
        value = compare_tool.extract_value_from_web(web_content, keyword)
        if value:
            print(f"  ✓ 提取成功: {value}")
            results[keyword] = value
            success_count += 1
        else:
            print(f"  ✗ 未找到")
            results[keyword] = None
        print()
    
    print("=" * 80)
    print(f"测试结果汇总: {success_count}/{len(test_keywords)} 成功")
    print("=" * 80)
    
    # 显示所有结果
    print("\n提取结果:")
    for keyword, value in results.items():
        status = "✓" if value else "✗"
        chinese_labels = keyword_mapping[keyword]
        print(f"  {status} {keyword:20s}: {value or '未找到'}")
        print(f"      对应中文: {', '.join(chinese_labels)}")
    
    # 如果有失败的关键字，提供调试建议
    failed_keywords = [k for k, v in results.items() if v is None]
    if failed_keywords:
        print(f"\n⚠ 有 {len(failed_keywords)} 个关键字未找到:")
        for kw in failed_keywords:
            chinese_labels = keyword_mapping[kw]
            print(f"   - {kw} (中文标签: {', '.join(chinese_labels)})")
        print("\n建议:")
        print("  1. 检查页面内容是否包含这些字段")
        print("  2. 查看 page_content_debug.txt 确认HTML结构")
        print("  3. 可能需要调整正则表达式或添加新的HTML模式")
        print("  4. 确认中文标签是否与页面实际显示一致")
    else:
        print("\n🎉 所有关键字都成功提取！")

if __name__ == "__main__":
    test_with_real_content()
