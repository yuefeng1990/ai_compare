"""
测试HTML结构关键字提取功能
"""
from tools.compare import CompareTool

def test_html_extraction():
    """测试从HTML结构中提取关键字"""
    
    # 模拟网页内容（包含label+text结构）
    web_content = """
    <div class="wrapper wrapper-content">
        <div class="form_div">
            <label class="label_left color-b5b5b5">品牌英文名：</label>
        </div>
        <div class="form_div mb-28">
            <text class="label_left" style="white-space: pre-wrap;">zdeer</text>
        </div>
        
        <div class="form_div">
            <label class="label_left color-b5b5b5">设备型号：</label>
        </div>
        <div class="form_div mb-28">
            <text class="label_left" style="white-space: pre-wrap;">YNS-200</text>
        </div>
        
        <div class="form_div">
            <label class="label_left color-b5b5b5">软件版本号：</label>
        </div>
        <div class="form_div mb-28">
            <text class="label_left" style="white-space: pre-wrap;">V2.0.4-3</text>
        </div>
        
        <div class="form_div">
            <label class="label_left color-b5b5b5">传播名：</label>
        </div>
        <div class="form_div mb-28">
            <text class="label_left" style="white-space: pre-wrap;">二参数融合控制器</text>
        </div>
    </div>
    """
    
    # 初始化对比工具
    compare_tool = CompareTool()
    
    # 测试关键字提取
    test_keywords = ['Brand', 'ProductModel', 'DisplayVersion', 'MarketName']
    
    print("=" * 80)
    print("测试HTML结构关键字提取")
    print("=" * 80)
    
    for keyword in test_keywords:
        print(f"\n关键字: {keyword}")
        value = compare_tool.extract_value_from_web(web_content, keyword)
        if value:
            print(f"  ✓ 提取成功: {value}")
        else:
            print(f"  ✗ 未找到")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    test_html_extraction()
