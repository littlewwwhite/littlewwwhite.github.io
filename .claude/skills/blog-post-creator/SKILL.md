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
| `references/writing-guidelines.md` | Step 4 — before writing | Voice baseline (Part 1-4), style rules & forbidden patterns (Part 2-3), progression architecture (Part 6), narrative depth (Part 7) |
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
- **Author presence (Part 7.1)**: identify at least one angle where zjding has personal experience, a similar project, or a strong independent judgment. If none exists, flag it — consider adding a quick experiment or switching the angle.
- **Turning point (Part 7.4)**: identify the most counter-intuitive finding or the moment where the obvious approach fails. This becomes the article's narrative pivot.

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

| # | Section thesis | 升维点 (compared to previous) | 叙事手法 |
|---|---|---|---|
| 1 | [thesis] | Starting point: [what dimension this establishes] | [告诉/展示/转折/深案例] |
| 2 | [thesis] | +[new dimension]: from [previous level] to [new level] | [告诉/展示/转折/深案例] |
| 3 | [thesis] | +[new dimension]: from [previous level] to [new level] | [告诉/展示/转折/深案例] |
| N | [thesis] | +[new dimension]: from [previous level] to [new level] | [告诉/展示/转折/深案例] |

🔄 转折点位置: Section [N] — [一句话描述：什么预期被打破]
👤 作者在场位置: Section [N] — [亲历/类比迁移/判断]
🎯 可执行收尾: [是/否] — [概述 2-3 条动作]
```

**叙事手法标注说明**：
- **告诉**：直接陈述观点 + 解释（默认手法，不应占全文超过 60%）
- **展示**：困惑 → 探索 → 揭示的弧线（核心洞察必须用此手法，见 writing-guidelines.md 7.2）
- **转折**：预期 → 打破 → 新框架（每篇至少一个，见 writing-guidelines.md 7.4）
- **深案例**：一个完整的故事弧线，代替多个浅例子（见 writing-guidelines.md 7.3）

**Self-check**:
- 读"升维点"列：是否构成连贯的递进？
- 读"叙事手法"列：是否全部为"告诉"？→ 至少改一个为"展示"或"转折"
- 转折点和作者在场位置是否已标注？未标注 = 不通过

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

**9 Hard Rules (violation = rewrite):**
1. **Title**: creates curiosity without spoiling the conclusion — use 5 varied sentence patterns, never repeat the same pattern in consecutive posts (see writing-guidelines.md 2.0)
2. **First paragraph**: hook from the toolkit (杀手数据/先破后立/场景投掷/悖论/结果先行) — never a preamble or bare thesis statement (see writing-guidelines.md 2.1)
3. **Section headers**: thesis statements, not topic labels
4. **No forbidden structures**: no 摘要/总结/结语, no 首先…其次…最后…, no 1.1/1.2 subsections
5. **Transitions mandatory**: every section pair needs explicit connective tissue (see writing-guidelines.md Part 6)
6. **Last section = highest altitude**: most abstract/impactful insight lands last
7. **Closing**: must contain the article's core thesis at a higher altitude than the opening — not just stop, but crystallize (see writing-guidelines.md 2.3)
8. **Structural tightness**: every section opening must connect to the previous section (承上 or 启下), every paragraph follows 论断→证据→推论 rhythm (see writing-guidelines.md 6.4)
9. **Content richness**: each section must have enough concrete detail, vivid descriptions, and supporting evidence — never just abstract statements (see Content Richness below)
10. **Narrative depth (Part 7)**: author presence ≥ B level, at least one "show don't tell" moment, at least one turning point with 300+ words, no more than 3 parallel shallow examples in a row (see writing-guidelines.md Part 7)

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

Run these 9 checks against the draft:

1. **Title pattern**: Does the title spoil the conclusion? Is it using the same sentence pattern as the previous post? Check against writing-guidelines.md 2.0.
2. **Opening hook**: Does the first paragraph use a hook from the toolkit (杀手数据/先破后立/场景投掷/悖论/结果先行)? Is it a thesis statement disguised as a hook? (bad)
3. **Parallel section test**: Read section headers in order — could they be reordered without losing meaning? If yes → parallel, not progressive. Fix.
4. **Transition check**: Does each section's opening reference or build on the previous section's conclusion? No topic jumps.
5. **Red thread test**: Read ONLY the first sentence of each section top-to-bottom. Do they form a coherent argument chain? If they read like unrelated observations → restructure.
6. **Last section altitude**: Is the final section the most abstract/impactful? If it's a specific technique → reorder.
7. **Closing thesis**: Does the last paragraph contain a clear core judgment at a higher altitude than the opening hook? Read opening + closing together — do they tell the full story?
8. **Forbidden patterns**: Any 摘要/总结/结语/综上所述? Any 赋能/闭环/深耕/值得注意的是? → delete
9. **Paragraph structure**: Spot-check 3 random paragraphs — does each follow 论断→证据→推论? Flag any that are pure fact-listing or pure assertion without evidence.

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

### Step 4.8: 深入浅出核验 — Narrative Depth Final Gate (MANDATORY)

This is the **final quality gate** before output. It checks the five dimensions that separate a "survey paper" from an engaging article. **All 5 checks must pass. Any failure = revise before proceeding.**

**Output to user as a checklist:**

```markdown
## 🔍 深入浅出核验

| # | 维度 | 检查标准 | 状态 | 具体位置/问题 |
|---|------|---------|------|-------------|
| 1 | **作者在场** | 文中至少有 1 段基于亲身经历、类比迁移或独立判断的内容（≥ B 级，见 Part 7.1）。全文不能只分析别人的工作。 | ✅/❌ | Section X: [引用具体段落] |
| 2 | **展示而非告诉** | 至少 1 个核心洞察通过"困惑→探索→揭示"的弧线呈现，而非直接宣布结论再解释（见 Part 7.2）。 | ✅/❌ | Section X: [洞察是被"发现"还是被"宣布"的] |
| 3 | **深度优于广度** | 同一节内不存在 3 个以上结构相同的平行浅例子。需要多案例时用 1 个深案例 + 一句话概括替代（见 Part 7.3）。 | ✅/❌ | Section X: [标注平行例子数量] |
| 4 | **张力与转折** | 至少 1 个转折点（预期被打破）被充分展开（≥ 300 字），而非一带而过。全文不能从头到尾平铺直叙（见 Part 7.4）。 | ✅/❌ | Section X: [转折点描述 + 字数估计] |
| 5 | **可执行收尾** | 分析/框架类文章：结尾前有"明天就能做"的 2-3 条具体行动。观点/前瞻类文章：结尾有可验证的预测或判断标准（见 Part 7.5）。 | ✅/❌ | [引用具体行动或预测] |
```

**判定规则：**
- 5/5 通过 → 进入 Step 5
- 4/5 通过 → 标注失败项，给出具体修复建议，询问用户是否修复
- ≤ 3/5 通过 → **必须修复**后才能进入 Step 5，不得跳过

**After outputting the checklist, if any checks failed:**
> "深入浅出核验发现 [N] 个问题。建议修复：[具体修改方案]。是否修复后再发布？"

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
- **Title**: curiosity-driven, varied sentence pattern, no conclusion spoiling (writing-guidelines.md 2.0)
- **First paragraph**: hook from the toolkit — never a preamble or bare thesis statement (writing-guidelines.md 2.1)
- **Section headers**: thesis statements, not topic labels
- **Transitions**: explicit connective sentences between every pair of sections
- **No forbidden structures**: no 摘要/总结/结语, no 首先…其次…最后…, no 1.1/1.2 subsections
- **Specific data**: numbers, comparisons, real code — not vague claims
- **Visual aids**: at least 1 mermaid diagram or comparison table when the content involves systems, processes, or multi-item comparisons
- **Section depth**: every section has 2-4 substantial paragraphs with vivid detail — no thin, abstract-only sections
- **Closing**: core thesis at higher altitude than opening, 1-3 sentences — no wrap-up, no "值得关注" (writing-guidelines.md 2.3)
- **Structural tightness**: red thread test passes (first sentences of all sections form coherent chain), paragraphs follow 论断→证据→推论 (writing-guidelines.md 6.4)
- **Image paths**: relative Page Bundle format only (`![alt](1.png)`) — no absolute paths, no `image/` subfolder
- **Frontmatter**: must have title, date, categories (1-2), tags (2-4)
- **延伸阅读** at the end
- **Content review passed**: Step 4.7 review checklist completed — all spine items covered, key source data included, no under-developed sections
- **深入浅出核验 passed**: Step 4.8 checklist completed — author presence ≥ B, at least 1 show-don't-tell moment, no 3+ parallel shallow examples, at least 1 turning point ≥ 300 words, actionable or verifiable closing

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
