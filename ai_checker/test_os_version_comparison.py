"""
测试OsFullName版本号比较逻辑
"""
from tools.compare import CompareTool

def test_os_version_comparison():
    """测试操作系统版本号的智能比较"""
    
    compare_tool = CompareTool()
    
    print("=" * 80)
    print("测试OsFullName版本号比较逻辑")
    print("=" * 80)
    
    # 测试用例：(log版本, web版本, 预期结果, 说明)
    test_cases = [
        # 相同前缀，应该返回True
        ("OpenHarmony 5.1.0 Release", "OpenHarmony 5.1.2", True, "相同主版本和次版本"),
        ("OpenHarmony 5.1.0", "OpenHarmony 5.1.0 Release", True, "相同完整版本"),
        ("Android 12.0.0", "Android 12.0.5", True, "Android相同前缀"),
        ("iOS 16.5.1", "iOS 16.5.3", True, "iOS相同前缀"),
        
        # 不同前缀，应该返回False
        ("OpenHarmony 5.1.0", "OpenHarmony 5.2.0", False, "次版本不同"),
        ("OpenHarmony 5.1.0", "OpenHarmony 6.0.0", False, "主版本不同"),
        ("Android 12.0.0", "Android 13.0.0", False, "Android主版本不同"),
        
        # 边界情况
        ("OpenHarmony 5.1.0 Release", "openharmony 5.1.2", True, "不区分大小写"),
        ("", "OpenHarmony 5.1.0", False, "空值"),
        (None, "OpenHarmony 5.1.0", False, "None值"),
    ]
    
    success_count = 0
    total_count = len(test_cases)
    
    for i, (log_ver, web_ver, expected, description) in enumerate(test_cases, 1):
        result = compare_tool.compare_values(log_ver, web_ver, keyword='OsFullName')
        status = "✓" if result == expected else "✗"
        
        if result == expected:
            success_count += 1
        
        print(f"\n测试{i}: {description}")
        print(f"  Log版本: {log_ver or '(空)'}")
        print(f"  Web版本: {web_ver or '(空)'}")
        print(f"  预期: {expected}, 实际: {result}")
        print(f"  {status} {'通过' if result == expected else '失败'}")
    
    print("\n" + "=" * 80)
    print(f"测试结果: {success_count}/{total_count} 通过")
    print("=" * 80)
    
    if success_count == total_count:
        print("\n🎉 所有测试通过！")
    else:
        print(f"\n⚠ 有 {total_count - success_count} 个测试失败")
    
    # 测试版本前缀提取
    print("\n" + "=" * 80)
    print("测试版本前缀提取功能")
    print("=" * 80)
    
    extraction_tests = [
        "OpenHarmony 5.1.0 Release",
        "OpenHarmony 5.1.2",
        "Android 12.0.0",
        "iOS 16.5.1",
        "Windows 11.0.22000",
        "macOS 13.4.1",
    ]
    
    for version in extraction_tests:
        prefix = compare_tool._extract_os_version_prefix(version)
        print(f"  {version:40s} -> {prefix}")

if __name__ == "__main__":
    test_os_version_comparison()
