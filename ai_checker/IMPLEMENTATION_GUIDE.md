# 浏览器自动化操作指南

## 📋 当前状态分析

根据录制结果，我们发现：

### 1. 网页需要登录
- **登录页面**: `https://compatibility.openharmony.cn/mng/login`
- **页面标题**: "OpenAtom OpenHarmony"
- **菜单项**: 样机管理、审核管理、兼容性测评审核等

### 2. 下一步操作

您需要完成以下步骤来实现完全自动化：

---

## 🔧 实施步骤

### 第一步：手动登录并观察（重要！）

1. **运行录制脚本**（已完成✓）
   ```bash
   python record_browser.py
   ```

2. **在打开的浏览器中手动操作**：
   - ✅ 输入用户名和密码进行登录
   - ✅ 点击"样机管理"或相关菜单
   - ✅ 找到显示设备信息的页面
   - ✅ 观察数据结构：
     - 右键点击任意数据 → 选择"检查"（Inspect）
     - 查看 HTML 结构
     - 记录关键字段的 CSS 选择器
   - ✅ 截图保存关键页面（可选）

3. **记录以下信息**：
   ```
   登录表单选择器：
   - 用户名输入框: _______________
   - 密码输入框: _______________
   - 登录按钮: _______________
   
   数据页面导航：
   - 样机管理菜单: _______________
   - 搜索框: _______________
   - 搜索按钮: _______________
   
   数据显示位置：
   - 数据表格/列表的选择器: _______________
   - 每个字段的标签和值的结构: _______________
   ```

---

### 第二步：更新代码实现自动化

根据您记录的信息，修改 `main.py` 中的 web 操作部分：

#### 示例代码模板：

```python
# 1. 打开登录页面
web_checker.navigate_to_url(WEB_URL)

# 2. 自动登录
print("正在登录...")
web_checker.fill_input('#username', 'YOUR_USERNAME')  # 替换为实际选择器
web_checker.fill_input('#password', 'YOUR_PASSWORD')  # 替换为实际选择器
web_checker.click_button('#login-btn')  # 替换为实际选择器
web_checker.wait_for_selector('.dashboard', timeout=10000)  # 等待登录成功
print("✓ 登录成功")

# 3. 导航到数据页面
print("正在导航到样机管理...")
web_checker.click_button('#device-management-menu')  # 替换为实际选择器
web_checker.wait_for_selector('.device-table', timeout=10000)
print("✓ 页面加载成功")

# 4. 搜索特定设备（如果需要）
print("正在搜索设备...")
web_checker.fill_input('#search-box', 'SYNCO')  # 根据Excel中的数据动态搜索
web_checker.click_button('#search-button')
web_checker.wait_for_selector('.search-results', timeout=10000)

# 5. 获取页面内容
web_content = web_checker.get_page_text()
print(f"✓ 获取到 {len(web_content)} 字符的内容")

# 6. 对每个关键字提取值
for match_info in matched_rows:
    keyword = match_info['matched_keyword']
    web_value = compare_tool.extract_value_from_web(web_content, keyword)
    # ... 后续比较逻辑
```

---

### 第三步：优化中文关键字映射

在 `tools/compare.py` 的 `extract_value_from_web` 方法中：

1. **根据实际网页调整映射关系**：
   ```python
   keyword_mapping = {
       'Manufacture': ['制造商', '厂商'],  # 根据网页实际显示的中文调整
       'OsFullName': ['操作系统全称'],
       # ... 更多映射
   }
   ```

2. **调整提取逻辑**：
   - 如果网页使用表格形式，可能需要解析表格结构
   - 如果网页使用键值对列表，当前的冒号分隔逻辑应该有效
   - 如果数据结构复杂，可能需要使用更高级的解析方法

---

### 第四步：测试和优化

1. **运行主程序测试**：
   ```bash
   python main.py
   ```

2. **检查输出**：
   - 是否成功登录？
   - 是否正确导航到数据页面？
   - 是否成功提取到 web 值？
   - 比较结果是否符合预期？

3. **调试技巧**：
   - 临时设置 `headless=False` 查看浏览器实际操作
   - 使用 `web_checker.screenshot('step1.png')` 截图调试
   - 打印中间变量检查数据流

---

## 🎯 常见问题解决

### 问题1：登录失败
**解决方案**：
- 检查用户名密码是否正确
- 检查是否有验证码（需要人工处理或使用OCR）
- 检查是否需要特殊的登录流程（如两步验证）

### 问题2：找不到元素
**解决方案**：
- 增加等待时间：`web_checker.wait_for_selector(selector, timeout=30000)`
- 检查选择器是否正确（在浏览器控制台测试：`document.querySelector('#your-selector')`）
- 元素可能是动态加载的，需要先触发某些操作

### 问题3：提取不到值
**解决方案**：
- 检查 `page_content_sample.txt` 确认数据确实在页面上
- 调整中文关键字映射
- 检查数据格式（是否有特殊字符、空格等）
- 尝试不同的提取策略（正则表达式、JSON解析等）

### 问题4：反爬虫限制
**解决方案**：
- 添加随机延迟：`time.sleep(random.uniform(1, 3))`
- 设置用户代理：`self.page.set_extra_http_headers({'User-Agent': '...'})`
- 减少请求频率
- 考虑使用浏览器配置文件保存登录状态

---

## 📝 快速参考：常用 Playwright 操作

```python
# 导航
web_checker.navigate_to_url(url)

# 填写表单
web_checker.fill_input('#username', 'admin')
web_checker.fill_input('#password', '123456')

# 点击元素
web_checker.click_button('#login-btn')

# 等待元素
web_checker.wait_for_selector('.result-table', timeout=10000)

# 获取内容
text = web_checker.get_page_text()
html = web_checker.get_page_content()
element_text = web_checker.get_element_text('#specific-element')

# 截图
web_checker.screenshot('debug.png')

# 执行JavaScript
result = web_checker.page.evaluate("document.title")
```

---

## ✅ 完成检查清单

- [ ] 已手动登录并观察到数据页面
- [ ] 已记录所有必要的CSS选择器
- [ ] 已更新 `main.py` 实现自动化登录和导航
- [ ] 已调整中文关键字映射
- [ ] 已测试自动化流程
- [ ] 所有关键字都能正确提取和比较
- [ ] 结果已保存到Excel

---

## 📞 需要帮助？

如果在实施过程中遇到问题：
1. 查看生成的 `recorded_actions.txt` 和 `page_content_sample.txt`
2. 使用浏览器的开发者工具（F12）检查元素
3. 临时启用可视化模式调试：`WebChecker(headless=False)`
4. 查看 Playwright 官方文档：https://playwright.dev/python/
