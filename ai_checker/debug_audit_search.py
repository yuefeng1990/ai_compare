"""
调试审核管理页面 - 在成功登录后检查页面结构
"""
from tools.web_checker import WebChecker
import time

def debug_audit_page_after_login():
    """调试审核管理页面结构（登录成功后）"""
    
    print("=" * 80)
    print("调试审核管理页面结构（登录后）")
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
        time.sleep(3)
        
        # === 执行完整登录流程 ===
        print("\n3. 执行登录流程...")
        
        # 点击立即登录
        web_checker.page.click('.btn', timeout=5000)
        time.sleep(3)
        
        # 输入用户名和密码
        web_checker.page.fill('input[placeholder*="账号"]', 'fanqiqi@iscas.ac.cn')
        web_checker.page.fill('input[type="password"]', 'iscas123.')
        
        # 点击用户登录
        web_checker.page.click('button:has-text("用户登录")', timeout=5000)
        time.sleep(3)
        
        # 点击授权
        try:
            web_checker.page.click('button:has-text("授权")', timeout=5000)
            time.sleep(3)
        except:
            pass
        
        # === 导航到审核管理页面 ===
        print("\n4. 导航到审核管理页面...")
        web_checker.page.click('text=审核管理', timeout=5000)
        time.sleep(2)
        
        # 点击"兼容性测评审核"子菜单
        print("   - 点击'兼容性测评审核'子菜单...")
        try:
            web_checker.page.click('text=兼容性测评审核', timeout=5000)
            print("   ✓ 已点击子菜单")
        except:
            print("   ⚠ 未找到子菜单")
        
        time.sleep(5)
        
        # === 获取页面详细信息 ===
        print("\n5. 获取页面详细信息...")
        
        # 滚动页面
        web_checker.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
        
        # 获取页面文本
        page_text = web_checker.get_page_text()
        print(f"   页面文本长度: {len(page_text)} 字符")
        print(f"   前500字符: {page_text[:500]}")
        
        # 保存页面内容
        with open('audit_page_after_login.txt', 'w', encoding='utf-8') as f:
            f.write(page_text)
        print(f"   ✓ 页面文本已保存到 audit_page_after_login.txt")
        
        # 查找所有输入框
        print("\n6. 查找所有输入框...")
        
        # 使用最后一个frame（有内容的）
        frames = web_checker.page.frames
        target_frame = frames[-1] if len(frames) > 1 else web_checker.page
        print(f"   使用frame: {target_frame.url}")
        
        inputs = target_frame.query_selector_all('input')
        print(f"   找到 {len(inputs)} 个输入框:")
        for i, inp in enumerate(inputs):
            try:
                input_type = inp.get_attribute('type')
                placeholder = inp.get_attribute('placeholder')
                name = inp.get_attribute('name')
                id_attr = inp.get_attribute('id')
                class_name = inp.get_attribute('class')
                visible = inp.is_visible()
                print(f"     [{i}] type='{input_type}' | placeholder='{placeholder}' | name='{name}' | id='{id_attr}' | class='{class_name}' | 可见:{visible}")
            except Exception as e:
                print(f"     [{i}] 错误: {str(e)}")
        
        # 查找包含"搜索"、"查询"、"测评编号"的元素
        print("\n7. 查找搜索相关元素...")
        search_keywords = ['搜索', '查询', '测评编号', 'search', 'query', 'filter']
        for keyword in search_keywords:
            try:
                elements = web_checker.page.query_selector_all(f'div, span, label, button')
                matching = []
                for elem in elements:
                    try:
                        text = elem.inner_text().strip()
                        if keyword.lower() in text.lower() and len(text) < 50:
                            matching.append(text)
                    except:
                        pass
                
                if matching:
                    print(f"   找到 {len(matching)} 个包含 '{keyword}' 的元素:")
                    for text in matching[:5]:
                        print(f"     - '{text}'")
            except:
                pass
        
        # 获取HTML结构
        print("\n8. 获取HTML结构...")
        html_content = web_checker.page.evaluate("document.body.innerHTML")
        with open('audit_page_after_login.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"   ✓ HTML结构已保存到 audit_page_after_login.html")
        
        print("\n" + "=" * 80)
        print("调试完成！请查看生成的文件分析页面结构")
        print("=" * 80)
        
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
    debug_audit_page_after_login()
