# 项目启动指南 - 完整版

> **目标**: 让团队成员快速在本地启动 Web Excel 项目进行调试

**适用环境**: macOS / Linux / Windows (WSL)
**最后更新**: 2026-02-05

---

## 目录

- [前置要求](#前置要求)
- [快速启动（推荐）](#快速启动推荐)
- [详细启动步骤](#详细启动步骤)
- [使用 uv 管理虚拟环境](#使用-uv-管理虚拟环境)
- [前端启动详解](#前端启动详解)
- [后端启动详解](#后端启动详解)
- [验证项目运行](#验证项目运行)
- [常见问题排查](#常见问题排查)
- [开发工具配置](#开发工具配置)

---

## 前置要求

### 必须安装的工具

| 工具 | 版本要求 | 检查命令 | 安装指南 |
|------|---------|---------|---------|
| **Node.js** | 18+ | `node --version` | [官网下载](https://nodejs.org/) |
| **npm** | 9+ | `npm --version` | 随 Node.js 一起安装 |
| **Python** | 3.11+ | `python3 --version` | [官网下载](https://www.python.org/) |
| **uv** | 最新版 | `uv --version` | 见下方 |
| **Git** | 任意版本 | `git --version` | [官网下载](https://git-scm.com/) |

### 检查环境

```bash
# 创建检查脚本
cat > check_env.sh << 'EOF'
#!/bin/bash
echo "========== 环境检查 =========="

echo -n "Node.js: "
if command -v node &> /dev/null; then
    node --version
else
    echo "❌ 未安装"
fi

echo -n "npm: "
if command -v npm &> /dev/null; then
    npm --version
else
    echo "❌ 未安装"
fi

echo -n "Python 3: "
if command -v python3 &> /dev/null; then
    python3 --version
else
    echo "❌ 未安装"
fi

echo -n "uv: "
if command -v uv &> /dev/null; then
    uv --version
else
    echo "❌ 未安装"
fi

echo -n "Git: "
if command -v git &> /dev/null; then
    git --version
else
    echo "❌ 未安装"
fi

echo "============================"
EOF

chmod +x check_env.sh
./check_env.sh
```

---

## 快速启动（推荐）

### 一键启动脚本

```bash
# 1. 克隆项目（如果还没有）
git clone https://github.com/CuriosityTomorrow/web-excel-agent.git
cd web-excel-agent

# 2. 使用一键启动脚本
chmod +x start.sh
./start.sh
```

### 预期结果

启动脚本会自动：
1. 检查环境
2. 创建后端虚拟环境（使用 uv）
3. 安装后端依赖
4. 安装前端依赖
5. 启动后端服务（端口 8000）
6. 启动前端服务（端口 3000）

看到以下输出表示成功：
```
✅ 后端服务已启动: http://localhost:8000
✅ 前端服务已启动: http://localhost:3000
🚀 项目启动成功！请在浏览器打开 http://localhost:3000
```

---

## 详细启动步骤

如果一键启动失败，请按以下步骤手动启动：

### 步骤 1: 获取项目代码

```bash
# 方式1: 克隆 GitHub 仓库（推荐）
git clone https://github.com/CuriosityTomorrow/web-excel-agent.git
cd web-excel-agent

# 方式2: 如果已经有代码压缩包
unzip web-excel-agent.zip
cd web-excel-agent

# 查看项目结构
ls -la
```

### 步骤 2: 安装 uv（Python 包管理器）

#### 什么是 uv？
- **uv**: 极速的 Python 包管理器，比 pip 快 10-100 倍
- 由 Astral 开发（开发 ruff 的公司）
- 自动管理虚拟环境

#### 安装 uv

**macOS / Linux**:
```bash
# 使用官方安装脚本
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或使用 pip
pip install uv

# 验证安装
uv --version
```

**Windows**:
```powershell
# 使用 PowerShell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 或使用 pip
pip install uv

# 验证安装
uv --version
```

#### 配置 uv（可选）

```bash
# 设置镜像源（中国用户推荐）
export UV_INDEX_URL="https://pypi.tuna.tsinghua.edu.cn/simple"

# 添加到 shell 配置文件
echo 'export UV_INDEX_URL="https://pypi.tuna.tsinghua.edu.cn/simple"' >> ~/.zshrc
source ~/.zshrc
```

---

## 使用 uv 管理虚拟环境

### 创建虚拟环境

```bash
# 进入后端目录
cd backend

# 使用 uv 创建虚拟环境
# uv 会自动创建 .venv 目录
uv venv

# 或者指定 Python 版本
uv venv --python 3.11
```

### 激活虚拟环境

**macOS / Linux**:
```bash
source .venv/bin/activate
```

**Windows**:
```powershell
.venv\Scripts\activate
```

### 安装依赖

```bash
# 方式1: 使用 uv sync（推荐）
# uv 会读取 pyproject.toml 自动安装依赖
uv sync

# 方式2: 使用 requirements.txt
uv pip install -r requirements.txt

# 验证安装
uv pip list
```

### uv 常用命令

```bash
# 查看已安装的包
uv pip list

# 添加新依赖
uv add openpyxl

# 移除依赖
uv remove openpyxl

# 更新依赖
uv lock --upgrade

# 运行 Python 脚本
uv run python script.py

# 停用虚拟环境
deactivate
```

---

## 前端启动详解

### 步骤 1: 进入前端目录

```bash
cd frontend
```

### 步骤 2: 安装依赖

```bash
# 使用 npm 安装依赖
npm install

# 或者使用 yarn（如果安装了）
# yarn install

# 或者使用 pnpm（推荐，更快）
# pnpm install
```

### 步骤 3: 配置环境变量（可选）

```bash
# 创建 .env 文件
cat > .env << 'EOF'
VITE_API_URL=http://localhost:8000/api
VITE_APP_TITLE=Web Excel Agent
EOF
```

### 步骤 4: 启动开发服务器

```bash
# 启动 Vite 开发服务器
npm run dev

# 或者
yarn dev

# 或者
pnpm dev
```

### 预期输出

```
VITE v6.4.1  ready in 500 ms

➜  Local:   http://localhost:3000/
➜  Network: use --host to expose
➜  press h + enter to show help
```

### 访问前端

打开浏览器访问：http://localhost:3000

---

## 后端启动详解

### 步骤 1: 进入后端目录

```bash
cd backend
```

### 步骤 2: 创建虚拟环境（如果还没有）

```bash
# 使用 uv 创建
uv venv

# 激活虚拟环境
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate  # Windows
```

### 步骤 3: 安装依赖

```bash
# 使用 uv
uv sync

# 或使用 requirements.txt
uv pip install -r requirements.txt
```

### 步骤 4: 验证依赖安装

```bash
# 查看已安装的包
uv pip list

# 应该看到以下关键包：
# - fastapi (0.115.6)
# - uvicorn (0.34.0)
# - openpyxl (3.1.5)
# - beautifulsoup4 (4.12.3)
# - requests (2.32.3)
# - pydantic (2.10.4)
```

### 步骤 5: 启动后端服务

```bash
# 使用 uvicorn 启动
uvicorn app.main:app --reload --port 8000

# 或者使用 uv run
uv run uvicorn app.main:app --reload --port 8000
```

### 预期输出

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 访问后端 API 文档

打开浏览器访问：
- API 文档（Swagger UI）: http://localhost:8000/docs
- API 文档（ReDoc）: http://localhost:8000/redoc
- 健康检查: http://localhost:8000/health

---

## 验证项目运行

### 1. 检查后端健康状态

```bash
# 新开一个终端
curl http://localhost:8000/health

# 预期输出
# {"status":"healthy"}
```

### 2. 检查前端页面

```bash
# 浏览器访问
open http://localhost:3000  # macOS
# 或手动在浏览器输入 http://localhost:3000
```

### 3. 测试完整流程

在浏览器的 AI 对话框中输入：

```
demo
```

**预期结果**:
- AI 回复生成数据成功
- 下方出现表格（6个月销售数据）
- 可以点击单元格编辑
- 可以点击"+行"或"+列"添加行列

继续输入：

```
创建柱状图
```

**预期结果**:
- 右侧出现图表预览
- 可以看到柱状图

最后点击"导出Excel"按钮：

**预期结果**:
- 浏览器下载一个 `.xlsx` 文件
- 使用 Excel/WPS 打开可以看到数据和图表

---

## 常见问题排查

### 问题 1: 端口被占用

**现象**:
```
Error: listen EADDRINUSE: address already in use :::3000
```

**解决方案**:

```bash
# 查找占用端口的进程
lsof -i :3000  # macOS/Linux
netstat -ano | findstr :3000  # Windows

# 杀死进程
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# 或者使用其他端口
npm run dev -- --port 3001
```

### 问题 2: npm install 失败

**现象**:
```
npm ERR! network request failed
```

**解决方案**:

```bash
# 使用国内镜像
npm config set registry https://registry.npmmirror.com

# 重新安装
rm -rf node_modules package-lock.json
npm install

# 验证镜像配置
npm config get registry
```

### 问题 3: uv 安装依赖失败

**现象**:
```
error: Failed to download distributions
```

**解决方案**:

```bash
# 使用国内镜像
export UV_INDEX_URL="https://pypi.tuna.tsinghua.edu.cn/simple"

# 重新安装
uv sync

# 或者使用 pip 安装
uv pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题 4: Python 版本不兼容

**现象**:
```
ERROR: This package requires Python 3.11+
```

**解决方案**:

```bash
# 检查 Python 版本
python3 --version

# 如果版本 < 3.11，使用 uv 安装指定版本
uv venv --python 3.11

# 或者使用 pyenv 安装新版本 Python
brew install pyenv  # macOS
pyenv install 3.11.0
pyenv local 3.11.0

# 然后重新创建虚拟环境
uv venv
```

### 问题 5: 前端无法连接后端

**现象**:
- 浏览器控制台显示 `Network Error`
- `ERR_CONNECTION_REFUSED`

**解决方案**:

```bash
# 1. 检查后端是否运行
curl http://localhost:8000/health

# 2. 检查前端代理配置
cat frontend/vite.config.js
# 确保有这个配置：
# proxy: {
#   '/api': 'http://localhost:8000'
# }

# 3. 检查 CORS 配置
# 打开 backend/app/main.py
# 确保有 CORS 中间件
```

### 问题 6: 图表不显示

**现象**: 导出的 Excel 没有图表

**解决方案**:

1. 使用 Microsoft Excel 或 WPS 打开（不支持 Numbers）
2. 检查后端日志是否有错误
3. 检查图表配置是否正确

### 问题 7: 数据抓取失败

**现象**: 输入 `抓取 [URL]` 后返回错误

**原因**: 只支持静态 HTML，不支持 JavaScript 渲染的页面

**解决方案**:

- 使用测试 URL: `https://www.w3schools.com/html/html_tables.asp`
- 避免抓取需要 JavaScript 的网站

---

## 开发工具配置

### VS Code 推荐配置

创建 `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/backend/.venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "eslint.workingDirectories": ["frontend"]
}
```

创建 `.vscode/extensions.json`:

```json
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "ms-python.python",
    "ms-python.vscode-pylance",
    "bradlc.vscode-tailwindcss"
  ]
}
```

### Chrome DevTools 调试

1. 打开浏览器开发者工具（F12）
2. 切换到 Network 标签
3. 执行操作（如输入 demo）
4. 查看 API 请求：
   - `POST /api/chat`
   - `PUT /api/excel/{id}/sync`
   - `GET /api/excel/export/{id}`

### 后端调试

```bash
# 使用 debug 模式启动
uv run uvicorn app.main:app --reload --log-level debug

# 使用 Python 调试器
uv run python -m pdb app/main.py
```

---

## 启动流程总结

### 首次启动（完整流程）

```bash
# 1. 克隆项目
git clone https://github.com/CuriosityTomorrow/web-excel-agent.git
cd web-excel-agent

# 2. 安装 uv（如果还没有）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. 后端设置
cd backend
uv venv                      # 创建虚拟环境
source .venv/bin/activate    # 激活虚拟环境
uv sync                      # 安装依赖
uv run uvicorn app.main:app --reload &  # 启动后端（后台运行）

# 4. 前端设置
cd ../frontend
npm install                  # 安装依赖
npm run dev &                # 启动前端（后台运行）

# 5. 验证
open http://localhost:3000   # 打开浏览器
```

### 日常开发（简化流程）

```bash
cd web-excel-agent

# 启动后端
cd backend
source .venv/bin/activate
uv run uvicorn app.main:app --reload

# 新开终端，启动前端
cd frontend
npm run dev
```

### 使用一键脚本

```bash
cd web-excel-agent
./start.sh
```

---

## 端口占用说明

| 服务 | 默认端口 | 用途 | 修改方法 |
|------|---------|------|---------|
| 前端 | 3000 | Vite 开发服务器 | `npm run dev -- --port 3001` |
| 后端 | 8000 | FastAPI 服务 | `uvicorn app.main:app --port 8001` |

---

## 停止服务

```bash
# 前端: 在终端按 Ctrl+C

# 后端: 在终端按 Ctrl+C

# 或者查找并杀死进程
ps aux | grep "uvicorn"
kill -9 <PID>

ps aux | grep "vite"
kill -9 <PID>
```

---

## 清理环境

### 清理前端

```bash
cd frontend
rm -rf node_modules
rm -rf .vite
rm package-lock.json
```

### 清理后端

```bash
cd backend
rm -rf .venv
rm -rf __pycache__
rm -rf .pytest_cache
```

### 完全清理

```bash
cd web-excel-agent
git clean -fdx  # 删除所有未跟踪的文件
```

---

## 目录结构

```
web-excel-agent/
├── frontend/                 # 前端项目
│   ├── node_modules/        # 依赖（npm install 后生成）
│   ├── .vite/              # Vite 缓存
│   ├── src/
│   │   ├── components/     # React 组件
│   │   ├── services/       # API 调用
│   │   └── App.jsx         # 主应用
│   ├── package.json        # 前端依赖配置
│   └── vite.config.js      # Vite 配置
│
├── backend/                 # 后端项目
│   ├── .venv/              # 虚拟环境（uv venv 后生成）
│   ├── app/
│   │   ├── api/           # API 路由
│   │   ├── services/      # 业务逻辑
│   │   └── main.py        # FastAPI 入口
│   ├── requirements.txt    # Python 依赖
│   └── pyproject.toml     # 项目配置
│
├── skills/                  # Skill 定义
├── start.sh                # 一键启动脚本
└── MIGRATION_GUIDE.md      # 迁移指南
```

---

## 下一步

启动成功后，建议：

1. **阅读文档**
   - `PROJECT_CONTEXT.md` - 项目完整上下文
   - `MIGRATION_GUIDE.md` - 迁移到公司项目指南
   - `COMPONENTS_USAGE.md` - 组件复用指南

2. **测试功能**
   - 输入 `demo` 测试数据生成
   - 编辑单元格测试在线编辑
   - 创建图表测试可视化
   - 导出 Excel 测试文件生成

3. **开始开发**
   - 修改组件代码
   - 添加新功能
   - 集成到公司项目

---

## 技术支持

- **GitHub Issues**: https://github.com/CuriosityTomorrow/web-excel-agent/issues
- **项目文档**: 查看 `docs/` 目录
- **内部联系**: [@你的联系方式]

---

**祝启动顺利！🚀**
