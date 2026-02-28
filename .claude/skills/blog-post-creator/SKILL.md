---
name: blog-post-creator
description: Generate high-quality technical blog posts from raw ideas and reference materials. Thesis-driven, depth-first writing in zjding's voice with automatic Hugo formatting.
allowed-tools: Read, Write, Edit, Glob, Bash, WebFetch
---

# Blog Post Creator

Generate a complete, ready-to-publish blog post from user's raw ideas, notes, and reference materials. User provides direction; Claude handles content, structure, and Hugo formatting.

## Workflow

1. **User provides** any combination of:
   - Raw ideas, thoughts, observations
   - Reference articles, blogs, or URLs
   - Direction, topic scope, and requirements
   - Notes, outlines, code snippets

2. **Claude does**:
   - Synthesize material into an **original thesis** (not just summarize)
   - Generate content in zjding's voice with intellectual depth
   - Add original analysis, frameworks, and cross-domain analogies
   - Auto-generate Hugo frontmatter and Page Bundle structure

3. **Result**: A complete `index.md` under `content/posts/YYMMDD/`, ready for `git push`.

## Quality Bar

Every post must pass these checks:
- **Has a clear thesis** — not a topic, but a position
- **Adds original insight** — not just rephrasing the source material
- **Contains at least one conceptual framework or memorable formulation**
- **Data supports claims** — benchmarks, comparisons, specific numbers
- **Strong closing** — actionable takeaway or crystallized insight

## Hugo Page Bundle Structure

```
content/posts/YYMMDD/
├── index.md         # Complete article with frontmatter
└── *.png / *.jpg    # Images alongside, referenced as ![alt](1.png)
```

## Frontmatter (Auto-generated)

```yaml
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
```

## Voice & Depth Guidelines

See [Writing Guidelines](references/writing-guidelines.md) for the full style guide.

Key principles:
- **Thesis-driven** — Lead with a position, not a topic
- **First person Chinese, strong opinions with evidence**
- **Zero preamble** — Jump straight into substance
- **Create frameworks** — Don't just describe, frame. Build mental models readers can reuse
- **Aphoristic summaries** — Crystallize complex ideas into one-liners
- **Cross-domain analogies** — Borrow from physics, biology, economics, history
- **Synthesize, don't summarize** — Add your own analysis on top of source material

See [Examples](references/examples.md) for reference posts.

## Philosophy

- **User focuses on ideas, Claude handles format**
- **Depth over breadth** — Better to go deep on one thesis than shallow on many topics
- **Git handles versioning** — no draft/published separation
- **Reference `technical-writing` skill** for editing checklist
