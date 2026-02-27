# zjding's Blog

基于 Hugo + PaperMod 主题的技术博客。

## 快速开始

### 写博客

使用 Claude Code Skills 工作流：

1. **创建新文章**
   ```
   /blog-new "My Article Title"
   ```

2. **格式化/验证文章**
   ```
   /blog-format 251028
   ```

### 本地预览

```bash
hugo server -D
```

访问 http://localhost:1313

### 发布

```bash
git add .
git commit -m "post: add new article"
git push
```

GitHub Actions 会自动部署到 GitHub Pages。

## 目录结构

```
content/posts/
├── 251028/              # 日期文件夹 (YYMMDD)
│   ├── index.md         # 主文章
│   ├── 1.png            # 图片（与 md 同级）
│   └── diagram.png
└── 251123/
    └── index.md
```

## 写作规范

### Frontmatter

```markdown
---
title: "文章标题"
date: 2025-10-28
categories:
  - 云计算
  - 后端架构
tags:
  - Upstash
  - QStash
  - Workflow
---
```

### 图片路径

使用 **相对路径**（Page Bundle 模式）：

```markdown
![图片描述](1.png)
![架构图](diagram.png)
```

### 数学公式

使用 `$$` 包裹 LaTeX 公式：

```markdown
$$y(t) = g(t) + s(t) + h(t) + \epsilon_t$$
```

## Skills 说明

| Skill | 用途 |
|-------|------|
| `/blog-new` | 创建新文章 |
| `/blog-format` | 格式化/验证现有文章 |
| `/technical-writing` | 技术写作辅助（可选） |
