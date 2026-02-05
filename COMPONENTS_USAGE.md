# 模块复用指南 - 各组件功能说明

> 本文档帮助团队成员快速了解项目各模块功能，并指导如何独立复用前端组件或后端逻辑。

---

## 快速导航

- [前端可复用组件](#前端可复用组件)
- [后端可复用服务](#后端可复用服务)
- [完整复用示例](#完整复用示例)

---

## 前端可复用组件

### 1. ChatInterface - AI 对话界面组件

**位置**: `frontend/src/components/ChatInterface/`

**功能**:
- 类似 ChatGPT 的对话界面
- 支持用户输入和 AI 响应展示
- 自动滚动到最新消息
- 加载状态显示

**可复用场景**:
- 任何需要 AI 对话功能的项目
- 客服聊天界面
- 命令行工具的 Web 界面

**如何复用**:

```javascript
// 1. 复制整个 ChatInterface 文件夹到你的项目
// 2. 在你的组件中引入

import ChatInterface from './components/ChatInterface';

function App() {
  const handleSendMessage = async (message) => {
    // 调用你自己的后端 API
    const response = await fetch('/api/your-endpoint', {
      method: 'POST',
      body: JSON.stringify({ message })
    });
    return response.json();
  };

  return (
    <ChatInterface
      onSendMessage={handleSendMessage}
      placeholder="输入您的消息..."
    />
  );
}
```

**依赖**:
- React 18+
- 无其他第三方依赖

---

### 2. Spreadsheet - Excel 表格编辑器

**位置**: `frontend/src/components/Spreadsheet/`

**功能**:
- 单元格编辑
- 添加行/列
- 实时数据更新
- 支持任意二维数据展示

**可复用场景**:
- 数据表格展示
- 在线表单编辑
- 配置管理界面
- 任何需要编辑二维数据的场景

**如何复用**:

```javascript
import Spreadsheet from './components/Spreadsheet';

function App() {
  const [data, setData] = useState({
    id: 'sheet-1',
    title: '销售数据',
    headers: ['产品', '一月', '二月', '三月'],
    rows: [
      ['产品A', 100, 200, 300],
      ['产品B', 150, 250, 350]
    ]
  });

  const handleDataChange = (newData) => {
    setData(newData);
    // 可以在这里保存到后端
  };

  return (
    <Spreadsheet
      data={data}
      onDataChange={handleDataChange}
      editable={true}
    />
  );
}
```

**依赖**:
- React 18+
- TailwindCSS（样式）

**数据格式**:
```javascript
{
  id: string,           // 唯一标识
  title: string,        // 表格标题
  headers: string[],    // 列标题
  rows: array[][]       // 二维数据数组
}
```

---

### 3. ChartBuilder - 图表配置预览组件

**位置**: `frontend/src/components/ChartBuilder/`

**功能**:
- 图表类型选择（柱状图、折线图、饼图）
- 数据范围选择
- 实时图表预览（使用 Recharts）
- 图表配置管理

**可复用场景**:
- 数据可视化配置
- 报表生成工具
- 数据分析平台

**如何复用**:

```javascript
import ChartBuilder from './components/ChartBuilder';

function App() {
  const [charts, setCharts] = useState([]);
  const spreadsheetData = {
    headers: ['产品', '一月', '二月', '三月'],
    rows: [['A', 100, 200, 300]]
  };

  const handleChartsChange = (newCharts) => {
    setCharts(newCharts);
  };

  return (
    <ChartBuilder
      charts={charts}
      spreadsheetData={spreadsheetData}
      onChartsChange={handleChartsChange}
    />
  );
}
```

**依赖**:
- React 18+
- Recharts (`npm install recharts`)
- TailwindCSS

**图表配置格式**:
```javascript
{
  id: string,
  type: 'bar' | 'line' | 'pie',
  title: string,
  dataRange: {
    headerIndex: number,  // 选择哪一列作为类别
    startRow: number,
    endRow: number
  }
}
```

---

### 4. API 服务封装

**位置**: `frontend/src/services/api.js`

**功能**:
- 统一的 API 调用封装
- 自动处理 baseURL
- 错误处理

**如何复用**:

```javascript
// 复制 api.js 到你的项目
// 修改 baseURL:

import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  timeout: 30000
});

// 导出使用
export default api;
```

**在你的组件中使用**:
```javascript
import api from './services/api';

// GET 请求
const data = await api.get('/users');

// POST 请求
const result = await api.post('/users', { name: 'John' });

// PUT 请求
await api.put('/users/1', { name: 'Jane' });
```

---

## 后端可复用服务

### 1. ExcelService - Excel 操作服务

**位置**: `backend/app/services/excel_service.py`

**功能**:
- 创建 Excel 工作簿
- 添加数据到工作表
- 生成图表（柱状图、折线图、饼图）
- 导出包含图表的 Excel 文件

**可复用场景**:
- 报表导出功能
- 数据分析工具
- Excel 批处理

**如何复用**:

```python
# 1. 复制 excel_service.py 到你的项目
# 2. 安装依赖: pip install openpyxl

from excel_service import ExcelService

# 初始化服务
excel_service = ExcelService()

# 准备数据
workbook_data = {
    'title': '销售报表',
    'headers': ['产品', '一月', '二月', '三月'],
    'rows': [
        ['产品A', 100, 200, 300],
        ['产品B', 150, 250, 350]
    ]
}

# 同步数据
excel_service.sync_workbook('report-1', workbook_data)

# 添加图表配置
charts = [{
    'type': 'bar',
    'title': '销售趋势',
    'dataRange': {'headerIndex': 0, 'startRow': 0, 'endRow': 1}
}]
excel_service.set_workbook_charts('report-1', charts)

# 导出 Excel 文件
excel_file = excel_service.export_to_excel_with_charts('report-1')

# 保存到文件
with open('report.xlsx', 'wb') as f:
    f.write(excel_file)

print('Excel 文件已生成！')
```

**独立脚本示例**:
```python
#!/usr/bin/env python3
# generate_report.py

from excel_service import ExcelService
import sys

def main():
    service = ExcelService()

    # 从数据库或其他来源获取数据
    data = {
        'title': sys.argv[1] if len(sys.argv) > 1 else '报表',
        'headers': ['类别', '数值1', '数值2'],
        'rows': [
            ['A', 100, 200],
            ['B', 150, 250]
        ]
    }

    service.sync_workbook('temp', data)
    excel_file = service.export_to_excel_with_charts('temp')

    with open('output.xlsx', 'wb') as f:
        f.write(excel_file)

    print('✅ 报表已生成: output.xlsx')

if __name__ == '__main__':
    main()
```

**依赖**:
```bash
pip install openpyxl==3.1.5
```

---

### 2. ScraperService - 网页数据抓取服务

**位置**: `backend/app/services/scraper_service.py`

**功能**:
- 抓取网页中的表格数据
- 提取列表数据
- 解析结构化数据
- 自动清理和格式化数据

**可复用场景**:
- 数据采集工具
- 爬虫项目
- 数据迁移工具

**如何复用**:

```python
# 1. 复制 scraper_service.py 到你的项目
# 2. 安装依赖: pip install beautifulsoup4 requests

from scraper_service import ScraperService

# 初始化服务
scraper = ScraperService()

# 示例1: 抓取网页表格
url = 'https://example.com/data-table'
result = scraper.scrape_table(url)

if result['success']:
    print(f"找到 {len(result['data'])} 个表格")
    for i, table in enumerate(result['data']):
        print(f"\n表格 {i+1}:")
        print(f"  列: {table['headers']}")
        print(f"  行数: {len(table['rows'])}")

# 示例2: 提取列表
result = scraper.scrape_list(url)
if result['success']:
    print(f"找到列表: {result['items']}")
```

**独立脚本示例**:
```python
#!/usr/bin/env python3
# scrape_data.py

import sys
import json
from scraper_service import ScraperService

def main():
    if len(sys.argv) < 2:
        print("用法: python scrape_data.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    scraper = ScraperService()

    print(f"正在抓取: {url}")
    result = scraper.scrape_table(url)

    if result['success']:
        # 输出 JSON
        print(json.dumps(result['data'], indent=2, ensure_ascii=False))

        # 保存到文件
        with open('scraped_data.json', 'w', encoding='utf-8') as f:
            json.dump(result['data'], f, indent=2, ensure_ascii=False)
        print(f"\n✅ 数据已保存到 scraped_data.json")
    else:
        print(f"❌ 抓取失败: {result['message']}")

if __name__ == '__main__':
    main()
```

**使用命令**:
```bash
python scrape_data.py https://www.w3schools.com/html/html_tables.asp
```

**依赖**:
```bash
pip install beautifulsoup4==4.12.3 requests==2.32.3
```

---

### 3. ChartService - 图表配置服务

**位置**: `backend/app/services/chart_service.py`

**功能**:
- 图表配置验证
- 图表数据提取
- 支持多种图表类型

**如何复用**:

```python
from chart_service import ChartService

chart_service = ChartService()

# 创建图表配置
chart = chart_service.create_chart({
    'type': 'bar',
    'title': '销售统计',
    'x_axis': '产品',
    'y_axis': '销售额'
})

# 验证配置
if chart_service.validate_chart(chart):
    print("图表配置有效")
```

---

### 4. AgentService - AI 规则引擎（可扩展为 LLM）

**位置**: `backend/app/services/agent_service.py`

**功能**:
- 规则引擎（当前实现）
- 可轻松替换为真实 LLM（OpenAI、Claude 等）
- 消息解析和任务路由

**如何复用/扩展**:

```python
from agent_service import AgentService

class YourAgentService(AgentService):
    def __init__(self):
        super().__init__()
        # 添加你的自定义规则
        self.rules.update({
            '生成报告': self._handle_report,
            '发送邮件': self._handle_email
        })

    def _handle_report(self, message):
        # 你的业务逻辑
        return {
            'type': 'report',
            'data': {...}
        }

# 集成真实 LLM 示例
class LLMService(AgentService):
    def __init__(self, api_key):
        super().__init__()
        self.client = OpenAI(api_key=api_key)

    def process_message(self, message: str):
        # 调用真实 LLM
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": message}]
        )
        # 解析响应并调用相应的工具
        return self._parse_llm_response(response)
```

---

### 5. API 路由模块

**位置**: `backend/app/api/`

**可复用的路由文件**:

#### chat.py - 对话 API
```python
# 复制到你的 FastAPI 项目
from app.api.chat import router as chat_router
app.include_router(chat_router, prefix="/api/chat", tags=["chat"])
```

#### excel.py - Excel API
```python
from app.api.excel import router as excel_router
app.include_router(excel_router, prefix="/api/excel", tags=["excel"])
```

#### scraper.py - 抓取 API
```python
from app.api.scraper import router as scraper_router
app.include_router(scraper_router, prefix="/api/scrape", tags=["scraper"])
```

---

## 完整复用示例

### 示例1: 只使用前端表格组件

```bash
# 1. 复制组件
cp -r frontend/src/components/Spreadsheet your-project/src/components/

# 2. 安装依赖
cd your-project
npm install tailwindcss

# 3. 在你的代码中使用
```

```javascript
import Spreadsheet from './components/Spreadsheet';

export default function DataEditor() {
  const [data, setData] = useState({
    id: 'data-1',
    title: '用户数据',
    headers: ['ID', '姓名', '邮箱'],
    rows: [
      [1, '张三', 'zhang@example.com'],
      [2, '李四', 'li@example.com']
    ]
  });

  return <Spreadsheet data={data} onDataChange={setData} />;
}
```

---

### 示例2: 只使用后端 Excel 导出功能

```bash
# 1. 复制服务文件
cp backend/app/services/excel_service.py your-project/services/

# 2. 安装依赖
pip install openpyxl

# 3. 创建脚本
```

```python
# your-project/export_report.py
from services.excel_service import ExcelService

def export_report(data, filename):
    service = ExcelService()
    service.sync_workbook('temp', data)
    excel_file = service.export_to_excel_with_charts('temp')

    with open(filename, 'wb') as f:
        f.write(excel_file)

# 使用
export_report({
    'title': '月度报表',
    'headers': ['项目', '金额'],
    'rows': [['A', 1000], ['B', 2000]]
}, 'monthly_report.xlsx')
```

---

### 示例3: 在现有 FastAPI 项目中集成抓取功能

```python
# your-fastapi-app/main.py
from fastapi import FastAPI
from services.scraper_service import ScraperService

app = FastAPI()
scraper = ScraperService()

@app.post("/scrape")
async def scrape_url(url: str):
    result = scraper.scrape_table(url)
    return result
```

---

## 依赖总结

### 前端组件复用所需依赖

```json
{
  "dependencies": {
    "react": "^18.0.0",
    "recharts": "^2.0.0",  // 仅 ChartBuilder 需要
    "axios": "^1.0.0",      // 仅 API 调用需要
    "tailwindcss": "^3.0.0" // 样式（可选）
  }
}
```

### 后端服务复用所需依赖

```txt
# requirements.txt
fastapi==0.115.6      # API 框架（可选）
openpyxl==3.1.5       # Excel 服务必需
beautifulsoup4==4.12.3 # 抓取服务必需
requests==2.32.3      # 抓取服务必需
pydantic==2.10.4      # 数据验证（可选）
```

---

## 常见问题

### Q: 前端组件可以用在其他框架吗？
A: 这些组件基于 React，如果想用在 Vue 或 Angular，需要参考组件逻辑重新实现。

### Q: 后端服务可以独立运行吗？
A: 可以，每个服务都是独立的类，可以直接实例化使用，不依赖 FastAPI。

### Q: Excel 支持哪些格式？
A: 使用 openpyxl，支持 `.xlsx` 格式，不支持旧版 `.xls`。

### Q: 抓取服务支持 JavaScript 渲染的页面吗？
A: 不支持，只能抓取静态 HTML。如需动态页面，考虑集成 Selenium 或 Playwright。

---

## 联系与支持

- **项目地址**: https://github.com/CuriosityTomorrow/web-excel-agent
- **问题反馈**: GitHub Issues
- **内部咨询**: [@你的联系方式]

---

## 快速查找

| 需求 | 文件位置 |
|------|----------|
| 前端表格组件 | `frontend/src/components/Spreadsheet/` |
| 前端对话组件 | `frontend/src/components/ChatInterface/` |
| 前端图表组件 | `frontend/src/components/ChartBuilder/` |
| Excel 导出服务 | `backend/app/services/excel_service.py` |
| 网页抓取服务 | `backend/app/services/scraper_service.py` |
| AI 规则引擎 | `backend/app/services/agent_service.py` |

---

**最后更新**: 2026-02-05
**维护者**: [你的名字/团队]
