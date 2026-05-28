# 🎯 测评编号搜索和对比功能使用指南

## 📋 功能概述

本工具支持通过测评编号自动搜索网页、进入详情页，提取关键字并与log.txt进行对比。

---

## 🚀 使用方法

### 方法1：命令行参数（推荐）

```bash
python main.py <测评编号>
```

**示例：**
```bash
python main.py CP2024001
python main.py MEASUREMENT_2024_001
```

### 方法2：交互式输入

```bash
python main.py
```

运行后会提示输入测评编号：
```
================================================================================
兼容性测评自动化检查工具
================================================================================

用法:
  python main.py <测评编号>

示例:
  python main.py CP2024001
================================================================================

请输入测评编号（直接回车跳过搜索）: CP2024001
```

### 方法3：仅登录不搜索

直接按回车跳过搜索，只执行登录和导航操作：
```bash
python main.py
# 输入时直接按回车
```

---

## 🔄 完整执行流程

```
1. 启动浏览器
   ↓
2. 打开首页 https://compatibility.openharmony.cn/mng/index
   ↓
3. 检测登录状态
   ├─ 已登录 → 跳过登录
   └─ 未登录 → 执行OAuth两步授权登录
       ├─ 点击"立即登录"
       ├─ 输入用户名密码
       ├─ 点击"用户登录"
       ├─ 点击"授权"按钮
       └─ 等待跳转到首页
   ↓
4. 导航到"审核管理" → "兼容性测评审核"
   ↓
5. 切换到iframe (system/certificate/apply)
   ↓
6. 【如果提供了测评编号】
   ├─ 点击测评编号列的排序按钮
   ├─ 在搜索框中输入测评编号
   ├─ 点击搜索按钮
   ├─ 等待表格更新
   └─ 点击第一行的"详情"按钮
   ↓
7. 等待详情页加载
   ↓
8. 提取页面文本内容
   ↓
9. 从网页和log.txt中提取8个关键字的值：
   ├─ MarketName (设备名称/传播名)
   ├─ ProductModel (设备型号)
   ├─ DeviceType (版本id)
   ├─ Brand (品牌英文名)
   ├─ DisplayVersion (软件版本号)
   ├─ SecurityPatchTag (安全补丁标签)
   ├─ VersionId (版本Id)
   └─ BuildRootHash (版本Hash)
   ↓
10. 对比网页值和log.txt值
    ↓
11. 保存结果到 output/result.xlsx
    ↓
12. 关闭浏览器
```

---

## 📊 输出结果

### 控制台输出示例

```
使用命令行参数 - 测评编号: CP2024001

1. 读取关键字模板...
找到 8 个关键字

2. 读取Excel测试数据（从第5行开始）...

3. 读取E列描述...
E列共有 100 行数据

4. 提取E列中包含目标关键字的行...
共找到 8 行包含目标关键字的数据

5. 读取log.txt内容...
   - log.txt文件大小: 5000 字符

6. 启动浏览器（可视化模式以便调试）...

7. 执行自动化操作...

      === 执行登录和导航 ===
      ✓ 检测到已登录状态

      === 导航到兼容性测评审核 ===
      ✓ 点击审核管理成功
      ✓ 点击兼容性测评审核成功
      ✓ 切换到iframe: system/certificate/apply

      === 搜索测评编号: CP2024001 ===
      ✓ 找到测评编号排序按钮
      ✓ 点击成功，进入搜索状态
      ✓ 输入测评编号成功
      ✓ 点击搜索按钮成功

      === 进入详情页 ===
      ✓ 找到详情按钮
      ✓ 点击详情按钮成功
      ✓ 已完成搜索并进入详情页

8. 获取详情页内容...
   ✓ 获取到 15000 字符的页面内容

9. 从网页和log.txt中提取关键字对应的值...

处理关键字: MarketName
   ✓ log.txt: OpenHarmony Device
   ✓ 网页: OpenHarmony Device
   → 比较结果: 一致

处理关键字: ProductModel
   ✓ log.txt: OH-Device-Pro
   ✓ 网页: OH-Device-Pro
   → 比较结果: 一致

...

📊 比对结果汇总:
================================================================================

✓ MarketName
   log.txt: OpenHarmony Device
   网页: OpenHarmony Device
   状态: 一致

✓ ProductModel
   log.txt: OH-Device-Pro
   网页: OH-Device-Pro
   状态: 一致

...

✅ 处理完成！结果已保存到: output/result.xlsx
```

### Excel输出格式

| 关键字 | 中文说明 | log.txt值 | 网页值 | 是否一致 | 状态 |
|--------|---------|-----------|--------|---------|------|
| MarketName | 设备名称（传播名） | OpenHarmony Device | OpenHarmony Device | TRUE | 一致 |
| ProductModel | 设备型号 | OH-Device-Pro | OH-Device-Pro | TRUE | 一致 |
| DeviceType | 版本id | v1.0 | v1.0 | TRUE | 一致 |
| ... | ... | ... | ... | ... | ... |

---

## 🔧 关键技术实现

### 1. **命令行参数解析**

```python
import sys

if __name__ == "__main__":
    # 从命令行获取测评编号参数
    measurement_id = None
    if len(sys.argv) > 1:
        measurement_id = sys.argv[1]
    else:
        # 交互式输入
        measurement_id = input("请输入测评编号: ").strip()
    
    main(measurement_id)
```

### 2. **条件执行搜索逻辑**

```python
def main(measurement_id=None):
    # ...
    
    if measurement_id:
        print(f"搜索测评编号: {measurement_id}")
        automate_browser_with_search(web_checker, measurement_id)
    else:
        # 只执行登录和导航
        automate_browser(web_checker)
```

### 3. **完整的搜索和详情访问流程**

```python
def automate_browser_with_search(web_checker, measurement_id):
    # 1. 执行登录（复用原有逻辑）
    # 2. 导航到审核管理
    # 3. 切换到iframe
    # 4. 点击排序按钮进入搜索状态
    # 5. 输入测评编号
    # 6. 点击搜索按钮
    # 7. 点击详情按钮
    # 8. 等待详情页加载
```

### 4. **JavaScript点击绕过元素拦截**

```python
# 点击排序按钮（fixed-columns覆盖）
element.evaluate('el => el.click()')

# 点击详情按钮（fixed-columns-right覆盖）
element.evaluate('el => el.click()')
```

---

## 💡 最佳实践

### 1. **首次使用建议**

```bash
# 第一次运行时，建议使用可视化模式观察整个流程
python main.py CP2024001
```

观察：
- 登录流程是否正常
- 菜单导航是否正确
- 搜索框是否出现
- 详情页是否成功打开

### 2. **调试技巧**

如果遇到问题，可以：

```bash
# 1. 只执行登录，不搜索
python main.py
# 输入时直接按回车

# 2. 检查生成的截图和HTML文件
ls -la *.png *.html

# 3. 查看详细错误信息
python main.py CP2024001 2>&1 | tee debug.log
```

### 3. **批量处理多个测评编号**

创建批处理脚本 `batch_run.sh` (Linux/Mac) 或 `batch_run.bat` (Windows)：

**Linux/Mac:**
```bash
#!/bin/bash
for id in CP2024001 CP2024002 CP2024003; do
    echo "Processing $id..."
    python main.py $id
done
```

**Windows:**
```batch
@echo off
for %%i in (CP2024001 CP2024002 CP2024003) do (
    echo Processing %%i...
    python main.py %%i
)
```

---

## ⚠️ 注意事项

### 1. **测评编号格式**

- 确保输入的测评编号与网页中完全一致
- 区分大小写
- 不要包含多余空格

### 2. **网络环境**

- 确保能访问 `https://compatibility.openharmony.cn`
- 首次登录可能需要较长时间
- 建议使用稳定的网络连接

### 3. **浏览器要求**

- 需要安装 Chromium 浏览器
- Playwright 会自动下载浏览器
- 首次运行可能需要几分钟下载浏览器

### 4. **文件依赖**

确保以下文件存在：
```
data/
├── checklist.xlsx      # Excel测试数据
├── keywords.txt        # 关键字模板
└── log .txt            # 日志文件（注意文件名有空格）

output/
└── result.xlsx         # 输出结果（自动生成）
```

---

## 🐛 常见问题

### Q1: 提示"无法找到测评编号排序按钮"

**原因：** 页面结构可能发生变化

**解决：**
1. 运行调试脚本查看当前页面结构
2. 更新选择器配置
3. 联系管理员确认页面是否有变化

### Q2: 搜索后没有找到数据

**原因：** 
- 测评编号不存在
- 测评编号输入错误
- 该编号不在当前用户的权限范围内

**解决：**
1. 检查测评编号是否正确
2. 手动在网页上搜索验证
3. 确认登录账号有权限查看该数据

### Q3: 详情页加载超时

**原因：**
- 网络速度慢
- 详情页内容较多
- iframe嵌套层级复杂

**解决：**
1. 增加等待时间（修改代码中的 `time.sleep()` 值）
2. 检查网络连接
3. 尝试刷新页面重新搜索

### Q4: 关键字提取失败

**原因：**
- 详情页中没有该关键字
- 关键字格式与预期不符
- 页面使用了动态渲染

**解决：**
1. 检查详情页HTML结构
2. 调整关键字匹配规则
3. 使用更灵活的正则表达式

---

## 📁 相关文件

- ✅ [main.py](file://d:\AI_TEST\ai_compare\ai_checker\main.py) - 主入口程序
- ✅ [auto_login.py](file://d:\AI_TEST\ai_compare\ai_checker\auto_login.py) - 自动化登录和搜索逻辑
- ✅ [tools/compare.py](file://d:\AI_TEST\ai_compare\ai_checker\tools\compare.py) - 关键字提取和对比工具
- ✅ [COMPLETE_AUTOMATION_GUIDE.md](file://d:\AI_TEST\ai_compare\ai_checker\COMPLETE_AUTOMATION_GUIDE.md) - 完整自动化指南

---

## 🎉 总结

本工具实现了：
1. ✅ 命令行参数支持测评编号
2. ✅ 自动搜索测评编号并进入详情页
3. ✅ 提取8个关键字的值
4. ✅ 与log.txt进行对比
5. ✅ 生成对比结果Excel

使用简单，功能强大，大大提高了兼容性测评的检查效率！
