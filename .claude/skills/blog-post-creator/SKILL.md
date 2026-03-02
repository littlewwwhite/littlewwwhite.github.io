---
name: blog-post-creator
description: Generate high-quality technical blog posts from raw ideas and reference materials. Thesis-driven, depth-first writing in zjding's voice with automatic Hugo formatting.
allowed-tools: Read, Write, Edit, Glob, Bash, WebFetch, AskUserQuestion
---

# Blog Post Creator

Generate a complete, ready-to-publish blog post from user's raw ideas, notes, and reference materials. User provides direction; Claude handles digestion, thinking, and writing.

## Workflow

### Step 1: Gather — Collect and parse all input

- **URLs**: Fetch content via WebFetch, extract key arguments and data
- **Pasted text**: Organize into structured notes
- **File paths**: Read local files
- **User direction**: Note the angle, scope, and emphasis the user wants

Output: Internal structured notes of all source material.

### Step 2: Think — Structured reflection (MUST output to user)

After reading all material, Claude MUST output a **thinking note** before writing. This is the critical step that prevents "rewrite syndrome."

```markdown
## 📌 Source Key Points
- Article A argues X
- Article B argues Y
- Key data: [specific numbers/benchmarks from sources]

## 🤔 Reflections & Extensions
- [Observation] resonates because... [extend with cross-domain case or analogy]
- Pushing [concept] to its extreme implies...
- An angle none of the sources mention but I find important: ...
- This reminds me of [case from another field]...

## 🎯 My Article Thesis
- Not "sources say X" but "I believe Z"
- Z is supported by digesting sources + my own extensions
- Proposed structure: [Pattern A/B/C from writing guidelines]

## 📎 References for 延伸阅读
- [Title](url)
- [Title](url)
```

**Thinking principles:**
- Default stance is **agreement + extension**, not forced criticism
- Depth comes from "thinking further" — cross-domain analogies, extreme-case reasoning, connecting dots the sources didn't connect
- Only express disagreement when genuinely warranted
- The thesis must be YOUR position, not a summary of sources

**After outputting the thinking note, ask the user:**
> "Here's my thinking. Want to adjust the direction, add your own thoughts, or proceed to writing?"

### Step 3: Thesis — Lock in article structure

Based on confirmed thinking note:
- Finalize the thesis statement (one sentence, directional, opinionated)
- Choose structure pattern (A: Numbered Analysis / B: Problem→Solution / C: Original Thesis)
- Outline sections with sub-theses

### Step 4: Write — Generate the article

Write the full article following these rules:

**Voice Requirements (CRITICAL):**
- Use personal experience tone: "I tried...", "I hit this issue...", "In my project..."
- Avoid AI-speak: no "本质上是", "这让我想到", "泛化", "核心论点", "值得注意的是"
- No filler words like "我认为", "我发现" when stating obvious facts
- Be specific: use real scenarios, not abstract generalizations
- Avoid "等等"、"之类" instead of concrete examples

**Content Depth Requirements (CRITICAL):**
- Every post must be 1200+ characters
- Include personal cases: "I encountered X when..."
- Include actual code/config you've used
- Show failure + fix journey, not just success
- Specific comparisons: "方案 A 用了 3 秒，方案 B 用了 1.2 秒"
- Actionable conclusions, not just "worth thinking"

**Writing Rules:**
- **Zero inline citations** — do not write "according to [source]" or link to sources in the body
- **Weave in source insights naturally** — as if they are your own observations
- **Add original extensions**: cross-domain analogies, cases, frameworks, aphoristic summaries
- **End with `## 延伸阅读`** section listing source URLs

See `writing-guidelines.md` for complete anti-AI-speak word list and depth requirements.

### Step 5: Output — Generate Hugo Page Bundle

```
content/posts/YYMMDD/
├── index.md         # Complete article with frontmatter + 延伸阅读
└── *.png / *.jpg    # Images alongside
```

Auto-generate frontmatter:
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

## Quality Bar

Every post must pass these checks:
- **Length: 1200+ characters** — short posts are incomplete thoughts
- **Has a clear thesis** — not a topic, but a position
- **Personal experience** — "I tried/encountered/hit" not just abstract analysis
- **Specific examples** — real code/config/data, not hypothetical
- **Failure narrative** — what didn't work and why, not just success path
- **Data-driven claims** — benchmarks, comparisons, specific numbers
- **No AI-speak** — avoid 禁用词汇列表 (see writing-guidelines.md)
- **Strong closing** — actionable takeaway or crystallized insight
- **延伸阅读 at the end** — source links for reference

## Voice & Depth Guidelines

See [Writing Guidelines](references/writing-guidelines.md) for:
- Complete anti-AI-speak 禁用词汇列表
- Content depth requirements (1200+ chars, specific cases, failure journey)
- Tone and style patterns

See [Examples](references/examples.md) for reference posts.

## Philosophy

- **User focuses on ideas, Claude handles format**
- **Think before you write** — the thinking note is not optional
- **Depth over breadth** — better to go deep on one thesis than shallow on many
- **The post is yours** — write as if every insight came from your own experience
- **Git handles versioning** — no draft/published separation
