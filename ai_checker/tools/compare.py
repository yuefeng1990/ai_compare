class CompareTool:
    def __init__(self, target_measurement_id=None):
        self.results = {}
        self._target_measurement_id = target_measurement_id  # 保存目标测评编号用于表格数据定位
    
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
            'MarketName': ['设备名称（传播名）'],
            'ProductModel': ['设备型号'],
            'DeviceType': ['设备类型'],
            'Brand': ['品牌英文名'],
            'Manufacture': ['企业简称（英文）'],
            'DisplayVersion': ['软件版本号'],
            'SecurityPatchTag': ['安全补丁标签'],
            'VersionId': ['版本Id'],
            'BuildRootHash': ['版本Hash'],
            'OsFullName': ['操作系统版本号']
        }
        
        # 获取可能的中文标签
        chinese_labels = keyword_mapping.get(keyword, [keyword])
        
        # 方法1：尝试从结构化HTML中提取（label + text结构，包括成对div）
        # 这是最精确的提取方式，优先使用
        for label in chinese_labels:
            value = self._extract_value_from_html_structure(web_content, label)
            if value:
                # 特殊处理：DeviceType需要从VersionId中提取第一个/前的部分
                if keyword == 'DeviceType' and '/' in value:
                    return value.split('/')[0].strip()
                return value.strip()
        
        # 方法2：尝试从垂直文本结构中提取（标签行 + 值行）
        # 作为备选方案，当HTML结构提取失败时使用
        vertical_value = self._extract_value_from_vertical_text(web_content, chinese_labels)
        if vertical_value:
            # 特殊处理：DeviceType需要从VersionId中提取第一个/前的部分
            if keyword == 'DeviceType' and '/' in vertical_value:
                return vertical_value.split('/')[0].strip()
            return vertical_value.strip()
        
        # 方法3：尝试从表格格式中提取（制表符分隔的行列数据）
        table_value = self._extract_value_from_table_format(web_content, keyword, chinese_labels)
        if table_value:
            return table_value.strip()
        
        # 方法4：回退到文本行匹配（兼容旧格式）
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
    
    def _extract_value_from_vertical_text(self, web_content, chinese_labels):
        """
        从垂直文本结构中提取值（标签行 + 下一行是值）
        结构示例：
        设备名称（传播名）：
        二参数融合控制器
        
        设备型号：
        YNS-200
        """
        lines = web_content.split('\n')
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # 跳过空行和包含问号的行（可能是占位符）
            if not line_stripped or '?' in line_stripped or '？' in line_stripped:
                continue
            
            # 检查当前行是否是目标标签
            for label in chinese_labels:
                # 精确匹配：标签应该在行的开头或包含在行中
                if line_stripped.startswith(label) or line_stripped == label:
                    # 找到标签后，向后查找第一个非空、非标签的值行
                    for j in range(i + 1, min(i + 5, len(lines))):  # 最多查找4行
                        value_line = lines[j].strip()
                        
                        # 跳过空行
                        if not value_line:
                            continue
                        
                        # 跳过包含问号的行（占位符）
                        if '?' in value_line or '？' in value_line:
                            continue
                        
                        # 跳过看起来像标签的行（以冒号结尾）
                        if value_line.endswith('：') or value_line.endswith(':'):
                            continue
                        
                        # 找到了有效值
                        return value_line
        
        return None
    
    def _extract_value_from_table_format(self, web_content, keyword, chinese_labels):
        """从表格格式中提取关键字对应的值（支持多行数据，定位到目标测评编号行）"""
        lines = web_content.split('\n')
        
        # 已知的表头标签列表（按顺序）
        known_labels = ['测评编号', 'ProdId', '测评类型', '操作系统类型', 
                       '操作系统版本号', '传播名', '设备型号', '芯片型号', 
                       '软件版本号', '提交时间', '企业名称', '企业简称（英文）', 
                       '测评状态', '审核人', '操作']
        
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
        
        # 步骤2：查找包含目标测评编号的数据行
        target_measurement_id = getattr(self, '_target_measurement_id', None)
        target_data_line = None
        
        for line in lines:
            if line.count('\t') >= 10:  # 这是一个数据行
                # 如果有目标测评编号，查找匹配的行
                if target_measurement_id and target_measurement_id in line:
                    target_data_line = line
                    print(f"      ✓ 找到目标测评编号 {target_measurement_id} 所在行")
                    break
                # 如果没有目标ID，使用第一个数据行（向后兼容）
                elif not target_measurement_id and not target_data_line:
                    target_data_line = line
        
        if not target_data_line:
            if target_measurement_id:
                print(f"      ⚠ 未找到包含测评编号 {target_measurement_id} 的行，使用第一个数据行")
                # 回退到第一个数据行
                for line in lines:
                    if line.count('\t') >= 10:
                        target_data_line = line
                        break
            else:
                return None
        
        # 步骤3：解析目标数据行
        data_columns = target_data_line.split('\t')
        
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
        支持两种结构：
        
        结构1：垂直文本结构（纯文本）
        设备名称（传播名）：
        二参数融合控制器
        
        结构2：成对div结构（HTML源码）
        <div class="form_div">
            <label class="label_left">企业全称：</label>
            <label class="label_right">企业全称（英文）：</label>
        </div>
        <div class="form_div mb-28">
            <text class="label_left">福建远恩智能技术有限公司</text>
            <text class="label_right">Fujian Yuanen Intelligent Technology Co., Ltd.</text>
        </div>
        """
        import re
        
        # 首先尝试从成对div结构中提取
        paired_div_value = self._extract_value_from_paired_divs(html_content, label)
        if paired_div_value:
            return paired_div_value
        
        # 回退到原有的label+text结构
        label_pattern = rf'<label[^>]*>{re.escape(label)}[：:]?\s*</label>'
        label_matches = list(re.finditer(label_pattern, html_content))
        
        if not label_matches:
            return None
        
        for label_match in label_matches:
            label_end_pos = label_match.end()
            remaining_content = html_content[label_end_pos:]
            
            value_patterns = [
                r'<text[^>]*>([^<]+)</text>',
                r'<span[^>]*>([^<]+)</span>',
                r'<div[^>]*class="form_div[^"]*"[^>]*>\s*<[^>]+>([^<]+)</[^>]+>',
            ]
            
            for pattern in value_patterns:
                value_match = re.search(pattern, remaining_content[:500])
                if value_match:
                    value = value_match.group(1).strip()
                    if value and len(value) > 0:
                        return value
        
        return None
    
    def _extract_value_from_paired_divs(self, html_content, label):
        """
        从成对div结构中提取值
        结构：
        <div class="form_div">
            <label class="label_left">标签1</label>
            <label class="label_right">标签2</label>
        </div>
        <div class="form_div mb-28">
            <text class="label_left">值1</text>
            <text class="label_right">값2</text>
        </div>
        """
        import re
        
        # 查找所有包含目标label的form_div（标签div）
        # 模式：<div class="form_div">...<label...>label_text</label>...</div>
        div_pattern = r'<div[^>]*class="form_div[^"]*"[^>]*>(.*?)</div>'
        div_matches = list(re.finditer(div_pattern, html_content, re.DOTALL))
        
        for i, div_match in enumerate(div_matches):
            div_content = div_match.group(1)
            
            # 检查这个div是否包含目标label（支持label_left或label_right）
            label_pattern = rf'<label[^>]*class="label_(left|right)[^"]*"[^>]*>{re.escape(label)}[：:]?\s*</label>'
            label_match = re.search(label_pattern, div_content)
            
            if label_match:
                # 确定是左边还是右边
                position = label_match.group(1)  # 'left' or 'right'
                
                # 查找下一个form_div（应该包含对应的值）
                if i + 1 < len(div_matches):
                    next_div_content = div_matches[i + 1].group(1)
                    
                    # 在下一个div中查找对应位置的text元素
                    text_pattern = rf'<text[^>]*class="label_{position}[^"]*"[^>]*>([^<]+)</text>'
                    text_match = re.search(text_pattern, next_div_content)
                    
                    if text_match:
                        value = text_match.group(1).strip()
                        if value:
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