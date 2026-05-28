"""
登录后首页调试工具
用于查找"审核管理"菜单的正确选择器
"""
from playwright.sync_api import sync_playwright
import time

def debug_homepage():
    """调试登录后首页的元素"""
    
    print("=" * 80)
    print("🔍 登录后首页调试工具")
    print("=" * 80)
    print("\n说明：")
    print("1. 自动打开浏览器并执行完整登录流程")
    print("2. 登录成功后，会显示首页所有菜单元素")
    print("3. 帮助您找到'审核管理'菜单的正确选择器")
    print("=" * 80)
    
    with sync_playwright() as p:
        # 启动浏览器（可视化模式）
        print("\n🚀 启动浏览器...")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()
        
        # 打开首页
        print("\n🌐 打开网页: https://compatibility.openharmony.cn/mng/index")
        page.goto('https://compatibility.openharmony.cn/mng/index', wait_until='networkidle')
        print("✓ 网页加载成功")
        
        # 检查是否已登录
        print("\n🔐 检查登录状态...")
        time.sleep(2)
        
        # 尝试点击"立即登录"
        try:
            login_btn = page.query_selector('.btn, div:has-text("立即登录")')
            if login_btn:
                print("      - 发现'立即登录'按钮，点击...")
                login_btn.click()
                print("      ✓ 已点击立即登录")
                
                # 等待跳转到授权页面
                print("      - 等待授权页面...")
                try:
                    page.wait_for_selector('input[type="text"], input[type="password"], input[placeholder*="账号"], input[placeholder*="用户名"]', timeout=15000)
                    print("      ✓ 授权页面加载完成")
                except:
                    print("      ⚠ 等待授权页面超时，尝试继续...")
                    time.sleep(3)
                
                # 输入用户名
                print("      - 输入用户名...")
                page.fill('input[placeholder*="账号"], input[placeholder*="用户名"]', 'fanqiqi@iscas.ac.cn')
                
                # 输入密码
                print("      - 输入密码...")
                page.fill('input[type="password"]', 'iscas123.')
                
                # 等待按钮出现
                print("      - 等待登录按钮...")
                page.wait_for_selector('button:has-text("用户登录"), button.el-button--primary', timeout=10000)
                time.sleep(1)
                
                # 点击"用户登录"
                print("      - 点击用户登录...")
                page.click('button:has-text("用户登录")', timeout=10000)
                print("      ✓ 点击成功")
                
                # 等待第二个授权页面
                print("      - 等待第二个授权页面...")
                time.sleep(3)
                
                # 尝试点击第二个"授权"按钮
                try:
                    auth_btn = page.query_selector('button:has-text("授权")')
                    if auth_btn:
                        print("      ✓ 发现第二个授权按钮，点击...")
                        auth_btn.click(timeout=10000)
                        print("      ✓ 第二个授权按钮点击成功")
                        
                        # 等待跳转到首页
                        print("      - 等待跳转到首页...")
                        for attempt in range(10):
                            current_url = page.url
                            if 'compatibility.openharmony.cn' in current_url and '/mng/' in current_url:
                                print(f"      ✓ 已跳转到目标页面")
                                break
                            time.sleep(3)
                except:
                    print("      ⚠ 未发现第二个授权按钮")
                    
        except Exception as e:
            print(f"      ⚠ 登录过程异常: {str(e)}")
        
        # 现在应该在首页了，开始调试
        print("\n" + "=" * 80)
        print("🔍 开始调试首页元素...")
        print("=" * 80)
        
        # 等待页面加载
        time.sleep(3)
        
        try:
            current_url = page.url
            print(f"\n当前URL: {current_url}")
            print(f"页面标题: {page.title()}")
            
            # 保存截图
            page.screenshot(path='homepage_debug.png', full_page=True)
            print("✓ 截图已保存到: homepage_debug.png")
        except Exception as e:
            print(f"⚠ 截图失败: {str(e)}")
        
        # 查找所有菜单相关元素
        print("\n" + "=" * 80)
        print("🔍 查找所有菜单元素...")
        print("=" * 80)
        
        # 1. 查找包含"审核管理"文本的元素
        print("\n1️⃣ 查找包含'审核管理'文本的元素:")
        audit_elements = page.query_selector_all(':has-text("审核管理")')
        print(f"   找到 {len(audit_elements)} 个元素\n")
        
        for i, elem in enumerate(audit_elements):
            try:
                text = elem.inner_text() or '无文本'
                tag = elem.evaluate('el => el.tagName')
                class_name = elem.get_attribute('class') or '无class'
                id_attr = elem.get_attribute('id') or '无ID'
                
                print(f"   元素 {i+1}:")
                print(f"     标签: <{tag}>")
                print(f"     文本: '{text[:100]}'")
                print(f"     ID: {id_attr}")
                print(f"     Class: {class_name[:100]}")
                
                # 获取父元素信息
                parent = elem.evaluate('el => el.parentElement ? el.parentElement.tagName : "无"')
                print(f"     父元素: <{parent}>")
                print()
            except Exception as e:
                print(f"   元素 {i+1}: 读取失败 - {str(e)}\n")
        
        # 2. 查找所有菜单项
        print("\n2️⃣ 查找所有菜单项 (.el-menu-item, .menu-item, nav a):")
        menu_items = page.query_selector_all('.el-menu-item, .menu-item, nav a, .sidebar a, .nav-item')
        print(f"   找到 {len(menu_items)} 个菜单项\n")
        
        for i, item in enumerate(menu_items[:20]):  # 只显示前20个
            try:
                text = item.inner_text() or '无文本'
                class_name = item.get_attribute('class') or '无class'
                href = item.get_attribute('href') or '无href'
                
                print(f"   菜单项 {i+1}: '{text[:50]}' (class: {class_name[:50]}, href: {href[:50]})")
            except:
                pass
        
        # 3. 查找侧边栏导航
        print("\n3️⃣ 查找侧边栏/导航容器:")
        nav_containers = page.query_selector_all('.el-menu, .sidebar, nav, .menu, .navigation, .aside')
        print(f"   找到 {len(nav_containers)} 个导航容器\n")
        
        for i, container in enumerate(nav_containers):
            try:
                class_name = container.get_attribute('class') or '无class'
                id_attr = container.get_attribute('id') or '无ID'
                
                # 获取容器内的文本
                text = container.inner_text() or '无文本'
                text_preview = text[:200].replace('\n', ' | ')
                
                print(f"   容器 {i+1}:")
                print(f"     Class: {class_name[:100]}")
                print(f"     ID: {id_attr}")
                print(f"     内容预览: {text_preview[:150]}...")
                print()
            except Exception as e:
                print(f"   容器 {i+1}: 读取失败 - {str(e)}\n")
        
        # 4. 保存HTML
        html_content = page.content()
        with open('homepage_debug.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("\n✓ HTML已保存到: homepage_debug.html")
        
        print("\n" + "=" * 80)
        print("✅ 调试完成！")
        print("=" * 80)
        print("\n请查看以上输出，找到'审核管理'菜单的正确选择器")
        print("提示：优先使用.el-menu-item或包含特定class的元素")
        print("\n按回车键关闭浏览器...")
        input()
        
        # 关闭浏览器
        print("\n🔒 关闭浏览器...")
        browser.close()
        print("✓ 浏览器已关闭")

if __name__ == '__main__':
    debug_homepage()
