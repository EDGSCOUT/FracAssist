#!/bin/bash

# 股骨颈骨折辅助诊断系统 - 一键启动脚本

echo "============================================================"
echo "  股骨颈骨折辅助诊断系统 - Web版本"
echo "============================================================"
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3"
    echo "请先安装Python 3.7或更高版本"
    exit 1
fi

echo "✅ Python3 已安装"

# 检查依赖是否安装
echo ""
echo "📦 检查依赖包..."
python3 -c "import flask, numpy, cv2, PIL" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📥 正在安装依赖包..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败"
        exit 1
    fi
    echo "✅ 依赖包安装成功"
else
    echo "✅ 依赖包已安装"
fi

echo ""
echo "🚀 启动Web服务器..."
echo ""

# 启动Web服务器（后台运行）
nohup python3 app.py > app.log 2>&1 &

# 获取进程ID
SERVER_PID=$!
echo "✅ 服务器进程ID: $SERVER_PID"

# 等待服务器启动
echo "⏳ 等待服务器启动..."
for i in {1..10}; do
    sleep 1
    if curl -s http://localhost:8080 > /dev/null 2>&1; then
        echo "✅ 服务器启动成功"
        echo ""
        break
    fi
    echo "   尝试连接 ($i/10)..."
done

# 再次检查服务器状态
if ! curl -s http://localhost:8080 > /dev/null 2>&1; then
    echo "❌ 服务器启动失败"
    echo "📋 请查看日志：tail -f app.log"
    kill $SERVER_PID 2>/dev/null
    exit 1
fi

# 自动打开浏览器
echo "🌐 正在打开浏览器..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open http://localhost:8080
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open http://localhost:8080 2>/dev/null || sensible-browser http://localhost:8080 2>/dev/null
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    start http://localhost:8080
else
    echo "请手动在浏览器中打开: http://localhost:8080"
fi

echo ""
echo "============================================================"
echo "  🎉 系统已启动！"
echo "============================================================"
echo ""
echo "📍 访问地址: http://localhost:8080"
echo ""
echo "📋 使用步骤:"
echo "   1. 上传医学影像"
echo "   2. 标注骨折近端点（红色）和远端点（蓝色）"
echo "   3. 点击【计算分析】获取结果"
echo ""
echo "⏹️  停止服务器: 按 Ctrl+C 或运行"
echo "   pkill -f 'python3 app.py'"
echo ""
echo "============================================================"

# 等待用户输入（保持脚本运行）
read -p "按回车键停止服务器..."