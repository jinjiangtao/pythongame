"""
贪吃蛇游戏 - 启动器脚本
跨平台版本，支持 Windows/Linux/Mac
"""

import sys
import os

def main():
    print("=" * 60)
    print("        经典贪吃蛇游戏 - 启动器")
    print("=" * 60)
    print()

    # 检查 Python 版本
    version = sys.version_info
    print(f"Python 版本: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("⚠  建议使用 Python 3.8 或更高版本")
    print()

    # 检查 pygame
    try:
        import pygame
        print(f"✓ pygame 已安装 (版本: {pygame.version.ver})")
        print(f"  SDL 版本: {pygame.version.SDL}")
    except ImportError:
        print("✗ pygame 未安装")
        print()
        print("请先安装 pygame:")
        print("  pip install pygame-ce")
        print()
        input("按 Enter 键退出...")
        sys.exit(1)

    print()

    # 检查游戏文件
    game_file = "snake_game.py"
    if not os.path.exists(game_file):
        print(f"✗ 找不到游戏文件: {game_file}")
        print()
        input("按 Enter 键退出...")
        sys.exit(1)

    print(f"✓ 找到游戏文件: {game_file}")
    print()

    # 启动游戏
    print("=" * 60)
    print("正在启动游戏...")
    print()
    print("控制说明:")
    print("  方向键/WASD - 控制蛇的移动")
    print("  空格键 - 暂停/继续")
    print("  R - 重新开始（游戏结束后）")
    print("  Q/ESC - 退出游戏")
    print("=" * 60)
    print()

    try:
        # 导入并运行游戏
        from snake_game import Game
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\n游戏被用户中断")
    except Exception as e:
        print()
        print("=" * 60)
        print("✗ 游戏运行出错！")
        print("=" * 60)
        print()
        print(f"错误信息: {e}")
        print()
        import traceback
        print("详细错误信息:")
        traceback.print_exc()
        print()
        input("按 Enter 键退出...")

if __name__ == "__main__":
    main()
