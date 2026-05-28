"""
菜单点击后页面调试工具
用于查看点击"兼容性测评审核"后页面的实际内容
"""
from playwright.sync_api import sync_playwright
import time
import sys
sys.path.append('.')
from auto_login import automate_browser
from tools.web_checker import WebChecker

def debug_menu_navigation():
    """调试菜单导航后的页面内容"""
    
    print("=" * 80)
    print("🔍 菜单导航调试工具")
    print("=" * 80)
    print("\n说明：")
    print("1. 自动执行完整登录流程")
    print("2. 点击'审核管理' -> '兼容性测评审核'")
    print("3. 显示页面内容和所有元素")
    print("=" * 80)
    
    # 启动WebChecker
    web_checker = WebChecker(headless=False)
    
    try:
        # 打开网页
        print("\n🌐 打开网页...")
        web_checker.launch_browser()
        web_checker.navigate_to_url('https://compatibility.openharmony.cn/mng/index')
        
        # 执行自动登录
        print("\n🔐 执行登录流程...")
        automate_browser(web_checker)
        
        # 现在应该在兼容性测评审核页面了
        print("\n" + "=" * 80)
        print("🔍 开始调试页面内容...")
        print("=" * 80)
        
        time.sleep(3)
        
        current_url = web_checker.page.url
        print(f"\n当前URL: {current_url}")
        print(f"页面标题: {web_checker.page.title()}")
        
        # 保存截图
        web_checker.page.screenshot(path='menu_navigation_debug.png', full_page=True)
        print("✓ 截图已保存到: menu_navigation_debug.png")
        
        # 查找所有文本包含"测评"的元素
        print("\n1️⃣ 查找包含'测评'的文本:")
        measurement_elements = web_checker.page.query_selector_all(':has-text("测评")')
        print(f"   找到 {len(measurement_elements)} 个元素\n")
        
        for i, elem in enumerate(measurement_elements[:20]):
            try:
                text = elem.inner_text() or '无文本'
                tag = elem.evaluate('el => el.tagName')
                class_name = elem.get_attribute('class') or '无class'
                
                print(f"   元素 {i+1}: <{tag}> '{text[:80]}' (class: {class_name[:50]})")
            except Exception as e:
                print(f"   元素 {i+1}: 读取失败 - {str(e)}")
        
        # 查找所有表格
        print("\n2️⃣ 查找表格:")
        tables = web_checker.page.query_selector_all('.el-table, table, .table-container, .data-table')
        print(f"   找到 {len(tables)} 个表格\n")
        
        for i, table in enumerate(tables):
            try:
                class_name = table.get_attribute('class') or '无class'
                rows = table.query_selector_all('tr, .el-table__row')
                print(f"   表格 {i+1}: class='{class_name[:50]}', 行数={len(rows)}")
            except Exception as e:
                print(f"   表格 {i+1}: 读取失败 - {str(e)}")
        
        # 查找所有按钮
        print("\n3️⃣ 查找所有按钮:")
        buttons = web_checker.page.query_selector_all('button, .el-button, [role="button"]')
        print(f"   找到 {len(buttons)} 个按钮\n")
        
        for i, btn in enumerate(buttons[:30]):
            try:
                text = btn.inner_text() or '无文本'
                class_name = btn.get_attribute('class') or '无class'
                
                if text.strip() and text != '无文本':
                    print(f"   按钮 {i+1}: '{text[:50]}' (class: {class_name[:50]})")
            except:
                pass
        
        # 查找所有输入框
        print("\n4️⃣ 查找所有输入框:")
        inputs = web_checker.page.query_selector_all('input, .el-input__inner')
        print(f"   找到 {len(inputs)} 个输入框\n")
        
        for i, inp in enumerate(inputs[:20]):
            try:
                input_type = inp.get_attribute('type') or 'text'
                placeholder = inp.get_attribute('placeholder') or '无placeholder'
                class_name = inp.get_attribute('class') or '无class'
                
                print(f"   输入框 {i+1}: type={input_type}, placeholder='{placeholder[:40]}'")
            except:
                pass
        
        # 保存HTML
        html_content = web_checker.page.content()
        with open('menu_navigation_debug.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("\n✓ HTML已保存到: menu_navigation_debug.html")
        
        print("\n" + "=" * 80)
        print("✅ 调试完成！")
        print("=" * 80)
        print("\n请查看以上输出和生成的文件，了解页面结构")
        print("\n按回车键关闭浏览器...")
        input()
        
    finally:
        # 关闭浏览器
        print("\n🔒 关闭浏览器...")
        web_checker.close_browser()
        print("✓ 浏览器已关闭")

if __name__ == '__main__':
    debug_menu_navigation()
