# Blog Post Examples

## Complete Example Structure

```markdown
---
date: 2025-05-18
categories:
- 支付系统
- 软件开发
tags:
- Stripe
- 订阅计费
- 混合计费
- Webhook
title: Stripe 的接入(独立开发者探索版)
---

## The Problem

So, there I was at 3am when production went down...

## Investigation

I traced the issue through logs and found:

1. First symptom: database locked errors
2. Then: cascading failures
3. Root cause: improper file handling in fs.copyFile

## The Solution

Here's the fix I implemented:

\`\`\`typescript // Before (broken) fs.copyFile(source, dest, (err) =>
{ ... })

// After (working) import { copyFile } from 'fs/promises' await
copyFile(source, dest) \`\`\`

## Results

This prevented 99% of corruption issues. The numbers don't lie.

Want to check the code?
[See the full implementation](https://github.com/spences10/project)
```

## Frontmatter Template

Every post must start with:

```markdown
---
date: YYYY-MM-DD
categories:
- 分类1
- 分类2
- ...
tags:
- 标签1
- 标签2
- ...
title: 文章标题
---
```

**Important:** Always set `published: false` initially. Only change to
`true` when ready for publication.
