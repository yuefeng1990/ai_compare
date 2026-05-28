"""
调试授权页面 - 查找授权按钮的正确选择器
"""
from tools.web_checker import WebChecker
import time

def debug_auth_page():
    """调试授权页面的元素"""
    
    WEB_URL = "https://compatibility.openharmony.cn/mng/index"
    web_checker = None
    
    try:
        print("="*80)
        print("🔍 授权页面调试工具")
        print("="*80)
        print("\n说明：")
        print("1. 自动打开网页并点击'立即登录'")
        print("2. 您需要手动输入用户名和密码")
        print("3. 然后程序会查找并显示所有可点击的按钮")
        print("="*80)
        
        # 启动可视化浏览器
        print("\n🚀 启动浏览器...")
        web_checker = WebChecker(headless=False)
        web_checker.launch_browser()
        
        # 打开网页
        print(f"\n🌐 打开网页: {WEB_URL}")
        web_checker.navigate_to_url(WEB_URL)
        print("✓ 网页加载成功")
        
        # 点击立即登录
        print("\n🔘 点击'立即登录'按钮...")
        time.sleep(1)
        try:
            web_checker.page.click('.btn', timeout=5000)
            print("✓ 已点击立即登录")
            time.sleep(3)  # 等待跳转到授权页面
        except Exception as e:
            print(f"⚠ 点击失败: {str(e)}")
        
        print("\n" + "="*80)
        print("👉 请在浏览器中：")
        print("   1. 输入用户名: fanqiqi@iscas.ac.cn")
        print("   2. 输入密码: iscas123.")
        print("   3. 不要点击任何按钮")
        print("   4. 完成后按回车继续")
        print("="*80)
        input("\n完成后按回车...")
        
        # 获取当前页面信息
        print(f"\n当前URL: {web_checker.page.url}")
        print(f"页面标题: {web_checker.page.title()}")
        
        # 截图
        web_checker.screenshot('auth_page.png')
        print("✓ 截图已保存到 auth_page.png")
        
        # 查找所有按钮元素
        print("\n" + "="*80)
        print("🔍 查找所有可点击元素...")
        print("="*80)
        
        # 查找button元素
        buttons = web_checker.page.query_selector_all('button')
        print(f"\n找到 {len(buttons)} 个button元素:")
        for i, btn in enumerate(buttons):
            try:
                btn_text = btn.inner_text() or '无文本'
                btn_id = btn.get_attribute('id') or '无ID'
                btn_class = btn.get_attribute('class') or '无class'
                btn_type = btn.get_attribute('type') or '无type'
                print(f"\n  Button {i+1}:")
                print(f"    文本: '{btn_text}'")
                print(f"    ID: {btn_id}")
                print(f"    Class: {btn_class}")
                print(f"    Type: {btn_type}")
            except:
                pass
        
        # 查找a链接
        links = web_checker.page.query_selector_all('a')
        print(f"\n找到 {len(links)} 个a链接元素:")
        for i, link in enumerate(links):
            try:
                link_text = link.inner_text() or '无文本'
                link_href = link.get_attribute('href') or '无href'
                link_class = link.get_attribute('class') or '无class'
                if '授权' in link_text or '登录' in link_text or 'Login' in link_text or 'Authorize' in link_text:
                    print(f"\n  Link {i+1} (可能相关):")
                    print(f"    文本: '{link_text}'")
                    print(f"    Href: {link_href[:100]}")
                    print(f"    Class: {link_class}")
            except:
                pass
        
        # 查找div和span元素
        clickable_divs = web_checker.page.query_selector_all('div.btn, div[onclick], span:has-text("授权"), span:has-text("登录")')
        print(f"\n找到 {len(clickable_divs)} 个可能的可点击div/span元素:")
        for i, elem in enumerate(clickable_divs):
            try:
                elem_text = elem.inner_text() or '无文本'
                elem_class = elem.get_attribute('class') or '无class'
                elem_onclick = elem.get_attribute('onclick') or '无onclick'
                print(f"\n  Element {i+1}:")
                print(f"    文本: '{elem_text}'")
                print(f"    Class: {elem_class}")
                print(f"    Onclick: {elem_onclick[:80] if elem_onclick != '无onclick' else '无'}")
            except:
                pass
        
        print("\n" + "="*80)
        print("✅ 调试完成！")
        print("="*80)
        print("\n请查看以上输出，找到授权按钮的正确选择器")
        print("然后更新 auto_login.py 中的 login_button_selectors 列表")
        print("\n提示：优先使用包含'授权'或'登录'文本的元素")
        
        input("\n按回车键关闭浏览器...")
        
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        if web_checker:
            print("\n🔒 关闭浏览器...")
            try:
                web_checker.close_browser()
                print("✓ 浏览器已关闭")
            except:
                pass

if __name__ == "__main__":
    debug_auth_page()
