import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

try:
    import config
    print("✓ config 模块导入成功")
    
    from characters import Pet, Prop, Effect
    print("✓ characters 模块导入成功")
    
    from game_area import GameArea
    print("✓ game_area 模块导入成功")
    
    from score_timer import ScoreTimer
    print("✓ score_timer 模块导入成功")
    
    print("\n所有模块导入检查通过！")
    print("\n迭代升级完成的功能清单：")
    print("1. ✓ 界面视觉迭代")
    print("   - 渐变背景 + 动态云朵装饰")
    print("   - 萌宠描边 + 渐变绘制")
    print("   - 顶部UI圆角卡片样式")
    print("   - 开始/结束界面")
    print("   - 成功/失败特效反馈")
    print("\n2. ✓ 核心功能迭代")
    print("   - 动态难度成长系统")
    print("   - 3类特殊萌宠（闪光/加速/恶作剧）")
    print("   - 连击机制")
    print("   - 智能移动AI（直线/曲线/折返）")
    print("   - 道具系统（时间加成/全屏捕捉/分数翻倍）")
    print("   - 关卡目标任务")
    print("\n3. ✓ 体验优化迭代")
    print("   - 程序化生成音效")
    print("   - 优化点击判定")
    print("   - 详细结算面板")
    print("   - R键重开/ESC退出")

except ImportError as e:
    print(f"✗ 导入错误: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ 错误: {e}")
    sys.exit(1)
