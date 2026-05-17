@echo off
chcp 65001 >nul
echo ================================================
echo         经典贪吃蛇游戏 - 启动器
echo ================================================
echo.
echo 正在启动游戏，请稍候...
echo.

:: 使用完整路径运行 Python 和游戏
C:\Users\84012\AppData\Local\Programs\Python\Python314\python.exe snake_game.py

:: 如果游戏退出，显示提示
echo.
echo 游戏已退出。
pause
