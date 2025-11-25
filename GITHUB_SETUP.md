# GitHub 上传指南 / GitHub Upload Guide

## 已完成 / Completed

✅ Git 仓库已初始化
✅ 所有代码文件已提交到本地仓库
✅ .gitignore 已配置（排除 node_modules, .env 等）

## 下一步：上传到 GitHub / Next Steps: Upload to GitHub

### 1. 在 GitHub 上创建新仓库 / Create New Repository on GitHub

1. 访问 https://github.com/new
2. 仓库名称: `SuperQuantLab2.0` (或你喜欢的名称)
3. 描述: "Crypto Quant Trading Engine & Research Platform"
4. 选择 **Public** 或 **Private**
5. **不要**勾选 "Initialize this repository with a README" (因为我们已经有代码)
6. 点击 "Create repository"

### 2. 连接本地仓库到 GitHub / Connect Local Repository to GitHub

复制 GitHub 提供的命令，或者使用以下命令（替换 `YOUR_USERNAME` 和 `YOUR_REPO_NAME`）：

```bash
# 添加远程仓库 / Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 或者使用 SSH (如果配置了 SSH key)
git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git

# 查看远程仓库配置 / Check remote configuration
git remote -v
```

### 3. 推送代码到 GitHub / Push Code to GitHub

```bash
# 推送到主分支 / Push to main branch
git branch -M main
git push -u origin main
```

### 4. 验证 / Verify

访问你的 GitHub 仓库页面，应该能看到所有文件已上传。

## 重要文件说明 / Important Files

以下文件**不会**被上传（已在 .gitignore 中）：
- `node_modules/` - Node.js 依赖
- `.env` 文件 - 环境变量（包含敏感信息）
- `__pycache__/` - Python 缓存
- `*.csv` 数据文件 - 数据文件（但保留了 .gitkeep）

## 后续更新 / Future Updates

当你修改代码后，使用以下命令更新 GitHub：

```bash
# 查看更改 / Check changes
git status

# 添加更改 / Add changes
git add .

# 提交更改 / Commit changes
git commit -m "描述你的更改"

# 推送到 GitHub / Push to GitHub
git push
```

## 分支管理 / Branch Management

如果需要创建新分支：

```bash
# 创建并切换到新分支 / Create and switch to new branch
git checkout -b feature/new-feature

# 推送新分支 / Push new branch
git push -u origin feature/new-feature
```

## 许可证 / License

如果你想添加许可证文件，可以在 GitHub 仓库页面添加，或创建 LICENSE 文件。

## 问题排查 / Troubleshooting

### 如果推送失败

1. **认证问题**: 确保已配置 GitHub 认证（Personal Access Token 或 SSH key）
2. **权限问题**: 确保你对仓库有写入权限
3. **网络问题**: 检查网络连接

### 配置 GitHub 认证

**使用 Personal Access Token**:
1. GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)
2. 生成新 token，勾选 `repo` 权限
3. 使用 token 作为密码

**使用 SSH Key**:
```bash
# 生成 SSH key (如果还没有)
ssh-keygen -t ed25519 -C "your_email@example.com"

# 添加到 ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# 复制公钥并添加到 GitHub
cat ~/.ssh/id_ed25519.pub
# 然后添加到 GitHub Settings > SSH and GPG keys
```

