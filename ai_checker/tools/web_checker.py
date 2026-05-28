from playwright.sync_api import sync_playwright
import time

class WebChecker:
    def __init__(self, headless=False):
        """
        初始化WebChecker
        :param headless: 是否无头模式，False为可视化模式（可以看到浏览器操作）
        """
        self.playwright = None
        self.browser = None
        self.page = None
        self.headless = headless
    
    def launch_browser(self):
        """启动浏览器"""
        self.playwright = sync_playwright().start()
        # headless=False 表示可视化模式，可以看到浏览器窗口
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.page = self.browser.new_page()
    
    def close_browser(self):
        """关闭浏览器"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    
    def navigate_to_url(self, url):
        """导航到指定URL"""
        if not self.page:
            raise Exception("浏览器未启动")
        
        try:
            # 使用domcontentloaded而不是load，加快页面加载
            self.page.goto(url, timeout=60000, wait_until='domcontentloaded')
            return True
        except Exception as e:
            raise Exception(f"导航到URL失败: {str(e)}")
    
    def click_button(self, selector):
        """点击按钮"""
        try:
            # 尝试多种选择器策略
            selectors_to_try = [selector]
            
            # 如果选择器包含:has-text，尝试其他策略
            if ':has-text' in selector:
                text = selector.split('"')[1] if '"' in selector else selector.split("'")[1]
                selectors_to_try.extend([
                    f'button:has-text("{text}")',
                    f'a:has-text("{text}")',
                    f'span:has-text("{text}")',
                    f'*:has-text("{text}")'
                ])
            
            # 依次尝试不同的选择器
            for sel in selectors_to_try:
                try:
                    self.page.click(sel, timeout=5000)
                    time.sleep(1)  # 等待操作完成
                    return True
                except:
                    continue
            
            raise Exception(f"所有选择器都失败: {selectors_to_try}")
        except Exception as e:
            raise Exception(f"点击按钮失败: {str(e)}")
    
    def get_popup_content(self):
        """获取弹窗内容"""
        try:
            # 等待弹窗出现
            self.page.wait_for_selector("body", timeout=10000)
            content = self.page.inner_text("body")
            return content
        except Exception as e:
            raise Exception(f"获取弹窗内容失败: {str(e)}")
    
    def get_page_content(self):
        """获取页面内容"""
        try:
            return self.page.content()
        except Exception as e:
            raise Exception(f"获取页面内容失败: {str(e)}")
    
    def get_page_text(self):
        """获取页面可见文本内容"""
        try:
            return self.page.inner_text("body")
        except Exception as e:
            raise Exception(f"获取页面文本失败: {str(e)}")
    
    def wait_for_user_action(self, prompt="请在浏览器中完成操作后按回车继续..."):
        """等待用户手动操作，用于录制脚本"""
        print(f"\n{'='*80}")
        print(prompt)
        print(f"{'='*80}")
        
        # 先获取当前页面状态（在等待之前）
        try:
            current_url = self.page.url
            page_title = self.page.title()
        except Exception as e:
            current_url = "未知"
            page_title = "未知"
            print(f"警告: 无法获取页面信息: {str(e)}")
        
        print(f"\n当前URL: {current_url}")
        print(f"页面标题: {page_title}")
        
        # 使用更兼容的方式等待用户输入
        try:
            input("完成后按回车键继续...")
        except EOFError:
            print("\n检测到输入流结束，继续执行...")
        
        return {
            'url': current_url,
            'title': page_title
        }
    
    def save_recording_info(self, info, filename="recorded_actions.txt"):
        """保存录制的操作信息"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("# 录制的浏览器操作步骤\n")
                f.write(f"# URL: {info['url']}\n")
                f.write(f"# 标题: {info['title']}\n")
                f.write(f"# 时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("# 请根据实际观察到的操作，补充以下步骤：\n")
                f.write("# 1. 点击了哪个按钮？按钮的CSS选择器是什么？\n")
                f.write("# 2. 输入了什么搜索关键词？\n")
                f.write("# 3. 需要等待哪些元素加载？\n")
                f.write("# 4. 数据在页面的哪个位置？如何提取？\n\n")
                f.write("# 示例：\n")
                f.write("# click('#login-button')\n")
                f.write("# fill('#search-input', 'keyword')\n")
                f.write("# click('#search-button')\n")
                f.write("# wait_for_selector('.result-table')\n")
            print(f"✓ 录制信息已保存到: {filename}")
        except Exception as e:
            print(f"✗ 保存录制信息失败: {str(e)}")
    
    def fill_input(self, selector, value):
        """填写输入框"""
        try:
            self.page.fill(selector, value)
            time.sleep(0.5)  # 短暂等待
            return True
        except Exception as e:
            raise Exception(f"填写输入框失败: {str(e)}")
    
    def wait_for_selector(self, selector, timeout=10000):
        """等待元素出现"""
        try:
            self.page.wait_for_selector(selector, timeout=timeout)
            return True
        except Exception as e:
            raise Exception(f"等待元素超时: {selector}")
    
    def get_element_text(self, selector):
        """获取指定元素的文本"""
        try:
            return self.page.inner_text(selector)
        except Exception as e:
            raise Exception(f"获取元素文本失败: {selector}")
    
    def get_element_value(self, selector):
        """获取指定元素的值（用于input等）"""
        try:
            return self.page.input_value(selector)
        except Exception as e:
            raise Exception(f"获取元素值失败: {selector}")
    
    def screenshot(self, filename="screenshot.png"):
        """截图保存"""
        try:
            self.page.screenshot(path=filename)
            print(f"✓ 截图已保存到: {filename}")
            return True
        except Exception as e:
            print(f"✗ 截图失败: {str(e)}")
            return False
    
    def extract_keywords_from_description(self, description):
        """从描述中提取关键字（简化版）"""
        # 这里可以实现更复杂的提取逻辑
        # 简单示例：按空格分割并取前几个词
        words = description.split()[:5]
        return words
    
    def check_website_with_keywords(self, url, keywords):
        """检查网站内容是否包含关键字"""
        try:
            self.navigate_to_url(url)
            
            # 点击按钮打开弹窗（假设按钮选择器为"#popup-button"）
            self.click_button("#popup-button")
            
            # 获取弹窗内容
            popup_content = self.get_popup_content()
            
            # 检查关键字是否在弹窗内容中
            results = {}
            for keyword in keywords:
                results[keyword] = keyword.lower() in popup_content.lower()
            
            return results, popup_content
        except Exception as e:
            raise Exception(f"网站检查失败: {str(e)}")