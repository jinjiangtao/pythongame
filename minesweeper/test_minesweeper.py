import pygame
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()
pygame.display.set_mode((1, 1))

from minesweeper import MinesweeperGame, GameStatus

try:
    print("正在测试扫雷游戏初始化...")
    game = MinesweeperGame(9, 9, 10)
    print(f"✓ 游戏初始化成功")
    print(f"  - 棋盘大小: 9×9")
    print(f"  - 地雷数量: 10")
    print(f"  - 窗口尺寸: {game.screen_width}×{game.screen_height}")
    
    print("\n正在测试游戏逻辑...")
    
    assert game.game_status == GameStatus.READY, "游戏初始状态应该是 READY"
    print(f"✓ 游戏初始状态正确: READY")
    
    print("\n正在测试格子翻开功能...")
    game.reveal_cell(5, 5)
    assert game.mines_placed == True, "第一次点击后地雷应该已经放置"
    print(f"✓ 地雷放置逻辑正常")
    assert game.game_status in [GameStatus.PLAYING, GameStatus.WON, GameStatus.LOST], "游戏状态应该已更新"
    print(f"✓ 游戏状态更新正常")
    
    print("\n正在测试标记功能...")
    initial_flags = game.flag_count
    game.toggle_flag(0, 0)
    assert game.flag_count == initial_flags + 1, "标记后旗子数量应该增加"
    print(f"✓ 标记功能正常")
    
    game.toggle_flag(0, 0)
    assert game.flag_count == initial_flags, "取消标记后旗子数量应该恢复"
    print(f"✓ 取消标记功能正常")
    
    print("\n正在测试重置功能...")
    game.reset_game()
    assert game.game_status == GameStatus.READY, "重置后游戏状态应该是 READY"
    assert game.mines_placed == False, "重置后地雷应该未放置"
    print(f"✓ 重置功能正常")
    
    print("\n" + "=" * 50)
    print("🎮 所有测试通过！扫雷游戏运行正常！")
    print("=" * 50)
    print("\n运行游戏命令:")
    print("  py -3 minesweeper.py")
    print("\n或使用:")
    print("  python minesweeper.py  (需要配置Python环境变量)")
    
except Exception as e:
    print(f"\n✗ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    pygame.quit()
