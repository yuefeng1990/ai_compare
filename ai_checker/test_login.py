"""
测试登录流程脚本
用于验证两步登录是否正常工作
"""
from tools.web_checker import WebChecker
from auto_login import automate_browser

def test_login():
    """测试完整的登录流程"""
    
    WEB_URL = "https://compatibility.openharmony.cn/mng/index"
    web_checker = None
    
    try:
        print("="*80)
        print("🧪 登录流程测试")
        print("="*80)
        print("\n测试步骤：")
        print("1. 打开首页")
        print("2. 点击'立即登录'按钮")
        print("3. 输入用户名和密码")
        print("4. 点击登录")
        print("5. 验证登录成功")
        print("="*80)
        
        # 启动可视化浏览器以便观察
        print("\n🚀 启动浏览器（可视化模式）...")
        web_checker = WebChecker(headless=False)
        web_checker.launch_browser()
        
        # 打开网页
        print(f"\n🌐 打开网页: {WEB_URL}")
        web_checker.navigate_to_url(WEB_URL)
        print("✓ 网页加载成功")
        
        # 执行自动化登录
        print("\n🔐 开始执行登录流程...")
        print("-"*80)
        automate_browser(web_checker)
        print("-"*80)
        
        # 验证登录成功
        print("\n✅ 登录流程测试完成！")
        print("\n请检查：")
        print("  1. 是否成功点击了'立即登录'按钮？")
        print("  2. 是否正确输入了用户名和密码？")
        print("  3. 是否成功跳转到主页面？")
        print("  4. 菜单是否正常显示？")
        
        input("\n按回车键关闭浏览器...")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
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
    test_login()
