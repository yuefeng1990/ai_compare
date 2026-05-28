"""
测试不同测评编号的完整流程
演示每次都会启动浏览器获取最新数据
"""
import subprocess
import sys

def test_multiple_measurement_ids():
    """测试多个不同的测评编号"""
    
    # 测试用的测评编号列表
    test_ids = [
        "OHC443600006741",
        # 可以添加更多测评编号进行测试
        # "OHC443600006742",
        # "OHC443600006743",
    ]
    
    print("=" * 80)
    print("测试多个测评编号的完整流程")
    print("=" * 80)
    print("\n注意：每次测试都会启动浏览器获取最新的页面内容\n")
    
    for i, measurement_id in enumerate(test_ids, 1):
        print(f"\n{'='*80}")
        print(f"开始第 {i} 个测试: 测评编号 {measurement_id}")
        print(f"{'='*80}\n")
        
        try:
            # 运行主程序
            result = subprocess.run(
                [sys.executable, "main.py", measurement_id],
                cwd="d:\\AI_TEST\\ai_compare\\ai_checker",
                capture_output=False,
                text=True
            )
            
            if result.returncode == 0:
                print(f"\n✓ 第 {i} 个测试完成")
            else:
                print(f"\n✗ 第 {i} 个测试失败，返回码: {result.returncode}")
                
        except Exception as e:
            print(f"\n✗ 第 {i} 个测试异常: {str(e)}")
        
        print(f"\n{'='*80}")
        print(f"第 {i} 个测试结束")
        print(f"{'='*80}\n")
        
        # 如果还有更多测试，询问是否继续
        if i < len(test_ids):
            input("按 Enter 键继续下一个测试...")
    
    print("\n" + "=" * 80)
    print("所有测试完成！")
    print("=" * 80)

if __name__ == "__main__":
    test_multiple_measurement_ids()
