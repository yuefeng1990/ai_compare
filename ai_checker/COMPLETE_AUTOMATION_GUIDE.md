# 🎯 自动化登录和操作流程完整指南

## ✅ 已实现的功能

### 1. **完整的OAuth两步授权登录流程**

```
首页 → 点击"立即登录" 
  ↓
OAuth页面1 → 输入用户名密码 → 点击"用户登录"
  ↓
OAuth页面2 → 点击"授权"按钮
  ↓
目标首页 → 登录成功
```

**关键实现：**
- ✅ 自动检测并点击"立即登录"按钮
- ✅ 智能识别授权页面的文本内容（而非依赖URL）
- ✅ 处理两步OAuth授权流程
- ✅ 循环检查直到跳转到目标域名

---

### 2. **Tab式菜单导航（iframe支持）**

```
点击"审核管理"菜单
  ↓
展开子菜单，点击"兼容性测评审核"
  ↓
检测到iframe结构
  ↓
切换到正确的iframe (iframe3: system/certificate/apply)
```

**关键实现：**
- ✅ 识别Tab式导航结构
- ✅ 自动检测多个iframe
- ✅ 智能选择包含`certificate/apply`的目标iframe
- ✅ 在iframe上下文中执行后续操作

---

### 3. **表格搜索功能**

```
点击测评编号列的排序按钮 <button class="my-table-sort-icon sort-btn">
  ↓
进入搜索状态
  ↓
找到搜索输入框
  ↓
输入测评号（待从Excel读取）
  ↓
点击搜索按钮
  ↓
等待表格更新
```

**关键实现：**
- ✅ 使用JavaScript直接触发点击（绕过fixed-columns拦截）
- ✅ 验证按钮属于"测评编号"列
- ✅ 在iframe中查找和操作元素
- ✅ 多种选择器策略提高成功率

---

### 4. **详情页访问**

```
点击第一行的"详情"链接
  ↓
使用JavaScript触发点击（避免元素拦截）
  ↓
等待详情页加载
  ↓
检测多种详情页标识
```

**关键实现：**
- ✅ JavaScript点击绕过fixed-columns-right拦截
- ✅ 多种详情页标识检测
- ✅ 检查新iframe出现（详情页可能在新iframe中）

---

## 🔧 核心技术要点

### 1. **基于文本内容的等待策略**

```python
# ✅ 好：基于页面实际内容
web_checker.wait_for_selector(
    'input[type="text"], :has-text("用户名"), :has-text("授权")', 
    timeout=15000
)

# ❌ 不好：基于URL（OAuth URL复杂多变）
web_checker.page.wait_for_url('**/mng/logon**', timeout=15000)
```

**优势：**
- 不受URL参数变化影响
- 适应多次跳转
- 更可靠地检测页面加载完成

---

### 2. **iframe上下文操作**

```python
# 获取目标iframe
target_frame = web_checker.page.frame_locator('iframe[name="iframe3"]')

# 在iframe中查找元素
element = target_frame.locator('button.sort-btn').first

# 在iframe中执行操作
element.evaluate('el => el.click()')  # JavaScript点击
```

**关键点：**
- 所有后续操作必须在iframe上下文中执行
- 使用`frame_locator()`切换到iframe
- 使用`locator()`而不是`query_selector()`

---

### 3. **JavaScript点击绕过元素拦截**

```python
# 问题：fixed-columns覆盖导致常规点击失败
element.click(timeout=5000)  # ❌ Timeout: subtree intercepts pointer events

# 解决：使用JavaScript直接触发
element.evaluate('el => el.click()')  # ✅ 成功
```

**适用场景：**
- 固定列（fixed-columns）覆盖
- 其他元素z-index更高
- 元素被遮挡但需要点击

---

### 4. **多重选择器策略**

```python
sort_button_selectors = [
    'button.my-table-sort-icon.sort-btn',
    '.my-table-sort-icon.sort-btn',
    '[data-field="certificationNumber"] button.sort-btn',
    'th[data-field="certificationNumber"] button'
]

for selector in sort_button_selectors:
    element = target_frame.locator(selector).first
    if element.count() > 0:
        # 验证是目标列
        parent_text = element.evaluate('el => el.closest("th").innerText')
        if '测评编号' in parent_text:
            element.evaluate('el => el.click()')
            break
```

**优势：**
- 提高在不同UI版本下的适应性
- 通过父元素验证确保准确性
- 一个失败自动尝试下一个

---

## 📊 完整执行流程

```
1. 启动浏览器（可视化模式）
   ↓
2. 打开首页 https://compatibility.openharmony.cn/mng/index
   ↓
3. 检测登录状态
   ├─ 已登录 → 跳过登录步骤
   └─ 未登录 → 执行登录流程
       ├─ 点击"立即登录"
       ├─ 等待授权页面（基于文本内容）
       ├─ 输入用户名和密码
       ├─ 点击"用户登录"
       ├─ 等待第二个授权页面
       ├─ 点击"授权"按钮
       └─ 循环检查直到跳转到目标域名
   ↓
4. 点击"审核管理"菜单
   ↓
5. 点击"兼容性测评审核"子菜单
   ↓
6. 检测iframe结构
   ├─ 找到2个iframe
   ├─ 选择iframe3 (system/certificate/apply)
   └─ 切换到iframe上下文
   ↓
7. 在iframe中执行搜索
   ├─ 点击测评编号排序按钮（JavaScript点击）
   ├─ 等待搜索输入框出现
   ├─ 输入测评号（待实现）
   ├─ 点击搜索按钮
   └─ 等待表格更新
   ↓
8. 在iframe中查看详情
   ├─ 找到"详情"链接
   ├─ JavaScript点击（绕过拦截）
   ├─ 等待详情页加载
   └─ 检测多种详情页标识
   ↓
9. 完成！
```

---

## 🚀 当前状态

### ✅ 已完成
- [x] OAuth两步授权登录
- [x] Tab式菜单导航
- [x] iframe检测和切换
- [x] 排序按钮点击（JavaScript方式）
- [x] 搜索按钮点击
- [x] 详情按钮点击（JavaScript方式）
- [x] 详细的调试输出

### ⏳ 待完成
- [ ] 从Excel读取测评号并填入搜索框
- [ ] 详情页内容提取
- [ ] 数据对比逻辑
- [ ] 结果导出

---

## 💡 最佳实践总结

### 1. **调试先行**
```bash
# 遇到问题时，先运行调试脚本
python debug_menu_navigation.py
```

### 2. **iframe操作要点**
```python
# 始终在iframe上下文中操作
target_frame = page.frame_locator('iframe[name="xxx"]')
element = target_frame.locator('selector').first
element.evaluate('el => el.click()')  # 优先使用JavaScript点击
```

### 3. **处理元素拦截**
```python
# 遇到 "subtree intercepts pointer events" 错误时
try:
    element.evaluate('el => el.click()')  # JavaScript点击
except:
    element.click(timeout=5000)  # 备选方案
```

### 4. **详细日志输出**
```python
print(f"✓ 找到元素 '{selector}'")
print(f"✓ 确认是目标元素 (父元素文本: '{parent_text}')")
print(f"✓ 操作成功")
```

---

## 📁 相关文档

- ✅ [auto_login.py](file://d:\AI_TEST\ai_compare\ai_checker\auto_login.py) - 主自动化脚本
- ✅ [test_login.py](file://d:\AI_TEST\ai_compare\ai_checker\test_login.py) - 测试脚本
- ✅ [debug_menu_navigation.py](file://d:\AI_TEST\ai_compare\ai_checker\debug_menu_navigation.py) - 菜单导航调试工具
- ✅ [TWO_STEP_AUTHORIZATION.md](file://d:\AI_TEST\ai_compare\ai_checker\TWO_STEP_AUTHORIZATION.md) - 两步授权流程说明
- ✅ [TEXT_BASED_WAITING.md](file://d:\AI_TEST\ai_compare\ai_checker\TEXT_BASED_WAITING.md) - 文本等待策略说明

---

## 🎉 总结

目前已成功实现：
1. ✅ 完整的OAuth登录流程
2. ✅ Tab式菜单导航和iframe切换
3. ✅ 表格搜索功能（点击排序按钮）
4. ✅ 详情页访问（JavaScript点击绕过拦截）

下一步将从Excel读取测评号并实现完整的数据对比功能！
