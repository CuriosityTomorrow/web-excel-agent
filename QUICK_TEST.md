# 快速测试指南

## 最简单的方式：使用Demo数据

### 1. 启动应用

```bash
# 终端1 - 启动后端
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# 终端2 - 启动前端
cd frontend
npm install
npm run dev
```

### 2. 打开浏览器

访问：http://localhost:3000

### 3. 测试Demo数据

在AI对话框中输入：

```
demo
```

或者

```
演示数据
```

**预期结果：**
- ✅ 立即生成一个包含6个月销售数据的表格
- ✅ 表格包含：月份、销售额、成本、利润、增长率
- ✅ 可以看到数据已经填充到Excel编辑器中

### 4. 测试编辑功能

- 点击任意单元格，修改数值
- 点击"+行"添加新行
- 点击"+列"添加新列

### 5. 测试导出功能

点击"导出Excel"按钮，浏览器会下载 `excel_export.xlsx`

---

## 测试真实网页抓取

### 可用的测试URL

以下是一些包含表格的公开网页，可以直接测试：

#### 1. W3Schools HTML表格（推荐）

在对话框输入：
```
帮我抓取 https://www.w3schools.com/html/html_tables.asp 的第一个表格
```

这个网页包含标准的HTML表格，非常适合测试。

#### 2. 使用维基百科

```
抓取 https://zh.wikipedia.org/wiki/世界人口 的表格
```

#### 3. 其他测试网站

```
抓取 https://www.w3schools.com/html/html_tables.asp 的第2个表格
```

### 抓取失败的可能原因

如果抓取失败，可能是：
- ❌ 网页需要JavaScript渲染（如React/Vue应用）
- ❌ 网页有反爬虫保护
- ❌ 网络连接问题
- ❌ URL格式错误

**解决方法：使用 `demo` 命令生成测试数据**

---

## 完整测试流程演示

### Step 1: 生成Demo数据

```
你: demo
AI: 已生成演示数据：包含6个月的销售数据...
```

### Step 2: 编辑数据

```
1. 点击单元格 "一月" 的 "销售额"
2. 修改为 "55000"
3. 点击外部确认修改
```

### Step 3: 创建图表

```
你: 创建一个柱状图
AI: 图表功能已准备就绪...
```

然后在右侧图表区域会显示图表。

### Step 4: 导出文件

```
点击"导出Excel"按钮
```

---

## 测试检查清单

运行以下命令检查所有功能：

```
✅ demo                    # 生成演示数据
✅ 点击单元格编辑          # 测试编辑功能
✅ 点击+行按钮            # 测试添加行
✅ 点击+列按钮            # 测试添加列
✅ 点击导出Excel          # 测试导出功能
✅ 创建柱状图              # 测试图表功能
```

---

## 对话示例

### 示例1：完整工作流

```
你: demo
AI: 已生成演示数据：包含6个月的销售数据...

你: 帮我抓取 https://www.w3schools.com/html/html_tables.asp 的表格
AI: 成功抓取 ... 的表格数据，共 X 行数据

你: 创建一个柱状图
AI: 图表功能已准备就绪...
```

### 示例2：仅使用Demo数据

```
你: demo
AI: 已生成演示数据...

[编辑数据...]

你: 帮助
AI: 我可以帮你：1. 输入"demo"生成演示数据...
```

---

## API测试（可选）

如果你想直接测试后端API：

```bash
# 测试Demo数据生成
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "demo"}'

# 测试网页抓取
curl -X POST http://localhost:8000/api/scrape/table \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.w3schools.com/html/html_tables.asp"}'
```

---

## 常见命令速查

| 命令 | 功能 |
|------|------|
| `demo` | 生成演示数据 |
| `演示数据` | 生成演示数据（中文） |
| `抓取 [URL]` | 抓取网页表格 |
| `创建柱状图` | 创建柱状图 |
| `创建折线图` | 创建折线图 |
| `创建饼图` | 创建饼图 |
| `帮助` | 显示帮助信息 |

---

## 下一步

完成基础测试后，你可以：

1. ✅ **集成真实LLM** - 替换 `agent_service.py` 中的规则引擎
2. ✅ **添加更多功能** - 在 `mcp_tools/` 中添加新工具
3. ✅ **创建自定义Skill** - 在 `skills/` 目录定义新工作流
4. ✅ **优化前端** - 添加更多Excel功能

---

## 问题排查

### Demo数据不显示？

检查：
```bash
# 后端是否运行？
curl http://localhost:8000/health

# 前端是否运行？
打开 http://localhost:3000
```

### 抓取失败？

使用 `demo` 命令代替，或者尝试更简单的静态网页。

### 图表不显示？

确保表格中有数值列（不是纯文本）。

---

**开始测试：输入 `demo` 即可！** 🚀
