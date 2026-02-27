---
name: blog-generate
description: Generate complete blog posts from raw ideas, notes, and reference materials. User provides direction, Claude handles everything else.
allowed-tools: Read, Write, Edit, Glob, Bash
---

# Blog: Generate

Generate a complete blog post from user's raw ideas, notes, and reference materials. The user provides direction and素材; Claude handles the rest, including Hugo formatting.

## Workflow

1. **User provides**:
   - Raw ideas and thoughts
   - Reference articles/blogs they like
   - Direction and requirements
   - Optional: notes, outlines, snippets

2. **Claude does**:
   - Understand and synthesize the material
   - Generate content in user's voice
   - Organize into proper structure
   - Add Hugo frontmatter automatically
   - Handle image paths correctly
   - Create proper Page Bundle structure

3. **Result**:
   - A complete, ready-to-publish blog post
   - Correct Hugo format
   - No manual formatting needed

## User's Voice Guidelines

Write in zjding's voice:
- First person perspective ("I", "my")
- Technical but conversational tone
- Practical, hands-on examples
- Sharing real experience and learnings
- Clear explanations of technical concepts
- Authentic, not overly formal

## Hugo Page Bundle Structure

Generate automatically:

```
content/posts/YYMMDD/
├── index.md         # Complete article with frontmatter
└── (images go here, referenced as ![alt](1.png))
```

## Frontmatter Template (Auto-generated)

```markdown
---
title: "Article Title"
date: YYYY-MM-DD
categories:
  - Category1
  - Category2
tags:
  - Tag1
  - Tag2
  - Tag3
---

Article content here...
```

## Philosophy

- **User focuses on ideas, not format**
- **Claude handles all Hugo details**
- **No manual formatting required**
- **Git handles versioning, no draft/published separation**
- **Images use simple relative paths: ![alt](1.png)**
