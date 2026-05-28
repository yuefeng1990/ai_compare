"""
快速测试wrapper元素检测
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from tools.web_checker import WebChecker
from auto_login import automate_browser_with_search
import time

def test_wrapper_detection():
    """测试wrapper元素检测"""
    measurement_id = "OHC443600006741"
    web_checker = None
    
    try:
        print("=" * 80)
        print("测试wrapper元素检测")
        print("=" * 80)
        
        # 启动浏览器
        print("\n1. 启动浏览器...")
        web_checker = WebChecker(headless=False)
        web_checker.launch_browser()
        
        # 执行自动化登录和搜索
        print(f"\n2. 执行自动化操作（测评编号: {measurement_id}）...")
        web_checker.navigate_to_url("https://compatibility.openharmony.cn/mng/index")
        automate_browser_with_search(web_checker, measurement_id)
        
        # 等待详情页加载
        print("\n3. 等待详情页加载...")
        time.sleep(5)
        
        # 检测wrapper元素
        print("\n4. 检测wrapper元素...")
        
        # 检查所有iframe
        all_iframes = web_checker.page.query_selector_all('iframe')
        print(f"   - 检测到 {len(all_iframes)} 个iframe")
        
        for i, iframe in enumerate(all_iframes):
            iframe_name = iframe.get_attribute('name') or '无名'
            iframe_src = iframe.get_attribute('src') or '无src'
            print(f"     iframe{i+1}: name='{iframe_name}', src='{iframe_src}'")
            
            # 在每个iframe中查找wrapper
            try:
                frame_locator = web_checker.page.frame_locator(f'iframe[name="{iframe_name}"]')
                wrapper_count = frame_locator.locator('div.wrapper.wrapper-content').count()
                print(f"       - wrapper元素数量: {wrapper_count}")
                
                if wrapper_count > 0:
                    print(f"       ✓ 在iframe{i+1}中找到wrapper元素！")
                    
                    # 提取wrapper内容
                    wrapper_text = frame_locator.locator('div.wrapper.wrapper-content').first.inner_text(timeout=5000)
                    print(f"       ✓ 提取到 {len(wrapper_text)} 字符的内容")
                    
                    # 保存前500字符
                    preview = wrapper_text[:500] if len(wrapper_text) > 500 else wrapper_text
                    print(f"\n       内容预览:\n{preview}\n")
                    
                    # 保存到文件
                    with open('wrapper_content.txt', 'w', encoding='utf-8') as f:
                        f.write(wrapper_text)
                    print(f"       ✓ 完整内容已保存到 wrapper_content.txt")
                    
            except Exception as e:
                print(f"       ⚠ 检查失败: {str(e)}")
        
        print("\n" + "=" * 80)
        print("测试完成！")
        print("=" * 80)
        
        input("\n按回车键关闭浏览器...")
        
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        if web_checker:
            try:
                web_checker.close_browser()
            except:
                pass

if __name__ == "__main__":
    test_wrapper_detection()
