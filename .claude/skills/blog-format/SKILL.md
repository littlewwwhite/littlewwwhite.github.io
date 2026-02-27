---
name: blog-format
description: Validate blog post structure and image paths. Prefer minimal changes.
allowed-tools: Read, Write, Edit, Glob, Bash
---

# Blog: Format & Validate

Validate blog posts with minimal changes. Focus on verification rather than modification.

## What This Does

1. **Verify**: Check that frontmatter has required fields
2. **Validate**: Ensure image paths use relative Page Bundle format
3. **Confirm**: No absolute paths, no `image/` subfolder references
4. **Minimal Fix**: Only fix obvious issues, prefer to flag and ask

## Frontmatter Requirements

Required fields:
- `title`: string (quoted if contains special chars)
- `date`: YYYY-MM-DD
- `categories`: list of 1-2 categories
- `tags`: list of 2-4 tags

Optional but recommended:
- `description`: short summary
- `ShowToc`: true/false

## Image Path Validation

**Good** (use these):
```markdown
![alt](1.png)
![description](diagram.png)
```

**Bad** (fix or flag these):
```markdown
![alt](image/1.png)           ❌ no image/ subfolder
![alt](/post/251028/1.png)   ❌ no absolute path
![alt](/posts/251028/1.png)  ❌ no absolute path
```

## Philosophy

- **Prefer verification over modification**
- **Ask before making significant changes**
- **Keep content intact**
- **Git is our safety net**
