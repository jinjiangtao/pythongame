"""
游戏测试脚本
用于验证 pygame 和游戏依赖是否正确安装
"""

import sys

def test_pygame():
    """测试 pygame 是否正确安装"""
    try:
        import pygame
        print(f"✓ pygame 安装成功")
        print(f"  版本: {pygame.version.ver}")
        print(f"  SDL 版本: {pygame.version.SDL}")
        return True
    except ImportError as e:
        print(f"✗ pygame 导入失败: {e}")
        print("\n请运行以下命令安装 pygame:")
        print("  pip install pygame-ce")
        return False

def test_pygame_init():
    """测试 pygame 初始化"""
    try:
        import pygame
        pygame.init()
        print(f"✓ pygame 初始化成功")

        # 测试显示模式
        screen = pygame.display.set_mode((800, 600))
        print(f"✓ 显示模式创建成功 (800x600)")

        # 获取显示信息
        info = pygame.display.Info()
        print(f"✓ 显示信息: {info.current_w}x{info.current_h}")

        pygame.quit()
        print(f"✓ pygame 清理成功")
        return True
    except Exception as e:
        print(f"✗ pygame 初始化失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_game_import():
    """测试游戏模块导入"""
    try:
        from snake_game import Game, Snake, Food
        print(f"✓ 游戏类导入成功")
        print(f"  - Game 类: 可用")
        print(f"  - Snake 类: 可用")
        print(f"  - Food 类: 可用")
        return True
    except ImportError as e:
        print(f"✗ 游戏模块导入失败: {e}")
        return False
    except Exception as e:
        print(f"✗ 游戏模块测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("贪吃蛇游戏 - 依赖测试")
    print("=" * 60)
    print()

    tests = [
        ("Pygame 安装检查", test_pygame),
        ("Pygame 初始化测试", test_pygame_init),
        ("游戏模块导入测试", test_game_import),
    ]

    results = []
    for name, test_func in tests:
        print(f"\n测试: {name}")
        print("-" * 40)
        result = test_func()
        results.append((name, result))
        print()

    print("=" * 60)
    print("测试结果汇总")
    print("=" * 60)

    all_passed = True
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{status}: {name}")
        if not result:
            all_passed = False

    print()
    if all_passed:
        print("🎉 所有测试通过！游戏应该可以正常运行。")
        print()
        print("运行游戏:")
        print("  python snake_game.py")
    else:
        print("⚠ 部分测试失败，请解决上述问题后再试。")

    print()
    print("=" * 60)

    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
