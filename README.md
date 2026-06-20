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

### 发布

```bash
git add .
git commit -m "post: add new article"
git push
```

GitHub Actions 会自动部署到 GitHub Pages。

### 内容分发

```bash
bun run publish:pack
bun run publish:open
```

`publish:pack` 会按 frontmatter date 选择最新文章，生成 `_dist/<slug>/` 发布包和 `aibeike-fill-plan.json`，默认停在同步前。
`publish:open` 会生成发布包和填表计划，然后打开爱贝壳扩展。

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

需要图片底部说明时，使用 Markdown title；Hugo 会渲染为 `<figcaption>`：

```markdown
![语义化图片描述](1.png "图片底部说明")
![架构图](diagram.png "请求进入系统后，先经过网关，再进入任务编排层")
```

约定：

- `[]` 内是 alt text，用于可访问性和图片不可加载时的替代文本。
- `""` 内是 caption，会显示为图片底部说明。
- 需要可见说明的技术图、截图、对比图都应写 caption。

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
