# AI Checker — 日志关键字提取与网页比对工具

从设备日志 (`test.txt`) 中自动提取产品参数关键字，与 OpenHarmony 兼容性网站的内容进行比对，生成比对结果 Excel。

## 流程概览

```
┌─────────────────────────────────────────────────────────────┐
│  1. 读取 log.txt (data/test.txt)--将获取的日志或者基本信息拷到log.txt                           │
│     自动识别 UTF-8 / GB18030 / GBK 等编码，避免中文乱码       │
├─────────────────────────────────────────────────────────────┤
│  2. 从 log.txt 提取关键字                                    │
│     解析 key = value / key: value 行，提取参数名              │
│     支持中文 key，并忽略开头 get 前缀                         │
│     保存到 data/keywords.txt                                 │
├─────────────────────────────────────────────────────────────┤
│  3. 使用 9 个预定义目标关键字覆盖提取结果                    │
│     TARGET_KEYWORDS = [Manufacture, OsFullName,              │
│       MarketName, ProductModel, Brand, DisplayVersion,       │
│       VersionId, SecurityPatchTag, BuildRootHash]            │
├─────────────────────────────────────────────────────────────┤
│  4. 读取 Excel 检查清单 (data/checklist.xlsx)                │
├─────────────────────────────────────────────────────────────┤
│  5. 初始化对比工具 (CompareTool, 含目标测评编号)             │
├─────────────────────────────────────────────────────────────┤
│  6. 浏览器自动化（如提供 measurement_id）                    │
│     → 登录 → 导航审核管理 → 搜索测评编号 → 进入详情页       │
│     → 获取页面 HTML/文本内容                                 │
├─────────────────────────────────────────────────────────────┤
│  7. 从 log.txt 提取每个关键字的值（归一化匹配）              │
│     归一化忽略大小写、空格、_、- 和开头 get                  │
├─────────────────────────────────────────────────────────────┤
│  8. 从网页内容提取每个关键字的值                              │
│     （支持 4 种提取策略：成对 div / 垂直文本 / 表格 / 行匹配）│
├─────────────────────────────────────────────────────────────┤
│  9. 逐项比较 log 值与网页值（OsFullName 只比较前两位版本号） │
├─────────────────────────────────────────────────────────────┤
│ 10. 生成对比结果 Excel (output/result.xlsx)                  │
├─────────────────────────────────────────────────────────────┤
│ 11. 将比对结果写入 checklist.xlsx F 列（自检结果 ✔ / ❌）    │
│     首个数据行按 OsFullName 主/次版本是否 > 5.0 特殊判断     │
└─────────────────────────────────────────────────────────────┘
```

## 文件结构

```
ai_checker/
├── main.py                      # 主入口，流程编排（11 步完整流程）
├── auto_login.py                # 浏览器自动化（登录+导航+搜索+进入详情页）
├── tools/
│   ├── compare.py               # 关键字提取、网页值提取、比对逻辑（核心引擎）
│   ├── excel_reader.py          # Excel 读取（pandas + openpyxl）
│   ├── txt_reader.py            # TXT 关键字读取（备用工具，当前未在主流程中使用）
│   ├── web_checker.py           # Playwright 浏览器控制（导航/点击/填充/截图/iframe）
│   └── writer.py                # Excel 写入工具（当前未在主流程中使用）
├── data/
│   ├── test.txt                 # 设备日志（输入）
│   ├── keywords.txt             # 提取出的关键字（自动生成）
│   └── checklist.xlsx           # 检查清单（输入 + F 列写入自检结果）
├── output/
│   └── result.xlsx              # 比对结果（自动生成）
├── page_content_debug.txt       # 浏览器页面内容调试缓存（自动生成）
└── README.md
```

## 函数说明

### `main.py`

| 函数 | 说明 |
|---|---|
| `read_log_text(file_path)` | 读取日志文本，会尝试 `utf-8-sig` / `utf-8` / `gb18030` / `gbk` 并按乱码特征打分，尽量避开带 `�`、`锟斤拷` 等标记的解码结果。返回 `(content, encoding)`。 |
| `is_os_version_greater_than(os_full_name, minimum_version)` | 从 `OsFullName` 中提取主/次版本并判断是否大于指定版本。用于 checklist 首个数据行的 `> 5.0` 自检。 |
| `extract_keywords_from_log(log_content)` | 从日志中提取 `key = value` 或 `key: value` 行的参数名；如果存在 `Product Params` 标记则只解析标记范围，否则解析整段日志。支持中文 key，并会去掉开头的 `get`。返回 `list[str]`。 |
| `main(measurement_id=None)` | 主函数，编排完整流程（参见流程概览）。`measurement_id` 为可选的测评编号，提供时将启动浏览器搜索该编号的详情页。 |

**关键行为：** 第 2 步从 log 提取到所有关键字后，第 3 步会用 `TARGET_KEYWORDS`（9 个预定义关键字）覆盖，后续所有提取/比对只针对这 9 个关键字。

### `tools/compare.py` — 核心比对引擎

| 函数 | 说明 |
|---|---|
| `CompareTool.__init__(target_measurement_id)` | 初始化对比工具。`target_measurement_id` 用于在网页表格数据中精确定位目标行。 |
| `_normalize_keyword(text)` | 归一化关键字：移除空白、`_`、`-`，转小写，并忽略开头的 `get`（静态方法）。 |
| `extract_value_from_log(log_content, keyword)` | 从日志文本中查找 `keyword = value` 或 `keyword: value` 行，返回值。支持大小写、空格、`_`、`-` 和开头 `get` 不敏感匹配。 |
| `extract_value_from_web(web_content, keyword)` | 从网页内容中提取关键字对应的值。按优先级依次尝试 4 种策略——见下方"网页值提取策略"。 |
| `_extract_value_from_html_structure(html_content, label)` | **策略1（最高优先）：** 从 HTML 结构中提取。先尝试成对 div 结构提取，回退到 label+value 标签匹配。 |
| `_extract_value_from_paired_divs(html_content, label)` | 从成对 div 结构 `<div class="form_div"><label>标签</label>...</div>` + 下一个 `<div class="form_div"><text>值</text>...</div>` 中提取对应标签的值。 |
| `_extract_value_from_vertical_text(web_content, chinese_labels)` | **策略2：** 从垂直文本结构中提取（标签行 + 下一行是值）。跳过空行、问号占位符、冒号结尾行。 |
| `_extract_value_from_table_format(web_content, keyword, chinese_labels)` | **策略3：** 从制表符分隔的表格格式中提取。识别表头标签 → 定位目标测评编号所在行 → 按列索引取值。 |
| `_extract_value_after_label(line, label)` | **策略4（最低优先）：** 从单行文本中提取冒号/等号后的值（兼容旧格式）。 |
| `compare_values(log_value, web_value, keyword)` | 比较两个值是否一致。`OsFullName` 特殊处理：只比较前两位版本号（如 `5.1`）。 |
| `_compare_os_version(log_version, web_version)` | 比较 OS 版本号前两位数字（如 `OpenHarmony 5.1.0 Release` → `5.1`）。 |
| `_extract_os_version_prefix(version_string)` | 从版本字符串中提取数字部分的前两位版本号（正则 `\d+\.\d+`）。 |
| `compare_content_with_keywords(content, keywords)` | 检查内容是否包含指定关键字（简单包含匹配）。 |

### `tools/web_checker.py` — Playwright 浏览器控制

| 函数 | 说明 |
|---|---|
| `WebChecker.__init__(headless=False)` | 初始化浏览器控制器（默认可视模式）。 |
| `launch_browser()` | 启动 Chromium 浏览器。 |
| `close_browser()` | 关闭浏览器和 Playwright 实例。 |
| `navigate_to_url(url)` | 导航到指定 URL（wait_until='domcontentloaded'）。 |
| `click_button(selector)` | 点击按钮（按 `:has-text` 等多策略兜底）。 |
| `fill_input(selector, value)` | 填写输入框。 |
| `get_page_content()` | 获取页面 HTML 源码。 |
| `get_page_text()` | 获取页面可见文本（`body.innerText`）。 |
| `wait_for_selector(selector, timeout)` | 等待元素出现。 |
| `wait_for_user_action(prompt)` | 等待用户手动操作并按回车继续（用于录制脚本）。 |
| `get_element_text(selector)` | 获取指定元素的文本内容。 |
| `get_element_value(selector)` | 获取输入框的值。 |
| `screenshot(filename)` | 页面截图保存。 |
| `save_recording_info(info, filename)` | 保存录制的操作信息。 |
| `get_popup_content()` | 获取弹窗内容。 |
| `check_website_with_keywords(url, keywords)` | 综合检查：导航 → 点击弹窗 → 提取内容 → 比对关键字。 |

### `auto_login.py` — 浏览器自动化流程

| 函数 | 说明 |
|---|---|
| `automate_browser(web_checker)` | 自动化登录 + 导航到审核管理 → 兼容性测评审核。含完整 OAuth 授权流程（用户名密码 → 用户登录 → 授权确认），支持 iframe 切换。 |
| `automate_browser_with_search(web_checker, measurement_id)` | 在 `automate_browser` 基础上增加：在 iframe 表格中搜索目标测评编号 → 进入详情页。返回 `True/False`。 |
| `manual_login(web_checker)` | 输入用户名密码 + 点击授权按钮（支持两级授权流程），等待跳转到目标域名。 |



## 关键字提取规则

1. 读取日志时会尝试 UTF-8、`gb18030`、`gbk` 等编码，并按 `�`、`锟斤拷` 等乱码特征选择更可信的结果；如果源文件本身已经被错误编码保存并包含替换字符，只能提示告警，无法完全自动还原原始汉字。
2. 如果日志包含 `******To Obtain Product Params Start******` 和 `******To Obtain Product Params End  ******`，只解析该区域；如果没有该标记，则解析整段日志。
3. 逐行检查，筛选包含 `=` 或 `:` 的行。
4. 取分隔符左侧作为参数名（去除首尾空格）。
5. 如果参数名以 `get` 开头（如 `GetSecurityPatchTag`、`get Market Name`），提取和匹配时忽略该前缀。
6. 仅保留参数名只含中英文、数字、空格、`_`、`-`、中英文括号的**干净行**。
7. 所有提取到的参数名写入 `data/keywords.txt`，每行一个。
8. **提取后被 9 个预定义目标关键字覆盖**（`TARGET_KEYWORDS`），后续只处理这 9 个关键字的提取与比对。

## 9 个目标关键字与 Excel 检查项映射

| 序号 | 关键字（英文） | Excel C 列匹配文本 | 提取说明 |
|---|---|---|---|
| 10 | Manufacture | 企业简称（英文） | 从 log `Manufacture` 字段提取 |
| 13 | OsFullName | 操作系统版本号 | log 与网页只比较前两位版本号（如 `5.1`）；checklist 首个数据行特殊判断 `OsFullName > 5.0` |
| 14 | MarketName | 设备名称（传播名） | 从 log `MarketName` 字段提取 |
| 15 | ProductModel | 设备型号 | log 提取 + 网页映射 |
| 17 | Brand | 品牌英文名称 | 从 log `Brand` 字段提取 |
| 20 | DisplayVersion | 软件版本号 | 用户可见的软件版本号 |
| 21 | SecurityPatchTag | 安全补丁标签 | 也支持 `Security Patch` / `GetSecurityPatchTag` 等别名或 getter 形式匹配 |
| 22 | VersionId | 版本id | 设备类型 + 版本号组合 |
| 23 | BuildRootHash | 版本Hash | 版本哈希值 |

> 第 11 步利用 `keyword_checklist_map` 将比对结果写回 `checklist.xlsx` 的 F 列（自检结果），一致标记为 `✔`，不一致标记为 `❌`。首个数据行（当前 Excel 第 5 行、序号 1）不走普通映射，而是根据日志中的 `OsFullName` 主/次版本是否大于 `5.0` 写入 `✔/❌`。其他映射 key 统一使用 `CompareTool._normalize_keyword()`，因此同样忽略大小写、空格和开头 `get`。

## 网页值提取策略（按优先级）

当 `extract_value_from_web()` 提取网页关键字值时，按以下优先级依次尝试：

1. **成对 div 结构** (`_extract_value_from_paired_divs`)
   - 匹配 `<div class="form_div"><label>标签</label><label>...</label></div>` + 下一组 `<div class="form_div"><text>值</text><text>...</text></div>`
2. **垂直文本结构** (`_extract_value_from_vertical_text`)
   - 标签行 → 下一行取值，跳过空行、问号占位符、冒号结尾行
3. **表格格式** (`_extract_value_from_table_format`)
   - 识别表头标签 → 按测评编号定位目标行 → 按列索引取值
4. **行内文本匹配** (`_extract_value_after_label`)
   - 在单行文本中查找 `标签：值` 格式


## 使用方法

```bash
# 不启动浏览器（仅提取+保存关键字 + 跳过网页比对，只输出 log 提取结果）
python main.py

# 提供测评编号（启动浏览器，自动登录 → 搜索 → 获取网页内容 → 比对）
python main.py MEASUREMENT_ID_HERE
```
