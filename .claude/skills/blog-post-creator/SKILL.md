---
name: blog-post-creator
description: Create and write blog posts — from quick scaffolding to full thesis-driven articles. Use when user says "write a blog post", "draft a post about", "turn this into a blog", "发博客", "写篇文章", "new post", "新文章", "validate post", "检查格式", or provides URLs/notes for blog content creation. Do NOT use for quick edits or translation.
allowed-tools: Read, Write, Edit, Glob, Bash, WebFetch, AskUserQuestion
---

# Blog Post Creator

Generate a complete, ready-to-publish blog post from user's raw ideas, notes, and reference materials. User provides direction; Claude handles digestion, thinking, and writing.

## Reference Files

| File | Read when | Content |
|------|-----------|---------|
| `references/writing-guidelines.md` | Step 4 — before writing | Voice baseline (Part 1-4), style rules & forbidden patterns (Part 2-3), progression architecture (Part 6) |
| `references/examples.md` | Step 2-3 — format calibration | Think note format, Spine table format, article positive/negative examples |
| `references/progression-patterns.md` | Step 3 — spine design | 5 annotated real-world progression analyses with transition techniques |
| `references/learning-log.md` | Step 4 — latest corrections | Style corrections from zjding's real edits — overrides all other rules |

## Quick Scaffold Mode

When user just wants to create a post skeleton and write conversationally (not a full thesis-driven article):

1. Create Hugo Page Bundle: `content/posts/YYMMDD/index.md`
2. Fill frontmatter template (title, date, categories, tags)
3. Help write through conversation — skip Steps 2-3 (Think + Spine)
4. Run the Quality Bar checks before finishing

**Trigger**: user says "new post", "新文章", "create a post" without providing research material or URLs.

---

## Full Workflow

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

### Step 3: Thesis + Progression Spine — Lock in structure AND narrative arc

Based on confirmed thinking note, complete THREE decisions in order:

**3a. Thesis**: Finalize the thesis statement (one sentence, directional, opinionated).

**3b. Progression Type**: Choose ONE progression type that determines how sections relate to each other. This is NOT optional — a flat list of parallel points is a structural failure.

| Type | Mechanism | When to use | Reference |
|------|-----------|-------------|-----------|
| **同心圆展开** | Each section's conclusion becomes the next section's premise. Inside-out layers. | Survey/analysis of a single big topic | 黄东旭《AI Agent 基础软件》 |
| **认知升级线** | Each section shifts the reader's mental model deeper. | Deep technical content with counter-intuitive insights | Manus《上下文工程》 |
| **失败→发现叙事** | Each section is a "tried X → failed → discovered Y" mini-arc. | Experience reports, tool evaluations, war stories | @trq212《Building Claude Code》 |
| **期望→打碎→重建** | Set up expectation, shatter it, present the fix. | Problem-solving posts, architecture decisions | Anthropic《Long-running Agents》 |

**3c. Progression Spine Table**: Output a section order table. Each row must state HOW this section deepens the reader's understanding compared to the previous one. If the "升维点" is empty or identical to the previous row, the sections are parallel — merge them or reorder.

```markdown
## 🔗 Progression Spine

Type: [chosen type]

| # | Section thesis | 升维点 (compared to previous) |
|---|---|---|
| 1 | [thesis] | Starting point: [what dimension this establishes] |
| 2 | [thesis] | +[new dimension]: from [previous level] to [new level] |
| 3 | [thesis] | +[new dimension]: from [previous level] to [new level] |
| N | [thesis] | +[new dimension]: from [previous level] to [new level] |
```

**Self-check**: Read the "升维点" column top-to-bottom. Does it tell a coherent escalation story? If not, reorder. See `references/progression-patterns.md` for 5 annotated real-world examples.

**3d. Structure Pattern**: Choose the skeleton from `writing-guidelines.md` "Structure Patterns" section:

| Pattern | Fits | Progression logic |
|---------|------|-------------------|
| **A: 同心圆分析** | Survey/review posts | Inside-out: each layer's conclusion → next layer's premise |
| **B: 工程叙事** | Tool/project posts | Failure→discovery: each attempt builds on previous failure |
| **C: 论证升维** | Opinion/analysis posts | Thesis deepening: each evidence expands thesis scope |

**After completing 3a-3d, ask the user:**
> "Here's my thesis, progression type, and section spine. Does the escalation make sense, or should I reorder?"

### Step 4: Write — Generate the article

Read `references/writing-guidelines.md` (full file) and `references/learning-log.md` (latest corrections override all other rules). Then write the full article.

**6 Hard Rules (violation = rewrite):**
1. **First sentence**: concrete fact, number, or counterintuitive claim — never a preamble
2. **Section headers**: thesis statements, not topic labels
3. **No forbidden structures**: no 摘要/总结/结语, no 首先…其次…最后…, no 1.1/1.2 subsections
4. **Transitions mandatory**: every section pair needs explicit connective tissue (see writing-guidelines.md Part 6)
5. **Last section = highest altitude**: most abstract/impactful insight lands last
6. **Content richness**: each section must have enough concrete detail, vivid descriptions, and supporting evidence — never just abstract statements (see Content Richness below)

**Content Richness (anti-terse rule):**
Terse, over-compressed writing is as bad as bloated writing. Each section needs:
- **Vivid detail**: storytelling-level specifics (e.g., "a worker standing next to the steam engine, eyes on the speed, hand on the valve" not just "a worker adjusted the valve")
- **Visual aids where they help**: use mermaid diagrams for architectures, flows, and feedback loops; use tables for structured comparisons. At least 1 diagram or table per post when the content involves systems, processes, or multi-item comparisons.
- **Concrete examples**: specific tool names, code snippets, real numbers, named projects — not "some teams found that..."
- **Section depth**: each section should have 2-4 substantial paragraphs. A section with only 1-2 short paragraphs is under-developed — expand with examples, implications, or vivid analogies.
- **Target length**: 2500-4000 Chinese characters for a typical analysis post. Below 2000 is almost certainly too compressed. Above 5000 risks losing focus.

**Source handling:**
- Zero inline citations — weave source insights as your own observations
- Add original extensions: cross-domain analogies, frameworks, aphoristic summaries
- End with `## 延伸阅读` section listing source URLs

All other voice, style, forbidden-word, depth, and formatting rules: follow `writing-guidelines.md` Parts 1-6.

### Step 4.5: Style Self-Check — Before finalizing

Run these 6 checks against the draft:

1. **Parallel section test**: Read section headers in order — could they be reordered without losing meaning? If yes → parallel, not progressive. Fix.
2. **Transition check**: Does each section's opening reference or build on the previous section's conclusion? No topic jumps.
3. **Last section altitude**: Is the final section the most abstract/impactful? If it's a specific technique → reorder.
4. **First sentence**: Is it a concrete fact or provocative claim? (not "In today's..." or "随着...")
5. **Forbidden patterns**: Any 摘要/总结/结语/综上所述? Any 赋能/闭环/深耕/值得注意的是? → delete
6. **Closing**: Crystallized insight or just stops? (good) vs wrap-up paragraph? → delete wrap-up

### Step 4.7: Content Review — Verify completeness and depth

After writing and style self-check, perform a content review before finalizing. This step catches under-developed sections and missing key points.

**Review checklist (output to user as a table):**

| Check | What to verify | Status |
|-------|---------------|--------|
| **Key points coverage** | Are all major arguments from the Spine table present in the article? List each spine item and whether it was adequately covered. | ✅/❌ |
| **Source data used** | Were the important data points, numbers, and quotes from source material included? List the top 3-5 data points and whether they appear. | ✅/❌ |
| **Diagram/table presence** | Does the article include mermaid diagrams or tables where they would aid understanding? | ✅/❌ |
| **Section depth** | Is any section noticeably thinner than others? Flag under-developed sections. | ✅/❌ |
| **Vivid detail** | Does each section have at least one concrete, story-level detail (not just abstract claims)? | ✅/❌ |

**After outputting the review table, ask the user:**
> "Review complete. [N issues found / All checks passed]. Want me to expand any section, or is this ready to publish?"

If the user confirms, proceed to Step 5. If the user requests changes, revise and re-run Step 4.5 + 4.7.

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
- **Progression**: sections form an escalation arc, not a parallel list — each section deepens the previous one
- **Length**: 2500-4000 Chinese characters for analysis posts (below 2000 = too compressed, above 5000 = losing focus)
- **Thesis**: one directional position, not a topic
- **First sentence**: concrete fact or provocative claim — never a preamble
- **Section headers**: thesis statements, not topic labels
- **Transitions**: explicit connective sentences between every pair of sections
- **No forbidden structures**: no 摘要/总结/结语, no 首先…其次…最后…, no 1.1/1.2 subsections
- **Specific data**: numbers, comparisons, real code — not vague claims
- **Visual aids**: at least 1 mermaid diagram or comparison table when the content involves systems, processes, or multi-item comparisons
- **Section depth**: every section has 2-4 substantial paragraphs with vivid detail — no thin, abstract-only sections
- **Closing**: crystallized insight or stops cleanly — no wrap-up paragraph
- **Image paths**: relative Page Bundle format only (`![alt](1.png)`) — no absolute paths, no `image/` subfolder
- **Frontmatter**: must have title, date, categories (1-2), tags (2-4)
- **延伸阅读** at the end
- **Content review passed**: Step 4.7 review checklist completed — all spine items covered, key source data included, no under-developed sections

### Step 6: Learn — Post-write feedback loop (when user edits)

When zjding manually edits an AI-generated post, this is the most valuable signal for improving future writing.

**Trigger**: User says "我改了" / provides before-after diff / commits a modified version of an AI draft.

**Process**:
1. Read the AI draft (from git history or user-provided text)
2. Read zjding's edited version
3. Run diff analysis — categorize every change:
   - **Structural**: moved/deleted/added sections
   - **Tone**: word substitutions revealing voice preference
   - **Content**: added depth, removed fluff
   - **Mechanical**: formatting, punctuation
4. Extract **reusable rules** (not one-off fixes)
5. Append to `references/learning-log.md` using this format:
   ```
   ### YYYY-MM-DD — Post: {post_slug}
   **Pattern**: {one-line description}
   **Category**: tone | structure | word-choice | depth | formatting
   **Before**: > {AI draft text}
   **After**: > {zjding edit text}
   **Rule**: {reusable rule}
   ```
6. If a pattern appears 2+ times in the log → promote to `writing-guidelines.md` Part 2 or Part 3

**Key principle**: zjding's edits are ground truth. The learning log is the only legitimate source of new writing rules.

## Philosophy

- **User focuses on ideas, Claude handles format**
- **Think before you write** — the thinking note is not optional
- **Depth over breadth** — better to go deep on one thesis than shallow on many
- **The post is yours** — write as if every insight came from your own experience
- **Git handles versioning** — no draft/published separation
