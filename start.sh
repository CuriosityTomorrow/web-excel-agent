#!/bin/bash

# Web Excel Agent 启动脚本

echo "🚀 启动 Web Excel Agent..."

# 检查是否安装了依赖
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 安装前端依赖..."
    cd frontend && npm install && cd ..
fi

if [ ! -d "backend/venv" ]; then
    echo "🐍 创建Python虚拟环境..."
    cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && cd ..
fi

# 启动后端
echo "🔧 启动后端服务..."
cd backend
if [ -d "venv" ]; then
    source venv/bin/activate
fi
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

# 等待后端启动
sleep 3

# 启动前端
echo "🎨 启动前端服务..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ 服务已启动！"
echo "   前端: http://localhost:3000"
echo "   后端: http://localhost:8000"
echo "   API文档: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待用户中断
trap "echo ''; echo '🛑 停止服务...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT TERM

wait
