---
name: blog-format
description: Format and validate blog posts. Fix frontmatter, image paths, and markdown structure.
allowed-tools: Read, Write, Edit, Glob, Bash
---

# Blog: Format Post

Format and validate existing blog posts.

## What This Does

1. **Frontmatter Check**: Verify required fields (title, date, categories, tags)
2. **Image Paths**: Fix paths to use Page Bundle relative paths
3. **Markdown Cleanup**: Remove duplicate titles, fix formatting issues
4. **Structure Validation**: Ensure consistent structure

## Frontmatter Requirements

Required fields:
- `title`: string (quoted if contains special chars)
- `date`: YYYY-MM-DD
- `categories`: list of 1-2 categories
- `tags`: list of 2-4 tags

Optional but recommended:
- `description`: short summary
- `ShowToc`: true/false
- `summary`: alternative to description

## Image Path Correction

Fix these patterns:

| Bad | Good |
|-----|------|
| `![alt](image/1.png)` | `![alt](1.png)` |
| `![alt](/post/251028/image/1.png)` | `![alt](1.png)` |
| `![alt](/posts/251028/image/1.png)` | `![alt](1.png)` |

Keep images in the same folder as `index.md`.

## Common Fixes

1. Remove duplicate H1 titles (keep only frontmatter `title`)
2. Fix LaTeX: use `$$` for math
3. Ensure proper spacing around code blocks
4. Validate mermaid diagrams format
