@echo off
chcp 65001 >nul
title 股骨颈骨折辅助诊断系统

echo ============================================================
echo   股骨颈骨折辅助诊断系统 - Web版本
echo ============================================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python
    echo 请先安装Python 3.7或更高版本
    pause
    exit /b 1
)

echo ✅ Python 已安装
echo.

REM 检查依赖是否安装
echo 📦 检查依赖包...
python -c "import flask, numpy, cv2, PIL" >nul 2>&1
if errorlevel 1 (
    echo 📥 正在安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
    echo ✅ 依赖包安装成功
) else (
    echo ✅ 依赖包已安装
)

echo.
echo 🚀 启动Web服务器...
echo.

REM 启动Web服务器
start /B python app.py

REM 等待服务器启动
echo ⏳ 等待服务器启动...
timeout /t 3 /nobreak >nul

echo.
echo 🌐 正在打开浏览器...
start http://localhost:8080

echo.
echo ============================================================
echo   🎉 系统已启动！
echo ============================================================
echo.
echo 📍 访问地址: http://localhost:8080
echo.
echo 📋 使用步骤:
echo    1. 上传医学影像
echo    2. 标注骨折近端点（红色）和远端点（蓝色）
echo    3. 点击【计算分析】获取结果
echo.
echo ⏹️  停止服务器: 关闭此窗口或运行
echo    taskkill /f /im python.exe
echo.
echo ============================================================
echo.

pause

REM 停止服务器
taskkill /f /im python.exe >nul 2>&1