@echo off
chcp 65001 >nul
title 银行管理系统GUI启动器

echo ================================================
echo 银行管理系统 GUI 启动器
echo ================================================
echo.

echo 正在启动银行管理系统GUI界面...
echo.

python start_gui.py

if %errorlevel% neq 0 (
    echo.
    echo 启动失败！请检查以下事项：
    echo 1. Python是否已正确安装
    echo 2. 是否已安装所需依赖包 (pip install -r requirements.txt)
    echo 3. MySQL服务是否已启动
    echo 4. 数据库连接配置是否正确
    echo.
    pause
) else (
    echo.
    echo 程序已正常退出
)

pause
