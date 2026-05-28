"""
测试版本号前缀提取功能
"""
import re

def extract_os_version_prefix(version_string):
    """从版本字符串中提取前两位版本号"""
    
    # 匹配模式：系统名称 + 主版本号.次版本号
    pattern = r'^([a-zA-Z\u4e00-\u9fa5]+)\s+(\d+\.\d+)'
    match = re.search(pattern, version_string)
    
    print(f"测试: {version_string}")
    print(f"  正则表达式: {pattern}")
    print(f"  匹配结果: {match}")
    
    if match:
        system_name = match.group(1)
        version_prefix = match.group(2)
        result = f"{system_name} {version_prefix}"
        print(f"  ✓ 提取成功: {result}")
        return result
    
    # 如果没有匹配到，尝试更宽松的模式（只要有数字.数字）
    pattern_loose = r'(\d+\.\d+)'
    match_loose = re.search(pattern_loose, version_string)
    print(f"  宽松模式: {pattern_loose}")
    print(f"  宽松匹配: {match_loose}")
    
    if match_loose:
        result = match_loose.group(1)
        print(f"  ✓ 宽松提取成功: {result}")
        return result
    
    # 完全无法提取，返回原字符串
    print(f"  ✗ 无法提取，返回原字符串")
    return version_string

if __name__ == "__main__":
    print("=" * 80)
    print("测试版本号前缀提取")
    print("=" * 80)
    
    test_cases = [
        "OpenHarmony-5.1.0.0",
        "OpenHarmony 5.1.0 Release",
        "Android 12.0.0",
    ]
    
    for version in test_cases:
        prefix = extract_os_version_prefix(version)
        print(f"  最终结果: {prefix}\n")
