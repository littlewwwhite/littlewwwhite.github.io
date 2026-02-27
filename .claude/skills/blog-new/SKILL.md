---
name: blog-new
description: Create a new blog post with proper structure. Use when starting a new article via conversation.
allowed-tools: Read, Write, Edit, Glob, Bash
---

# Blog: New Post

Create a new blog post with Hugo Page Bundle structure, optimized for conversation-style writing.

## Quick Start

Create a new post with this structure:

```
content/posts/YYMMDD/
├── index.md
└── (images go here, same level as index.md)
```

## Conversation Workflow

This skill is designed for writing via conversation with Claude:

1. User says: "I want to write about X"
2. Create the structure
3. Help the user write the content through conversation
4. Write the final content to file
5. (Optional) Use `/blog-format` to validate

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

## Image Paths

Use **relative paths** with Page Bundle:

```markdown
![Description](1.png)
![Architecture](diagram.png)
```

No leading slash, no `image/` subfolder.

## Git as "Draft vs Published"

- Use git history to distinguish versions
- No need for separate draft/published folders
- Commit frequently as you write
- Push when ready to publish
