# Web Excel Agent 测试指南

## 快速测试方法

### 方法1：使用真实网页测试（推荐）

以下是一些包含表格数据的公开网页，可以直接测试：

#### 测试URL列表：

1. **维基百科表格**
   ```
   帮我抓取 https://zh.wikipedia.org/wiki/List_of_highest-grossing_films 的表格数据
   ```

2. **示例数据网站**
   ```
   抓取 https://www.w3schools.com/html/html_tables.asp 的表格
   ```

3. **GitHub示例**
   ```
   抓取 https://github.com (需要先在浏览器查看是否有表格)
   ```

### 方法2：使用内置演示数据

我已创建演示模式，可以直接生成测试数据：

#### 对话输入：

```
演示数据
```
或

```
demo
```

这会自动生成一个包含示例Excel数据的表格。

## 完整测试流程

### Step 1: 启动应用

```bash
# 安装依赖
cd backend && pip install -r requirements.txt
cd ../frontend && npm install

# 启动后端（终端1）
cd backend && uvicorn app.main:app --reload

# 启动前端（终端2）
cd frontend && npm run dev
```

### Step 2: 测试数据抓取

#### 测试用例1：抓取HTML表格

在AI对话框输入：
```
帮我抓取 https://www.w3schools.com/html/html_tables.asp 的第一个表格
```

预期结果：
- AI返回成功消息
- Spreadsheet显示抓取的表格数据
- 可以看到"Company", "Contact", "Country"等列

#### 测试用例2：使用演示数据

在AI对话框输入：
```
demo
```

预期结果：
- 自动生成示例销售数据
- 表格包含月份、销售额、利润等列

### Step 3: 测试编辑功能

1. **修改单元格**
   - 点击任意单元格
   - 输入新值
   - 点击外部确认修改

2. **添加行/列**
   - 点击"+行"按钮添加新行
   - 点击"+列"按钮添加新列
   - 在新单元格中输入数据

3. **验证数据更新**
   - 修改后的数据应立即显示
   - 可以继续编辑其他单元格

### Step 4: 测试导出功能

1. **导出Excel**
   - 点击"导出Excel"按钮
   - 浏览器会下载 `excel_export.xlsx` 文件
   - 用Excel/Microsoft Numbers/WPS打开验证

2. **验证导出内容**
   - 检查所有数据是否正确
   - 检查格式是否保留
   - 检查多个sheet（如果有）

### Step 5: 测试图表功能

首先在表格中输入一些示例数据：

```
月份,销售额,成本
一月,50000,30000
二月,60000,35000
三月,70000,40000
四月,80000,45000
五月,90000,50000
```

然后在AI对话框输入：

```
创建一个柱状图
```

或

```
创建一个折线图
```

预期结果：
- 右侧显示图表区域
- 显示对应类型的图表
- 可以切换不同的图表类型

## 测试检查清单

### 功能测试

- [ ] 启动前端和后端服务
- [ ] AI对话框显示正常
- [ ] 抓取网页表格成功
- [ ] Excel数据正确显示
- [ ] 单元格可以编辑
- [ ] 可以添加行和列
- [ ] 导出Excel文件成功
- [ ] 创建图表成功
- [ ] 图表正确显示数据

### 边界测试

- [ ] 空数据情况
- [ ] 大量数据（>100行）
- [ ] 特殊字符（中文、符号）
- [ ] 无效URL处理
- [ ] 网络错误处理

### 性能测试

- [ ] 多次连续操作
- [ ] 大表格渲染性能
- [ ] 导出大文件速度

## 常见问题排查

### 问题1：抓取失败

**可能原因：**
- 网页需要JavaScript渲染（当前版本仅支持静态HTML）
- 网络连接问题
- 网页有反爬虫机制

**解决方法：**
```
使用更简单的静态网页，或输入 "demo" 使用演示数据
```

### 问题2：图表不显示

**可能原因：**
- 数据格式不正确
- 缺少数值列

**解决方法：**
```
确保表格第一行是标题，至少有一列数值数据
```

### 问题3：导出文件损坏

**可能原因：**
- 浏览器兼容性问题

**解决方法：**
```
尝试使用Chrome或Firefox浏览器
```

## 手动创建测试数据模板

### 销售数据模板

直接在表格中输入：

```
产品名称    单价    数量    销售额
iPhone 15   5999    10      =C2*B2
MacBook Pro 12999   5       =C3*B3
iPad Air    4799    8       =C4*B4
AirPods     1299    20      =C5*B5
Apple Watch 2999    15      =C6*B6
```

### 财务数据模板

```
月份    收入    支出    净利润
一月    50000   30000   20000
二月    60000   35000   25000
三月    70000   40000   30000
四月    80000   45000   35000
五月    90000   50000   40000
```

## API测试

### 使用curl测试后端

```bash
# 测试健康检查
curl http://localhost:8000/health

# 测试聊天接口
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "demo"}'

# 测试抓取接口
curl -X POST http://localhost:8000/api/scrape/table \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.w3schools.com/html/html_tables.asp", "table_index": 0}'
```

### 使用Swagger UI测试

访问：http://localhost:8000/docs

- 可以直接在浏览器中测试所有API
- 查看请求/响应格式
- 调试接口问题

## 下一步扩展

完成基础测试后，你可以：

1. **集成真实LLM**
   - 替换 `agent_service.py` 中的规则引擎
   - 调用OpenAI/Claude API

2. **添加更多MCP工具**
   - 数据分析工具
   - 数据清洗工具
   - 高级图表工具

3. **创建自定义Skill**
   - 在 `skills/` 目录添加新配置
   - 定义特定场景的工作流

4. **优化前端**
   - 添加更多Excel功能（公式、格式化）
   - 改进图表交互
   - 添加数据验证
