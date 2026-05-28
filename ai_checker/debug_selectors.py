"""
调试脚本 - 查找正确的CSS选择器
"""
from tools.web_checker import WebChecker
import time

def debug_selectors():
    """调试并查找正确的选择器"""
    
    WEB_URL = "https://compatibility.openharmony.cn/mng/index"
    
    web_checker = None
    
    try:
        print("="*80)
        print("🔍 CSS选择器调试工具")
        print("="*80)
        
        # 启动可视化浏览器
        print("\n启动浏览器...")
        web_checker = WebChecker(headless=False)
        web_checker.launch_browser()
        
        # 打开网页
        print(f"打开网页: {WEB_URL}")
        web_checker.navigate_to_url(WEB_URL)
        
        print("\n等待页面加载...")
        time.sleep(3)
        
        # 获取页面HTML结构
        print("\n获取页面HTML...")
        html_content = web_checker.get_page_content()
        
        # 保存HTML供分析
        with open('login_page.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("✓ HTML已保存到 login_page.html")
        
        # 尝试查找输入框
        print("\n尝试查找用户名输入框...")
        try:
            # 方法1: 查找所有input元素
            inputs = web_checker.page.query_selector_all('input')
            print(f"找到 {len(inputs)} 个input元素")
            for i, inp in enumerate(inputs):
                input_type = inp.get_attribute('type') or 'text'
                input_id = inp.get_attribute('id') or '无ID'
                input_name = inp.get_attribute('name') or '无name'
                input_placeholder = inp.get_attribute('placeholder') or '无placeholder'
                input_class = inp.get_attribute('class') or '无class'
                print(f"  Input {i+1}: type={input_type}, id={input_id}, name={input_name}")
                print(f"           placeholder={input_placeholder}")
                print(f"           class={input_class}")
        except Exception as e:
            print(f"查找input失败: {str(e)}")
        
        # 尝试查找所有可点击元素（button, a, div等）
        print("\n尝试查找可点击元素...")
        try:
            # 查找button元素
            buttons = web_checker.page.query_selector_all('button')
            print(f"找到 {len(buttons)} 个button元素")
            for i, btn in enumerate(buttons):
                btn_text = btn.inner_text() or '无文本'
                btn_id = btn.get_attribute('id') or '无ID'
                btn_class = btn.get_attribute('class') or '无class'
                print(f"  Button {i+1}: text='{btn_text}', id={btn_id}")
                print(f"              class={btn_class}")
            
            # 查找a链接元素
            links = web_checker.page.query_selector_all('a')
            print(f"\n找到 {len(links)} 个a链接元素")
            for i, link in enumerate(links):
                link_text = link.inner_text() or '无文本'
                link_href = link.get_attribute('href') or '无href'
                link_id = link.get_attribute('id') or '无ID'
                link_class = link.get_attribute('class') or '无class'
                print(f"  Link {i+1}: text='{link_text[:50]}', href={link_href[:80]}")
                print(f"           id={link_id}, class={link_class}")
            
            # 查找有onclick事件的div元素
            clickable_divs = web_checker.page.query_selector_all('div[onclick], .btn, [role="button"]')
            print(f"\n找到 {len(clickable_divs)} 个可点击的div元素")
            for i, div in enumerate(clickable_divs):
                div_text = div.inner_text() or '无文本'
                div_id = div.get_attribute('id') or '无ID'
                div_class = div.get_attribute('class') or '无class'
                div_onclick = div.get_attribute('onclick') or '无onclick'
                print(f"  Div {i+1}: text='{div_text[:50]}'")
                print(f"          id={div_id}, class={div_class}")
                print(f"          onclick={div_onclick[:80] if div_onclick != '无onclick' else '无'}")
                
        except Exception as e:
            print(f"查找可点击元素失败: {str(e)}")
        
        print("\n" + "="*80)
        print("请在浏览器中查看页面结构，然后按回车继续...")
        print("="*80)
        input()
        
        # 截图
        web_checker.screenshot('login_debug.png')
        print("\n✓ 截图已保存到 login_debug.png")
        
        print("\n请查看以下文件以确定正确的选择器：")
        print("  1. login_page.html - 完整HTML")
        print("  2. login_debug.png - 页面截图")
        print("  3. 上方输出的input和button信息")
        
        input("\n按回车键关闭浏览器...")
        
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        if web_checker:
            web_checker.close_browser()

if __name__ == "__main__":
    debug_selectors()
