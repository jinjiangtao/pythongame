# ========== test_all.py ==========
"""
综合测试脚本
用于测试所有模块的功能
"""
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

from utils import format_file_size, is_supported_image, get_file_extension
from file_selector import FileSelector
from compressor import Compressor
from task_manager import TaskManager


def test_utils():
    """测试工具函数"""
    print("\n1. 测试 utils 模块")
    print("-" * 40)

    # 测试 format_file_size
    assert format_file_size(1024) == "1.00 KB"
    assert format_file_size(1048576) == "1.00 MB"
    assert format_file_size(500) == "500.00 B"
    print("   ✓ format_file_size 测试通过")

    # 测试 is_supported_image
    assert is_supported_image("test.jpg") == True
    assert is_supported_image("test.png") == True
    assert is_supported_image("test.txt") == False
    print("   ✓ is_supported_image 测试通过")

    # 测试 get_file_extension
    assert get_file_extension("path/to/file.JPEG") == ".jpeg"
    assert get_file_extension("path/to/file.PNG") == ".png"
    print("   ✓ get_file_extension 测试通过")

    print("   utils 模块所有测试通过！")


def test_compressor():
    """测试压缩器"""
    print("\n2. 测试 compressor 模块")
    print("-" * 40)

    compressor = Compressor()

    # 创建一个测试图片
    from PIL import Image
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        tmp_path = tmp.name

    # 创建测试图片
    img = Image.new('RGB', (100, 100), color='red')
    img.save(tmp_path, 'PNG')

    # 创建输出目录
    output_dir = tempfile.mkdtemp()
    output_path = os.path.join(output_dir, 'test.png')

    # 测试压缩
    success, error, size = compressor.compress_image(tmp_path, output_dir, quality=80)
    assert success == True, f"压缩失败: {error}"
    assert os.path.exists(output_path), "输出文件不存在"
    print(f"   ✓ 压缩成功，输出大小: {format_file_size(size)}")

    # 清理
    os.unlink(tmp_path)
    os.unlink(output_path)
    os.rmdir(output_dir)

    print("   compressor 模块测试通过！")


def test_file_selector():
    """测试文件选择器"""
    print("\n3. 测试 file_selector 模块")
    print("-" * 40)

    selector = FileSelector()

    # 测试初始状态
    assert selector.get_file_count() == 0
    assert selector.get_total_size() == 0
    print("   ✓ 初始状态正确")

    print("   注意: 文件选择需要图形界面，跳过交互测试")
    print("   file_selector 模块基本测试通过！")


def test_task_manager():
    """测试任务管理器"""
    print("\n4. 测试 task_manager 模块")
    print("-" * 40)

    manager = TaskManager()

    assert hasattr(manager, 'file_selector')
    assert hasattr(manager, 'compressor')
    assert hasattr(manager, 'is_running')
    print("   ✓ 任务管理器初始化正确")

    print("   task_manager 模块测试通过！")


def main():
    """主测试函数"""
    print("=" * 60)
    print("图片批量压缩工具 - 模块测试")
    print("=" * 60)

    try:
        test_utils()
        test_compressor()
        test_file_selector()
        test_task_manager()

        print("\n" + "=" * 60)
        print("🎉 所有测试通过！")
        print("=" * 60)
        print("\n下一步:")
        print("1. 安装依赖: pip install -r requirements.txt")
        print("2. 运行程序: python main.py")
        print("3. 选择图片 -> 选择输出文件夹 -> 点击开始压缩")

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
    input("\n按 Enter 键退出...")
