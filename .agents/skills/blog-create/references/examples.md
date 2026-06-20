# Blog Post Examples

**Scope**: Format calibration — what Think notes, Spine tables, and finished articles should look like. For deep progression analysis of real articles, see `progression-patterns.md`.

## Example 1: Thesis-Driven Analysis (Pattern C)

A post analyzing infrastructure software design for AI Agents — demonstrates avoiding AI-speak and adding depth:

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

TiDB Cloud 上每天新创建的集群，超过 90% 已经是 AI Agent 直接创建的。这个数字不是假设，是生产环境的真实情况。

面对这个变化，一开始我直觉想的是"给 Agent 设计更强的特化接口"。试了几个月后，我发现方向错了。

## 1. 顺应，而不是教育

我之前的项目里给 Agent 设计了一套 REST API，结果 Agent 调用得非常别扭。后来换成标准 SQL 接口，调用成功率从 60% 跳到了 95%。

这不是巧合——LLM 在预训练时见过大量 SQL，但没见过你的自定义 API。

> Agent 不是在等一个更强大的系统，它更喜欢一个它已经懂的系统。

## 2. 接口设计三条件

我总结了三个让 Agent 用起来顺手的标准：

| 条件 | 含义 | 实例 |
|------|------|------|
| 可被自然语言描述 | 接口语义用一句话能讲清楚 | "查询用户过去30天的订单" |
| 可被符号逻辑固化 | 意图可以冻结为确定的代码/结构 | SELECT...WHERE user_id = $id |
| 交付确定性结果 | 同样输入总产生同样输出 | 不用"随机生成一个ID" |

## 3. 代码是最好的 Meta Tool

我把项目的工具函数从"预定义的 Python 函数"改成"让 Agent 写代码脚本自己执行"后，意外的发现是：能解决的问题类型变多了。

之前 Agent 只能用我提供的工具，遇到我没想到的场景就卡住。现在它能自己写临时的 Python 脚本来处理边缘情况。

这个改动的代价是单次调用的延迟从 200ms 涨到 800ms，但整体任务的完成率从 70% 涨到了 90%。

## 我的三点结论

1. 顺应先验知识比创新更重要。给 Agent 设计软件时，优先复用它已经懂的范式。
2. 虚拟化是 Agent 的前提条件，不是可选的优化项。
3. 当代码的生产成本趋零时，商业模式的定价逻辑都要重构。

Welcome to the machine.
```

### Why this example works:
- Clear thesis in opening paragraph (not "let me explore X")
- Numbered sections with individual sub-theses
- Table for structured comparison
- Blockquote for key insight / aphorism
- "My take" section with original analysis
- Strong closing line

## Example: Progression Spine Output (Step 3)

After confirming the thinking note, Claude outputs a Progression Spine before writing:

```markdown
## 🔗 Progression Spine

Type: 同心圆展开

| # | Section thesis | 升维点 (compared to previous) |
|---|---|---|
| 1 | 0.50 是方差最大的合约 | Starting point: single contract, static estimation precision |
| 2 | 低概率事件，普通模拟看不见 | +Extreme region: from "imprecise" to "invisible to sampling" |
| 3 | 选举夜的实时更新问题 | +Time dimension: from static snapshot to dynamic information flow |
| 4 | 相关合约的隐藏炸弹 | +Inter-contract: from single to portfolio, correlation regime change |
| 5 | 市场为什么有效，即使多数人在猜 | +Participant structure: from mathematical models to social mechanism |
```

### Why this progression spine works:
- **Escalation is visible**: Read the 升维点 column top-to-bottom — it tells a story of expanding scope
- **No parallel sections**: Each section opens a dimension the previous one didn't have
- **Last section is highest altitude**: "social mechanism" is more abstract than "correlation math"
- **Sections cannot be reordered**: You need "static problems" before you can appreciate "dynamic problems"

### Anti-example: Flat progression spine (BAD)

```markdown
## 🔗 Progression Spine

Type: ??? (no clear type — this is the problem)

| # | Section thesis | 升维点 |
|---|---|---|
| 1 | Agent 的好处是速度快 | Starting point |
| 2 | Agent 还能处理多语言 | Another benefit (parallel, not progressive) |
| 3 | Agent 的部署也很方便 | Yet another benefit (still parallel) |
| 4 | Agent 的成本在下降 | A fourth benefit |
```

This is a list of parallel benefits — swapping any two sections changes nothing. It would produce a flat, listy blog post.

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
