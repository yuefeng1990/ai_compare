"""
自动生成的浏览器自动化脚本
根据用户提供的操作步骤生成
"""
import time

def automate_browser(web_checker):
    """执行自动化登录和导航操作"""
    
    try:
        # === 第一步：检查是否已登录或需要登录 ===
        print("      - 检查登录状态...")
        
        # 等待页面加载完成
        try:
            web_checker.wait_for_selector('body', timeout=10000)
        except:
            pass
        
        # 检查是否已经登录（通过检测菜单是否存在）
        is_logged_in = False
        try:
            # 尝试查找菜单元素，如果存在说明已登录
            web_checker.wait_for_selector('.el-menu, .sidebar, nav', timeout=3000)
            is_logged_in = True
            print("      ✓ 检测到已登录状态")
        except:
            print("      - 未检测到登录状态，准备登录...")
        
        if not is_logged_in:
            # 首先检查是否有"立即登录"按钮，需要先点击它
            print("      - 检查是否有'立即登录'按钮...")
            has_immediate_login = False
            
            immediate_login_selectors = [
                '.btn',  # 主要的"立即登录"按钮（div元素）
                'div.btn',
                'div:has-text("立即登录")',
                'div[onclick*="login"]',
                'button:has-text("立即登录")',
                'button:has-text("快速登录")',
                'a:has-text("立即登录")',
                '.immediate-login-btn',
                '#immediate-login',
                '.quick-login',
                'span:has-text("立即登录")'
            ]
            
            for selector in immediate_login_selectors:
                try:
                    element = web_checker.page.query_selector(selector)
                    if element:
                        has_immediate_login = True
                        print(f"      ✓ 发现'{selector}'按钮，点击立即登录...")
                        web_checker.page.click(selector, timeout=5000)
                        print(f"      - 等待跳转到授权页面...")
                        
                        # 等待授权页面的特征元素出现（使用文本内容而非URL）
                        try:
                            # 等待输入框或授权相关文本出现
                            web_checker.wait_for_selector(
                                'input[type="text"], input[type="password"], :has-text("用户名"), :has-text("账号"), :has-text("密码"), :has-text("OAuth"), :has-text("授权")', 
                                timeout=15000
                            )
                            print(f"      ✓ 检测到授权页面元素")
                            
                            # 额外等待确保页面完全渲染
                            time.sleep(2)
                        except:
                            print(f"      ⚠ 等待授权页面元素超时")
                            time.sleep(3)
                        
                        print(f"      ✓ 授权页面加载完成")
                        break
                except Exception as e:
                    continue
            
            if has_immediate_login:
                print("      ✓ 已点击立即登录，现在输入用户名和密码...")
                # 点击后立即输入用户名密码
                manual_login(web_checker)
            else:
                # 没有"立即登录"按钮，直接输入用户名密码
                print("      - 未发现'立即登录'按钮，直接执行登录...")
                manual_login(web_checker)
        else:
            print("      ✓ 已登录，跳过登录步骤")
        
        # 等待页面加载完成
        try:
            web_checker.wait_for_selector('.el-menu, .sidebar, nav', timeout=5000)
            print("      ✓ 首页加载完成")
        except:
            print("      ⚠ 等待首页加载超时")
        
        # === 第二步：导航到审核管理 ===
        print("      - 点击审核管理菜单...")
        menu_clicked = False
        
        # 方法1：使用 Playwright 的文本选择器（推荐）
        try:
            print("      - 尝试使用文本选择器点击审核管理...")
            web_checker.page.click('text=审核管理', timeout=5000)
            print("      ✓ 已点击审核管理菜单（使用text选择器）")
            menu_clicked = True
            # 等待子菜单展开
            time.sleep(1)
        except Exception as e:
            print(f"      ⚠ text选择器失败: {str(e)}")
        
        # 方法2：如果方法1失败，尝试查找包含文本的元素并点击
        if not menu_clicked:
            try:
                print("      - 尝试遍历元素查找'审核管理'...")
                # 获取所有可能的菜单元素类型
                elements = web_checker.page.query_selector_all('a, div, span, li, button')
                for element in elements:
                    try:
                        text = element.inner_text()
                        if '审核管理' in text and element.is_visible():
                            print(f"      ✓ 找到菜单项，文本: '{text[:50]}...'")
                            # 使用 JavaScript 直接触发点击事件，避免元素拦截
                            web_checker.page.evaluate('(el) => el.click()', element)
                            print("      ✓ 已点击菜单项")
                            menu_clicked = True
                            time.sleep(1)
                            break
                    except:
                        continue
            except Exception as e:
                print(f"      ⚠ 元素遍历失败: {str(e)}")

        if not menu_clicked:
             print(f"      ⚠ 未找到审核管理菜单")
             # 不再尝试硬编码URL跳转，而是依赖UI交互

        print("      - 点击兼容性测评审核...")
        # 等待子菜单出现
        time.sleep(1)
        
        sub_menu_clicked = False
        # 方法1：使用 Playwright 的文本选择器
        try:
            print("      - 尝试使用文本选择器点击兼容性测评审核...")
            web_checker.page.click('text=兼容性测评审核', timeout=5000)
            print("      ✓ 已点击兼容性测评审核菜单（使用text选择器）")
            sub_menu_clicked = True
        except Exception as e:
            print(f"      ⚠ text选择器失败: {str(e)}")

        # 方法2：如果方法1失败，尝试查找包含文本的元素并点击
        if not sub_menu_clicked:
            try:
                print("      - 尝试遍历元素查找'兼容性测评审核'...")
                elements = web_checker.page.query_selector_all('a, div, span, li, button')
                for element in elements:
                    try:
                        text = element.inner_text()
                        if '兼容性测评审核' in text and element.is_visible():
                            print(f"      ✓ 找到子菜单项，文本: '{text[:50]}...'")
                            web_checker.page.evaluate('(el) => el.click()', element)
                            print("      ✓ 已点击子菜单项")
                            sub_menu_clicked = True
                            break
                    except:
                        continue
            except Exception as e:
                print(f"      ⚠ 元素遍历失败: {str(e)}")

        if sub_menu_clicked:
            # 等待标签页切换和内容加载
            time.sleep(3)
            
            # 尝试等待iframe或主内容区域加载
            try:
                # 等待主内容区域
                web_checker.wait_for_selector('.main-content, .J_mainContent, iframe, .el-table', timeout=15000)
                print("      ✓ 内容区域加载成功")
                
                # 如果存在iframe，切换到第一个
                iframes = web_checker.page.query_selector_all('iframe')
                if iframes:
                    print(f"      - 检测到 {len(iframes)} 个iframe")
                    
                    # 打印所有iframe的信息
                    for i, iframe in enumerate(iframes):
                        iframe_name = iframe.get_attribute('name') or '无名'
                        iframe_src = iframe.get_attribute('src') or '无src'
                        print(f"        iframe{i+1}: name='{iframe_name}', src='{iframe_src}'")
                    
                    # 尝试找到包含'certificate'或'apply'的iframe（兼容性测评审核页面）
                    target_iframe = None
                    for iframe in iframes:
                        iframe_src = iframe.get_attribute('src') or ''
                        iframe_name = iframe.get_attribute('name') or ''
                        # 优先选择包含certificate或apply的iframe
                        if 'certificate' in iframe_src or 'apply' in iframe_src:
                            target_iframe = iframe
                            print(f"      - 找到目标iframe: name='{iframe_name}', src='{iframe_src}'")
                            break
                    
                    # 如果没找到，使用最后一个iframe
                    if not target_iframe and iframes:
                        target_iframe = iframes[-1]
                        print(f"      - 使用最后一个iframe: name='{target_iframe.get_attribute('name')}'")
                    
                    if target_iframe:
                        print(f"      - 切换到目标iframe...")
                        # 使用frame_locator切换到iframe
                        frame = web_checker.page.frame_locator(f'iframe[name="{target_iframe.get_attribute("name")}"]')
                        
                        # 等待iframe内容加载
                        try:
                            frame.locator('body').wait_for(timeout=10000)
                            print("      ✓ iframe内容加载成功")
                            
                            # 在iframe中查找表格
                            table_in_iframe = frame.locator('.el-table, table').first
                            if table_in_iframe.count() > 0:
                                print("      ✓ 在iframe中找到表格")
                        except Exception as e:
                            print(f"      ⚠ iframe内容等待异常: {str(e)}")
                    else:
                        print(f"      ⚠ 未找到目标iframe")
                
                # 额外等待确保数据加载完成
                time.sleep(2)
            except Exception as e:
                print(f"      ⚠ 内容加载等待异常: {str(e)}")
                time.sleep(3)
        else:
            print(f"      ⚠ 未找到兼容性测评审核菜单")
        
        # === 在iframe中执行后续操作 ===
        print("\n      === 在iframe中执行搜索和详情操作 ===")
        
        # 获取目标iframe
        target_frame = None
        try:
            iframes = web_checker.page.query_selector_all('iframe')
            for iframe in iframes:
                iframe_src = iframe.get_attribute('src') or ''
                if 'certificate' in iframe_src or 'apply' in iframe_src:
                    target_frame = web_checker.page.frame_locator(f'iframe[name="{iframe.get_attribute("name")}"]')
                    print(f"      ✓ 使用iframe: {iframe_src}")
                    break
        except Exception as e:
            print(f"      ⚠ 获取iframe失败: {str(e)}")
        
        if target_frame:
            # === 第三步：在iframe中搜索测评编号 ===
            print("      - 查找并点击测评编号的排序按钮...")
            try:
                # 等待表格加载
                time.sleep(2)
                
                # 点击测评编号列的排序按钮（这是进入搜索状态的关键步骤）
                sort_button_selectors = [
                    'button.my-table-sort-icon.sort-btn',
                    '.my-table-sort-icon.sort-btn',
                    'button.sort-btn i.icon.icon-sort',
                    '[data-field="certificationNumber"] button.sort-btn',
                    '[data-field="certificationNumber"] .sort-btn',
                    'th[data-field="certificationNumber"] button'
                ]
                
                clicked = False
                for selector in sort_button_selectors:
                    try:
                        element = target_frame.locator(selector).first
                        if element.count() > 0:
                            print(f"      ✓ 找到测评编号排序按钮 '{selector}'")
                            
                            # 验证这是"测评编号"列的按钮
                            parent_text = element.evaluate('el => el.closest("th") ? el.closest("th").innerText : ""')
                            if '测评编号' in parent_text:
                                print(f"      ✓ 确认是测评编号列的按钮 (父元素文本: '{parent_text[:30]}')")
                                
                                # 执行点击（使用JavaScript直接触发，避免被其他元素拦截）
                                try:
                                    element.evaluate('el => el.click()')
                                    print(f"      ✓ 点击排序按钮成功（使用JavaScript），进入搜索状态")
                                    
                                    # 等待搜索输入框出现
                                    time.sleep(2)
                                    clicked = True
                                except Exception as click_error:
                                    print(f"      ⚠ JavaScript点击失败: {str(click_error)}")
                                    # 尝试常规点击作为备选
                                    try:
                                        element.click(timeout=5000)
                                        print(f"      ✓ 点击排序按钮成功（常规方式）")
                                        time.sleep(2)
                                        clicked = True
                                    except Exception as e2:
                                        print(f"      ⚠ 常规点击也失败: {str(e2)}")
                                # 无论点击成功与否，都退出循环
                                break
                            else:
                                print(f"      ⚠ 找到按钮但不是测评编号列 (父元素文本: '{parent_text[:30]}')，继续查找...")
                    except Exception as e:
                        continue
                
                if not clicked:
                    print(f"      ⚠ 未成功点击测评编号排序按钮")
                    
                    # 调试：查找iframe中的所有排序按钮
                    try:
                        all_sort_buttons = target_frame.locator('button.sort-btn, .my-table-sort-icon').all()
                        print(f"      - iframe中共有 {len(all_sort_buttons)} 个排序按钮")
                        for i, btn in enumerate(all_sort_buttons[:10]):
                            class_name = btn.get_attribute('class') or '无class'
                            parent_text = btn.evaluate('el => el.closest("th") ? el.closest("th").innerText : "无父元素"')
                            print(f"        按钮{i+1}: class='{class_name[:50]}', 父元素文本='{parent_text[:40]}'")
                    except Exception as e:
                        print(f"      - 调试信息获取失败: {str(e)}")
                        
                    # 尝试查找所有包含icon-sort的元素
                    try:
                        sort_icons = target_frame.locator('i.icon-sort').all()
                        print(f"      - 找到 {len(sort_icons)} 个icon-sort图标")
                        for i, icon in enumerate(sort_icons[:5]):
                            parent_btn = icon.evaluate('el => el.closest("button") ? el.closest("button").className : "无父按钮"')
                            print(f"        图标{i+1}: 父按钮class='{parent_btn[:60]}'")
                    except:
                        pass
            except Exception as e:
                print(f"      ⚠ 点击排序按钮失败: {str(e)}")
            
            # 在iframe中查找测评编号搜索框
            print("      - 查找测评编号搜索输入框...")
            try:
                # 等待搜索区域展开
                time.sleep(1)
                
                # 查找测评编号相关的输入框
                search_input_selectors = [
                    'input[placeholder*="测评编号"]',
                    'input[placeholder*="测评"]',
                    'input[placeholder*="编号"]',
                    'input[placeholder*="搜索"]',
                    '.el-input__inner',
                    'input[type="text"]:not([type="hidden"])'
                ]
                
                found = False
                for selector in search_input_selectors:
                    try:
                        inputs = target_frame.locator(selector).all()
                        if inputs and len(inputs) > 0:
                            print(f"      ✓ 使用选择器 '{selector}' 在iframe中找到 {len(inputs)} 个输入框")
                            for i, inp in enumerate(inputs[:5]):
                                placeholder = inp.get_attribute('placeholder') or '无placeholder'
                                input_type = inp.get_attribute('type') or 'text'
                                print(f"        输入框{i+1}: type={input_type}, placeholder='{placeholder[:40]}'")
                            found = True
                            break
                    except:
                        continue
                
                if not found:
                    print(f"      ⚠ 未找到搜索输入框")
                    
                    # 调试：查找iframe中所有的输入框
                    try:
                        all_inputs = target_frame.locator('input:not([type="hidden"]):not([type="checkbox"])').all()
                        print(f"      - iframe中共有 {len(all_inputs)} 个可见输入框")
                        for i, inp in enumerate(all_inputs[:10]):
                            input_type = inp.get_attribute('type') or 'text'
                            placeholder = inp.get_attribute('placeholder') or '无placeholder'
                            class_name = inp.get_attribute('class') or '无class'
                            print(f"        输入框{i+1}: type={input_type}, placeholder='{placeholder[:30]}', class='{class_name[:30]}'")
                    except Exception as e:
                        print(f"      - 调试失败: {str(e)}")
            except Exception as e:
                print(f"      ⚠ 查找搜索框失败: {str(e)}")
            
            print("      - 输入测评号...")
            try:
                # 这里暂时不输入具体的测评号，因为需要从Excel获取
                print(f"      ℹ 提示：需要从Excel读取测评号后填入")
                # 示例：target_frame.locator('input[placeholder*="测评编号"]').fill('MEASUREMENT_ID', timeout=5000)
            except Exception as e:
                print(f"      ⚠ 输入测评号失败: {str(e)}")
            
            print("      - 点击搜索按钮...")
            try:
                search_button_selectors = [
                    'button:has-text("搜索")',
                    '.el-button--primary:has-text("搜索")',
                    '.el-button:has-text("搜索")',
                    '.search-btn',
                    'button .el-icon-search + span',
                    'i.el-icon-search'
                ]
                
                clicked = False
                for selector in search_button_selectors:
                    try:
                        element = target_frame.locator(selector).first
                        if element.count() > 0:
                            btn_text = element.inner_text() or '无文本'
                            print(f"      ✓ 找到搜索按钮 '{selector}' (文本: '{btn_text}')")
                            element.click(timeout=5000)
                            print(f"      ✓ 点击搜索按钮成功")
                            clicked = True
                            break
                    except:
                        continue
                
                if not clicked:
                    print(f"      ⚠ 未找到搜索按钮")
                    
                    # 调试：查找iframe中所有包含"搜索"文本的元素
                    try:
                        search_elements = target_frame.locator(':has-text("搜索")').all()
                        print(f"      - iframe中找到 {len(search_elements)} 个包含'搜索'的元素")
                        for i, elem in enumerate(search_elements[:10]):
                            text = elem.inner_text() or '无文本'
                            tag = elem.evaluate('el => el.tagName')
                            class_name = elem.get_attribute('class') or '无class'
                            print(f"        元素{i+1}: <{tag}> '{text[:40]}' (class: {class_name[:40]})")
                    except:
                        pass
                    
                    # 如果之前已经点击过排序按钮，可能自动触发搜索
                    print(f"      - 尝试等待表格更新...")
                
                # 等待搜索结果表格更新
                try:
                    target_frame.locator('.el-table__body, tbody, .table-data').first.wait_for(timeout=10000)
                    print("      ✓ 搜索完成")
                    
                    # 额外等待确保数据加载完成
                    time.sleep(2)
                except:
                    print("      ⚠ 搜索结果状态未确认")
                    time.sleep(2)
            except Exception as e:
                print(f"      ⚠ 点击搜索按钮失败: {str(e)}")
            
            # === 第四步：在iframe中进入详情页 ===
            print("      - 点击详情按钮...")
            try:
                # 先等待表格完全加载
                time.sleep(2)
                
                detail_selectors = [
                    '.el-table__row:first-child .el-button:has-text("详情")',
                    '.el-table__row:first-child a:has-text("详情")',
                    '.el-table__row:first-child button:has-text("详情")',
                    'button:has-text("详情")',
                    'a:has-text("详情")',
                    '.detail-btn',
                    'span:has-text("详情")'
                ]
                
                clicked = False
                for selector in detail_selectors:
                    try:
                        element = target_frame.locator(selector).first
                        if element.count() > 0:
                            btn_text = element.inner_text() or '无文本'
                            print(f"      ✓ 找到详情按钮 '{selector}' (文本: '{btn_text}')")
                            
                            # 执行点击（使用JavaScript直接触发，避免被其他元素拦截）
                            try:
                                element.evaluate('el => el.click()')
                                print(f"      ✓ 点击详情按钮成功（使用JavaScript）")
                                clicked = True
                            except Exception as click_error:
                                print(f"      ⚠ JavaScript点击失败: {str(click_error)}")
                                # 尝试常规点击作为备选
                                try:
                                    element.click(timeout=5000)
                                    print(f"      ✓ 点击详情按钮成功（常规方式）")
                                    clicked = True
                                except Exception as e2:
                                    print(f"      ⚠ 常规点击也失败: {str(e2)}")
                            # 无论点击成功与否，都退出循环
                            break
                    except Exception as e:
                        continue
                
                if not clicked:
                    print(f"      ⚠ 未成功点击详情按钮")
                    
                    # 调试：查找iframe中表格的所有按钮
                    try:
                        table_buttons = target_frame.locator('.el-table__row button, .el-table__row a').all()
                        print(f"      - iframe表格中共有 {len(table_buttons)} 个可点击元素")
                        for i, btn in enumerate(table_buttons[:10]):
                            btn_text = btn.inner_text() or '无文本'
                            btn_class = btn.get_attribute('class') or ''
                            row_info = btn.evaluate('el => { const row = el.closest(".el-table__row"); return row ? "第" + (Array.from(row.parentElement.children).indexOf(row) + 1) + "行" : "未知行"; }')
                            print(f"        元素{i+1}: '{btn_text[:30]}' (class: {btn_class[:40]}, {row_info})")
                    except Exception as e:
                        print(f"      - 调试失败: {str(e)}")
            except Exception as e:
                print(f"      ⚠ 点击详情按钮失败: {str(e)}")
            
            # 等待详情页加载
            try:
                # 尝试多种详情页标识
                detail_indicators = [
                    '.detail-content',
                    '.el-descriptions',
                    '.form-detail',
                    '.page-detail',
                    '.certificate-detail',
                    'h3:has-text("详情"), h2:has-text("详情")'
                ]
                
                detail_found = False
                for indicator in detail_indicators:
                    try:
                        target_frame.locator(indicator).first.wait_for(timeout=5000)
                        print(f"      ✓ 详情页加载成功 (找到 {indicator})")
                        detail_found = True
                        break
                    except:
                        continue
                
                if not detail_found:
                    # 检查是否有新的iframe出现（详情页可能在新的iframe中）
                    time.sleep(2)
                    new_iframes = web_checker.page.query_selector_all('iframe')
                    if len(new_iframes) > len(iframes):
                        print(f"      ✓ 检测到新iframe，详情页可能在新iframe中")
                    else:
                        print(f"      ⚠ 详情页加载状态未确认，但操作已完成")
            except Exception as e:
                print(f"      ⚠ 详情页等待异常: {str(e)}")
                time.sleep(2)
        else:
            print("      ⚠ 未找到目标iframe，无法执行后续操作")
        
        print("\n✓ 自动化操作执行完成")
        
    except Exception as e:
        print(f"\n❌ 自动化操作失败: {str(e)}")
        raise


def manual_login(web_checker):
    """手动登录流程：输入用户名和密码"""
    
    # 首先确认当前页面URL，确保在正确的授权页面上
    current_url = web_checker.page.url
    print(f"      - 当前页面URL: {current_url}")
    
    # 检查是否在授权/登录页面（而不是首页）
    if '/mng/index' in current_url and 'logon' not in current_url and 'login' not in current_url:
        print(f"      ⚠ 警告：似乎仍在首页，未在授权页面")
        print(f"      - 等待页面加载...")
        time.sleep(3)
        current_url = web_checker.page.url
        print(f"      - 重新检查URL: {current_url}")
    
    print("      - 正在输入用户名...")
    # 尝试多种常见的用户名输入框选择器
    username_selectors = [
        'input[placeholder*="用户名"]',
        'input[placeholder*="账号"]',
        'input[placeholder*="邮箱"]',
        'input[type="text"]',
        '.el-input__inner',
        'input[name="username"]',
        'input[name="account"]'
    ]
    
    username_filled = False
    for selector in username_selectors:
        try:
            web_checker.page.fill(selector, 'fanqiqi@iscas.ac.cn', timeout=5000)
            print(f"      ✓ 使用选择器 '{selector}' 填写用户名成功")
            username_filled = True
            break
        except:
            continue
    
    if not username_filled:
        raise Exception("无法找到用户名输入框，请检查页面结构")
    
    print("      - 正在输入密码...")
    # 尝试多种常见的密码输入框选择器
    password_selectors = [
        'input[type="password"]',
        'input[placeholder*="密码"]',
        '.el-input__inner[type="password"]',
        'input[name="password"]'
    ]
    
    password_filled = False
    for selector in password_selectors:
        try:
            web_checker.page.fill(selector, 'iscas123.', timeout=5000)
            print(f"      ✓ 使用选择器 '{selector}' 填写密码成功")
            password_filled = True
            break
        except:
            continue
    
    if not password_filled:
        raise Exception("无法找到密码输入框，请检查页面结构")
    
    # 等待授权页面完全加载（使用文本内容而非URL）
    print("      - 等待授权页面完全加载...")
    try:
        # 等待"用户登录"按钮出现，确认页面已完全加载
        web_checker.wait_for_selector('button:has-text("用户登录"), button.el-button--primary', timeout=15000)
        print("      ✓ 检测到授权按钮已就绪")
        
        # 额外等待确保页面完全渲染和JavaScript执行完成
        time.sleep(2)
    except:
        print("      ⚠ 等待授权按钮超时，尝试继续...")
        time.sleep(3)
    
    print("      - 点击授权按钮...")
    # 尝试多种常见的登录/授权按钮选择器（按优先级排序）
    login_button_selectors = [
        'button:has-text("用户登录")',            # 最高优先级：实际页面显示的文本
        'button.el-button--primary:has-text("用户登录")',  # Element UI主按钮且文本为"用户登录"
        '.btns button.el-button--primary',        # .btns容器下的主按钮
        'div.btns button',                        # div.btns下的button
        'button[type="button"].el-button--primary',  # type="button"的主按钮
        'button:has-text("授权")',                # 备选：如果文本是"授权"
        'span:has-text("授权")',                  # span中包含"授权"
        'button:has-text("用户登录-授权")',       # 完整文本
        'button:has-text("确认")',
        'button:has-text("同意")',
        '.auth-btn',
        '.authorize-btn',
        'button[type="submit"]',
        '.login-btn',
        '#login-btn',
        'a:has-text("授权")'
    ]
    
    login_clicked = False
    for selector in login_button_selectors:
        try:
            element = web_checker.page.query_selector(selector)
            if element:
                # 验证按钮文本确实包含预期内容
                btn_text = element.inner_text() or ''
                if '用户登录' in btn_text or '授权' in btn_text or '登录' in btn_text:
                    print(f"      ✓ 找到按钮 '{selector}' (文本: '{btn_text}')，点击...")
                    web_checker.page.click(selector, timeout=10000)
                    print(f"      ✓ 点击成功")
                    login_clicked = True
                    break
                else:
                    print(f"      ⚠ 找到元素但文本不匹配: '{btn_text}'，跳过")
        except Exception as e:
            continue
    
    if not login_clicked:
        print(f"      ⚠ 未找到授权按钮，尝试查找所有可点击元素...")
        # 如果没找到，尝试查找页面上所有可能的按钮
        try:
            all_buttons = web_checker.page.query_selector_all('button, a, div[onclick], .btn')
            print(f"      - 找到 {len(all_buttons)} 个可点击元素")
            for i, btn in enumerate(all_buttons):
                btn_text = btn.inner_text() or '无文本'
                btn_class = btn.get_attribute('class') or ''
                print(f"        元素{i+1}: '{btn_text[:50]}' (class: {btn_class[:30]})")
            
            # 优先点击"用户登录"按钮
            for btn in all_buttons:
                btn_text = btn.inner_text() or ''
                if '用户登录' in btn_text:
                    print(f"      ✓ 点击'用户登录'按钮: '{btn_text}'")
                    btn.click(timeout=10000)
                    login_clicked = True
                    break
            
            # 如果还没找到，再尝试"授权"
            if not login_clicked:
                for btn in all_buttons:
                    btn_text = btn.inner_text() or ''
                    if '授权' in btn_text:
                        print(f"      ✓ 点击包含'授权'文本的元素: '{btn_text}'")
                        btn.click(timeout=10000)
                        login_clicked = True
                        break
            
            # 最后尝试"登录"
            if not login_clicked:
                for btn in all_buttons:
                    btn_text = btn.inner_text() or ''
                    if '登录' in btn_text or 'Login' in btn_text or 'Authorize' in btn_text:
                        print(f"      ✓ 点击包含登录文本的元素: '{btn_text}'")
                        btn.click(timeout=10000)
                        login_clicked = True
                        break
        except Exception as e:
            print(f"      ⚠ 查找按钮失败: {str(e)}")
    
    if not login_clicked:
        raise Exception("无法找到授权按钮，请检查页面结构")
    
    # 等待第一个授权页面加载完成（点击"用户登录"后）
    print("      - 等待第一个授权页面加载...")
    try:
        # 等待页面跳转和加载
        time.sleep(3)
        
        # 检查是否还有第二个授权按钮需要点击
        current_url = web_checker.page.url
        print(f"      - 当前URL: {current_url[:100]}...")
        
        # 尝试查找第二个"授权"按钮
        second_auth_selectors = [
            'button:has-text("授权")',
            'button.el-button--primary:has-text("授权")',
            '.btns button.el-button--primary:has-text("授权")',
            'div.btns button:has-text("授权")',
            'button[type="button"]:has-text("授权")',
            'span:has-text("授权")',
            'button:has-text("同意")',
            'button:has-text("确认")',
            'button:has-text("Authorize")',
            'button:has-text("允许")'
        ]
        
        second_auth_clicked = False
        for selector in second_auth_selectors:
            try:
                element = web_checker.page.query_selector(selector)
                if element:
                    btn_text = element.inner_text() or ''
                    if '授权' in btn_text or '同意' in btn_text or '确认' in btn_text or 'Authorize' in btn_text or '允许' in btn_text:
                        print(f"      ✓ 发现第二个授权按钮 '{selector}' (文本: '{btn_text}')")
                        print(f"      - 点击第二个授权按钮...")
                        web_checker.page.click(selector, timeout=10000)
                        print(f"      ✓ 第二个授权按钮点击成功")
                        second_auth_clicked = True
                        break
            except:
                continue
        
        if second_auth_clicked:
            print("      - 等待第二次授权后跳转...")
            # 等待最终跳转到目标页面
            for attempt in range(10):  # 最多等待30秒
                current_url = web_checker.page.url
                print(f"      - 第{attempt+1}次检查，当前域名: {current_url.split('/')[2] if len(current_url.split('/')) > 2 else '未知'}")
                
                # 如果已经跳转到目标域名（compatibility.openharmony.cn），跳出循环
                if 'compatibility.openharmony.cn' in current_url and '/mng/' in current_url:
                    print(f"      ✓ 已跳转到目标页面")
                    break
                
                time.sleep(3)
        else:
            print("      ⚠ 未发现第二个授权按钮，可能只需一次授权")
            # 继续等待跳转到目标页面
            for attempt in range(8):
                current_url = web_checker.page.url
                print(f"      - 第{attempt+1}次检查，当前域名: {current_url.split('/')[2] if len(current_url.split('/')) > 2 else '未知'}")
                
                if 'compatibility.openharmony.cn' in current_url and '/mng/' in current_url:
                    print(f"      ✓ 已跳转到目标页面")
                    break
                
                time.sleep(3)
        
        print(f"      ✓ 当前URL: {web_checker.page.url[:100]}...")
    except Exception as e:
        print(f"      ⚠ 等待授权跳转异常: {str(e)}")
    
    print("      - 等待登录成功标志...")
    try:
        # 等待菜单出现，表示登录成功
        web_checker.wait_for_selector('.el-menu, .sidebar, nav', timeout=20000)
        print("      ✓ 登录成功")
    except:
        print("      ⚠ 未检测到菜单，尝试其他登录成功标志...")
        try:
            # 尝试检测用户信息或退出按钮
            web_checker.wait_for_selector('.user-info, .avatar, .logout-btn, .username', timeout=10000)
            print("      ✓ 检测到用户信息，登录成功")
        except:
            # 最后再等待一下
            time.sleep(3)
            current_url = web_checker.page.url
            print(f"      ⚠ 登录状态未确认，当前URL: {current_url}")
            print("      - 继续执行后续操作...")


def automate_browser_with_search(web_checker, measurement_id):
    """
    执行自动化登录、导航、搜索和进入详情页的完整流程
    :param web_checker: WebChecker实例
    :param measurement_id: 测评编号
    :return: True 如果成功，False 如果失败
    """
    
    try:
        # === 第一步：导航到目标网站 ===
        print("\n      === 执行登录和导航 ===")
        
        # 首先导航到目标网站
        target_url = "https://compatibility.openharmony.cn/mng/index"
        print(f"      - 正在导航到: {target_url}")
        web_checker.navigate_to_url(target_url)
        print("      ✓ 页面加载完成")
        
        # 等待页面稳定
        time.sleep(3)
        
        # 检查是否已登录
        print("      - 检查登录状态...")
        is_logged_in = False
        try:
            web_checker.wait_for_selector('.el-menu, .sidebar, nav', timeout=3000)
            is_logged_in = True
            print("      ✓ 检测到已登录状态")
        except:
            print("      - 未检测到登录状态，准备登录...")
        
        if not is_logged_in:
            # 点击"立即登录"按钮
            print("      - 检查是否有'立即登录'按钮...")
            immediate_login_selectors = [
                '.btn',
                'div.btn',
                'div:has-text("立即登录")',
                'button:has-text("立即登录")'
            ]
            
            clicked_immediate_login = False
            for selector in immediate_login_selectors:
                try:
                    element = web_checker.page.query_selector(selector)
                    if element:
                        print(f"      ✓ 发现'{selector}'按钮，点击立即登录...")
                        web_checker.page.click(selector, timeout=5000)
                        print("      ✓ 已点击立即登录")
                        clicked_immediate_login = True
                        break
                except:
                    continue
            
            # 如果点击了立即登录，等待登录表单页面加载
            if clicked_immediate_login:
                print("      - 等待登录表单页面加载...")
                time.sleep(3)  # 等待页面跳转和渲染
            
            # 输入用户名和密码
            print("      - 正在输入用户名...")
            username_selectors = [
                'input[placeholder*="账号"]',
                'input[placeholder*="用户名"]',
                'input[type="text"]:not([type="hidden"])',
                'input[name="username"]',
                'input[id="username"]'
            ]
            
            username_filled = False
            for selector in username_selectors:
                try:
                    web_checker.page.fill(selector, 'fanqiqi@iscas.ac.cn', timeout=5000)
                    print(f"      ✓ 使用选择器 '{selector}' 填写用户名成功")
                    username_filled = True
                    break
                except:
                    continue
            
            if not username_filled:
                raise Exception("无法找到用户名输入框")
            
            print("      - 正在输入密码...")
            password_selectors = [
                'input[type="password"]',
                'input[name="password"]',
                'input[id="password"]'
            ]
            
            password_filled = False
            for selector in password_selectors:
                try:
                    web_checker.page.fill(selector, 'iscas123.', timeout=5000)
                    print(f"      ✓ 使用选择器 '{selector}' 填写密码成功")
                    password_filled = True
                    break
                except:
                    continue
            
            if not password_filled:
                raise Exception("无法找到密码输入框")
            
            # 点击"用户登录"或"登录"按钮
            print("      - 正在点击登录按钮...")
            login_button_selectors = [
                'button:has-text("用户登录")',
                'button:has-text("登录")',
                'div:has-text("用户登录")',
                'div:has-text("登录")',
                'button[type="submit"]',
                '.login-btn',
                '#loginBtn'
            ]
            
            login_clicked = False
            for selector in login_button_selectors:
                try:
                    element = web_checker.page.query_selector(selector)
                    if element:
                        print(f"      ✓ 发现登录按钮 '{selector}'，点击...")
                        web_checker.page.click(selector, timeout=5000)
                        print("      ✓ 已点击登录按钮")
                        login_clicked = True
                        break
                except:
                    continue
            
            if not login_clicked:
                print("      ⚠ 未找到明确的登录按钮，尝试按Enter键提交")
                web_checker.page.press('body', 'Enter')
            
            # 等待跳转到授权页面
            print("      - 等待跳转到授权页面...")
            try:
                web_checker.wait_for_selector(
                    'input[type="text"], input[type="password"], input[placeholder*="账号"], input[placeholder*="用户名"]', 
                    timeout=15000
                )
                print("      ✓ 检测到授权页面元素")
            except:
                print("      ⚠ 等待授权页面超时")
            
            time.sleep(2)
            print("      ✓ 授权页面加载完成")
            
            # 处理授权确认（如果需要）
            print("      - 检查是否需要授权确认...")
            auth_button_selectors = [
                'button:has-text("授权")',
                'button:has-text("同意")',
                'button:has-text("确认")',
                'div:has-text("授权")',
                '.auth-btn',
                '#authBtn'
            ]
            
            for selector in auth_button_selectors:
                try:
                    element = web_checker.page.query_selector(selector)
                    if element:
                        text = element.inner_text()
                        if '授权' in text or '同意' in text or '确认' in text:
                            print(f"      ✓ 发现授权按钮 '{selector}'，点击...")
                            web_checker.page.click(selector, timeout=5000)
                            print("      ✓ 已点击授权按钮")
                            
                            # 等待授权完成，通过检测页面内容变化而非URL
                            print("      - 等待授权完成（检测页面加载）...")
                            try:
                                # 等待首页特征元素出现（如导航菜单、主内容区域等）
                                web_checker.wait_for_selector(
                                    '.nav, .sidebar, .main-content, #content-main', 
                                    timeout=20000
                                )
                                print("      ✓ 检测到首页元素，授权完成")
                            except:
                                print("      ⚠ 等待首页元素超时，但仍继续")
                            
                            # 额外等待确保iframe完全加载
                            time.sleep(5)
                            break
                except:
                    continue
        
        # === 第二步：导航到审核管理页面 ===
        print("\n      === 导航到审核管理页面 ===")
        
        # 尝试展开侧边栏（如果折叠了）
        print("      - 尝试展开侧边栏...")
        try:
            # 查找并点击展开按钮
            expand_buttons = web_checker.page.query_selector_all('.sidebar-toggle, .navbar-minimalize, [data-toggle="offcanvas"]')
            for btn in expand_buttons:
                if btn.is_visible():
                    print("      ✓ 找到展开按钮，点击...")
                    web_checker.page.evaluate('(el) => el.click()', btn)
                    time.sleep(1)
                    break
        except:
            pass
        
        # 尝试多种方式导航到审核管理页面
        menu_clicked = False
        
        # 方法1：使用 JavaScript 强制点击包含"审核管理"的元素
        try:
            print("      - 尝试使用JavaScript点击'审核管理'...")
            elements = web_checker.page.query_selector_all('a, div, span, li')
            for element in elements:
                try:
                    text = element.inner_text()
                    if '审核管理' in text:
                        print(f"      ✓ 找到菜单项: '{text[:30]}...'")
                        # 使用 JavaScript 强制触发点击事件
                        web_checker.page.evaluate('''
                            (el) => {
                                // 尝试多种点击方式
                                if (el.click) el.click();
                                // 如果是链接，直接设置href
                                if (el.href) window.location.href = el.href;
                            }
                        ''', element)
                        print("      ✓ 已点击审核管理菜单")
                        menu_clicked = True
                        break
                except:
                    continue
        except Exception as e:
            print(f"      ⚠ JavaScript点击失败: {str(e)}")
        
        if not menu_clicked:
            print("      ✗ 无法找到或点击审核管理菜单")
            return False
        
        # 等待子菜单展开（增加等待时间）
        print("      - 等待子菜单展开...")
        time.sleep(3)
        
        # 点击"兼容性测评审核"子菜单
        print("      - 尝试点击'兼容性测评审核'子菜单...")
        submenu_clicked = False
        
        # 多次尝试查找子菜单
        for attempt in range(3):
            try:
                print(f"      - 第{attempt + 1}次尝试查找子菜单...")
                
                # 直接查找<a>标签，避免匹配到<li>父元素
                submenu_links = web_checker.page.query_selector_all('a.J_menuItem, a[href*="certificate"], a[href*="audit"]')
                
                for link in submenu_links:
                    try:
                        text = link.inner_text().strip()
                        if '兼容性测评审核' in text:
                            print(f"      ✓ 找到子菜单链接: '{text}'")
                            
                            # 获取href属性
                            href = link.get_attribute('href')
                            print(f"      - href: {href}")
                            
                            # 直接点击<a>标签
                            web_checker.page.evaluate('(el) => el.click()', link)
                            print("      ✓ 已点击兼容性测评审核子菜单")
                            submenu_clicked = True
                            break
                    except Exception as e:
                        print(f"      ⚠ 处理链接时出错: {str(e)}")
                        continue
                
                if submenu_clicked:
                    break
                    
                # 如果没找到，等待一下再试
                if not submenu_clicked and attempt < 2:
                    print(f"      ⚠ 未找到子菜单，等待后重试...")
                    time.sleep(2)
            except Exception as e:
                print(f"      ⚠ 第{attempt + 1}次尝试失败: {str(e)}")
                if attempt < 2:
                    time.sleep(2)
        
        if not submenu_clicked:
            print("      ⚠ 未找到兼容性测评审核子菜单")
        
        # 等待页面加载和稳定（增加等待时间）
        print("      - 等待审核管理页面加载...")
        time.sleep(15)  # 大幅增加等待时间，确保iframe完全加载
        
        # === 重新检测iframe（因为点击子菜单后旧frame会被销毁）===
        print("      - 重新检测iframe...")
        target_frame = web_checker.page  # 重置为默认值
        
        try:
            frames = web_checker.page.frames
            print(f"      找到 {len(frames)} 个frame")
            
            # 查找所有非主页面的frame
            best_frame = None
            max_content_len = 0
            
            for i, frame in enumerate(frames):
                if frame != web_checker.page.main_frame:
                    print(f"      Frame[{i}]: {frame.url}")
                    
                    # 尝试获取内容
                    try:
                        frame_text = frame.inner_text('body')
                        content_len = len(frame_text)
                        print(f"      Frame[{i}] 内容长度: {content_len} 字符")
                        
                        # 记录内容最多的frame
                        if content_len > max_content_len:
                            max_content_len = content_len
                            best_frame = frame
                        
                        # 如果包含测评相关关键词且内容足够多，优先选择
                        if ('测评' in frame_text or '审核' in frame_text) and content_len > 500:
                            best_frame = frame
                            print(f"      ✓ 找到包含审核/测评内容的frame（{content_len} 字符）")
                            break
                    except Exception as e:
                        print(f"      Frame[{i}] 获取内容失败: {str(e)}")
            
            # 使用找到的最佳frame
            if best_frame:
                target_frame = best_frame
                print(f"      ✓ 使用目标frame: {target_frame.url}（{max_content_len} 字符）")
                
                # 如果内容仍然较少，再次等待并重试
                if max_content_len < 500:
                    print(f"      ⚠ 内容较少，再次等待并刷新...")
                    time.sleep(10)
                    
                    # 重新获取frames
                    frames = web_checker.page.frames
                    for i, frame in enumerate(frames):
                        if frame != web_checker.page.main_frame:
                            try:
                                frame_text = frame.inner_text('body')
                                if len(frame_text) > max_content_len:
                                    target_frame = frame
                                    max_content_len = len(frame_text)
                                    print(f"      ✓ 更新frame，内容增加到 {max_content_len} 字符")
                            except:
                                pass
            elif len(frames) > 1:
                target_frame = frames[-1]
                print(f"      ⚠ 使用最后一个frame")
        except Exception as e:
            print(f"      ⚠ iframe检测失败: {str(e)}")
        
        # 验证是否成功跳转
        try:
            page_text = target_frame.inner_text('body') if hasattr(target_frame, 'inner_text') else ""
            if len(page_text) < 100:
                print(f"      ⚠ 页面内容过少 ({len(page_text)} 字符)，但仍继续尝试...")
            else:
                print(f"      ✓ 页面加载完成，内容长度: {len(page_text)} 字符")
        except:
            print(f"      ⚠ 无法获取页面内容")
        
        # === 第三步：搜索/筛选测评编号 ===
        print(f"\n      === 搜索测评编号: {measurement_id} ===")
        
        # 查找"测评编号"列标题中的排序图标并点击
        search_clicked = False
        
        try:
            print("      - 查找'测评编号'列标题...")
            
            # 方法1：查找包含"测评编号"文本的元素
            headers = target_frame.query_selector_all('div, th, span')
            for header in headers:
                try:
                    text = header.inner_text().strip()
                    if '测评编号' in text:
                        print(f"      ✓ 找到'测评编号'列标题")
                        
                        # 查找该元素内的排序图标 <i class="icon icon-sort">
                        sort_icon = header.query_selector('i.icon-sort, .icon-sort, button.my-table-sort-icon')
                        if sort_icon:
                            print("      ✓ 找到排序图标，点击...")
                            target_frame.evaluate('(el) => el.click()', sort_icon)
                            print("      ✓ 已点击排序图标")
                            search_clicked = True
                            
                            # 等待遮罩层出现（表示正在加载）
                            print("      - 等待加载遮罩层出现...")
                            try:
                                # 等待 layui-layer-shade 元素出现
                                target_frame.wait_for_selector('.layui-layer-shade', timeout=10000)
                                print("      ✓ 检测到加载遮罩层")
                                
                                # 等待遮罩层消失（加载完成）
                                print("      - 等待加载完成（遮罩层消失）...")
                                target_frame.wait_for_selector('.layui-layer-shade', state='hidden', timeout=15000)
                                print("      ✓ 加载完成，遮罩层已消失")
                            except Exception as e:
                                print(f"      ⚠ 等待遮罩层超时或失败: {str(e)}")
                                # 即使超时也继续执行，使用固定等待作为备选
                                time.sleep(3)
                            
                            break
                        else:
                            print("      ⚠ 未找到排序图标，尝试直接点击列标题...")
                            target_frame.evaluate('(el) => el.click()', header)
                            print("      ✓ 已点击列标题")
                            search_clicked = True
                            time.sleep(3)
                            break
                except:
                    continue
            
            # 方法2：如果方法1失败，尝试使用CSS选择器直接定位
            if not search_clicked:
                try:
                    print("      - 尝试使用CSS选择器定位排序图标...")
                    sort_buttons = target_frame.query_selector_all('.my-table-sort-icon, .sort-btn, i.icon-sort')
                    if sort_buttons:
                        print(f"      ✓ 找到 {len(sort_buttons)} 个排序按钮，点击第一个...")
                        target_frame.evaluate('(el) => el.click()', sort_buttons[0])
                        print("      ✓ 已点击排序按钮")
                        search_clicked = True
                        time.sleep(3)
                except Exception as e:
                    print(f"      ⚠ CSS选择器定位失败: {str(e)}")
            
        except Exception as e:
            print(f"      ⚠ 搜索操作失败: {str(e)}")
        
        if not search_clicked:
            print("      ⚠ 未能触发搜索/排序操作，但仍继续尝试查找数据")
        
        # === 第四步：进入详情页 ===
        print(f"\n      === 进入测评编号 {measurement_id} 的详情页 ===")
        
        # 等待搜索结果
        print("      - 等待搜索结果...")
        time.sleep(3)
        
        # 查找包含测评编号的链接或行
        detail_clicked = False
        
        try:
            # 获取所有表格行
            rows = target_frame.query_selector_all('tr')
            for row in rows:
                try:
                    text = row.inner_text()
                    if measurement_id in text:
                        print(f"      ✓ 找到包含 {measurement_id} 的行，点击进入详情...")
                        # 查找行中的第一个可点击元素（通常是链接或按钮）
                        clickable = row.query_selector('a, button, [role="button"]')
                        if clickable:
                            target_frame.evaluate('(el) => el.click()', clickable)
                        else:
                            # 如果没有可点击元素，直接点击行
                            target_frame.evaluate('(el) => el.click()', row)
                        print("      ✓ 已点击进入详情页")
                        detail_clicked = True
                        break
                except:
                    continue
        except Exception as e:
            print(f"      ⚠ 查找详情链接失败: {str(e)}")
        
        if not detail_clicked:
            print(f"      ⚠ 未找到包含 {measurement_id} 的可点击元素")
            return False
        
        # 等待详情页加载
        print("      - 等待详情页加载...")
        time.sleep(5)
        
        # 重新检测iframe（详情页可能在新iframe中打开）
        print("      - 检查是否有新的iframe（详情页）...")
        try:
            frames = web_checker.page.frames
            print(f"      找到 {len(frames)} 个frame")
            
            # 查找最新的非主frame（可能是详情页）
            # 注意：这里我们遍历所有frame，寻找内容最丰富且包含ID的那个
            best_frame = None
            max_content_len = 0
            
            for i, frame in enumerate(frames):
                if frame != web_checker.page.main_frame and frame.url:
                    print(f"      Frame[{i}]: {frame.url}")
                    
                    # 尝试获取内容
                    try:
                        frame_text = frame.inner_text('body')
                        content_len = len(frame_text)
                        print(f"      Frame[{i}] 内容长度: {content_len} 字符")
                        
                        # 如果内容足够多且包含测评编号，优先使用这个frame
                        if content_len > 500 and measurement_id in frame_text:
                            best_frame = frame
                            max_content_len = content_len
                            print(f"      ✓ 发现候选详情页iframe，内容长度: {content_len} 字符")
                            # 不立即break，继续查找是否有更合适的，或者直接使用第一个匹配的
                            # 这里为了稳健性，如果找到匹配ID且内容多的，直接选中并break
                            target_frame = frame
                            print(f"      ✓ 选定该Frame为详情页Frame")
                            break
                    except Exception as e:
                        print(f"      Frame[{i}] 读取内容失败: {str(e)}")
                        continue
            
            # 如果没找到包含ID的frame，但之前有切换过frame，保持原样或尝试最后一个
            if 'target_frame' not in locals() or target_frame == web_checker.page:
                 # 如果上面循环没break导致target_frame未更新，或者初始就是page
                 # 尝试使用刚才找到的best_frame，或者最后一个frame
                 if best_frame:
                     target_frame = best_frame
                 elif len(frames) > 1:
                     target_frame = frames[-1]
                     print(f"      ⚠ 未找到明确匹配的详情页iframe，使用最后一个frame")
                 
        except Exception as e:
            print(f"      ⚠ iframe检测失败: {str(e)}")
        
        # 滚动页面触发懒加载
        try:
            print("      - 滚动页面以触发懒加载...")
            target_frame.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)
        except Exception as e:
            print(f"      ⚠ 滚动失败: {str(e)}")
        
        # 检测详情页特征（wrapper元素）
        wrapper_found = False
        wrapper_selectors = [
            '.detail-wrapper',
            '.page-detail',
            '.detail-container',
            '#detailContent',
            '.el-card'
        ]
        
        for selector in wrapper_selectors:
            try:
                target_frame.wait_for_selector(selector, timeout=5000)
                print(f"      ✓ 检测到详情页wrapper元素: {selector}")
                wrapper_found = True
                break
            except:
                continue
        
        if wrapper_found:
            print(f"      ✓ 详情页加载成功（检测到wrapper元素）")
            time.sleep(2)
        else:
            print(f"      ⚠ 未找到wrapper元素，但仍继续提取数据")
                
        print("\n      ✓ 已完成搜索并进入详情页")
        
        # 将target_frame保存到web_checker对象，以便main.py使用
        web_checker.detail_frame = target_frame
        
        return True  # 成功
        
    except Exception as e:
        print(f"\n      ✗ 自动化操作失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False  # 失败