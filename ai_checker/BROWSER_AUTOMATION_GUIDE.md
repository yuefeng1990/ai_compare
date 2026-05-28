# 浏览器自动化工作流程

## 第一步：录制浏览器操作（可视化模式）

运行录制脚本，观察网页操作流程：

```bash
python record_browser.py
```

### 录制步骤：
1. 脚本会以**可视化模式**打开浏览器（可以看到浏览器窗口）
2. 自动打开目标网页：`https://compatibility.openharmony.cn/mng/index`
3. **您需要手动完成以下操作**：
   - 如果需要登录，完成登录流程
   - 点击必要的按钮或菜单
   - 执行搜索操作
   - 找到需要提取数据的页面
   - 观察数据结构（可以右键检查元素，查看HTML结构）
4. 完成后按回车键
5. 程序会保存：
   - `recorded_actions.txt` - 录制信息
   - `page_content_sample.txt` - 页面文本内容样本

---

## 第二步：分析录制结果

查看生成的文件，了解：
1. **操作流程**：需要点击哪些按钮、输入什么内容
2. **CSS选择器**：通过浏览器开发者工具（F12）找到元素的CSS选择器
3. **数据结构**：页面中文本的组织方式
4. **关键字映射**：英文关键字对应的中文标签是什么

---

## 第三步：实现自动化

根据录制的信息，更新代码：

### 1. 在 `main.py` 中添加操作步骤：
```python
# 示例：登录后搜索
web_checker.navigate_to_url(WEB_URL)

# 点击登录按钮
web_checker.click_button("#login-button")

# 填写登录表单
web_checker.fill_form({
    '#username': 'your_username',
    '#password': 'your_password'
})

# 点击搜索
web_checker.fill_input('#search-input', '搜索关键词')
web_checker.click_button('#search-button')

# 等待结果加载
web_checker.wait_for_selector('.result-table')

# 获取数据
web_content = web_checker.get_page_text()
```

### 2. 在 `compare.py` 中优化值提取逻辑：
```python
def extract_value_from_web(self, web_content, keyword):
    """从网页内容中提取关键字对应的值（中文）"""
    # 建立英文关键字到中文标签的映射
    keyword_mapping = {
        'Manufacture': '制造商',
        'OsFullName': '操作系统全称',
        'MarketName': '市场名称',
        # ... 更多映射
    }
    
    chinese_label = keyword_mapping.get(keyword, keyword)
    
    # 在网页内容中查找中文标签和对应的值
    # 根据实际网页格式调整提取逻辑
    lines = web_content.split('\n')
    for line in lines:
        if chinese_label in line:
            # 提取冒号或特定分隔符后的值
            if ':' in line:
                return line.split(':', 1)[1].strip()
            elif '：' in line:  # 中文冒号
                return line.split('：', 1)[1].strip()
    
    return None
```

---

## 第四步：测试自动化

运行主程序测试自动化流程：

```bash
python main.py
```

---

## 常用 Playwright 操作方法

在 `web_checker.py` 中可以添加以下方法：

```python
def fill_input(self, selector, value):
    """填写输入框"""
    self.page.fill(selector, value)

def wait_for_selector(self, selector, timeout=10000):
    """等待元素出现"""
    self.page.wait_for_selector(selector, timeout=timeout)

def get_element_text(self, selector):
    """获取指定元素的文本"""
    return self.page.inner_text(selector)

def click_and_wait(self, selector, wait_timeout=2000):
    """点击并等待"""
    self.page.click(selector)
    time.sleep(wait_timeout / 1000)
```

---

## 注意事项

1. **登录问题**：如果网站需要登录，可能需要：
   - 在录制时完成登录
   - 保存登录状态（cookies/localStorage）
   - 或在代码中实现自动登录

2. **动态加载**：如果页面内容是动态加载的：
   - 使用 `wait_for_selector()` 等待元素出现
   - 适当增加等待时间

3. **反爬虫**：某些网站可能有反爬虫机制：
   - 设置合理的请求间隔
   - 模拟真实用户行为
   - 可能需要处理验证码

4. **元素选择器**：
   - 优先使用 ID 选择器（最稳定）
   - 其次使用 CSS 类选择器
   - 避免使用容易变化的 XPath
