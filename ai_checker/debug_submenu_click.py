"""
调试授权后导航到审核管理页面的完整流程
"""
from tools.web_checker import WebChecker
import time

def debug_post_auth_navigation():
    """调试授权后的页面导航流程"""
    
    print("=" * 80)
    print("调试授权后导航到审核管理页面")
    print("=" * 80)
    
    web_checker = WebChecker(headless=False)
    
    try:
        # 启动浏览器并导航
        print("\n1. 启动浏览器...")
        web_checker.launch_browser()
        web_checker.navigate_to_url("https://compatibility.openharmony.cn/mng/index")
        time.sleep(3)
        
        # === 执行完整登录流程 ===
        print("\n2. 执行登录流程...")
        web_checker.page.click('.btn', timeout=5000)
        time.sleep(3)
        
        web_checker.page.fill('input[placeholder*="账号"]', 'fanqiqi@iscas.ac.cn')
        web_checker.page.fill('input[type="password"]', 'iscas123.')
        web_checker.page.click('button:has-text("用户登录")', timeout=5000)
        time.sleep(3)
        
        # 点击授权
        try:
            web_checker.page.click('button:has-text("授权")', timeout=5000)
            print("   ✓ 已点击授权按钮")
            
            # 等待授权完成
            web_checker.wait_for_selector('.nav, .sidebar, .main-content, #content-main', timeout=20000)
            print("   ✓ 授权完成")
            time.sleep(5)
        except Exception as e:
            print(f"   ⚠ 授权失败: {str(e)}")
        
        # === 展开侧边栏 ===
        print("\n3. 展开侧边栏...")
        expand_buttons = web_checker.page.query_selector_all('.sidebar-toggle, .navbar-minimalize, [data-toggle="offcanvas"]')
        for btn in expand_buttons:
            if btn.is_visible():
                print("   ✓ 找到展开按钮，点击...")
                web_checker.page.evaluate('(el) => el.click()', btn)
                time.sleep(1)
                break
        
        # === 点击审核管理菜单 ===
        print("\n4. 点击'审核管理'菜单...")
        elements = web_checker.page.query_selector_all('a, div, span, li')
        for element in elements:
            try:
                text = element.inner_text()
                if '审核管理' in text and len(text.strip()) < 20:
                    print(f"   ✓ 找到菜单项: '{text.strip()}'")
                    web_checker.page.evaluate('(el) => el.click()', element)
                    print("   ✓ 已点击审核管理")
                    break
            except:
                continue
        
        time.sleep(3)
        
        # === 查找并点击子菜单 ===
        print("\n5. 查找'兼容性测评审核'子菜单...")
        submenu_found = False
        
        # 列出所有可能的子菜单项
        print("   - 当前可见的子菜单项:")
        all_elements = web_checker.page.query_selector_all('a, li')
        for elem in all_elements:
            try:
                text = elem.inner_text().strip()
                if text and len(text) < 30 and ('测评' in text or '审核' in text or '豁免' in text):
                    print(f"     - '{text}'")
            except:
                pass
        
        # 尝试点击子菜单
        for attempt in range(2):
            elements = web_checker.page.query_selector_all('a, li')
            for element in elements:
                try:
                    text = element.inner_text().strip()
                    if '兼容性测评审核' in text and len(text) < 20:
                        print(f"\n   ✓ 找到子菜单: '{text}'")
                        print(f"   元素标签: {element.evaluate('el => el.tagName')}")
                        print(f"   是否可见: {element.is_visible()}")
                        
                        # 获取元素的HTML
                        html = element.evaluate('el => el.outerHTML')
                        print(f"   HTML: {html[:200]}")
                        
                        web_checker.page.evaluate('(el) => el.click()', element)
                        print("   ✓ 已点击子菜单")
                        submenu_found = True
                        break
                except Exception as e:
                    print(f"   ⚠ 处理元素时出错: {str(e)}")
            
            if submenu_found:
                break
            
            if not submenu_found and attempt == 0:
                print("   ⚠ 未找到，等待后重试...")
                time.sleep(2)
        
        if not submenu_found:
            print("   ✗ 未找到兼容性测评审核子菜单")
        
        # === 等待页面加载 ===
        print("\n6. 等待页面加载...")
        time.sleep(8)
        
        # === 检查iframe状态 ===
        print("\n7. 检查iframe状态...")
        frames = web_checker.page.frames
        print(f"   找到 {len(frames)} 个frame:")
        
        for i, frame in enumerate(frames):
            print(f"\n   Frame[{i}]:")
            print(f"     URL: {frame.url}")
            
            try:
                frame_text = frame.inner_text('body')
                print(f"     内容长度: {len(frame_text)} 字符")
                
                if len(frame_text) > 100:
                    print(f"     前300字符: {frame_text[:300]}")
                    
                    # 保存这个frame的内容
                    filename = f'debug_frame_{i}.txt'
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(frame_text)
                    print(f"     ✓ 已保存到 {filename}")
                    
                    # 查找输入框
                    inputs = frame.query_selector_all('input')
                    print(f"     输入框数量: {len(inputs)}")
                    for j, inp in enumerate(inputs[:5]):
                        try:
                            placeholder = inp.get_attribute('placeholder')
                            input_type = inp.get_attribute('type')
                            print(f"       [{j}] type='{input_type}' | placeholder='{placeholder}'")
                        except:
                            pass
                else:
                    print(f"     内容: {frame_text}")
            except Exception as e:
                print(f"     ⚠ 获取内容失败: {str(e)}")
        
        print("\n" + "=" * 80)
        print("调试完成！请查看生成的文件")
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
    debug_post_auth_navigation()
