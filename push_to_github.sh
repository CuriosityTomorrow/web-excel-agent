#!/bin/bash

echo "======================================"
echo "   Web Excel Agent - GitHub 推送工具"
echo "======================================"
echo ""
echo "👤 用户: Sylsylgo310!"
echo "📧 邮箱: 490233318@qq.com"
echo ""

# 检查GitHub CLI登录状态
echo "📋 步骤1: 检查GitHub登录状态..."
if gh auth status &>/dev/null; then
    echo "✅ 已登录GitHub"
    GITHUB_USER=$(gh api user --jq '.login')
    echo "   用户名: $GITHUB_USER"
    echo ""
else
    echo "❌ 未登录GitHub CLI"
    echo ""
    echo "请先执行以下命令登录："
    echo ""
    echo "  gh auth login"
    echo ""
    echo "登录步骤："
    echo "  1. 选择 GitHub.com (按回车)"
    echo "  2. 选择 HTTPS (按回车)"
    echo "  3. 选择 Login with a web browser (按回车)"
    echo "  4. 浏览器打开后，点击 Authorize 授权"
    echo "  5. 回到终端按回车完成"
    echo ""
    echo "登录完成后，再次运行此脚本"
    exit 1
fi

echo "📋 步骤2: 创建GitHub仓库..."
echo ""
echo "仓库名称: web-excel-agent"
echo "可见性: 私有（Private）"
echo ""

# 创建仓库
echo "正在创建仓库..."
gh repo create web-excel-agent --private --source=. --remote=origin --push

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "        ✅ 推送成功！"
    echo "======================================"
    echo ""
    echo "📍 仓库地址: https://github.com/$GITHUB_USER/web-excel-agent"
    echo ""
    echo "🏢 在公司使用："
    echo ""
    echo "  1. 克隆仓库："
    echo "     git clone https://github.com/$GITHUB_USER/web-excel-agent.git"
    echo ""
    echo "  2. 安装依赖："
    echo "     cd web-excel-agent/backend"
    echo "     python3 -m venv venv"
    echo "     source venv/bin/activate"
    echo "     pip install -r requirements.txt"
    echo ""
    echo "     cd ../frontend"
    echo "     npm install"
    echo ""
    echo "  3. 启动服务："
    echo "     # 终端1 - 后端"
    echo "     cd backend && uvicorn app.main:app --reload"
    echo ""
    echo "     # 终端2 - 前端"
    echo "     cd frontend && npm run dev"
    echo ""
    echo "  4. 访问: http://localhost:3000"
    echo ""
    echo "📚 查看完整文档: cat PUSH_TO_GITHUB.md"
    echo ""
else
    echo ""
    echo "❌ 推送失败，请检查错误信息"
    echo ""
    exit 1
fi

