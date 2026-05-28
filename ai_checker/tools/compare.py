class CompareTool:
    def __init__(self):
        self.results = {}
    
    def extract_value_from_log(self, log_content, keyword):
        """从log.txt中提取关键字对应的值"""
        lines = log_content.split('\n')
        for line in lines:
            # 匹配格式: keyword = value 或 keyword: value
            if '=' in line or ':' in line:
                parts = line.split('=', 1) if '=' in line else line.split(':', 1)
                if len(parts) == 2:
                    key_part = parts[0].strip()
                    value_part = parts[1].strip()
                    # 不区分大小写比较关键字
                    if key_part.lower() == keyword.lower():
                        return value_part
        return None
    
    def extract_value_from_web(self, web_content, keyword):
        """从网页内容中提取关键字对应的值（中文）"""
        # 建立英文关键字到中文标签的精确映射关系
        keyword_mapping = {
            'MarketName': ['设备名称（传播名）', '设备名称', '传播名'],
            'ProductModel': ['设备型号', '产品型号', '型号'],
            'DeviceType': ['设备类型'],  # 设备类型
            'Brand': ['品牌英文名', '品牌英文名称', '品牌'],
            'Manufacture': ['企业简称（英文）', '企业简称', '英文简称', 'Manufacturer'],
            'DisplayVersion': ['软件版本号', '显示版本', '软件版本'],
            'SecurityPatchTag': ['安全补丁标签', '安全补丁', '补丁标签'],
            'VersionId': ['版本Id', '版本ID', '版本标识', 'ProdId'],
            'BuildRootHash': ['版本Hash', '版本哈希', '根哈希', 'Hash'],
            'OsFullName': ['操作系统版本号', '系统版本', 'OS版本']
        }
        
        # 获取可能的中文标签
        chinese_labels = keyword_mapping.get(keyword, [keyword])
        
        # 方法1：尝试从结构化HTML中提取（label + text结构）
        for label in chinese_labels:
            value = self._extract_value_from_html_structure(web_content, label)
            if value:
                # 特殊处理：DeviceType需要从VersionId中提取第一个/前的部分
                if keyword == 'DeviceType' and '/' in value:
                    return value.split('/')[0].strip()
                return value.strip()
        
        # 方法2：尝试从表格格式中提取（制表符分隔的行列数据）
        table_value = self._extract_value_from_table_format(web_content, keyword, chinese_labels)
        if table_value:
            return table_value.strip()
        
        # 方法3：回退到文本行匹配（兼容旧格式）
        lines = web_content.split('\n')
        for line in lines:
            for label in chinese_labels:
                if label in line:
                    # 尝试提取冒号后的值
                    value = self._extract_value_after_label(line, label)
                    if value:
                        # 特殊处理：DeviceType需要从VersionId中提取第一个/前的部分
                        if keyword == 'DeviceType' and '/' in value:
                            return value.split('/')[0].strip()
                        return value.strip()
        
        return None
    
    def _extract_value_from_table_format(self, web_content, keyword, chinese_labels):
        """
        从表格格式中提取值
        支持两种格式：
        1. 传统表格：表头和数据都是水平排列
        2. 垂直表头：每个字段名单独一行，数据在后续行中
        
        当前页面格式（垂直表头）：
        测评编号
        ProdId
        测评类型
        ...
        传播名          <- 第6个标签
        设备型号         <- 第7个标签
        ...
        (空行)
        OHC443600006741	OH0001OM	商用设备	...	二参数融合控制器	YNS-200	...	V2.0.4-3
        """
        lines = web_content.split('\n')
        
        # 首先尝试传统的水平表格格式
        for i, line in enumerate(lines):
            if any(label in line for label in chinese_labels):
                if line.count('\t') >= 5:
                    # 找到表头行，使用传统方法提取
                    header_line_idx = i
                    header_line = lines[header_line_idx]
                    columns = header_line.split('\t')
                    
                    target_col_idx = None
                    for idx, col_name in enumerate(columns):
                        col_name_stripped = col_name.strip()
                        for label in chinese_labels:
                            if label in col_name_stripped:
                                target_col_idx = idx
                                break
                        if target_col_idx is not None:
                            break
                    
                    if target_col_idx is not None:
                        for j in range(header_line_idx + 1, min(header_line_idx + 10, len(lines))):
                            data_line = lines[j]
                            if not data_line.strip() or data_line.count('\t') < 3:
                                continue
                            
                            data_columns = data_line.split('\t')
                            if target_col_idx < len(data_columns):
                                value = data_columns[target_col_idx].strip()
                                if value and len(value) > 0:
                                    return value
        
        # 如果传统方法失败，尝试垂直表头格式
        # 策略：找到第一组标签（前14个），建立标签到列索引的映射
        
        known_labels = ['测评编号', 'ProdId', '测评类型', '操作系统类型', '操作系统版本号', 
                       '传播名', '设备型号', '芯片型号', '软件版本号', '提交时间', 
                       '企业名称', '企业简称（英文）', '测评状态', '审核人', '操作']
        
        # 步骤1：收集第一组标签行（遇到数据行就停止）
        label_to_index = {}
        current_index = 0
        found_data_row = False
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # 如果遇到数据行，停止收集标签
            if line.count('\t') >= 10:
                found_data_row = True
                break
            
            # 跳过空行和包含制表符的行
            if not line_stripped or '\t' in line:
                continue
            
            # 检查这一行是否是已知的标签
            for label in known_labels:
                if label == line_stripped and label not in label_to_index:
                    label_to_index[label] = current_index
                    current_index += 1
                    break
        
        if not found_data_row or not label_to_index:
            return None
        
        # 步骤2：找到第一个数据行
        data_line = None
        for line in lines:
            if line.count('\t') >= 10:
                data_line = line
                break
        
        if not data_line:
            return None
        
        # 步骤3：解析数据行
        data_columns = data_line.split('\t')
        
        # 步骤4：查找目标标签对应的列
        for label in chinese_labels:
            if label in label_to_index:
                col_idx = label_to_index[label] + 1  # +1 因为数据行第一列是空的
                if col_idx < len(data_columns):
                    value = data_columns[col_idx].strip()
                    if value and len(value) > 0:
                        return value
        
        return None
    
    def _extract_value_from_html_structure(self, html_content, label):
        """
        从HTML结构中提取label对应的值
        结构示例：
        <div class="form_div">
            <label class="label_left color-b5b5b5">品牌英文名：</label>
        </div>
        <div class="form_div mb-28">
            <text class="label_left" style="white-space: pre-wrap;">zdeer</text>
        </div>
        """
        import re
        
        # 查找包含label的div
        # 模式：<label...>label_text</label>
        label_pattern = rf'<label[^>]*>{re.escape(label)}[：:]?\s*</label>'
        label_matches = list(re.finditer(label_pattern, html_content))
        
        if not label_matches:
            return None
        
        # 对于每个找到的label，查找紧随其后的text元素
        for label_match in label_matches:
            label_end_pos = label_match.end()
            
            # 在label之后查找下一个包含text或span元素的div
            # 查找模式：<div...><text...>value</text></div> 或 <div...><span...>value</span></div>
            remaining_content = html_content[label_end_pos:]
            
            # 尝试匹配各种可能的值容器结构
            value_patterns = [
                r'<text[^>]*>([^<]+)</text>',  # <text>value</text>
                r'<span[^>]*>([^<]+)</span>',  # <span>value</span>
                r'<div[^>]*class="form_div[^"]*"[^>]*>\s*<[^>]+>([^<]+)</[^>]+>',  # div内的任何元素
            ]
            
            for pattern in value_patterns:
                value_match = re.search(pattern, remaining_content[:500])  # 限制搜索范围
                if value_match:
                    value = value_match.group(1).strip()
                    if value and len(value) > 0:
                        return value
        
        return None
    
    def _extract_value_after_label(self, line, label):
        """从行中提取标签后的值"""
        # 尝试多种分隔符
        separators = ['：', ':', '=', '： ', ': ']
        
        for sep in separators:
            if sep in line:
                parts = line.split(sep, 1)
                if len(parts) == 2:
                    # 检查label是否在parts[0]中
                    if label in parts[0]:
                        value = parts[1].strip()
                        if value:
                            return value
        
        return None
    
    def compare_values(self, log_value, web_value, keyword=None):
        """比较两个值是否相同"""
        if log_value is None or web_value is None:
            return False
        
        # 特殊处理：OsFullName 只比较前两位版本号
        if keyword == 'OsFullName':
            return self._compare_os_version(log_value, web_value)
        
        # 不区分大小写比较
        return log_value.lower() == web_value.lower()
    
    def _compare_os_version(self, log_version, web_version):
        """
        比较操作系统版本号（只比较前两位）
        例如：OpenHarmony 5.1.0 Release vs OpenHarmony 5.1.2 -> True
              OpenHarmony 5.1.x vs OpenHarmony 5.2.x -> False
        """
        if not log_version or not web_version:
            return False
        
        # 提取前两位版本号
        log_prefix = self._extract_os_version_prefix(log_version)
        web_prefix = self._extract_os_version_prefix(web_version)
        
        if not log_prefix or not web_prefix:
            # 如果无法提取版本号，回退到完整比较
            return log_version.lower() == web_version.lower()
        
        # 比较前缀（不区分大小写）
        return log_prefix.lower() == web_prefix.lower()
    
    def _extract_os_version_prefix(self, version_string):
        """
        从版本字符串中提取前两位版本号（只提取数字部分）
        例如：
        - "OpenHarmony 5.1.0 Release" -> "5.1"
        - "OpenHarmony-5.1.0.0" -> "5.1"
        - "Android 12.0.0" -> "12.0"
        - "iOS 16.5.1" -> "16.5"
        """
        import re
        
        # 直接匹配版本号数字（支持空格或连字符分隔）
        pattern = r'(\d+\.\d+)'
        match = re.search(pattern, version_string)
        
        if match:
            return match.group(1)
        
        # 完全无法提取，返回原字符串
        return version_string
    
    def compare_content_with_keywords(self, content, keywords):
        """比较内容是否包含关键字"""
        comparison_results = {}
        
        for keyword in keywords:
            # 检查关键字是否在内容中（不区分大小写）
            found = keyword.lower() in content.lower()
            comparison_results[keyword] = found
        
        return comparison_results