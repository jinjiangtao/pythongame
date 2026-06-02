# ========== test_file_select.py ==========
"""
测试文件选择功能的脚本
用于验证文件选择逻辑是否正常工作
"""
import os
import sys

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(__file__))

from file_selector import FileSelector


def test_file_selector():
    """测试文件选择器"""
    print("=" * 50)
    print("测试文件选择器")
    print("=" * 50)

    selector = FileSelector()

    # 测试选择图片（这会打开文件对话框）
    print("\n1. 测试选择图片功能")
    print("   请在弹出的对话框中选择一些图片文件")
    files = selector.select_images()

    if files:
        print(f"\n   成功选择了 {len(files)} 个文件：")
        for i, (path, size) in enumerate(files[:5], 1):  # 只显示前5个
            print(f"   {i}. {path} ({size} bytes)")
        if len(files) > 5:
            print(f"   ... 还有 {len(files) - 5} 个文件")
    else:
        print("\n   未选择任何文件（这是正常的，如果您取消了对话框）")

    # 测试选择输出文件夹
    print("\n2. 测试选择输出文件夹")
    print("   请在弹出的对话框中选择一个文件夹")
    output_dir = selector.select_output_dir()

    if output_dir:
        print(f"\n   选择的输出文件夹: {output_dir}")
    else:
        print("\n   未选择输出文件夹（这是正常的，如果您取消了对话框）")

    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)


if __name__ == "__main__":
    try:
        test_file_selector()
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        input("\n按 Enter 键退出...")
