"""
调试登录页面结构
可视化浏览器操作，查看实际的页面元素
"""
from tools.web_checker import WebChecker
import time

def debug_login_page():
    """调试登录页面的HTML结构"""
    
    print("=" * 80)
    print("调试登录页面结构")
    print("=" * 80)
    
    web_checker = WebChecker(headless=False)
    
    try:
        # 启动浏览器
        print("\n1. 启动浏览器...")
        web_checker.launch_browser()
        print("   ✓ 浏览器已启动")
        
        # 导航到首页
        print("\n2. 导航到首页...")
        web_checker.page.goto("https://compatibility.openharmony.cn/mng/index", timeout=30000)
        print("   ✓ 页面加载完成")
        
        # 等待页面稳定
        time.sleep(3)
        
        # 获取页面内容
        print("\n3. 获取页面HTML内容...")
        page_content = web_checker.get_page_text()
        print(f"   页面文本长度: {len(page_content)} 字符")
        
        # 保存页面内容
        with open('login_page_debug.txt', 'w', encoding='utf-8') as f:
            f.write(page_content)
        print(f"   ✓ 页面内容已保存到 login_page_debug.txt")
        
        # 查找所有按钮和输入框
        print("\n4. 查找页面中的按钮和输入框...")
        
        # 获取所有按钮
        buttons = web_checker.page.query_selector_all('button, [role="button"], .btn, div.btn')
        print(f"\n   找到 {len(buttons)} 个按钮元素:")
        for i, btn in enumerate(buttons[:10]):  # 只显示前10个
            try:
                text = btn.inner_text()
                visible = btn.is_visible()
                print(f"     [{i}] 文本: '{text}' | 可见: {visible}")
            except:
                print(f"     [{i}] (无法获取文本)")
        
        # 获取所有输入框
        inputs = web_checker.page.query_selector_all('input')
        print(f"\n   找到 {len(inputs)} 个输入框元素:")
        for i, inp in enumerate(inputs[:10]):  # 只显示前10个
            try:
                input_type = inp.get_attribute('type')
                placeholder = inp.get_attribute('placeholder')
                name = inp.get_attribute('name')
                id_attr = inp.get_attribute('id')
                visible = inp.is_visible()
                print(f"     [{i}] type='{input_type}' | placeholder='{placeholder}' | name='{name}' | id='{id_attr}' | 可见: {visible}")
            except:
                print(f"     [{i}] (无法获取属性)")
        
        # 获取完整的HTML结构（只提取body部分）
        print("\n5. 获取页面HTML结构...")
        html_content = web_checker.page.evaluate("document.body.innerHTML")
        with open('login_page_html.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"   ✓ HTML结构已保存到 login_page_html.html")
        
        print("\n" + "=" * 80)
        print("调试完成！请查看生成的文件分析页面结构")
        print("=" * 80)
        
        # 保持浏览器打开，方便手动查看
        input("\n按 Enter 键关闭浏览器...")
        
    except Exception as e:
        print(f"\n✗ 调试失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            web_checker.close()
            print("✓ 浏览器已关闭")
        except:
            pass

if __name__ == "__main__":
    debug_login_page()
