# Blog Post Examples

## Example 1: Thesis-Driven Analysis (Pattern C)

A post analyzing infrastructure software design for AI Agents:

```markdown
---
title: "AI Agent 时代，基础软件该怎么做？"
date: 2026-02-28
categories:
  - AI
  - Infrastructure
tags:
  - AI Agent
  - System Design
  - Database
---

当基础软件的核心用户从人类变成 AI Agent，整个设计范式会发生
什么变化？这不是假设性问题——TiDB Cloud 上每天新创建的集群，
超过 90% 已经是 AI Agent 直接创建的。

## 1. 心智模型：顺应，而不是教育

给 AI Agent 设计的软件，不应该发明全新接口，而应该贴合已经被
训练进模型的认知结构。Agent 不是在等一个更强大的系统，它更喜欢
一个"它已经懂的系统"。

> 如果没有稳定的约束容易失控，但如果抽象是封闭的，
> 又没办法利用效率来演化。这个张力很精妙。

## 2. 接口设计三条件

| 条件 | 含义 |
|------|------|
| 可被自然语言描述 | 接口语义能用一句话讲清楚 |
| 可被符号逻辑固化 | 意图可以冻结为确定的代码/结构 |
| 交付确定性结果 | 同样输入总产生同样输出 |

**代码是最好的 Meta Tool。** 与其给 Agent 堆特化工具，不如让它
直接写代码——认知密度远高于自然语言，且可无限复用。

## 我的思考

1. **"顺应"而不是"教育"** — 反直觉但务实
2. **虚拟化是 Agent Infra 的前提条件**，不是优化项
3. **商业模式变化可能比技术变化更深刻**

Welcome to the machine.
```

### Why this example works:
- Clear thesis in opening paragraph (not "let me explore X")
- Numbered sections with individual sub-theses
- Table for structured comparison
- Blockquote for key insight / aphorism
- "My take" section with original analysis
- Strong closing line

## Example: Think Stage Output

Before writing, Claude outputs a thinking note like this:

```markdown
## 📌 Source Key Points
- 黄东旭的文章核心论点：给 AI 设计的软件应该"复古"而非创新，因为 LLM 的先验知识偏好已有范式
- 关键数据：TiDB Cloud 90%+ 新集群由 Agent 创建
- 接口设计三条件：可自然语言描述、可符号固化、交付确定性结果

## 🤔 Reflections & Extensions
- "熟悉度优先"这个观点说到了点上——这跟生物学里的生态位理论很像，进化中最成功的不是最强壮的物种，而是对已有生态位适应最好的
- 把"代码是最好的 Meta Tool"推到极致：如果 Agent 能自己写工具，那 MCP 这类工具协议的价值不在于工具本身，而在于提供"写工具的脚手架"
- 源材料没提到但我认为重要的：商业模式的断裂可能比技术变化更深刻——当代码生产成本趋零，整个 SaaS 定价逻辑都要重构

## 🎯 My Article Thesis
- 不是"黄东旭说了什么"，而是"我认为给 AI 做软件的核心策略是复古，这背后有三个可迁移的思考框架"
- 结构：Pattern C (Original Thesis Essay)，用三个框架串联

## 📎 References for 延伸阅读
- [AI Agent 时代，基础软件该怎么做？ — 黄东旭](url)
```

### Why this thinking note works:
- Extracts key points without just listing them — identifies the core argument
- Extensions go beyond the source: biology analogy, MCP implication, business model angle
- Thesis is the writer's own position, not a summary
- References tracked for end-of-post 延伸阅读

## Example: 延伸阅读 Section

Every post that draws from external sources ends with:

```markdown
## 延伸阅读

- [AI Agent 时代，基础软件该怎么做？ — 黄东旭](https://example.com/article)
- [The Bitter Lesson — Rich Sutton](http://www.incompleteideas.net/IncIdeas/BitterLesson.html)
```

No inline citations in the body. All opinions presented as the writer's own.

## Example 2: Tool Evaluation (Pattern B)

```markdown
---
title: "Marker: Document Conversion 的实测赢家"
date: 2025-02-21
categories:
  - Technical Tools
tags:
  - Document Conversion
  - PDF Processing
---

项目里需要高效解析输入文本。markitdown 把内容切得太碎，
MinerU 效果也不理想。测试了三个方案后，Marker 在结构化
输出质量上胜出——以下是数据。

| Tool | Structured Output | Speed | Limitation |
|...benchmark data...|

## 我的选择和理由

综合对比后选取了 Marker。不是因为它完美，而是因为...
```

### Why this example works:
- Title states the conclusion ("实测赢家"), not just the topic
- Opens with the problem context, not tool description
- Benchmark table as evidence
- Ends with reasoned recommendation, not "各有千秋"

## Hugo Page Bundle

Files go in `content/posts/YYMMDD/`:
- `index.md` — the article
- `*.png`, `*.jpg` — images referenced as `![alt](filename.png)`

No absolute paths. No `image/` subfolder.
