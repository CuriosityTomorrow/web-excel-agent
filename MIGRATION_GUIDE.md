# Excel 功能迁移指南

> **目标**: 将 Web Excel 项目的表格展示/编辑/导出功能迁移到公司现有项目

**创建日期**: 2026-02-05
**适用场景**: 公司项目已有 MCP 网页抓取功能，但缺少在线 Excel 展示和编辑能力

---

## 目录

- [迁移概述](#迁移概述)
- [架构对比](#架构对比)
- [需要迁移的代码清单](#需要迁移的代码清单)
- [前端实现详解](#前端实现详解)
- [后端实现详解](#后端实现详解)
- [Excel 处理逻辑](#excel-处理逻辑)
- [数据流设计](#数据流设计)
- [迁移步骤](#迁移步骤)
- [适配层开发](#适配层开发)
- [测试验证](#测试验证)

---

## 迁移概述

### 现状分析

**公司项目现状**:
- ✅ 使用 React + JS 构建前端
- ✅ 实现了基于 MCP 的自然语言网页数据抓取
- ❌ 直接生成本地 Excel 文件（无法在线预览/编辑）
- ❌ 缺少表格展示组件

**Web Excel 项目能力**:
- ✅ 在线 Excel 表格展示和编辑
- ✅ 单元格编辑、行列添加
- ✅ 后端 Excel 文件生成（包含图表）
- ✅ 前后端分离架构

### 迁移目标

```
现有流程:
用户输入 → MCP 抓取 → 直接生成本地 Excel

改造后流程:
用户输入 → MCP 抓取 → 返回 JSON → 前端展示 → 在线编辑 → 导出 Excel
```

---

## 架构对比

### Web Excel 项目架构

```
┌─────────────────────────────────────────────────────────────┐
│                         前端 (React)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ChatInterface │  │ Spreadsheet  │  │  ChartBuilder    │   │
│  │  AI 对话      │  │  表格编辑     │  │   图表配置       │   │
│  └──────────────┘  └──────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↕ REST API
┌─────────────────────────────────────────────────────────────┐
│                      后端 (FastAPI)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │AgentService  │  │ ExcelService │  │ ScraperService   │   │
│  │  规则引擎     │  │  Excel生成   │  │  网页抓取        │   │
│  └──────────────┘  └──────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 公司项目改造后架构

```
┌─────────────────────────────────────────────────────────────┐
│                    公司项目前端 (React)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ 现有页面      │  │ Spreadsheet  │  │  数据展示区      │   │
│  │ (MCP输入)     │  │  【新增】     │  │  【新增】        │   │
│  └──────────────┘  └──────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↕ REST API
┌─────────────────────────────────────────────────────────────┐
│                    公司项目后端                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ 现有MCP工具   │  │ ExcelService │  │  数据存储        │   │
│  │ 【需改造】     │  │  【新增】     │  │  【需适配】       │   │
│  └──────────────┘  └──────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 需要迁移的代码清单

### 前端部分

| 文件路径 | 功能 | 是否必须 | 说明 |
|---------|------|----------|------|
| `frontend/src/components/Spreadsheet/index.jsx` | 表格主组件 | ✅ 必须 | 核心组件 |
| `frontend/src/components/Spreadsheet/CellEditor.jsx` | 单元格编辑器 | ✅ 必须 | 如有子组件需一起迁移 |
| `frontend/src/components/ChartBuilder/` | 图表配置 | ⚪ 可选 | 按需求迁移 |
| `frontend/src/services/api.js` | API 封装 | ✅ 必须 | 需修改 baseURL |

### 后端部分

| 文件路径 | 功能 | 是否必须 | 说明 |
|---------|------|----------|------|
| `backend/app/services/excel_service.py` | Excel 生成服务 | ✅ 必须 | 核心逻辑 |
| `backend/app/api/excel.py` | Excel API 路由 | ✅ 必须 | 需适配到公司项目 |

### 新增代码

| 文件 | 用途 |
|------|------|
| `src/utils/dataAdapter.js` | 数据格式适配器 |
| `src/services/excelApi.js` | Excel API 调用封装 |

---

## 前端实现详解

### 1. Spreadsheet 核心组件

**文件位置**: `frontend/src/components/Spreadsheet/index.jsx`

**核心功能**:
```javascript
// 1. 数据结构
{
  id: string,           // 工作簿唯一标识
  title: string,        // 表格标题
  headers: string[],    // 列标题数组
  rows: array[][]       // 二维数据数组
}

// 2. 组件接口 (Props)
interface SpreadsheetProps {
  data: WorkbookData;           // 表格数据
  onDataChange: (data) => void; // 数据变更回调
  editable?: boolean;           // 是否可编辑（默认 true）
}

// 3. 核心功能
- 单元格编辑: 双击/点击进入编辑模式
- 添加行: 在表格末尾添加新行
- 添加列: 在表格末尾添加新列
- 实时更新: 编辑后立即更新 state
```

**实现逻辑**:
```javascript
function Spreadsheet({ data, onDataChange }) {
  // 1. 状态管理
  const [editingCell, setEditingCell] = useState(null);
  // { rowIndex, colIndex }

  // 2. 单元格编辑
  const handleCellChange = (rowIndex, colIndex, value) => {
    const newRows = [...data.rows];
    newRows[rowIndex][colIndex] = value;
    onDataChange({
      ...data,
      rows: newRows
    });
  };

  // 3. 添加行
  const handleAddRow = () => {
    const emptyRow = new Array(data.headers.length).fill('');
    onDataChange({
      ...data,
      rows: [...data.rows, emptyRow]
    });
  };

  // 4. 添加列
  const handleAddColumn = () => {
    const newHeaders = [...data.headers, '新列'];
    const newRows = data.rows.map(row => [...row, '']);
    onDataChange({
      ...data,
      headers: newHeaders,
      rows: newRows
    });
  };

  // 5. 渲染
  return (
    <div className="spreadsheet-container">
      <table>
        <thead>
          <tr>
            {data.headers.map((header, i) => (
              <th key={i}>{header}</th>
            ))}
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          {data.rows.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {row.map((cell, colIndex) => (
                <td key={colIndex}>
                  {editingCell?.rowIndex === rowIndex &&
                   editingCell?.colIndex === colIndex ? (
                    <input
                      value={cell}
                      onChange={(e) => handleCellChange(
                        rowIndex,
                        colIndex,
                        e.target.value
                      )}
                      onBlur={() => setEditingCell(null)}
                    />
                  ) : (
                    <span onClick={() => setEditingCell({
                      rowIndex,
                      colIndex
                    })}>
                      {cell}
                    </span>
                  )}
                </td>
              ))}
              <td>
                <button onClick={() => handleDeleteRow(rowIndex)}>
                  删除
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <button onClick={handleAddRow}>+ 添加行</button>
      <button onClick={handleAddColumn}>+ 添加列</button>
    </div>
  );
}
```

**样式依赖**:
```javascript
// 主要使用 TailwindCSS
import 'tailwindcss/tailwind.css';

// 核心样式类名
className="spreadsheet-container"
className="table-auto"
className="border-collapse"
```

---

### 2. 前端数据流

**状态管理流程**:
```
用户操作
  ↓
onDataChange(newData)
  ↓
父组件更新 state
  ↓
props.data 变化
  ↓
Spreadsheet 重新渲染
```

**导出流程**:
```
用户点击"导出"
  ↓
调用 exportExcel(data)
  ↓
① PUT /api/excel/{id}/sync
  同步最新数据到后端
  ↓
② POST /api/excel/{id}/charts/batch
  发送图表配置（如有）
  ↓
③ GET /api/excel/export/{id}
  获取 Excel 二进制文件
  ↓
创建 Blob 对象
  ↓
触发浏览器下载
```

**API 调用封装**:
```javascript
// frontend/src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 导出功能
export const exportExcel = async (workbookId) => {
  try {
    const response = await api.get(`/excel/export/${workbookId}`, {
      responseType: 'blob'  // 重要：接收二进制数据
    });

    // 创建下载链接
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `workbook-${workbookId}.xlsx`);
    document.body.appendChild(link);
    link.click();

    // 清理
    link.remove();
    window.URL.revokeObjectURL(url);

    return { success: true };
  } catch (error) {
    console.error('导出失败:', error);
    return { success: false, error: error.message };
  }
};

export default api;
```

---

## 后端实现详解

### 1. ExcelService 核心类

**文件位置**: `backend/app/services/excel_service.py`

**使用的包**:
```python
# requirements.txt
openpyxl==3.1.5        # Excel 文件操作
# 从 openpyxl 导入
from openpyxl import Workbook, load_workbook
from openpyxl.chart import BarChart, LineChart, PieChart, Reference
from openpyxl.styles import Font, Alignment, PatternFill
```

**类结构**:
```python
class ExcelService:
    """Excel 操作服务类"""

    def __init__(self):
        # 内存存储（生产环境建议改为数据库/缓存）
        self.workbooks = {}   # {workbook_id: workbook_data}
        self.charts = {}      # {workbook_id: [chart_configs]}

    # ========== 数据同步 ==========

    def sync_workbook(self, workbook_id: str, workbook_data: dict):
        """
        同步前端数据到后端

        Args:
            workbook_id: 工作簿 ID
            workbook_data: 工作簿数据
                {
                    "title": str,
                    "headers": List[str],
                    "rows": List[List[Any]]
                }
        """
        self.workbooks[workbook_id] = workbook_data
        return {"success": True, "workbook_id": workbook_id}

    def set_workbook_charts(self, workbook_id: str, charts: list):
        """
        设置图表配置

        Args:
            workbook_id: 工作簿 ID
            charts: 图表配置列表
                [{
                    "type": "bar|line|pie",
                    "title": str,
                    "dataRange": {
                        "headerIndex": int,
                        "startRow": int,
                        "endRow": int
                    }
                }]
        """
        self.charts[workbook_id] = charts
        return {"success": True, "count": len(charts)}

    # ========== Excel 生成 ==========

    def export_to_excel_with_charts(self, workbook_id: str) -> bytes:
        """
        生成包含图表的 Excel 文件

        Args:
            workbook_id: 工作簿 ID

        Returns:
            bytes: Excel 文件的二进制数据
        """
        # 1. 检查数据是否存在
        if workbook_id not in self.workbooks:
            raise ValueError(f"Workbook {workbook_id} not found")

        workbook_data = self.workbooks[workbook_id]
        charts = self.charts.get(workbook_id, [])

        # 2. 创建工作簿
        wb = Workbook()
        ws = wb.active
        ws.title = workbook_data.get('title', 'Sheet1')

        # 3. 写入标题行
        headers = workbook_data.get('headers', [])
        for col_idx, header in enumerate(headers, start=1):
            cell = ws.cell(row=1, column=col_idx, value=header)
            # 设置样式（可选）
            cell.font = Font(bold=True)
            cell.fill = PatternFill(
                start_color="E6E6FA",
                end_color="E6E6FA",
                fill_type="solid"
            )

        # 4. 写入数据行
        rows = workbook_data.get('rows', [])
        for row_idx, row_data in enumerate(rows, start=2):
            for col_idx, value in enumerate(row_data, start=1):
                ws.cell(row=row_idx, column=col_idx, value=value)

        # 5. 添加图表
        for chart_config in charts:
            self._add_chart_to_worksheet(ws, chart_config, len(rows))

        # 6. 保存到内存字节流
        from io import BytesIO
        output = BytesIO()
        wb.save(output)
        return output.getvalue()

    # ========== 图表生成（私有方法）==========

    def _add_chart_to_worksheet(self, ws, chart_config, data_row_count):
        """
        向工作表添加图表

        Args:
            ws: openpyxl Worksheet 对象
            chart_config: 图表配置
            data_row_count: 数据行数（用于确定数据范围）
        """
        chart_type = chart_config.get('type')
        title = chart_config.get('title', '图表')
        data_range = chart_config.get('dataRange', {})

        if chart_type == 'bar':
            chart = BarChart()
            chart.title = title
            chart.style = 10  # 样式编号

        elif chart_type == 'line':
            chart = LineChart()
            chart.title = title
            chart.style = 11

        elif chart_type == 'pie':
            chart = PieChart()
            chart.title = title

        else:
            return  # 不支持的图表类型

        # 确定数据范围
        header_index = data_range.get('headerIndex', 0)
        start_row = data_range.get('startRow', 0)
        end_row = data_range.get('endRow', data_row_count - 1)

        # openpyxl 使用 1-indexed
        data_start_row = start_row + 2  # +1 for header, +1 for 1-indexed
        data_end_row = end_row + 2

        # 创建数据引用
        # 假设数据在 B 列（第二列）
        data_ref = Reference(
            ws,
            min_col=header_index + 2,  # +1 for 1-indexed, +1 for data column
            min_row=data_start_row,
            max_row=data_end_row
        )

        # 类别引用（通常是第一列）
        cats_ref = Reference(
            ws,
            min_col=1,
            min_row=data_start_row,
            max_row=data_end_row
        )

        chart.add_data(data_ref, titles_from_data=True)
        chart.set_categories(cats_ref)

        # 将图表添加到工作表
        ws.add_chart(chart, f"{data_end_row + 2}")  # 放在数据下方
```

**使用示例**:
```python
# 初始化服务
excel_service = ExcelService()

# 1. 同步数据
workbook_data = {
    'title': '销售报表',
    'headers': ['产品', '一月', '二月', '三月'],
    'rows': [
        ['产品A', 100, 200, 300],
        ['产品B', 150, 250, 350],
        ['产品C', 200, 300, 400]
    ]
}
excel_service.sync_workbook('report-1', workbook_data)

# 2. 设置图表（可选）
charts = [{
    'type': 'bar',
    'title': '销售趋势',
    'dataRange': {
        'headerIndex': 1,  # 使用"一月"列
        'startRow': 0,
        'endRow': 2
    }
}]
excel_service.set_workbook_charts('report-1', charts)

# 3. 导出
excel_file = excel_service.export_to_excel_with_charts('report-1')

# 4. 保存到文件
with open('report.xlsx', 'wb') as f:
    f.write(excel_file)
```

---

### 2. API 路由实现

**文件位置**: `backend/app/api/excel.py`

**完整实现**:
```python
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from typing import List, Any, Optional
from services.excel_service import ExcelService

router = APIRouter(prefix="/api/excel", tags=["excel"])
excel_service = ExcelService()

# ========== 数据模型 ==========

class WorkbookData(BaseModel):
    """工作簿数据模型"""
    id: str
    title: str
    headers: List[str]
    rows: List[List[Any]]

class ChartConfig(BaseModel):
    """图表配置模型"""
    type: str  # 'bar', 'line', 'pie'
    title: str
    dataRange: dict

# ========== API 端点 ==========

@router.put("/{workbook_id}/sync")
async def sync_workbook(workbook_id: str, data: WorkbookData):
    """
    同步工作簿数据到后端

    前端在导出前调用此 API，确保后端有最新数据
    """
    try:
        result = excel_service.sync_workbook(
            workbook_id,
            data.dict()
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{workbook_id}/charts/batch")
async def set_workbook_charts(workbook_id: str, charts: List[ChartConfig]):
    """
    批量设置图表配置

    前端在导出前调用，发送所有图表配置
    """
    try:
        result = excel_service.set_workbook_charts(
            workbook_id,
            [chart.dict() for chart in charts]
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export/{workbook_id}")
async def export_excel(workbook_id: str):
    """
    导出 Excel 文件

    返回包含图表的 Excel 文件（二进制流）
    """
    try:
        # 生成 Excel 文件
        excel_file = excel_service.export_to_excel_with_charts(workbook_id)

        # 返回文件流
        return Response(
            content=excel_file,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f"attachment; filename=workbook-{workbook_id}.xlsx"
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/workbook")
async def create_workbook(data: WorkbookData):
    """
    创建新工作簿（可选）
    """
    try:
        result = excel_service.sync_workbook(data.id, data.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/workbook/{workbook_id}")
async def get_workbook(workbook_id: str):
    """
    获取工作簿数据（可选，用于数据恢复）
    """
    if workbook_id not in excel_service.workbooks:
        raise HTTPException(status_code=404, detail="Workbook not found")

    return excel_service.workbooks[workbook_id]
```

---

## Excel 处理逻辑

### 使用的 Python 包

| 包名 | 版本 | 用途 |
|------|------|------|
| **openpyxl** | 3.1.5 | 核心 Excel 文件操作 |
| openpyxl.chart | - | 图表生成（BarChart, LineChart, PieChart） |
| openpyxl.styles | - | 单元格样式（字体、颜色、对齐） |

### 安装依赖

```bash
pip install openpyxl==3.1.5
```

### 代码逻辑位置

```
公司项目后端/
├── services/
│   └── excel_service.py          【新增】Excel 核心逻辑
│       ├── ExcelService 类
│       ├── sync_workbook()       # 数据同步
│       ├── set_workbook_charts() # 图表设置
│       ├── export_to_excel_with_charts()  # 导出核心方法
│       └── _add_chart_to_worksheet()      # 图表生成（私有）
│
├── api/
│   └── excel.py                  【新增】API 路由
│       ├── PUT /{id}/sync        # 同步数据
│       ├── POST /{id}/charts/batch  # 设置图表
│       └── GET /export/{id}      # 导出文件
│
└── main.py                       【修改】注册路由
    app.include_router(excel_router)
```

### Excel 处理流程

```
1. 数据同步阶段
   前端发送 JSON → 后端存储在内存/缓存

2. 图表配置阶段
   前端发送图表配置 → 后端存储

3. 导出生成阶段
   ├── 创建 Workbook 对象
   ├── 获取活动工作表
   ├── 写入标题行（带样式）
   ├── 写入数据行
   ├── 遍历图表配置
   │   ├── 根据类型创建图表对象
   │   ├── 设置数据范围
   │   ├── 添加到工作表
   └── 保存到 BytesIO → 返回字节流
```

---

## 数据流设计

### 完整交互流程

```
┌─────────────────────────────────────────────────────────────┐
│                          用户操作                            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  1. 用户输入自然语言（如："抓取某某网站的销售数据"）          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  2. 公司 MCP 工具处理                                        │
│     ├── 抓取网页数据                                         │
│     ├── 解析结构化数据                                       │
│     └── 返回 JSON 格式数据                                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
        ┌───────────────────┴───────────────────┐
        │  数据格式适配器 (dataAdapter.js)       │
        │  MCP格式 → Spreadsheet格式            │
        └───────────────────┬───────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  3. 前端 Spreadsheet 组件展示                                │
│     ├── 渲染表格                                             │
│     ├── 支持单元格编辑                                       │
│     ├── 支持添加行列                                         │
│     └── state 存储最新数据                                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  4. 用户编辑数据（可选）                                     │
│     ├── 修改单元格值                                         │
│     ├── 添加/删除行列                                        │
│     └── 前端 state 更新                                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  5. 用户点击"导出 Excel"                                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
    ┌───────────────────┬───────────────────┬──────────────┐
    ↓                   ↓                   ↓              ↓
┌─────────┐        ┌─────────┐        ┌─────────┐    ┌──────────┐
│ API ①   │        │ API ②   │        │ API ③   │    │ 浏览器   │
│ PUT     │        │ POST    │        │ GET     │    │ 下载     │
│ /sync   │        │ /charts │        │ /export │    │ 文件     │
└─────────┘        └─────────┘        └─────────┘    └──────────┘
    │                   │                   │              │
    └───────────────────┴───────────────────┴──────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  6. 后端 ExcelService 生成 Excel 文件                        │
│     ├── 从内存获取数据                                       │
│     ├── 创建 Workbook                                        │
│     ├── 写入数据和图表                                       │
│     └── 返回二进制流                                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  7. 浏览器下载 Excel 文件                                    │
└─────────────────────────────────────────────────────────────┘
```

### 数据格式转换

#### MCP 返回格式（假设）
```javascript
{
  "success": true,
  "data": {
    "source": "https://example.com",
    "timestamp": "2026-02-05",
    "columns": ["产品", "价格", "库存"],
    "data": [
      ["产品A", 100, 50],
      ["产品B", 200, 30]
    ]
  }
}
```

#### Spreadsheet 需要的格式
```javascript
{
  "id": "workbook-123456",
  "title": "产品数据",
  "headers": ["产品", "价格", "库存"],
  "rows": [
    ["产品A", 100, 50],
    ["产品B", 200, 30]
  ]
}
```

#### 适配器实现
```javascript
// src/utils/dataAdapter.js
export function adaptMcpToSpreadsheet(mcpResponse, title) {
  const mcpData = mcpResponse.data;

  return {
    id: generateUniqueId(),  // 使用 uuid 或时间戳
    title: title || mcpData.source || '未命名',
    headers: mcpData.columns || mcpData.headers || [],
    rows: mcpData.data || mcpData.rows || []
  };
}

function generateUniqueId() {
  return `wb-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}
```

---

## 迁移步骤

### 阶段一：前端迁移（核心展示）

**步骤 1.1: 复制组件代码**
```bash
# 复制 Spreadsheet 组件
cp -r Web_excel/frontend/src/components/Spreadsheet \
     company-project/src/components/

# 复制 API 服务（作为参考）
cp Web_excel/frontend/src/services/api.js \
     company-project/src/services/excelApi.js
```

**步骤 1.2: 修改 API 配置**
```javascript
// company-project/src/services/excelApi.js
import axios from 'axios';

const excelApi = axios.create({
  baseURL: process.env.REACT_APP_API_URL,  // 使用公司项目配置
  timeout: 30000
});

export default excelApi;
```

**步骤 1.3: 在页面中集成**
```javascript
// company-project/src/pages/DataPage.js
import React, { useState } from 'react';
import Spreadsheet from '../components/Spreadsheet';
import { adaptMcpToSpreadsheet } from '../utils/dataAdapter';
import excelApi from '../services/excelApi';

function DataPage() {
  const [workbook, setWorkbook] = useState(null);

  // 现有 MCP 调用
  const handleMcpScrape = async (input) => {
    const mcpResponse = await mcpService.scrape(input);

    // 转换数据格式
    const spreadsheetData = adaptMcpToSpreadsheet(
      mcpResponse,
      '抓取的数据'
    );

    setWorkbook(spreadsheetData);
  };

  // 数据变更处理
  const handleDataChange = (newData) => {
    setWorkbook(newData);
  };

  // 导出功能
  const handleExport = async () => {
    if (!workbook) return;

    try {
      // 1. 同步数据
      await excelApi.put(`/excel/${workbook.id}/sync`, workbook);

      // 2. 导出
      const response = await excelApi.get(`/excel/export/${workbook.id}`, {
        responseType: 'blob'
      });

      // 3. 触发下载
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${workbook.title}.xlsx`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);

    } catch (error) {
      console.error('导出失败:', error);
      alert('导出失败，请重试');
    }
  };

  return (
    <div className="data-page">
      <h1>数据管理</h1>

      {/* 现有 MCP 输入 */}
      <div className="mcp-input-section">
        <input
          placeholder="输入要抓取的网站或描述..."
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              handleMcpScrape(e.target.value);
            }
          }}
        />
      </div>

      {/* 新增：表格展示 */}
      {workbook && (
        <div className="spreadsheet-section">
          <div className="toolbar">
            <h2>{workbook.title}</h2>
            <button onClick={handleExport}>导出 Excel</button>
          </div>

          <Spreadsheet
            data={workbook}
            onDataChange={handleDataChange}
          />
        </div>
      )}
    </div>
  );
}

export default DataPage;
```

**步骤 1.4: 样式适配**
```javascript
// 如果公司项目不使用 TailwindCSS，需要调整样式

// 方案1: 使用 CSS Modules
import styles from './Spreadsheet.module.css';

<div className={styles.container}>
  <table className={styles.table}>
    {/* ... */}
  </table>
</div>

// 方案2: 使用内联样式
<div style={{ border: '1px solid #ccc', padding: '10px' }}>
  <table style={{ width: '100%', borderCollapse: 'collapse' }}>
    {/* ... */}
  </table>
</div>
```

---

### 阶段二：后端迁移（核心逻辑）

**步骤 2.1: 复制服务代码**
```bash
# 复制 ExcelService
mkdir -p company-project/backend/services
cp Web_excel/backend/app/services/excel_service.py \
     company-project/backend/services/
```

**步骤 2.2: 安装依赖**
```bash
cd company-project/backend
pip install openpyxl==3.1.5
```

**步骤 2.3: 创建 API 路由**
```python
# company-project/backend/api/excel.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from typing import List, Any
from services.excel_service import ExcelService

router = APIRouter(prefix="/api/excel", tags=["excel"])
excel_service = ExcelService()

class WorkbookData(BaseModel):
    id: str
    title: str
    headers: List[str]
    rows: List[List[Any]]

class ChartConfig(BaseModel):
    type: str
    title: str
    dataRange: dict

@router.put("/{workbook_id}/sync")
async def sync_workbook(workbook_id: str, data: WorkbookData):
    """同步工作簿数据"""
    result = excel_service.sync_workbook(workbook_id, data.dict())
    return result

@router.post("/{workbook_id}/charts/batch")
async def set_charts(workbook_id: str, charts: List[ChartConfig]):
    """设置图表配置"""
    result = excel_service.set_workbook_charts(
        workbook_id,
        [chart.dict() for chart in charts]
    )
    return result

@router.get("/export/{workbook_id}")
async def export_excel(workbook_id: str):
    """导出 Excel 文件"""
    try:
        excel_file = excel_service.export_to_excel_with_charts(workbook_id)
        return Response(
            content=excel_file,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f"attachment; filename=workbook-{workbook_id}.xlsx"
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
```

**步骤 2.4: 注册路由**
```python
# company-project/backend/main.py
from fastapi import FastAPI
from api.excel import router as excel_router

app = FastAPI()

# 注册 Excel 路由
app.include_router(excel_router)

# 其他现有路由...
```

---

### 阶段三：数据存储优化（可选）

**问题**: 默认使用内存存储，重启后数据丢失

**方案 1: 使用 Redis 缓存**
```python
import redis

class ExcelService:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)

    def sync_workbook(self, workbook_id: str, workbook_data: dict):
        # 保存到 Redis，设置 1 小时过期
        self.redis.setex(
            f'workbook:{workbook_id}',
            3600,
            json.dumps(workbook_data)
        )

    def export_to_excel_with_charts(self, workbook_id: str):
        # 从 Redis 读取
        data_json = self.redis.get(f'workbook:{workbook_id}')
        if not data_json:
            raise ValueError(f"Workbook {workbook_id} not found")

        workbook_data = json.loads(data_json)
        # ... 继续生成 Excel
```

**方案 2: 使用数据库**
```python
from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Workbook(Base):
    __tablename__ = 'workbooks'

    id = Column(String, primary_key=True)
    title = Column(String)
    data = Column(Text)  # JSON 字符串
    charts = Column(Text)  # JSON 字符串

class ExcelService:
    def __init__(self):
        self.engine = create_engine('sqlite:///excel_data.db')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def sync_workbook(self, workbook_id: str, workbook_data: dict):
        workbook = self.session.query(Workbook).get(workbook_id)
        if workbook:
            workbook.data = json.dumps(workbook_data)
        else:
            workbook = Workbook(
                id=workbook_id,
                title=workbook_data['title'],
                data=json.dumps(workbook_data),
                charts='[]'
            )
            self.session.add(workbook)
        self.session.commit()
```

---

## 适配层开发

### 数据格式适配器

```javascript
// company-project/src/utils/dataAdapter.js

/**
 * 将 MCP 返回的数据转换为 Spreadsheet 格式
 * @param {Object} mcpResponse - MCP 工具返回的原始数据
 * @param {string} defaultTitle - 默认标题
 * @returns {Object} Spreadsheet 格式数据
 */
export function adaptMcpToSpreadsheet(mcpResponse, defaultTitle = '未命名') {
  // 处理不同的 MCP 响应格式
  const data = mcpResponse.data || mcpResponse;

  // 生成唯一 ID
  const id = generateUniqueId();

  // 提取标题
  const title = extractTitle(data, defaultTitle);

  // 提取列标题
  const headers = extractHeaders(data);

  // 提取数据行
  const rows = extractRows(data);

  return {
    id,
    title,
    headers,
    rows
  };
}

/**
 * 生成唯一 ID
 */
function generateUniqueId() {
  return `wb-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * 提取标题
 */
function extractTitle(data, defaultTitle) {
  return data.title ||
         data.name ||
         data.source ||
         data.sheetName ||
         defaultTitle;
}

/**
 * 提取列标题
 */
function extractHeaders(data) {
  // 尝试不同的字段名
  if (data.headers && Array.isArray(data.headers)) {
    return data.headers;
  }

  if (data.columns && Array.isArray(data.columns)) {
    return data.columns;
  }

  if (data.fields && Array.isArray(data.fields)) {
    return data.fields;
  }

  // 如果没有标题，从数据第一行提取
  if (data.rows && data.rows.length > 0) {
    const firstRow = data.rows[0];
    if (Array.isArray(firstRow)) {
      return firstRow.map((_, i) => `列${i + 1}`);
    }
  }

  return [];
}

/**
 * 提取数据行
 */
function extractRows(data) {
  if (data.rows && Array.isArray(data.rows)) {
    return data.rows;
  }

  if (data.data && Array.isArray(data.data)) {
    return data.data;
  }

  if (data.items && Array.isArray(data.items)) {
    return data.items;
  }

  return [];
}

/**
 * 反向转换：Spreadsheet → MCP 格式（如需要）
 */
export function adaptSpreadsheetToMcp(spreadsheetData) {
  return {
    success: true,
    data: {
      title: spreadsheetData.title,
      headers: spreadsheetData.headers,
      rows: spreadsheetData.rows
    }
  };
}
```

### 使用示例

```javascript
import { adaptMcpToSpreadsheet } from '../utils/dataAdapter';

// 在 MCP 回调中使用
const handleMcpResponse = (mcpResponse) => {
  try {
    const spreadsheetData = adaptMcpToSpreadsheet(
      mcpResponse,
      mcpResponse.query || '抓取的数据'
    );

    setWorkbook(spreadsheetData);
    setErrorMessage(null);
  } catch (error) {
    console.error('数据转换失败:', error);
    setErrorMessage('数据格式不支持');
  }
};
```

---

## 测试验证

### 前端测试

```javascript
// tests/Spreadsheet.test.js
import { render, screen, fireEvent } from '@testing-library/react';
import Spreadsheet from '../components/Spreadsheet';

describe('Spreadsheet 组件', () => {
  const mockData = {
    id: 'test-1',
    title: '测试',
    headers: ['A', 'B', 'C'],
    rows: [
      [1, 2, 3],
      [4, 5, 6]
    ]
  };

  test('应该渲染表格', () => {
    render(<Spreadsheet data={mockData} />);
    expect(screen.getByText('A')).toBeInTheDocument();
    expect(screen.getByText('1')).toBeInTheDocument();
  });

  test('应该支持单元格编辑', () => {
    const handleChange = jest.fn();
    render(<Spreadsheet data={mockData} onDataChange={handleChange} />);

    // 双击单元格
    const cell = screen.getByText('1');
    fireEvent.doubleClick(cell);

    // 修改值
    const input = screen.getByRole('textbox');
    fireEvent.change(input, { target: { value: '999' } });
    fireEvent.blur(input);

    expect(handleChange).toHaveBeenCalled();
  });

  test('应该支持添加行', () => {
    const handleChange = jest.fn();
    render(<Spreadsheet data={mockData} onDataChange={handleChange} />);

    const addButton = screen.getByText('+ 添加行');
    fireEvent.click(addButton);

    expect(handleChange).toHaveBeenCalledWith(
      expect.objectContaining({
        rows: expect.arrayContaining([
          expect.arrayContaining([''])
        ])
      })
    );
  });
});
```

### 后端测试

```python
# tests/test_excel_service.py
import pytest
from services.excel_service import ExcelService

def test_sync_workbook():
    service = ExcelService()
    data = {
        'title': '测试',
        'headers': ['A', 'B'],
        'rows': [[1, 2]]
    }

    result = service.sync_workbook('test-1', data)

    assert result['success'] == True
    assert 'test-1' in service.workbooks

def test_export_excel():
    service = ExcelService()
    data = {
        'title': '测试报表',
        'headers': ['产品', '销量'],
        'rows': [['A', 100], ['B', 200]]
    }

    service.sync_workbook('test-2', data)
    excel_file = service.export_to_excel_with_charts('test-2')

    assert isinstance(excel_file, bytes)
    assert len(excel_file) > 0

    # 验证可以保存为文件
    with open('test_output.xlsx', 'wb') as f:
        f.write(excel_file)

def test_export_with_charts():
    service = ExcelService()
    data = {
        'title': '带图表的报表',
        'headers': ['月份', '销售额'],
        'rows': [['一月', 100], ['二月', 200]]
    }

    service.sync_workbook('test-3', data)
    service.set_workbook_charts('test-3', [{
        'type': 'bar',
        'title': '销售趋势',
        'dataRange': {'headerIndex': 1, 'startRow': 0, 'endRow': 1}
    }])

    excel_file = service.export_to_excel_with_charts('test-3')

    assert isinstance(excel_file, bytes)
```

### 集成测试

```bash
# 1. 启动后端
cd company-project/backend
python -m pytest tests/test_excel_service.py -v

# 2. 启动前端
cd company-project/frontend
npm test

# 3. 手动测试流程
# - 打开页面
# - 输入自然语言抓取数据
# - 检查表格是否正确展示
# - 编辑单元格
# - 点击导出
# - 验证 Excel 文件内容
```

---

## 常见问题

### Q1: 前端样式冲突怎么办？

**方案**: 抽离样式为独立文件
```css
/* company-project/src/components/Spreadsheet/Spreadsheet.css */
.spreadsheet-container {
  border: 1px solid #ddd;
  overflow: auto;
}

.spreadsheet-container table {
  border-collapse: collapse;
  width: 100%;
}

.spreadsheet-container th,
.spreadsheet-container td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}
```

### Q2: 后端数据存储选什么？

**推荐**:
- 小规模/临时数据: Redis (1小时过期)
- 需要持久化: SQLite/PostgreSQL
- 分布式部署: Redis Cluster

### Q3: 如何处理大量数据？

**方案**:
```javascript
// 虚拟滚动（前端）
import { FixedSizeList } from 'react-window';

<FixedSizeList
  height={600}
  itemCount={rows.length}
  itemSize={35}
>
  {({ index, style }) => (
    <div style={style}>
      <TableRow data={rows[index]} />
    </div>
  )}
</FixedSizeList>

// 分页加载（后端）
@router.get("/workbook/{workbook_id}")
async def get_workbook(
    workbook_id: str,
    page: int = 1,
    page_size: int = 100
):
    # 分页返回数据
```

### Q4: Excel 文件太大怎么办？

**方案**:
```python
# 使用流式响应
from fastapi.responses import StreamingResponse

async def generate_excel(workbook_id: str):
    # 分块生成
    output = BytesIO()
    # ... 写入数据
    output.seek(0)
    while chunk := output.read(4096):
        yield chunk

@router.get("/export/{workbook_id}")
async def export_excel(workbook_id: str):
    return StreamingResponse(
        generate_excel(workbook_id),
        media_type="application/vnd.openxmlformats..."
    )
```

---

## 文件清单总结

### 前端需要新增/修改的文件

```
company-project/frontend/src/
├── components/
│   └── Spreadsheet/              【新增】
│       ├── index.jsx
│       └── Spreadsheet.css
├── services/
│   └── excelApi.js               【新增】
├── utils/
│   └── dataAdapter.js            【新增】
└── pages/
    └── DataPage.jsx              【修改】集成 Spreadsheet
```

### 后端需要新增/修改的文件

```
company-project/backend/
├── services/
│   └── excel_service.py          【新增】
├── api/
│   └── excel.py                  【新增】
├── main.py                       【修改】注册路由
└── requirements.txt              【修改】添加 openpyxl
```

---

## 依赖安装

### 前端
```bash
cd company-project/frontend
# 如果需要图表功能
npm install recharts

# 如果需要更好的表格体验
npm install react-window
```

### 后端
```bash
cd company-project/backend
pip install openpyxl==3.1.5

# 如果使用 Redis 存储
pip install redis

# 如果使用数据库
pip install sqlalchemy
```

---

## 总结

### 迁移工作量评估

| 任务 | 预计工时 | 难度 |
|------|---------|------|
| 前端组件迁移 | 2-4h | ⭐⭐ |
| 后端服务迁移 | 3-5h | ⭐⭐⭐ |
| 数据适配器开发 | 1-2h | ⭐⭐ |
| 样式适配 | 2-3h | ⭐⭐ |
| 集成测试 | 2-3h | ⭐⭐ |
| **总计** | **10-17h** | **⭐⭐⭐** |

### 关键成功因素

1. ✅ 理解现有 MCP 工具返回的数据格式
2. ✅ 正确实现数据格式适配器
3. ✅ 前后端数据格式对齐
4. ✅ 充分的测试验证

### 后续优化方向

1. 添加数据验证和错误处理
2. 支持更多 Excel 格式（合并单元格、公式等）
3. 优化大数据量性能
4. 添加协作编辑功能（WebSocket）
5. 支持导入现有 Excel 文件

---

**文档维护者**: 开发团队
**最后更新**: 2026-02-05
**版本**: 1.0
