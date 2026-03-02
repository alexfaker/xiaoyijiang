# 推送到远端仓库

本地 Git 已初始化并完成首次提交。请按以下步骤推送到远端：

## 1. 创建远端仓库

在您选择的平台上创建**空仓库**（不要初始化 README）：
- **GitHub**: https://github.com/new
- **GitLab**: https://gitlab.com/projects/new
- **Gitee**: https://gitee.com/projects/new

## 2. 添加远端并推送

将下面命令中的 `YOUR_REPO_URL` 替换为您的仓库地址，然后执行：

```bash
cd /Users/yananqi/go/src/github.com/anderson/xiaoyijiang
git remote add origin YOUR_REPO_URL
git push -u origin master
```

### URL 示例

| 平台   | SSH 格式                          | HTTPS 格式                                |
|--------|-----------------------------------|-------------------------------------------|
| GitHub | git@github.com:用户名/xiaoyijiang.git | https://github.com/用户名/xiaoyijiang.git |
| Gitee  | git@gitee.com:用户名/xiaoyijiang.git  | https://gitee.com/用户名/xiaoyijiang.git  |

## 3. 后续提交

日常提交时使用 `git -c commit.template= commit -m "您的提交信息"` 可绕过本地 commit template 问题。
