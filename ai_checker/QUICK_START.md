# 🚀 快速开始指南

## 📋 项目概述

这个项目用于**自动化比对**：
- Excel checklist 中的测试要求
- log.txt 中的设备信息
- 网页上的中文设备信息

---

## ⚡ 5分钟快速上手

### 步骤1️⃣：运行程序（当前状态）

```bash
cd d:\AI_TEST\ai_compare\ai_checker
python main.py
```

**当前功能**：
- ✅ 读取关键字模板（keywords.txt）
- ✅ 从Excel E列提取包含关键字的行
- ✅ 从log.txt提取关键字对应的值
- ⚠️ 网页部分需要登录和导航（待完善）

**输出结果**：`output/result.xlsx`

---

### 步骤2️⃣：录制浏览器操作（完善Web功能）

```bash
python record_browser.py
```

**操作流程**：
1. 浏览器自动打开
2. **您手动操作**：
   - 输入用户名和密码登录
   - 点击"样机管理"菜单
   - 找到数据显示页面
3. 按回车停止录制
4. 查看生成的文件

**生成文件**：
- `recorded_actions.json` - 完整操作记录
- `auto_login.py` - 自动生成的Python代码
- `page_content_sample.txt` - 页面内容
- `final_page.png` - 页面截图

---

### 步骤3️⃣：集成自动化代码

编辑 `main.py`，在注释 `TODO` 处添加录制的代码：

```python
# 1. 自动登录
web_checker.fill_input('#username', 'your_username')
web_checker.fill_input('#password', 'your_password')
web_checker.click_button('#login-button')
web_checker.wait_for_selector('.dashboard', timeout=10000)

# 2. 导航到数据页面
web_checker.click_button('#device-menu')
web_checker.wait_for_selector('.device-table')

# 3. 获取内容
web_content = web_checker.get_page_text()
```

---

### 步骤4️⃣：运行完整流程

```bash
python main.py
```

现在应该能：
- ✅ 自动登录网页
- ✅ 导航到数据页面
- ✅ 提取网页上的中文值
- ✅ 与log.txt的值进行比较
- ✅ 保存完整结果到Excel

---

## 📁 文件说明

### 核心文件
- `main.py` - 主程序入口
- `tools/web_checker.py` - 浏览器自动化工具
- `tools/compare.py` - 值比较工具
- `tools/excel_reader.py` - Excel读取工具
- `tools/txt_reader.py` - TXT文件读取工具

### 配置文件
- `data/keywords.txt` - 关键字模板（10个关键字）
- `data/checklist.xlsx` - 测试清单（从第5行开始）
- `data/log .txt` - 设备日志文件

### 录制工具
- `record_browser.py` - 智能录制脚本
- `auto_login.py` - 自动生成的登录代码
- `recorded_actions.json` - 录制数据

### 文档
- `RECORDING_GUIDE.md` - 录制工具使用指南
- `IMPLEMENTATION_GUIDE.md` - 详细实施指南
- `BROWSER_AUTOMATION_GUIDE.md` - 浏览器自动化工作流
- `QUICK_START.md` - 本文件

---

## 🎯 关键概念

### 工作流程
```
1. 读取关键字模板 (keywords.txt)
         ↓
2. 扫描Excel E列，找到包含关键字的行
         ↓
3. 对每个匹配的行：
   ├─ 从log.txt提取值
   ├─ 从网页提取值（需要登录+导航）
   └─ 比较两个值是否一致
         ↓
4. 保存结果到Excel
```

### 关键字映射
英文关键字 → 中文标签（网页上显示）
```python
'Manufacture' → ['制造商', '厂商']
'OsFullName' → ['操作系统全称', '系统名称']
'ProductModel' → ['产品型号', '设备型号']
# ... 更多映射在 compare.py 中
```

---

## 🔧 常用命令

```bash
# 运行主程序
python main.py

# 录制浏览器操作
python record_browser.py

# 查看生成的代码
cat auto_login.py

# 查看录制数据
cat recorded_actions.json
```

---

## ❓ 常见问题

### Q: 网页部分为什么显示"未在网页中找到"？
**A**: 因为还没有实现自动登录和导航。请运行 `record_browser.py` 录制操作步骤。

### Q: 如何查看浏览器实际操作过程？
**A**: 修改 `main.py` 中的这一行：
```python
web_checker = WebChecker(headless=False)  # False = 可视化模式
```

### Q: 录制的密码安全吗？
**A**: 是的。密码字段只会被标记为 `[PASSWORD_RECORDED]`，不会保存真实密码。您需要手动填入。

### Q: 如何选择正确的CSS选择器？
**A**: 
1. 在浏览器中右键点击元素 → "检查"
2. 在Elements面板中看到HTML结构
3. 优先使用ID选择器（如 `#username`）
4. 其次使用类选择器（如 `.login-btn`）

---

## 📊 输出示例

### 控制台输出
```
第13行 - 关键字: Manufacture
  描述: 公司英文名简称，最多32字符...
  log.txt值: Zhiying Technology
  web值: 智英科技
  比较结果: 不一致
```

### Excel输出 (`output/result.xlsx`)
| 行号 | E列描述 | 关键字 | log.txt值 | web值 | 值是否一致 | 比较状态 |
|------|---------|--------|-----------|-------|-----------|----------|
| 13 | 公司英文名简称... | Manufacture | Zhiying Technology | 智英科技 | 否 | 不一致 |

---

## 🎓 学习资源

- [Playwright Python文档](https://playwright.dev/python/)
- [CSS选择器教程](https://www.w3schools.com/cssref/css_selectors.asp)
- 项目文档：
  - `RECORDING_GUIDE.md` - 录制工具详解
  - `IMPLEMENTATION_GUIDE.md` - 实施步骤详解

---

## ✨ 下一步优化建议

1. **完善登录逻辑**：根据录制结果添加自动登录代码
2. **优化中文映射**：根据实际网页调整关键字到中文的映射
3. **添加错误处理**：处理网络超时、元素找不到等情况
4. **支持多设备**：批量处理多个设备的比对
5. **生成报告**：自动生成HTML格式的比对报告

---

**祝您使用愉快！** 🎉

如有问题，请查看详细文档或联系技术支持。
