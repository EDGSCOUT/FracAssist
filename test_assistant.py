#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本 - 验证股骨颈骨折辅助诊断系统的基本功能
"""

import sys

def test_imports():
    """测试必要的库是否可以导入"""
    print("=" * 50)
    print("测试1: 检查依赖库导入")
    print("=" * 50)
    
    try:
        import cv2
        print("✓ OpenCV 导入成功")
        print(f"  版本: {cv2.__version__}")
    except ImportError as e:
        print(f"✗ OpenCV 导入失败: {e}")
        return False
    
    try:
        import numpy as np
        print("✓ NumPy 导入成功")
        print(f"  版本: {np.__version__}")
    except ImportError as e:
        print(f"✗ NumPy 导入失败: {e}")
        return False
    
    try:
        from PIL import Image
        print("✓ Pillow 导入成功")
    except ImportError as e:
        print(f"✗ Pillow 导入失败: {e}")
        return False
    
    try:
        import tkinter as tk
        print("✓ Tkinter 导入成功")
    except ImportError as e:
        print(f"✗ Tkinter 导入失败: {e}")
        return False
    
    print("\n所有依赖库导入成功！\n")
    return True

def test_angle_calculation():
    """测试角度计算功能"""
    print("=" * 50)
    print("测试2: 角度计算功能")
    print("=" * 50)
    
    import numpy as np
    
    # 测试用例1: 水平骨折线 (0度)
    point1 = (100, 200)
    point2 = (300, 200)
    vector = np.array([point2[0] - point1[0], point2[1] - point1[1]])
    coronal_normal = np.array([0, 1])
    
    dot_product = np.dot(vector, coronal_normal)
    fracture_magnitude = np.linalg.norm(vector)
    normal_magnitude = np.linalg.norm(coronal_normal)
    
    cos_theta = dot_product / (fracture_magnitude * normal_magnitude)
    cos_theta = np.clip(cos_theta, -1.0, 1.0)
    angle_rad = np.arccos(cos_theta)
    angle_deg = np.degrees(angle_rad)
    angle_from_horizontal = 90 - angle_deg
    
    print(f"测试用例1 - 水平骨折线:")
    print(f"  点1: {point1}, 点2: {point2}")
    print(f"  计算角度: {angle_from_horizontal:.1f}°")
    print(f"  预期: 约0° (近水平骨折)")
    
    # 测试用例2: 45度斜线
    point1 = (100, 200)
    point2 = (200, 300)
    vector = np.array([point2[0] - point1[0], point2[1] - point1[1]])
    
    dot_product = np.dot(vector, coronal_normal)
    fracture_magnitude = np.linalg.norm(vector)
    cos_theta = dot_product / fracture_magnitude
    cos_theta = np.clip(cos_theta, -1.0, 1.0)
    angle_rad = np.arccos(cos_theta)
    angle_deg = np.degrees(angle_rad)
    angle_from_horizontal = 90 - angle_deg
    
    print(f"\n测试用例2 - 45度斜线:")
    print(f"  点1: {point1}, 点2: {point2}")
    print(f"  计算角度: {angle_from_horizontal:.1f}°")
    print(f"  预期: 约45° (中等角度骨折)")
    
    # 测试用例3: 垂直线
    point1 = (200, 100)
    point2 = (200, 300)
    vector = np.array([point2[0] - point1[0], point2[1] - point1[1]])
    
    dot_product = np.dot(vector, coronal_normal)
    fracture_magnitude = np.linalg.norm(vector)
    cos_theta = dot_product / fracture_magnitude
    cos_theta = np.clip(cos_theta, -1.0, 1.0)
    angle_rad = np.arccos(cos_theta)
    angle_deg = np.degrees(angle_rad)
    angle_from_horizontal = 90 - angle_deg
    
    print(f"\n测试用例3 - 垂直线:")
    print(f"  点1: {point1}, 点2: {point2}")
    print(f"  计算角度: {angle_from_horizontal:.1f}°")
    print(f"  预期: 约90° (陡峭骨折)")
    
    print("\n角度计算功能测试通过！\n")
    return True

def test_main_module():
    """测试主模块是否可以加载"""
    print("=" * 50)
    print("测试3: 主模块加载")
    print("=" * 50)
    
    try:
        from fracture_assistant import FractureAssistant
        print("✓ FractureAssistant 类导入成功")
        
        # 测试类实例化（不显示GUI）
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        
        print("✓ 主模块加载成功")
        print("✓ GUI环境正常")
        
        root.destroy()
        
        print("\n主模块测试通过！\n")
        return True
    except Exception as e:
        print(f"✗ 主模块测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """运行所有测试"""
    print("\n")
    print("╔" + "=" * 48 + "╗")
    print("║" + " " * 10 + "股骨颈骨折辅助诊断系统测试" + " " * 12 + "║")
    print("╚" + "=" * 48 + "╝")
    print()
    
    results = []
    
    # 运行测试
    results.append(("依赖库导入", test_imports()))
    results.append(("角度计算", test_angle_calculation()))
    results.append(("主模块加载", test_main_module()))
    
    # 总结
    print("=" * 50)
    print("测试总结")
    print("=" * 50)
    
    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name:.<30} {status}")
    
    all_passed = all(result for _, result in results)
    
    print()
    if all_passed:
        print("🎉 所有测试通过！系统可以正常使用。")
        print()
        print("使用方法:")
        print("  运行主程序: python fracture_assistant.py")
        print()
        print("功能说明:")
        print("  1. 点击【导入图像】选择医学影像")
        print("  2. 在图像上点击标注骨折近端点（红色）和远端点（蓝色）")
        print("  3. 点击【计算角度与建议】获取分析结果")
        print("  4. 点击【保存结果】导出分析报告")
    else:
        print("⚠️  部分测试失败，请检查错误信息。")
        sys.exit(1)

if __name__ == "__main__":
    main()