# 📤 推送项目到GitHub完整指南

## 步骤1: 登录GitHub CLI

在终端执行以下命令：

```bash
gh auth login
```

然后按照提示操作：
1. 选择 `GitHub.com`
2. 选择 `HTTPS` 或 `SSH`（推荐HTTPS）
3. 选择 `Login with a web browser`（推荐）或输入认证token
4. 完成授权

## 步骤2: 推送到GitHub

### 方式A: 自动创建仓库（推荐）

```bash
cd /Users/samdediannao/Web_excel

# 创建私有仓库并推送
gh repo create web-excel-agent --private --source=. --remote=origin --push

# 或创建公开仓库
gh repo create web-excel-agent --public --source=. --remote=origin --push
```

### 方式B: 手动创建仓库

1. 访问 https://github.com/new
2. 仓库名称：`web-excel-agent`
3. 设置为私有或公开（Private/Public）
4. **不要**初始化README、.gitignore或license
5. 点击"Create repository"

然后在终端执行：

```bash
cd /Users/samdediannao/Web_excel

# 添加远程仓库
git remote add origin https://github.com/你的用户名/web-excel-agent.git

# 推送代码
git push -u origin main
```

## 步骤3: 在公司拉取代码

### 方法1: 使用HTTPS（推荐）

```bash
# 克隆仓库
git clone https://github.com/你的用户名/web-excel-agent.git

# 进入项目目录
cd web-excel-agent

# 安装后端依赖
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 安装前端依赖
cd ../frontend
npm install

# 启动服务
# 终端1: 启动后端
cd ../backend
uvicorn app.main:app --reload

# 终端2: 启动前端
cd ../frontend
npm run dev
```

### 方法2: 使用SSH（需要配置SSH密钥）

```bash
# 克隆仓库
git clone git@github.com:你的用户名/web-excel-agent.git

# 其余步骤同上
```

## 步骤4: 配置公司环境

### 后端配置

```bash
cd backend

# 复制配置文件（如果需要）
cp .env.example .env

# 编辑配置，设置公司相关参数
# - API密钥
# - 数据库连接
# - 其他环境变量
```

### 前端配置

```bash
cd frontend

# 修改API地址（如果后端不在本地）
# 编辑 src/services/api.js
# 修改 baseURL 为实际的后端地址
```

## 步骤5: 启动项目

```bash
# 后端（终端1）
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn app.main:app --reload --port 8000

# 前端（终端2）
cd frontend
npm run dev
```

访问：http://localhost:3000

## 团队协作

### 添加团队成员

1. 进入GitHub仓库页面
2. 点击 `Settings` → `Collaborators`
3. 点击 `Add people`
4. 输入团队成员的GitHub用户名或邮箱
5. 设置权限（Read/Write/Admin）

### 创建开发分支

```bash
# 创建新分支
git checkout -b feature/新功能

# 开发完成后
git add .
git commit -m "feat: 添加新功能"
git push origin feature/新功能

# 在GitHub创建Pull Request
```

## 常用Git命令

```bash
# 查看状态
git status

# 拉取最新代码
git pull origin main

# 提交代码
git add .
git commit -m "描述你的修改"
git push origin main

# 查看分支
git branch -a

# 切换分支
git checkout 分支名
```

## 注意事项

1. **敏感信息**：不要提交以下文件
   - API密钥
   - 数据库密码
   - 环境变量文件（.env）
   - 公司内部配置

2. **依赖安装**：在公司电脑上首次运行需要安装依赖
   - Python依赖：`pip install -r requirements.txt`
   - Node依赖：`npm install`

3. **端口冲突**：如果端口被占用，修改启动命令
   ```bash
   # 后端使用其他端口
   uvicorn app.main:app --reload --port 8001

   # 前端使用其他端口
   npm run dev -- --port 3001
   ```

4. **Python版本**：确保Python版本 >= 3.11
   ```bash
   python3 --version
   ```

## 下一步

- ✅ 项目已推送到GitHub
- ✅ 团队成员可以克隆代码
- ✅ 可以开始功能开发
- ✅ 建议配置CI/CD（可选）

## 需要帮助？

- GitHub文档：https://docs.github.com
- Git文档：https://git-scm.com/doc
- 本项目README：查看 README.md
