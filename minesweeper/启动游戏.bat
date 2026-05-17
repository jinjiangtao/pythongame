@echo off
title 扫雷游戏
echo ========================================
echo         扫雷游戏启动器
echo ========================================
echo.
echo 正在启动游戏，请稍候...
echo.

py -3 minesweeper.py

if %errorlevel% neq 0 (
    echo.
    echo 游戏启动失败！
    echo 请确保已安装 pygame：
    echo   pip install pygame-ce
    echo.
    pause
)
