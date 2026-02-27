---
name: blog-new
description: Create a new blog post with proper structure. Use when starting a new article.
allowed-tools: Read, Write, Edit, Glob, Bash
---

# Blog: New Post

Create a new blog post with Hugo Page Bundle structure.

## Quick Start

Create a new post with this structure:

```
content/posts/YYMMDD/
├── index.md
└── (images go here)
```

## Frontmatter Template

```markdown
---
title: "Your Post Title"
date: YYYY-MM-DD
categories:
  - Category1
  - Category2
tags:
  - Tag1
  - Tag2
  - Tag3
---

Write your content here...
```

## Workflow

1. Create date folder (YYMMDD format)
2. Create `index.md` with frontmatter
3. Images go in the same folder, use relative paths like `![alt](image.png)`
4. Write content
5. Use `/blog-format` to validate before publishing

## Image Paths

Use **relative paths** with Page Bundle:

```markdown
![Description](1.png)
![Architecture](diagram.png)
```

No leading slash, no `image/` subfolder.
