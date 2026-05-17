"""
贪吃蛇游戏 - 诊断工具
运行此脚本以诊断和解决运行问题
"""

import sys
import os

def print_section(title):
    """打印分节标题"""
    print()
    print("=" * 70)
    print(f"  {title}")
    print("=" * 70)

def check_python():
    """检查 Python 版本"""
    print_section("1. Python 环境检查")
    version = sys.version_info
    print(f"Python 版本: {version.major}.{version.minor}.{version.micro}")
    print(f"可执行文件: {sys.executable}")

    if version.major < 3:
        print("✗ Python 3 是必需的")
        return False
    elif version.major == 3 and version.minor < 8:
        print("⚠  建议使用 Python 3.8 或更高版本")
    else:
        print("✓ Python 版本符合要求")
    return True

def check_pygame():
    """检查 pygame 安装"""
    print_section("2. Pygame 检查")
    try:
        import pygame
        print(f"✓ pygame 已安装")
        print(f"  版本: {pygame.version.ver}")
        print(f"  SDL 版本: {pygame.version.SDL}")
        print(f"  SDL 完整版本: {pygame.version.SDL}")

        # 测试 pygame 初始化
        print()
        print("正在测试 pygame 初始化...")
        pygame.init()
        print("✓ pygame.init() 成功")

        # 测试显示模式
        print("正在测试显示模式...")
        try:
            screen = pygame.display.set_mode((800, 600))
            print("✓ pygame.display.set_mode() 成功")

            # 获取显示信息
            info = pygame.display.Info()
            print(f"✓ 显示信息:")
            print(f"  分辨率: {info.current_w}x{info.current_h}")
            print(f"  窗口标题可设置: pygame.display.set_caption()")

            pygame.quit()
            print("✓ pygame 已正确关闭")
            return True
        except Exception as e:
            print(f"✗ 显示模式创建失败: {e}")
            pygame.quit()
            return False

    except ImportError:
        print("✗ pygame 未安装")
        print()
        print("解决方案:")
        print("  1. 推荐安装 pygame-ce (社区版，兼容性更好):")
        print("     pip install pygame-ce")
        print()
        print("  2. 或者尝试安装标准版 pygame:")
        print("     pip install pygame")
        return False
    except Exception as e:
        print(f"✗ pygame 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_game_files():
    """检查游戏文件"""
    print_section("3. 游戏文件检查")

    files_to_check = [
        ("snake_game.py", "游戏主程序"),
        ("test_game.py", "测试脚本"),
        ("launcher.py", "启动器"),
    ]

    all_exist = True
    for filename, description in files_to_check:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"✓ {filename} - {description} ({size} 字节)")
        else:
            print(f"✗ {filename} - {description} (未找到)")
            all_exist = False

    # 检查最高分文件
    if os.path.exists("snake_high_score.json"):
        print(f"✓ snake_high_score.json - 最高分记录文件 (已存在)")

    return all_exist

def test_game_import():
    """测试游戏模块导入"""
    print_section("4. 游戏模块导入测试")

    try:
        # 添加当前目录到路径
        if '.' not in sys.path:
            sys.path.insert(0, '.')

        from snake_game import Game, Snake, Food
        print("✓ 所有游戏类导入成功")
        print("  - Game 类: 可用")
        print("  - Snake 类: 可用")
        print("  - Food 类: 可用")
        return True
    except ImportError as e:
        print(f"✗ 游戏模块导入失败: {e}")
        print()
        print("可能的原因:")
        print("  1. 游戏文件不存在或损坏")
        print("  2. pygame 未正确安装")
        print("  3. Python 路径配置问题")
        return False
    except Exception as e:
        print(f"✗ 意外错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_display_environment():
    """检查显示环境"""
    print_section("5. 显示环境检查")

    # 检查操作系统
    print(f"操作系统: {sys.platform}")

    # 检查 DISPLAY 环境变量（仅 Linux/Mac）
    if sys.platform not in ['win32', 'cygwin']:
        display = os.environ.get('DISPLAY', None)
        if display:
            print(f"✓ DISPLAY 环境变量: {display}")
        else:
            print("✗ DISPLAY 环境变量未设置")
            print("  (在 Linux/Mac 上需要设置 DISPLAY 才能使用 pygame)")

    # Windows 检查
    if sys.platform == 'win32':
        print("✓ Windows 系统 - pygame 应该可以正常工作")
        print("  (无需额外的 DISPLAY 配置)")

    return True

def provide_solutions(results):
    """根据测试结果提供解决方案"""
    print_section("诊断总结与解决方案")

    if all(results.values()):
        print()
        print("🎉 所有检查通过！")
        print()
        print("游戏应该可以正常运行。请尝试以下方法启动游戏:")
        print()
        print("方法 1: 使用启动器")
        print("  python launcher.py")
        print()
        print("方法 2: 直接运行游戏")
        print("  python snake_game.py")
        print()
        print("方法 3: 使用批处理文件")
        print("  双击: 启动游戏.bat")
        print()
        print("如果游戏仍然无法运行:")
        print("  1. 检查是否安装了图形驱动")
        print("  2. 确认在有图形界面的环境中运行")
        print("  3. 尝试重启计算机")
    else:
        print()
        print("⚠ 发现问题，请根据上述测试结果解决:")
        print()

        if not results.get('python'):
            print("→ Python 版本问题")
            print("  解决: 升级到 Python 3.8 或更高版本")
            print()

        if not results.get('pygame'):
            print("→ Pygame 未安装或安装失败")
            print("  解决:")
            print("    pip install pygame-ce")
            print()

        if not results.get('game_files'):
            print("→ 游戏文件缺失")
            print("  解决: 重新创建或下载游戏文件")
            print()

        if not results.get('game_import'):
            print("→ 游戏模块导入失败")
            print("  解决:")
            print("    1. 确保 pygame 已安装")
            print("    2. 检查游戏文件是否完整")
            print()

    print()
    print("=" * 70)

def main():
    """主诊断流程"""
    print()
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "贪吃蛇游戏 - 诊断工具" + " " * 24 + "║")
    print("╚" + "═" * 68 + "╝")
    print()

    results = {
        'python': check_python(),
        'pygame': check_pygame(),
        'game_files': check_game_files(),
        'game_import': test_game_import(),
    }

    check_display_environment()

    provide_solutions(results)

    print()
    input("按 Enter 键退出...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n诊断被用户中断")
        sys.exit(0)
    except Exception as e:
        print()
        print("=" * 70)
        print("诊断过程出现错误:")
        print("=" * 70)
        print(e)
        import traceback
        traceback.print_exc()
        print()
        input("按 Enter 键退出...")
        sys.exit(1)
