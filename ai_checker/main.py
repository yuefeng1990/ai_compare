import sys
import os

# 设置标准输出编码为UTF-8，解决Windows命令行中文乱码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import pandas as pd
from openpyxl import load_workbook
from tools.excel_reader import ExcelReader
from tools.txt_reader import TxtReader
from tools.web_checker import WebChecker
from tools.compare import CompareTool
from auto_login import automate_browser, automate_browser_with_search

def main(measurement_id=None):
    """
    主函数
    :param measurement_id: 测评编号，如果提供则自动搜索该编号的详情信息
    """
    # 文件路径设置
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_excel_path = os.path.join(current_dir, 'data', 'checklist.xlsx')
    keywords_txt_path = os.path.join(current_dir, 'data', 'keywords.txt')
    log_txt_path = os.path.join(current_dir, 'data', 'log .txt')
    output_excel_path = os.path.join(current_dir, 'output', 'result.xlsx')
    
    # 网站URL定义
    WEB_URL = "https://compatibility.openharmony.cn/mng/index"
    
    # 要提取的关键字列表（根据用户需求）
    TARGET_KEYWORDS = [
        'MarketName',      # 设备名称（传播名）
        'ProductModel',    # 设备型号
        'DeviceType',      # 设备类型
        'Brand',           # 品牌英文名
        'Manufacture',     # 企业简称（英文）
        'DisplayVersion',  # 软件版本号
        'SecurityPatchTag',# 安全补丁标签
        'VersionId',       # 版本ID
        'BuildRootHash',   # 版本Hash
        'OsFullName'       # 操作系统版本号
    ]
    
    web_checker = None
    try:
        # 1. 读取关键字模板
        print("1. 读取关键字模板...")
        txt_reader = TxtReader(keywords_txt_path)
        all_keywords = txt_reader.get_keywords()
        print(f"找到 {len(all_keywords)} 个关键字")
        
        # 2. 读取Excel检查清单（参考用）
        print("\n2. 读取Excel检查清单...")
        excel_reader = ExcelReader(input_excel_path)
        checklist_data = excel_reader.read_excel()
        
        if checklist_data is None or checklist_data.empty:
            print("未找到检查清单数据！")
            return
        
        print(f"检查清单包含 {len(checklist_data)} 行数据")
        
        # 3. 读取log.txt内容
        print("\n3. 读取log.txt内容...")
        log_content = ""
        if os.path.exists(log_txt_path):
            with open(log_txt_path, 'r', encoding='utf-8') as f:
                log_content = f.read()
            print(f"log.txt文件大小: {len(log_content)} 字符")
        else:
            print(f"警告: {log_txt_path} 不存在")
            return
        
        # 4. 初始化对比工具（传入目标测评编号用于精确定位表格行）
        print("\n4. 初始化对比工具...")
        compare_tool = CompareTool(target_measurement_id=measurement_id)
        
        # 5. 如果提供了测评编号，启动浏览器自动化
        web_content = ""
        if measurement_id:
            print(f"\n5. 启动浏览器自动化，搜索测评编号: {measurement_id}")
            print("=" * 80)
            
            # 每次都启动浏览器获取最新页面内容（不使用缓存）
            print("⚠ 将启动浏览器获取最新页面内容...")
            
            # 初始化WebChecker
            from tools.web_checker import WebChecker
            import time
            web_checker = WebChecker(headless=False)
            
            try:
                # 启动浏览器
                print("      - 正在启动浏览器...")
                web_checker.launch_browser()
                print("      ✓ 浏览器已启动")
                
                # 使用带搜索功能的自动化脚本
                success = automate_browser_with_search(web_checker, measurement_id)
                
                if not success:
                    print("\n✗ 浏览器自动化流程失败")
                    web_content = ""
                else:
                    # 获取页面内容
                    print("\n      - 获取页面内容...")
                    
                    # 优先使用detail_frame（详情页的iframe），如果不存在则使用page
                    target_frame = None
                    if hasattr(web_checker, 'detail_frame') and web_checker.detail_frame:
                        target_frame = web_checker.detail_frame
                        print("      ✓ 使用详情页iframe获取内容")
                    elif web_checker and web_checker.page:
                        target_frame = web_checker.page
                        print("      ⚠ 使用主页面获取内容")
                    
                    if target_frame:
                        try:
                            # 滚动页面触发懒加载
                            target_frame.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                            time.sleep(2)
                            
                            # 获取页面HTML内容（用于成对div结构提取）
                            page_html = target_frame.content()
                            
                            # 同时获取纯文本作为备选
                            page_content = target_frame.inner_text('body')
                            
                            # 优先使用HTML内容，如果为空则使用纯文本
                            if page_html and len(page_html) > 100:
                                web_content = page_html
                                print(f"\n✓ 成功获取页面HTML内容: {len(web_content)} 字符")
                            elif page_content:
                                web_content = page_content
                                print(f"\n✓ 成功获取页面文本内容: {len(web_content)} 字符")
                            else:
                                print("\n✗ 未能获取到页面内容")
                                web_content = ""
                            
                            # 保存页面内容用于调试
                            if web_content:
                                debug_file = os.path.join(current_dir, 'page_content_debug.txt')
                                with open(debug_file, 'w', encoding='utf-8') as f:
                                    f.write(web_content)
                                print(f"✓ 页面内容已保存到: {debug_file}")
                        except Exception as e:
                            print(f"\n✗ 获取页面内容失败: {str(e)}")
                    else:
                        print("\n✗ 浏览器对象无效，无法获取页面内容")
                        
            except Exception as e:
                print(f"\n✗ 浏览器自动化异常: {str(e)}")
                print("⚠ 将跳过网页提取，继续处理其他数据源")
                web_content = ""
            finally:
                # 关闭浏览器
                try:
                    web_checker.close()
                    print("✓ 浏览器已关闭")
                except:
                    pass
        else:
            print("\n5. 跳过浏览器自动化（未提供测评编号）")
        
        # 6. 从log.txt提取关键字值
        print("\n6. 从log.txt提取关键字...")
        print("=" * 80)
        
        log_values = {}
        for keyword in TARGET_KEYWORDS:
            value = compare_tool.extract_value_from_log(log_content, keyword)
            log_values[keyword] = value
            status = "✓" if value else "✗"
            print(f"  {status} {keyword:20s}: {value or '(未找到)'}")
        
        # 7. 从网页提取关键字值（如果有网页内容）
        web_values = {}
        if web_content:
            print("\n7. 从网页提取关键字...")
            print("=" * 80)
            
            for keyword in TARGET_KEYWORDS:
                value = compare_tool.extract_value_from_web(web_content, keyword)
                web_values[keyword] = value
                status = "✓" if value else "✗"
                print(f"  {status} {keyword:20s}: {value or '(未找到)'}")
        else:
            print("\n7. 跳过网页提取（无网页内容）")
        
        # 8. 比较log.txt和网页的值
        print("\n8. 比较结果...")
        print("=" * 80)
        
        comparison_results = []
        matched_count = 0
        total_count = len(TARGET_KEYWORDS)
        
        for keyword in TARGET_KEYWORDS:
            log_value = log_values.get(keyword)
            web_value = web_values.get(keyword)
            
            is_match = compare_tool.compare_values(log_value, web_value, keyword=keyword)
            
            if is_match:
                matched_count += 1
            
            status = "✓" if is_match else "✗"
            match_text = "一致" if is_match else "不一致"
            
            print(f"\n  {status} {keyword:20s}")
            print(f"      log.txt: {log_value or '(未找到)'}")
            print(f"      网页:    {web_value or '(未找到)'}")
            print(f"      结果:    {match_text}")
            
            comparison_results.append({
                '关键字': keyword,
                'log값': log_value or '',
                'web값': web_value or '',
                '是否一致': '是' if is_match else '否'
            })
        
        # 9. 生成结果Excel
        print("\n" + "=" * 80)
        print("9. 生成结果Excel...")
        
        # 创建输出目录
        os.makedirs(os.path.dirname(output_excel_path), exist_ok=True)
        
        # 创建DataFrame并保存
        df_result = pd.DataFrame(comparison_results)
        df_result.to_excel(output_excel_path, index=False)
        
        print(f"✓ 结果已保存到: {output_excel_path}")
        
        # 统计一致性
        print(f"\n统计信息:")
        print(f"  总比较次数: {total_count}")
        print(f"  一致次数: {matched_count}")
        print(f"  不一致次数: {total_count - matched_count}")
        if total_count > 0:
            print(f"  一致率: {matched_count/total_count*100:.2f}%")
        else:
            print(f"  一致率: N/A")
        
        print("\n" + "=" * 80)
        print("✅ 处理完成！")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # 关闭浏览器（如果还在运行）
        if web_checker:
            try:
                web_checker.close()
                print("\n浏览器已关闭")
            except:
                pass

if __name__ == "__main__":
    # 从命令行参数获取测评编号
    measurement_id = sys.argv[1] if len(sys.argv) > 1 else None
    
    if measurement_id:
        print(f"📋 测评编号: {measurement_id}")
    else:
        print("⚠️  未提供测评编号，将跳过浏览器自动化")
    
    main(measurement_id)
