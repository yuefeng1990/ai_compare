"""
调试审核管理页面结构
在登录成功后，检查审核管理页面的HTML结构，找到正确的搜索框选择器
"""
from tools.web_checker import WebChecker
import time

def debug_audit_page():
    """调试审核管理页面结构"""
    
    print("=" * 80)
    print("调试审核管理页面结构")
    print("=" * 80)
    
    web_checker = WebChecker(headless=False)
    
    try:
        # 启动浏览器
        print("\n1. 启动浏览器...")
        web_checker.launch_browser()
        print("   ✓ 浏览器已启动")
        
        # 导航到首页
        print("\n2. 导航到首页...")
        web_checker.navigate_to_url("https://compatibility.openharmony.cn/mng/index")
        print("   ✓ 页面加载完成")
        time.sleep(3)
        
        # === 执行登录流程 ===
        print("\n3. 执行登录流程...")
        
        # 点击立即登录
        print("   - 点击立即登录按钮...")
        try:
            web_checker.page.click('.btn', timeout=5000)
            print("   ✓ 已点击立即登录")
            time.sleep(3)
        except:
            print("   ⚠ 未找到立即登录按钮")
        
        # 输入用户名
        print("   - 输入用户名...")
        web_checker.page.fill('input[placeholder*="账号"]', 'fanqiqi@iscas.ac.cn')
        print("   ✓ 用户名已输入")
        
        # 输入密码
        print("   - 输入密码...")
        web_checker.page.fill('input[type="password"]', 'iscas123.')
        print("   ✓ 密码已输入")
        
        # 点击用户登录
        print("   - 点击用户登录按钮...")
        web_checker.page.click('button:has-text("用户登录")', timeout=5000)
        print("   ✓ 已点击用户登录")
        time.sleep(3)
        
        # 点击授权
        print("   - 点击授权按钮...")
        try:
            web_checker.page.click('button:has-text("授权")', timeout=5000)
            print("   ✓ 已点击授权")
            time.sleep(3)
        except:
            print("   ⚠ 未找到授权按钮或已自动跳转")
        
        # === 导航到审核管理页面 ===
        print("\n4. 导航到审核管理页面...")
        
        # 点击审核管理菜单
        print("   - 点击审核管理菜单...")
        try:
            # 使用 JavaScript 点击以避免元素拦截
            web_checker.page.evaluate('''
                () => {
                    const el = document.querySelector('a:has-text("审核管理")');
                    if (el) el.click();
                }
            ''')
            print("   ✓ 已点击审核管理菜单")
            time.sleep(3)
        except Exception as e:
            print(f"   ⚠ 点击失败: {str(e)}")
            # 尝试直接导航
            print("   - 尝试直接导航...")
            web_checker.page.goto("https://compatibility.openharmony.cn/mng/audit", timeout=30000)
            time.sleep(3)
        
        # === 获取页面内容 ===
        print("\n5. 获取页面内容...")
        
        # 滚动页面触发懒加载
        web_checker.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
        
        # 获取页面文本
        page_text = web_checker.get_page_text()
        print(f"   页面文本长度: {len(page_text)} 字符")
        
        # 保存页面内容
        with open('audit_page_debug.txt', 'w', encoding='utf-8') as f:
            f.write(page_text)
        print(f"   ✓ 页面文本已保存到 audit_page_debug.txt")
        
        # 查找所有输入框
        print("\n6. 查找页面中的输入框...")
        inputs = web_checker.page.query_selector_all('input')
        print(f"   找到 {len(inputs)} 个输入框:")
        for i, inp in enumerate(inputs[:15]):  # 显示前15个
            try:
                input_type = inp.get_attribute('type')
                placeholder = inp.get_attribute('placeholder')
                name = inp.get_attribute('name')
                id_attr = inp.get_attribute('id')
                class_name = inp.get_attribute('class')
                visible = inp.is_visible()
                print(f"     [{i}] type='{input_type}' | placeholder='{placeholder}' | name='{name}' | id='{id_attr}' | class='{class_name}' | 可见:{visible}")
            except:
                print(f"     [{i}] (无法获取属性)")
        
        # 获取HTML结构
        print("\n7. 获取HTML结构...")
        html_content = web_checker.page.evaluate("document.body.innerHTML")
        with open('audit_page_html.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"   ✓ HTML结构已保存到 audit_page_html.html")
        
        # 查找包含"搜索"、"查询"、"测评编号"的元素
        print("\n8. 查找搜索相关元素...")
        search_keywords = ['搜索', '查询', '测评编号', 'search', 'query']
        for keyword in search_keywords:
            try:
                elements = web_checker.page.query_selector_all(f'div:has-text("{keyword}"), span:has-text("{keyword}"), label:has-text("{keyword}")')
                if elements:
                    print(f"   找到 {len(elements)} 个包含 '{keyword}' 的元素:")
                    for elem in elements[:5]:
                        try:
                            text = elem.inner_text().strip()
                            print(f"     - '{text}'")
                        except:
                            pass
            except:
                pass
        
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
    debug_audit_page()
