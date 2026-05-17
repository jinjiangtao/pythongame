# 扫雷游戏 - 使用说明

## 游戏简介
使用 Python + Pygame 开发的功能完善的经典扫雷游戏，单文件实现。

## 运行前准备

### 1. 安装依赖
游戏需要 pygame-ce（pygame 社区版，推荐用于 Python 3.14+）：

```bash
pip install pygame-ce
```

或者使用国内镜像（下载更快）：
```bash
pip install pygame-ce -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2. 运行游戏
**方式一：使用启动脚本（推荐）**
- 双击运行 `启动游戏.bat`

**方式二：命令行运行**
```bash
# 进入游戏目录
cd d:\trae\pythongame\minesweeper

# 运行游戏
py -3 minesweeper.py

# 或直接使用 Python（如果已配置环境变量）
python minesweeper.py
```

## 游戏配置
启动游戏后会提示输入：
- 棋盘宽度（默认 9，范围 5-30）
- 棋盘高度（默认 9，范围 5-30）
- 地雷数量（默认 10）

## 游戏操作
- **左键点击**：翻开格子
- **右键点击**：标记/取消标记地雷
- **R 键**：重新开始游戏
- **Q 键**：退出游戏

## 游戏特性
✅ 自定义棋盘大小和地雷数量  
✅ 左键翻开，右键标记  
✅ 空白区域自动连片展开  
✅ 首次点击不会踩雷  
✅ 实时计时和剩余地雷数量显示  
✅ 胜利/失败弹窗提示  
✅ 经典简约方格样式  
✅ 数字颜色区分清晰（1蓝色、2绿色、3红色等）  
✅ 支持重新开始和退出  

## 游戏截图说明
- 顶部显示：剩余地雷数量、已用时间、游戏状态
- 棋盘：经典灰色方格，未翻开的格子有立体感
- 数字：1蓝色、2绿色、3红色、4深蓝色等
- 红旗标记：红色背景+F标记
- 地雷：黑色星号

## 常见问题

**Q: 提示 "Python was not found"？**  
A: 使用 `py -3 minesweeper.py` 或先安装 Python 并配置环境变量

**Q: pygame 安装失败？**  
A: 建议安装 pygame-ce：`pip install pygame-ce`，这是 pygame 的社区维护版本，对 Python 3.14+ 支持更好

**Q: 游戏窗口无法显示？**  
A: 确保使用的是图形化环境的 Windows 系统，pygame 需要显示设备

## 技术实现
- **语言**：Python 3.14+
- **图形库**：Pygame-ce 2.5.7
- **架构**：单文件面向对象设计
- **主要类**：
  - `CellState`：格子状态枚举
  - `GameStatus`：游戏状态枚举
  - `MinesweeperGame`：游戏主类

## 文件结构
```
minesweeper/
├── minesweeper.py       # 游戏主程序
├── 启动游戏.bat         # Windows 启动脚本
├── test_game.py         # Pygame 测试脚本
├── test_minesweeper.py  # 游戏功能测试脚本
└── README.md           # 本说明文件
```

## 享受游戏！
🎮 点击格子，避开地雷，看你能多快通关！
