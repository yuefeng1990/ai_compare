# 🎬 智能浏览器录制工具使用指南

## 📖 使用方法

### 第一步：运行录制脚本

```bash
python record_browser.py
```

### 第二步：在浏览器中操作

脚本会自动打开浏览器并注入监听代码，**您需要手动完成以下操作**：

1. **输入登录信息**
   - 在用户名输入框中输入您的用户名
   - 在密码输入框中输入您的密码
   - 点击登录按钮

2. **导航到数据页面**
   - 点击"样机管理"或相关菜单
   - 执行搜索操作（如果需要）
   - 找到显示设备信息的页面

3. **观察数据结构**
   - 右键点击任意数据元素 → 选择"检查"
   - 查看 HTML 结构和 CSS 选择器

4. **完成后按回车**
   - 回到命令行窗口
   - 按回车键停止录制

### 第三步：查看生成的文件

录制完成后会生成以下文件：

#### 1. `recorded_actions.json` - 完整录制数据
```json
{
  "metadata": {
    "url": "最终URL",
    "title": "页面标题",
    "timestamp": "录制时间"
  },
  "login_info": {
    "username_field": "记录的用户名",
    "password_field": "[PASSWORD_RECORDED]"
  },
  "actions": [
    {
      "type": "click",
      "selector": "#login-button",
      "text": "登录",
      "timestamp": "..."
    },
    {
      "type": "input",
      "selector": "#username",
      "value": "admin",
      "timestamp": "..."
    }
  ]
}
```

#### 2. `auto_login.py` - 自动生成的Python代码
```python
def automate_browser(web_checker):
    # === 登录操作 ===
    web_checker.fill_input('#username', 'admin')
    web_checker.fill_input('#password', 'YOUR_PASSWORD_HERE')  # 需要手动填入密码
    
    # === 点击操作 ===
    web_checker.click_button('#login-button')
    time.sleep(1)
    
    # === 导航操作 ===
    web_checker.click_button('#device-menu')
    # ...
```

#### 3. `page_content_sample.txt` - 页面文本内容
包含页面上所有可见的文本，用于分析数据结构。

#### 4. `final_page.png` - 页面截图
最终页面的可视化截图。

---

## 🔧 如何集成到主程序

### 方法1：直接使用生成的代码

1. 编辑 `auto_login.py`，填入真实的密码
2. 在 `main.py` 中导入并使用：

```python
from auto_login import automate_browser

# 在 main.py 中
web_checker = WebChecker(headless=True)
web_checker.launch_browser()
web_checker.navigate_to_url(WEB_URL)

# 执行录制的自动化操作
automate_browser(web_checker)

# 继续后续的数据提取和比较
web_content = web_checker.get_page_text()
```

### 方法2：手动编写自动化代码

根据 `recorded_actions.json` 中的信息，在 `main.py` 中编写：

```python
# 1. 登录
web_checker.fill_input('#username', 'your_username')
web_checker.fill_input('#password', 'your_password')
web_checker.click_button('#login-btn')
web_checker.wait_for_selector('.dashboard', timeout=10000)

# 2. 导航
web_checker.click_button('#device-management')
web_checker.wait_for_selector('.device-table')

# 3. 搜索（如果需要）
web_checker.fill_input('#search-box', 'SYNCO')
web_checker.click_button('#search-btn')

# 4. 获取数据
web_content = web_checker.get_page_text()
```

---

## 💡 常见问题

### Q1: 为什么没有录制到操作？
**A**: 确保您在浏览器中实际进行了操作：
- 真正输入了文字（不是复制粘贴）
- 真正点击了按钮
- 等待JavaScript监听脚本加载完成（看到"✓ JavaScript监听脚本已注入"提示）

### Q2: 密码被记录为 `[PASSWORD_RECORDED]`？
**A**: 这是正常的安全措施。密码字段会被标记，但不会保存真实密码。您需要在生成的代码中手动填入密码。

### Q3: 选择器不准确怎么办？
**A**: 
- 查看 `recorded_actions.json` 中的 selector 字段
- 在浏览器控制台测试：`document.querySelector('#your-selector')`
- 如果不准确，手动调整选择器（优先使用ID）

### Q4: 登录后页面跳转了怎么办？
**A**: 录制工具会自动记录最终的URL。您可以在 `recorded_actions.json` 的 `metadata.url` 中看到。

### Q5: 如何调试录制过程？
**A**: 
1. 打开浏览器的开发者工具（F12）
2. 切换到 Console 标签
3. 您会看到类似 `📝 Recorded click: {...}` 的日志
4. 这些日志显示了每个操作的详细信息

---

## 🎯 最佳实践

1. **操作前等待**：看到"✓ JavaScript监听脚本已注入"后再开始操作
2. **缓慢操作**：每个操作之间间隔1-2秒，确保被正确记录
3. **避免刷新**：尽量不要刷新页面，这可能导致监听脚本失效
4. **记录关键步骤**：只记录必要的操作步骤，不需要记录所有点击
5. **验证选择器**：录制后在浏览器控制台测试生成的选择器是否有效

---

## 📝 示例操作流程

假设您要录制一个完整的登录和数据查询流程：

```
1. 运行: python record_browser.py
2. 浏览器自动打开登录页面
3. 在用户名框输入: admin
4. 在密码框输入: 123456
5. 点击"登录"按钮
6. 等待页面加载完成
7. 点击"样机管理"菜单
8. 在搜索框输入: SYNCO
9. 点击"搜索"按钮
10. 等待搜索结果加载
11. 回到命令行，按回车
12. 查看生成的文件
```

生成的 `auto_login.py` 将包含所有这些步骤的代码！

---

## 🚀 下一步

录制完成后：

1. ✅ 查看 `auto_login.py` 了解自动生成的代码
2. ✅ 编辑代码，填入真实的密码
3. ✅ 测试生成的代码是否能正常运行
4. ✅ 将代码集成到 `main.py` 中
5. ✅ 运行 `python main.py` 测试完整流程

祝您录制顺利！🎉
