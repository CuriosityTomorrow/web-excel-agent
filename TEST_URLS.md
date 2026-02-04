# 测试URL参考文档

## 快速测试命令

### 1. Demo数据（最简单）

```
demo
```

**功能**：立即生成包含6个月销售数据的演示表格

**包含数据**：
- 月份
- 销售额
- 成本
- 利润
- 增长率

---

## 可用的测试网页

### HTML表格测试网站

#### ✅ W3Schools HTML Tables（强烈推荐）

**URL**: `https://www.w3schools.com/html/html_tables.asp`

**测试命令**：
```
帮我抓取 https://www.w3schools.com/html/html_tables.asp 的第一个表格
```

**特点**：
- 简单的静态HTML表格
- 包含Company, Contact, Country列
- 非常适合测试

#### ✅ W3Schools更多表格示例

```
抓取 https://www.w3schools.com/html/html_tables.asp 的第2个表格
```

---

### 维基百科页面

#### ⚠️ 维基百科（可能需要多次尝试）

**URL**: `https://zh.wikipedia.org/wiki/世界人口`

**测试命令**：
```
抓取 https://zh.wikipedia.org/wiki/世界人口 的表格
```

**特点**：
- 包含多个表格
- 数据量大
- 可能有编码问题

**备用方案**：
```
抓取 https://en.wikipedia.org/wiki/List_of_highest-grossing_films
```

---

### 统计数据网站

#### ✅ Statista（如果可访问）

```
抓取 https://www.statista.com 的某个表格
```

#### ✅ Trading Economics

```
抓取 https://tradingeconomics.com 的表格
```

---

### 政府公开数据

#### ✅ 美国人口普查数据

```
抓取 https://www.census.gov 的表格
```

#### ✅ 数据.gov

```
抓取 https://catalog.data.gov 的表格
```

---

## 不支持的网站类型

以下类型的网站**不会工作**：

### ❌ 需要JavaScript渲染的单页应用

```
https://twitter.com         # Twitter/X
https://facebook.com        # Facebook
https://www.react.dev       # React文档
```

### ❌ 需要登录的网站

```
https://github.com/dashboard
https://mail.google.com
```

### ❌ 有反爬虫保护的网站

```
https://www.linkedin.com
https://www.amazon.com
```

### ❌ 动态加载内容的网站

```
https://www.reddit.com      # 内容是动态加载的
```

---

## 推荐的测试顺序

### 第一次测试：使用Demo

```
输入: demo
```

### 第二次测试：简单网页

```
输入: 帮我抓取 https://www.w3schools.com/html/html_tables.asp 的第一个表格
```

### 第三次测试：中文网页

```
输入: 抓取 https://baike.baidu.com 的表格
```

### 第四次测试：失败场景

```
输入: 抓取 https://www.google.com
```
预期会失败，因为Google有反爬虫保护

---

## 测试命令完整列表

| 命令 | 功能 | 示例 |
|------|------|------|
| `demo` | 生成演示数据 | `demo` |
| `演示数据` | 生成演示数据（中文） | `演示数据` |
| `抓取 [URL]` | 抓取网页表格 | `抓取 https://example.com 的表格` |
| `创建柱状图` | 创建柱状图 | `创建柱状图` |
| `创建折线图` | 创建折线图 | `创建折线图` |
| `创建饼图` | 创建饼图 | `创建饼图` |
| `帮助` | 显示帮助信息 | `帮助` |

---

## 实际测试案例

### 案例1：销售数据分析

```
你: demo
AI: 已生成演示数据...

[编辑数据，修改销售额]

你: 创建一个柱状图
AI: 图表功能已准备就绪...

你: 点击"导出Excel"
```

### 案例2：网页数据抓取

```
你: 帮我抓取 https://www.w3schools.com/html/html_tables.asp 的第一个表格
AI: 成功抓取 ... 的表格数据，共 8 行数据

[查看表格]

你: 创建一个饼图
AI: 图表功能已准备就绪...
```

### 案例3：失败处理

```
你: 抓取 https://www.google.com
AI: 抓取失败: Failed to fetch URL...

你: demo
AI: 已生成演示数据...（使用demo作为备选）
```

---

## 抓取失败的常见原因

### 1. 网页需要JavaScript

**症状**：抓取成功但数据为空

**解决**：使用静态网页或demo数据

### 2. 网络问题

**症状**：Timeout或连接错误

**解决**：检查网络连接，或使用demo数据

### 3. 编码问题

**症状**：中文乱码

**解决**：这是已知问题，可以使用demo数据测试

### 4. 网页结构复杂

**症状**：抓取到错误的数据

**解决**：指定不同的表格索引，如"第2个表格"

---

## 最佳实践建议

### 新手推荐流程

1. **第一次**：输入 `demo`
2. **第二次**：尝试导出功能
3. **第三次**：修改数据并创建图表
4. **第四次**：尝试抓取简单网页（W3Schools）
5. **第五次**：探索更多功能

### 开发者测试流程

1. API测试：使用Swagger UI (http://localhost:8000/docs)
2. 功能测试：使用demo数据测试所有功能
3. 集成测试：测试完整工作流
4. 边界测试：测试大数据量、特殊字符等

---

## 如果所有网页都抓取失败

**不要担心！** 使用 `demo` 命令即可完整体验所有功能：

```
✅ 数据生成
✅ 在线编辑
✅ 添加行列
✅ 创建图表
✅ 导出Excel
✅ 数据可视化
```

Demo数据包含了完整的测试场景，无需依赖外部网页。

---

## 需要帮助？

- 查看 `QUICK_TEST.md` - 快速测试指南
- 查看 `TESTING_GUIDE.md` - 完整测试指南
- 访问 http://localhost:8000/docs - API文档
- 在应用中输入 `帮助` - 查看内置帮助

---

**提示：Demo数据是最可靠的测试方式！** 🎯
