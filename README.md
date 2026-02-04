# Web Excel Agent

一个基于Web的AI驱动的Excel应用系统，可以从网页抓取数据、生成Excel、在线编辑和创建图表。

## 功能特性

- 🤖 **AI对话界面**：通过自然语言与AI助手交互
- 🌐 **网页数据抓取**：从静态HTML页面提取表格和列表数据
- 📊 **在线Excel编辑**：实时编辑单元格，支持添加行列
- 📈 **图表生成**：支持柱状图、折线图、饼图
- 💾 **导出功能**：一键导出为Excel文件
- 🔧 **MCP工具**：模块化的工具集，可扩展
- 📦 **Skill系统**：可复用的工作流配置

## 技术栈

### 前端
- React 18
- Vite
- react-spreadsheet-grid
- xlsx (Excel导出)
- Recharts (图表)
- TailwindCSS
- Axios

### 后端
- Python 3.11+
- FastAPI
- openpyxl
- BeautifulSoup4
- matplotlib
- uvicorn

## 快速开始

### 前置要求
- Node.js 18+
- Python 3.11+
- npm 或 yarn

### 安装依赖

#### 前端
```bash
cd frontend
npm install
```

#### 后端
```bash
cd backend
pip install -r requirements.txt
```

### 启动服务

#### 启动后端
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

#### 启动前端
```bash
cd frontend
npm run dev
```

### 访问应用
- 前端：http://localhost:3000
- 后端API文档：http://localhost:8000/docs

## 使用示例

### 快速体验（推荐）

#### 方式1：使用演示数据

在AI对话框中输入：
```
demo
```

或

```
演示数据
```

这将立即生成一个包含6个月销售数据的示例表格，你可以：
- ✅ 测试编辑功能
- ✅ 测试导出功能
- ✅ 测试图表生成

#### 方式2：抓取真实网页数据

在AI对话框中输入：
```
帮我抓取 https://www.w3schools.com/html/html_tables.asp 的表格数据
```

### 完整工作流示例

#### 1. 生成Demo数据
```
你: demo
AI: 已生成演示数据：包含6个月的销售数据，可以测试编辑、导出和图表功能
```

#### 2. 编辑数据
- 点击任意单元格进行编辑
- 使用"+行"/"+列"按钮添加行列
- 数据会自动保存

#### 3. 创建图表
```
你: 创建一个柱状图
```
右侧会显示对应的图表

#### 4. 导出Excel
点击"导出Excel"按钮，浏览器会下载 `.xlsx` 文件

## 项目结构

```
web_excel/
├── frontend/                 # React前端
│   ├── src/
│   │   ├── components/      # 组件
│   │   │   ├── ChatInterface/
│   │   │   ├── Spreadsheet/
│   │   │   └── ChartBuilder/
│   │   ├── services/        # API服务
│   │   └── App.jsx
│   └── package.json
├── backend/                 # Python后端
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── services/       # 业务逻辑
│   │   ├── models/         # 数据模型
│   │   └── main.py
│   ├── mcp_tools/          # MCP工具
│   └── requirements.txt
└── skills/                 # Skill定义
    ├── excel_agent.yaml
    ├── data_scraper.yaml
    ├── chart_builder.yaml
    └── skill_generator.yaml
```

## MCP工具

### Excel工具
- `create_excel_workbook` - 创建工作簿
- `read_excel_data` - 读取数据
- `update_cell` - 更新单元格
- `export_excel_file` - 导出文件

### 抓取工具
- `scrape_web_table` - 抓取网页表格
- `scrape_web_list` - 抓取网页列表
- `extract_structured_data` - 提取结构化数据

### 图表工具
- `create_chart` - 创建图表
- `create_chart_from_excel_sheet` - 从Excel创建图表
- `export_chart` - 导出图表

## Skills

系统包含以下预定义Skills：

1. **excel_agent** - 主Excel Agent，整合所有功能
2. **data_scraper** - 专注数据抓取
3. **chart_builder** - 专注图表生成
4. **skill_generator** - 自动生成自定义Skill

## API文档

启动后端服务后访问：http://localhost:8000/docs

## 开发指南

### 添加新的MCP工具

1. 在 `backend/mcp_tools/` 创建新文件
2. 定义工具函数
3. 在 `MCP_TOOLS` 字典中注册

### 创建自定义Skill

1. 在 `skills/` 目录创建 `.yaml` 文件
2. 定义工具和工作流
3. Agent会自动识别并使用

## 常见问题

### Q: 如何抓取需要登录的页面？
A: 当前版本仅支持静态公开页面。需要登录的场景请考虑后续集成浏览器自动化工具。

### Q: 支持哪些Excel公式？
A: 当前版本支持基础数据编辑。公式计算功能计划在后续版本添加。

### Q: 如何替换为真实LLM？
A: 修改 `backend/app/services/agent_service.py`，将规则引擎替换为LLM API调用即可。

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

项目地址：[GitHub Repo]
