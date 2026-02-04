# 🚀 3分钟推送到GitHub - 快速指南

## 步骤1：在GitHub创建仓库（2分钟）

1. **打开GitHub创建页面**
   - 访问：https://github.com/new
   - 或登录GitHub后，点击右上角 "+" → "New repository"

2. **填写仓库信息**
   ```
   Repository name: web-excel-agent
   Description: AI驱动的Web Excel应用
   设置: ☑️ Private (私有仓库)
   ```

3. **重要：不要勾选以下选项**
   - ❌ Add a README file
   - ❌ Add .gitignore
   - ❌ Choose a license

4. **点击绿色按钮**："Create repository"

---

## 步骤2：推送代码（1分钟）

创建仓库后，在**终端**执行：

```bash
cd /Users/samdediannao/Web_excel

# 添加远程仓库地址（替换YOUR_USERNAME为你的用户名）
git remote add origin https://github.com/YOUR_USERNAME/web-excel-agent.git

# 推送代码
git push -u origin main
```

如果提示需要认证：
- 用户名：输入你的GitHub用户名
- 密码：**这不是你的GitHub密码！** 需要用Personal Access Token

---

## 🔑 如果需要密码（Personal Access Token）

### 快速生成Token：

1. **访问**：https://github.com/settings/tokens
2. **点击**："Generate new token" → "Generate new token (classic)"
3. **设置**：
   - Note: `Web Excel Agent`
   - Expiration: `90 days`
   - 勾选：`repo` (这个最重要！)
4. **点击**：绿色按钮 "Generate token"
5. **复制**：token（只显示一次，格式：`ghp_xxxxxxxxxxxxxxxx`）

### 使用Token推送：

在终端推送时：
- 用户名：`Sylsylgo310!`
- 密码：粘贴刚才复制的token（不是GitHub密码）

---

## ✅ 验证推送成功

推送成功后，访问：
```
https://github.com/YOUR_USERNAME/web-excel-agent
```

你应该能看到所有代码文件！

---

## 🏢 在公司使用

推送成功后，在公司电脑上：

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/web-excel-agent.git
cd web-excel-agent

# 后端
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# 前端（新终端）
cd ../frontend
npm install
npm run dev
```

访问：http://localhost:3000

---

## 💡 常见问题

### Q: 推送时提示"认证失败"
**A**: 不要使用GitHub密码，必须用Personal Access Token

### Q: 找不到仓库地址
**A**: 创建仓库后，GitHub会显示地址，类似：
`https://github.com/用户名/web-excel-agent.git`

### Q: 推送太慢
**A**: 第一次推送可能较慢，包含所有依赖文件。后续推送很快。

---

## 📞 需要帮助？

如果遇到问题，告诉我具体的错误信息，我会帮你解决！
