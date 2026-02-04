# 📊 Web Excel Agent - 项目完整上下文

> **创建日期**: 2026-02-04
> **开发者**: Sylsylgo310! (GitHub: CuriosityTomorrow)
> **项目仓库**: https://github.com/CuriosityTomorrow/web-excel-agent

---

## 📋 项目概述

### 核心功能
一个基于Web的AI驱动Excel应用系统，支持：
- 🤖 AI对话界面（类似ChatGPT）
- 🌐 网页数据抓取（静态HTML）
- 📊 在线Excel编辑（单元格编辑、行列添加）
- 📈 图表生成（柱状图、折线图、饼图）
- 💾 Excel导出（包含图表）

### 使用场景
- 从网页抓取表格数据
- 快速生成Excel报表
- 数据可视化分析
- 团队协作编辑

---

## 🛠️ 技术栈

### 前端
```javascript
{
  "框架": "React 18",
  "构建工具": "Vite 6.4",
  "样式": "TailwindCSS",
  "Excel编辑": "自定义表格组件",
  "图表库": "Recharts (前端预览)",
  "文件导出": "xlsx (前端备用)",
  "HTTP客户端": "Axios",
  "语言": "JavaScript (JSX)"
}
```

### 后端
```python
{
  "框架": "FastAPI",
  "Python版本": "3.11+",
  "Excel处理": "openpyxl",
  "网页抓取": "BeautifulSoup4",
  "图表生成": "openpyxl.chart (BarChart, LineChart, PieChart)",
  "HTTP客户端": "requests",
  "ASGI服务器": "uvicorn",
  "数据验证": "Pydantic"
}
```

---

## 🏗️ 架构设计

### 架构类型
**前后端分离 + 混合渲染**

### 数据流

#### 1. 数据生成流程
```
用户输入 → 前端ChatInterface → POST /api/chat
  → 后端AgentService处理
  → 生成数据/抓取网页
  → 存储在内存(workbooks字典)
  → 返回JSON给前端
  → 前端更新state → 渲染表格
```

#### 2. 编辑流程
```
用户编辑单元格
  → 前端更新React state
  → 实时渲染表格
  → 后端数据此时是旧的
```

#### 3. 导出流程（关键）
```
用户点击"导出Excel"
  → 前端执行3个API：

  ① PUT /api/excel/{id}/sync
     功能：同步最新表格数据到后端
     后端：excel_service.sync_workbook()

  ② POST /api/excel/{id}/charts/batch
     功能：发送图表配置到后端
     后端：excel_service.set_workbook_charts()

  ③ GET /api/excel/export/{id}
     功能：生成Excel文件
     后端：excel_service.export_to_excel_with_charts()
     使用openpyxl创建Excel和图表对象
     返回二进制文件流
  → 前端接收 → 创建Blob → 触发下载
```

### 为什么这样设计？

| 决策 | 原因 |
|------|------|
| **后端生成Excel** | openpyxl功能强大，支持图表、格式、公式 |
| **前端触发下载** | 用户体验更好，可以看到进度 |
| **导出时同步数据** | 确保导出的是最新编辑的数据 |
| **混合渲染** | 前端提供实时UI，后端处理复杂逻辑 |

---

## 📁 目录结构

```
web_excel/
├── frontend/                 # React前端
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface/    # AI对话界面
│   │   │   ├── Spreadsheet/      # Excel编辑器（自定义组件）
│   │   │   └── ChartBuilder/      # 图表预览（Recharts）
│   │   ├── services/
│   │   │   └── api.js            # API调用封装
│   │   ├── App.jsx                # 主应用组件
│   │   └── main.jsx               # 入口文件
│   ├── package.json
│   └── vite.config.js             # Vite配置（含代理）
│
├── backend/                  # Python后端
│   ├── app/
│   │   ├── api/                   # FastAPI路由
│   │   │   ├── chat.py           # /api/chat
│   │   │   ├── excel.py          # /api/excel/*
│   │   │   ├── scraper.py        # /api/scrape/*
│   │   │   └── chart.py          # /api/chart
│   │   ├── services/
│   │   │   ├── agent_service.py   # AI Agent（规则引擎）
│   │   │   ├── excel_service.py   # Excel操作（openpyxl）
│   │   │   ├── scraper_service.py # 网页抓取
│   │   │   └── chart_service.py   # 图表配置
│   │   ├── models/
│   │   │   └── excel.py           # Pydantic数据模型
│   │   └── main.py               # FastAPI应用入口
│   ├── mcp_tools/               # MCP工具定义
│   │   ├── excel_tools.py       # Excel MCP工具
│   │   ├── scraper_tools.py     # 抓取MCP工具
│   │   └── chart_tools.py       # 图表MCP工具
│   └── requirements.txt
│
├── skills/                    # Skill定义（YAML）
│   ├── excel_agent.yaml        # 主Agent Skill
│   ├── data_scraper.yaml       # 数据抓取Skill
│   └── chart_builder.yaml      # 图表构建Skill
│
├── HOW_TO_TEST.md             # 3步测试指南
├── QUICK_TEST.md              # 快速命令参考
├── TEST_URLS.md               # 测试URL参考
├── TESTING_GUIDE.md           # 完整测试指南
├── EXPORT_GUIDE.md            # 导出功能说明
├── PUSH_TO_GITHUB.md          # GitHub推送指南
├── README.md                  # 项目说明
└── .gitignore                 # Git忽略文件
```

---

## 🔑 关键代码说明

### 1. 前端Excel组件（自定义实现）

**文件**: `frontend/src/components/Spreadsheet/index.jsx`

**特点**:
- 使用原生HTML table + input
- 支持单元格编辑
- 支持添加行列
- 导出时调用后端API生成Excel

**关键代码**:
```javascript
// 导出时的3个API调用
await api.put(`/excel/${data.id}/sync`, data)  // 同步数据
await api.post(`/excel/${data.id}/charts/batch`, charts)  // 发送图表
await api.get(`/excel/export/${data.id}`)  // 获取Excel文件
```

### 2. 后端Excel服务

**文件**: `backend/app/services/excel_service.py`

**关键功能**:
```python
class ExcelService:
    def __init__(self):
        self.workbooks = {}   # 存储workbook数据
        self.charts = {}      # 存储图表配置

    def sync_workbook(self, workbook_id, workbook_data):
        """同步前端数据"""
        self.workbooks[workbook_id] = workbook_data

    def set_workbook_charts(self, workbook_id, charts):
        """设置图表配置"""
        self.charts[workbook_id] = charts

    def export_to_excel_with_charts(self, workbook_id):
        """生成包含图表的Excel"""
        wb = Workbook()
        # 添加数据
        # 添加图表（使用openpyxl.chart）
        return output.read()
```

### 3. AI Agent（规则引擎）

**文件**: `backend/app/services/agent_service.py`

**实现方式**:
- 规则引擎（非真实LLM）
- 关键词匹配：`demo`, `抓取`, `创建柱状图`, `创建折线图`, `创建饼图`
- 可替换为真实LLM（如OpenAI API）

**关键函数**:
```python
def process_message(self, message: str):
    if 'demo' in message:
        return self._handle_demo_request()
    elif '抓取' in message:
        return self._handle_scrape_request(message)
    elif '图表' in message or 'chart' in message:
        return self._handle_chart_request(message)
```

---

## 🐛 已解决的问题

### 问题1: 对话框滚动
**现象**: 聊天消息被顶下去，看不到最新消息
**解决**:
- 添加`useRef`和`useEffect`
- 自动滚动到最新消息
- 固定输入框在底部（`flex-shrink-0`, `min-h-0`）

### 问题2: 图表导出失败
**现象**: 导出的Excel没有图表
**原因**:
1. 前端导入错误：`import { api }` 应该是 `import api`
2. 后端API路径重复：`/api/api/excel/...`
3. 饼图没有y_axis属性（PieChart）

**解决**:
```javascript
// 修正导入
import api from '../../services/api'

// 修正路径
await api.put(`/excel/${id}/sync`, data)  // 移除 /api 前缀
```

```python
# 修正饼图代码
if chart_type == 'pie':
    chart = PieChart()
    # 不要设置 y_axis 和 x_axis
```

### 问题3: 图表数据不同步
**现象**: 导出的图表数据与表格不匹配
**原因**: 创建图表时后端立即保存，但用户编辑了表格
**解决**:
- 移除创建图表时的后端保存
- 导出时使用批量API：`/charts/batch`
- 导出前先同步最新表格数据

### 问题4: Numbers无法显示图表
**现象**: Mac的Numbers打开Excel看不到图表
**原因**: Numbers对openpyxl生成的图表支持有限
**解决**: 使用Microsoft Excel或WPS打开

---

## 📊 API端点清单

### Chat API
- `POST /api/chat` - AI对话接口

### Excel API
- `POST /api/excel/workbook` - 创建工作簿
- `GET /api/excel/workbook/{id}` - 获取工作簿
- `PUT /api/excel/workbook/{id}/cell` - 更新单元格
- `GET /api/excel/export/{id}` - 导出Excel文件（含图表）
- `PUT /api/excel/{id}/sync` - 同步表格数据
- `POST /api/excel/{id}/chart` - 添加单个图表
- `POST /api/excel/{id}/charts/batch` - 批量设置图表

### Scraper API
- `POST /api/scrape/table` - 抓取网页表格

### Chart API
- `POST /api/chart` - 创建图表配置

### Health Check
- `GET /health` - 健康检查
- `GET /` - API文档链接

---

## 🚀 快速启动指南

### 开发环境启动

```bash
# 终端1 - 后端
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# 终端2 - 前端
cd frontend
npm install
npm run dev

# 访问
open http://localhost:3000
```

### 测试命令

| 命令 | 功能 |
|------|------|
| `demo` | 生成演示数据 |
| `抓取 [URL]` | 抓取网页表格 |
| `创建柱状图` | 创建柱状图 |
| `创建折线图` | 创建折线图 |
| `创建饼图` | 创建饼图 |

---

## 🔧 配置说明

### 前端配置

**文件**: `frontend/vite.config.js`
```javascript
export default defineConfig({
  server: {
    port: 3000,
    proxy: {
      '/api': 'http://localhost:8000',  // API代理
    },
  },
})
```

**重要**: 所有API调用不要加`/api`前缀，因为baseURL已经包含了

### 后端配置

**文件**: `backend/app/main.py`
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
```

---

## 📦 依赖说明

### 前端关键依赖
```json
{
  "react": "^18.3.1",
  "vite": "^6.4.1",
  "axios": "^1.7.7",
  "recharts": "^2.12.7",
  "tailwindcss": "^3.4.1"
}
```

### 后端关键依赖
```
fastapi==0.115.6
uvicorn==0.34.0
openpyxl==3.1.5
beautifulsoup4==4.12.3
requests==2.32.3
pydantic==2.10.4
```

---

## 🎯 功能特性清单

### 已实现功能
- ✅ AI对话界面（实时响应）
- ✅ Demo数据生成（6个月销售数据）
- ✅ 网页表格抓取（静态HTML）
- ✅ 在线Excel编辑
  - 单元格编辑
  - 添加行
  - 添加列
- ✅ 图表创建
  - 柱状图（BarChart）
  - 折线图（LineChart）
  - 饼图（PieChart）
- ✅ Excel导出（包含图表）
- ✅ 自动滚动
- ✅ 错误处理
- ✅ 加载状态显示

### 局限性
- ❌ 只支持静态HTML抓取（JavaScript渲染的网页不支持）
- ❌ 规则引擎AI（非真实LLM）
- ❌ 单用户（数据存储在内存）
- ❌ 图表只显示在Excel中（前端只有预览）

### 未来改进方向
1. **集成真实LLM**（OpenAI/Anthropic）
2. **持久化存储**（数据库）
3. **用户系统**（登录、权限）
4. **更多图表类型**（散点图、雷达图等）
5. **Excel公式支持**
6. **多Sheet支持**
7. **协作编辑**（WebSocket）
8. **文件上传**
9. **导出PDF**
10. **历史记录**

---

## 🌐 GitHub信息

**仓库**: https://github.com/CuriosityTomorrow/web-excel-agent
**类型**: 公开（Public）
**许可**: MIT License
**分支**: main

### 团队使用
```bash
# 克隆
git clone https://github.com/CuriosityTomorrow/web-excel-agent.git

# 启动
cd web-excel-agent
./start.sh

# 或手动启动
# 后端
cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload

# 前端
cd frontend && npm install && npm run dev
```

---

## 📝 开发决策记录

### 为什么选择自定义表格组件而非react-spreadsheet-grid？
- 更好的控制能力
- 避免第三方库的限制
- 学习价值高

### 为什么导出使用后端而非前端xlsx库？
- openpyxl功能更强大（支持图表）
- 数据一致性更好
- 便于扩展复杂功能

### 为什么使用规则引擎而非真实LLM？
- 快速开发（无需API key）
- 可控性强
- 易于调试
- 后续可替换

### 为什么图表在前端只显示预览？
- 减轻后端负担
- 实时反馈
- 最终图表在Excel中生成（更专业）

---

## 🧪 测试指南

### 基础测试
```bash
1. 访问 http://localhost:3000
2. 输入: demo
3. 检查表格是否显示
4. 编辑单元格
5. 输入: 创建柱状图
6. 点击"导出Excel"
7. 用Excel/WPS打开验证图表
```

### 网页抓取测试
```bash
输入: 帮我抓取 https://www.w3schools.com/html/html_tables.asp 的第一个表格
```

### 错误处理测试
```bash
1. 输入无效命令
2. 抓取需要JS的网页（应该失败）
3. 导出时没有图表（应该成功）
```

---

## 🐛 调试技巧

### 前端调试
```javascript
// 查看导出日志
按F12打开控制台，点击导出按钮，查看:
- Workbook ID
- Charts数量
- 每个步骤的执行结果
```

### 后端调试
```bash
# 查看后端日志
# 后端终端会显示API请求信息
INFO: 127.0.0.1:xxxxx - "POST /api/chat HTTP/1.1" 200 OK
```

### 常见问题
1. **导出失败404**: API路径错误（检查是否有重复的/api）
2. **图表不显示**: 使用Excel/WPS而非Numbers
3. **demo没反应**: 检查后端是否运行

---

## 📚 文档清单

| 文档 | 说明 |
|------|------|
| `README.md` | 项目介绍 |
| `HOW_TO_TEST.md` | 3步快速测试 |
| `QUICK_TEST.md` | 命令速查表 |
| `TEST_URLS.md` | 测试URL参考 |
| `TESTING_GUIDE.md` | 完整测试指南 |
| `EXPORT_GUIDE.md` | 导出功能说明 |
| `PUSH_TO_GITHUB.md` | GitHub推送指南 |
| `QUICK_PUSH_GUIDE.md` | 快速推送指南 |
| `PROJECT_CONTEXT.md` | **本文档** |

---

## 💡 关键经验总结

### 技术选型
1. **前端框架**: React > Vue（生态更好）
2. **构建工具**: Vite > Webpack（更快）
3. **后端框架**: FastAPI > Flask（异步支持）
4. **Excel库**: openpyxl > xlsx（功能更全）
5. **图表库**: openpyxl.chart > ECharts（直接嵌入Excel）

### 架构设计
1. **前后端分离**: 职责清晰，易于扩展
2. **混合渲染**: 前端负责UI，后端负责复杂逻辑
3. **API设计**: RESTful，语义化
4. **数据同步**: 导出时同步，保证一致性

### 开发流程
1. **先完成后端**: 数据和逻辑优先
2. **再对接前端**: UI交互
3. **最后完善**: 错误处理、边界情况
4. **文档先行**: 边开发边写文档

### 问题排查
1. **看日志**: 前端console + 后端终端
2. **简化问题**: 最小化复现
3. **二分法**: 逐步排除
4. **查文档**: 官方文档最可靠

---

## 🎓 学习资源

### React
- 官方文档: https://react.dev
- Vite文档: https://vitejs.dev

### FastAPI
- 官方文档: https://fastapi.tiangolo.com
- 教程: https://fastapi.tiangolo.com/tutorial/

### openpyxl
- 官方文档: https://openpyxl.readthedocs.io
- 图表教程: https://openpyxl.readthedocs.io/en/stable/charts.html

---

## 📞 联系方式

- **GitHub**: CuriosityTomorrow
- **邮箱**: 490233318@qq.com
- **项目**: https://github.com/CuriosityTomorrow/web-excel-agent

---

## ⭐ 项目亮点

1. **完整的前后端分离架构**
2. **实时Excel编辑体验**
3. **AI对话交互**
4. **网页数据抓取**
5. **Excel图表嵌入**
6. **详尽的文档**
7. **开箱即用**

---

## 📅 开发时间线

- **2026-02-04**: 项目创建
- **2026-02-04**: 核心功能开发完成
- **2026-02-04**: 推送到GitHub
- **持续改进**: 根据反馈优化

---

**本文档由 Claude Sonnet 辅助创建**
**最后更新**: 2026-02-04
