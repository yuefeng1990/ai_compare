"""
智能浏览器操作录制脚本
自动记录登录信息、点击元素和操作步骤
"""
import sys
import os
import json
import time
from tools.web_checker import WebChecker

class ActionRecorder:
    """操作录制器，自动记录用户操作"""
    
    def __init__(self, web_checker):
        self.web_checker = web_checker
        self.actions = []
        self.login_info = {}
        
    def start_recording(self):
        """开始录制"""
        print("\n" + "="*80)
        print("🎥 智能录制模式已启动")
        print("="*80)
        print("\n系统将自动记录：")
        print("  ✓ 登录用户名和密码")
        print("  ✓ 所有点击的元素及其CSS选择器")
        print("  ✓ 所有输入的内容")
        print("  ✓ 页面导航URL变化")
        print("\n提示：正常操作即可，系统会自动记录")
        print("="*80 + "\n")
        
        # 注入JavaScript监听代码到页面
        self._inject_recording_script()
    
    def _inject_recording_script(self):
        """注入JavaScript监听脚本"""
        try:
            # 监听所有点击事件
            self.web_checker.page.evaluate("""
                () => {
                    // 存储操作记录
                    window.recordedActions = [];
                    window.loginFields = {};
                    
                    // 监听点击事件
                    document.addEventListener('click', (e) => {
                        const target = e.target;
                        const action = {
                            type: 'click',
                            timestamp: new Date().toISOString(),
                            tagName: target.tagName,
                            id: target.id || null,
                            className: target.className || null,
                            text: target.innerText ? target.innerText.substring(0, 50) : null,
                            selector: this.getSelector(target)
                        };
                        window.recordedActions.push(action);
                        console.log('📝 Recorded click:', action);
                    }, true);
                    
                    // 监听输入事件
                    document.addEventListener('input', (e) => {
                        const target = e.target;
                        if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA') {
                            const inputType = target.type || 'text';
                            // 检测是否是密码或用户名输入框
                            if (inputType === 'password' || 
                                target.name?.toLowerCase().includes('password') ||
                                target.id?.toLowerCase().includes('password')) {
                                window.loginFields.password = '[PASSWORD_RECORDED]';
                            } else if (inputType === 'text' || inputType === 'email') {
                                const fieldName = target.name || target.id || 'unknown';
                                if (!window.loginFields[fieldName]) {
                                    window.loginFields[fieldName] = target.value;
                                }
                            }
                            
                            const action = {
                                type: 'input',
                                timestamp: new Date().toISOString(),
                                tagName: target.tagName,
                                id: target.id || null,
                                name: target.name || null,
                                type: inputType,
                                value: target.value,
                                selector: this.getSelector(target)
                            };
                            window.recordedActions.push(action);
                        }
                    }, true);
                    
                    // 辅助函数：生成CSS选择器
                    this.getSelector = function(element) {
                        if (element.id) {
                            return '#' + element.id;
                        }
                        if (element.className && typeof element.className === 'string') {
                            const classes = element.className.split(' ').filter(c => c).slice(0, 3);
                            if (classes.length > 0) {
                                return element.tagName.toLowerCase() + '.' + classes.join('.');
                            }
                        }
                        return element.tagName.toLowerCase();
                    };
                }
            """)
            print("✓ JavaScript监听脚本已注入\n")
        except Exception as e:
            print(f"⚠ 注入监听脚本失败: {str(e)}\n")
    
    def get_recorded_actions(self):
        """获取录制的操作"""
        try:
            actions = self.web_checker.page.evaluate("() => window.recordedActions || []")
            login_fields = self.web_checker.page.evaluate("() => window.loginFields || {}")
            return actions, login_fields
        except Exception as e:
            print(f"⚠ 获取录制数据失败: {str(e)}")
            return [], {}
    
    def save_recording(self, filename="recorded_actions.json"):
        """保存录制结果"""
        actions, login_fields = self.get_recorded_actions()
        
        recording_data = {
            'metadata': {
                'url': self.web_checker.page.url,
                'title': self.web_checker.page.title(),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'total_actions': len(actions)
            },
            'login_info': login_fields,
            'actions': actions
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(recording_data, f, ensure_ascii=False, indent=2)
            print(f"\n✓ 录制数据已保存到: {filename}")
            
            # 同时生成Python代码文件
            self._generate_python_code(recording_data, "auto_login.py")
            
            return True
        except Exception as e:
            print(f"✗ 保存失败: {str(e)}")
            return False
    
    def _generate_python_code(self, recording_data, filename="auto_login.py"):
        """生成可执行的Python代码"""
        try:
            login_info = recording_data.get('login_info', {})
            actions = recording_data.get('actions', [])
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('"""\n自动生成的浏览器自动化脚本\n根据录制操作生成\n"""\n\n')
                f.write('def automate_browser(web_checker):\n')
                f.write('    """执行录制的自动化操作"""\n\n')
                
                # 生成登录代码
                if login_info:
                    f.write('    # === 登录操作 ===\n')
                    for field_name, value in login_info.items():
                        if value == '[PASSWORD_RECORDED]':
                            f.write(f'    # 注意: {field_name} 是密码字段，需要手动配置\n')
                            f.write(f'    web_checker.fill_input(\'#{field_name}\', \'YOUR_PASSWORD_HERE\')\n')
                        else:
                            f.write(f'    web_checker.fill_input(\'#{field_name}\', \'{value}\')\n')
                    f.write('\n')
                
                # 生成点击操作
                click_actions = [a for a in actions if a['type'] == 'click']
                if click_actions:
                    f.write('    # === 点击操作 ===\n')
                    for i, action in enumerate(click_actions[:10]):  # 只取前10个点击
                        selector = action.get('selector', '')
                        text = action.get('text', '')
                        f.write(f'    # 点击: {text or "未知元素"}\n')
                        if selector:
                            f.write(f'    web_checker.click_button(\'{selector}\')\n')
                        f.write(f'    # time.sleep(1)  # 根据需要添加等待\n\n')
                
                # 生成输入操作
                input_actions = [a for a in actions if a['type'] == 'input']
                if input_actions:
                    f.write('    # === 输入操作 ===\n')
                    for action in input_actions[:10]:
                        selector = action.get('selector', '')
                        value = action.get('value', '')
                        f.write(f'    # 输入: {value[:50] if value else "未知"}\n')
                        if selector and value:
                            f.write(f'    web_checker.fill_input(\'{selector}\', \'{value}\')\n')
                        f.write('\n')
                
                f.write('    print("✓ 自动化操作执行完成")\n')
            
            print(f"✓ Python代码已生成: {filename}")
            
        except Exception as e:
            print(f"⚠ 生成Python代码失败: {str(e)}")


def record_browser_actions():
    """录制浏览器操作流程"""
    
    # 定义网页URL
    WEB_URL = "https://compatibility.openharmony.cn/mng/index"
    
    web_checker = None
    recorder = None
    
    try:
        print("="*80)
        print("🎬 智能浏览器操作录制工具")
        print("="*80)
        print("\n功能：")
        print("  • 自动记录登录用户名和密码")
        print("  • 自动记录所有点击的元素和CSS选择器")
        print("  • 自动生成可执行的Python代码")
        print("="*80)
        
        # 初始化浏览器（可视化模式）
        print("\n🚀 正在启动浏览器...")
        web_checker = WebChecker(headless=False)
        web_checker.launch_browser()
        
        # 创建录制器
        recorder = ActionRecorder(web_checker)
        
        # 打开网页
        print(f"\n🌐 正在打开网页: {WEB_URL}")
        web_checker.navigate_to_url(WEB_URL)
        print("✓ 网页已打开")
        
        # 开始录制
        recorder.start_recording()
        
        # 等待用户操作
        print("\n" + "="*80)
        print("👉 现在请在浏览器中进行操作：")
        print("   1. 输入用户名和密码登录")
        print("   2. 点击需要的菜单和按钮")
        print("   3. 执行搜索等操作")
        print("   4. 找到数据显示页面")
        print("\n💡 提示：所有操作都会被自动记录！")
        print("="*80)
        
        try:
            input("\n完成后按回车键停止录制...")
        except EOFError:
            print("\n检测到输入流结束")
        
        # 停止录制并保存
        print("\n⏹ 停止录制...")
        recorder.save_recording("recorded_actions.json")
        
        # 获取页面内容样本
        print("\n📄 正在获取页面内容...")
        try:
            page_text = web_checker.get_page_text()
            with open('page_content_sample.txt', 'w', encoding='utf-8') as f:
                f.write(f"# URL: {web_checker.page.url}\n")
                f.write(f"# 时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(page_text)
            print(f"✓ 页面文本已保存 ({len(page_text)} 字符)")
        except Exception as e:
            print(f"⚠ 获取页面文本失败: {str(e)}")
        
        # 截图
        print("\n📸 正在截图...")
        web_checker.screenshot("final_page.png")
        
        print("\n" + "="*80)
        print("✅ 录制完成！")
        print("="*80)
        print("\n生成的文件：")
        print("  📋 recorded_actions.json - 完整的录制数据（JSON格式）")
        print("  🐍 auto_login.py - 自动生成的Python代码")
        print("  📄 page_content_sample.txt - 页面内容样本")
        print("  🖼️ final_page.png - 最终页面截图")
        print("\n下一步：")
        print("  1. 查看 auto_login.py 了解自动生成的代码")
        print("  2. 编辑 auto_login.py，填入真实的密码")
        print("  3. 将代码集成到 main.py 中")
        print("="*80)
        
        input("\n按回车键关闭浏览器...")
        
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        if web_checker:
            print("\n🔒 正在关闭浏览器...")
            try:
                web_checker.close_browser()
                print("✓ 浏览器已关闭")
            except:
                pass

if __name__ == "__main__":
    record_browser_actions()
