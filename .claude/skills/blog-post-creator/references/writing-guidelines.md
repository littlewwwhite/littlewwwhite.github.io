# zjding's Blog Writing Guidelines

Style guide for writing high-quality technical blog posts. Inspired by Karpathy's clarity and depth, adapted for zjding's voice.

## Core Philosophy: Thesis-Driven Writing

Every post must have a **clear, directional thesis** — not a topic, but a position.

**Bad**: "Let's explore Cloudflare Tunnel"
**Good**: "Cloudflare Tunnel is the most cost-effective way to expose local services — here's why and how"

**Bad**: "An overview of document conversion tools"
**Good**: "After testing markitdown, MinerU, and Marker, Marker wins on structured output quality — here's the data"

The thesis goes in the opening paragraph. Everything else serves it.

## Voice: zjding's Register

- **First person Chinese** — "I found...", "my project needed..."
- **Peer-to-peer tone** — Talking to a fellow senior engineer, not lecturing students
- **Strong opinions, with evidence** — Take a position. "I think X got this wrong because..." is better than "X and Y each have pros and cons"
- **Honest about unknowns** — "I haven't fully validated this yet" beats false confidence
- **Zero preamble** — No "In today's rapidly evolving AI landscape". Jump straight in.

## Anti-AI-Speak Rules

**禁止词汇**（这些词让文章读起来像 AI 写的，必须避免）：
- "核心论点"、"关键洞察"、"本质上是"、"这让我想到"、"这让我联想到"
- "我的判断是"、"我认为"、"我发现"——如果是表达明显事实，不需要这些引入词
- "泛化"、"本质上"、"本质上说"——直接说是什么
- "一个有趣的现象/发现"、"有意思的是"——直接描述现象
- "值得注意的是"、"值得注意的是"——直接说重点
- "事实上"、"实际上"——直接陈述
- "可以泛化"、"可以类比"——直接做类比，不说"可以"
- "这个洞察可以泛化"——直接延伸说明

**替代写法**：
- ❌ "这让我想到更广泛的原则：..." → ✅ "这个原则不限于这一场景..."
- ❌ "本质上是一个流程问题" → ✅ "这是流程问题"
- ❌ "一个有趣的发现是" → ✅ "我发现"
- ❌ "值得注意的是" → ✅ 另起一段，直接说内容
- ❌ "可以泛化到" → ✅ "同样的逻辑也适用于"

**语气要求**：
- 用"我做过了"、"我试过"、"我遇到过的"，而不是"这让我想到"
- 用具体场景描述代替抽象概括
- 用"比如"、"像...那样"直接举例，而不是"例如"这类学术词汇
- 避免"综上所述"、"总而言之"——最后一个观点直接说，不需要总结词

## Content Depth Requirements

每篇博客**必须包含**以下元素（至少 1200 字）：

1. **具体个人案例** — "上周我遇到一个 bug..."、"我在项目 X 里试过..."
2. **实际代码片段或配置** — 不是伪代码，是你真实用过的
3. **失败经历** — "一开始我以为...但行不通，因为..."
4. **对比数据** — "方案 A 用了 3 秒，方案 B 用了 1.2 秒"
5. **可执行的结论** — 不是"值得思考"，而是"如果你遇到类似情况，建议..."

**禁止写法**：
- ❌ 只有抽象概念，没有具体例子
- ❌ 列举而不展开——每个要点至少 150 字
- ❌ 用"等等"、"之类"代替具体例子
- ❌ 用"更强大"、"更高效"这类模糊形容词——用具体数字或对比

## Intellectual Depth Techniques

### 1. Create Conceptual Frameworks
Don't just describe — **frame**. Build mental models that readers can apply elsewhere.

**Example** (Karpathy): "Software 1.0 easily automates what you can specify. Software 2.0 easily automates what you can verify."

**Example** (zjding style): "RAG systems have two failure modes: retrieval failure (didn't find it) and synthesis failure (found it, mangled it). Most teams only measure the second."

### 2. Aphoristic Summaries
Crystallize complex ideas into one-liners. Place them at section ends or as blockquotes.

**Examples**:
- "自然语言负责探索空间，符号负责收敛空间"
- "Agent 不是在等一个更强大的系统，而是更喜欢一个它已经懂的系统"
- "代码的生产成本趋零时，价值分配方式会彻底重构"

### 3. Cross-Domain Analogies
Borrow from physics, biology, economics, history to illuminate technical points. Makes writing feel intellectually richer.

**Example**: Technology diffusion patterns (government → corporation → individual) inverted by LLMs.

### 4. Surprising Juxtapositions
Highlight paradoxes and tensions. Readers remember contradictions.

**Example**: "LLMs are simultaneously a genius polymath and a confused grade schooler, seconds away from getting tricked by a jailbreak."

### 5. Data Before Claims
Every assertion should have supporting evidence — benchmarks, numbers, comparisons, personal test results.

## Structure Patterns

### Pattern A: Numbered Paradigm Analysis (for survey/review posts)
```
Opening: Clear thesis + why this matters now
1. Concept Name — thesis for this section
2. Concept Name — thesis for this section
...
N. Concept Name — thesis for this section
TLDR / My Take: Synthesis and actionable conclusion
```

### Pattern B: Problem → Investigation → Solution (for tool/project posts)
```
Opening: The problem I hit + what I tried
Investigation: Options evaluated, data collected
Solution: What I chose + working examples
Takeaway: One-liner crystallization
```

### Pattern C: Original Thesis Essay (for opinion/analysis posts)
```
Opening: Provocative thesis statement
Evidence 1-3: Supporting arguments with data
Counter-argument: Strongest objection, addressed honestly
Conclusion: Refined thesis + implications
```

## Formatting

- **Tables** for feature comparisons and benchmarks
- **Code blocks** with language identifiers
- **Mermaid diagrams** for architecture and flow
- **Blockquotes** for key insights / aphorisms
- **Bold** for emphasis, short paragraphs (2-3 sentences max)
- **Numbered sections** for multi-part analysis

## Language Rules

- **Prose**: Simplified Chinese
- **Code, identifiers, tool names**: English as-is
- **Comments in code**: English

## Thinking Depth: 感悟 → 延伸 → 原创

The thinking process has three layers. Each layer adds originality:

### Layer 1: 感悟 (Resonance)
What in the source material clicks? Why does it ring true? Connect it to your own experience or intuition.
- "This resonates because in my project I saw exactly this pattern..."
- "The reason this works is actually deeper than the author states..."

### Layer 2: 延伸 (Extension)
Push the source ideas further than the original author did. Techniques:
- **Cross-domain analogy**: Borrow from biology, economics, physics, history to illuminate the point
- **Extreme-case reasoning**: "If we push this logic to its limit, it implies..."
- **Connecting dots**: Link ideas from different sources that the authors themselves didn't connect
- **Real-world cases**: Cite specific products, companies, or incidents that illustrate the point

### Layer 3: 原创观点 (Original Thesis)
Formulate YOUR position — not a summary of what others said, but what YOU believe after digesting everything.
- The thesis should be something the source authors didn't explicitly state
- It should feel like a natural conclusion from your reflections, not a forced contrarian take

**Default stance: agreement + extension.** Only disagree when genuinely warranted.

## End-of-Post References

Every post that draws from external sources MUST end with a `## 延伸阅读` section:

```markdown
## 延伸阅读

- [Article Title — Author](url)
- [Article Title — Author](url)
```

Rules:
- **No inline citations in the body** — do not write "according to [source]" or link to sources mid-text
- All opinions in the body are presented as your own ("我认为", "我发现", "我的判断是")
- The 延伸阅读 section is a courtesy acknowledgment, not a source attribution
- List only the primary sources, not every link you encountered

## Don't Do This

- Summarize without synthesizing — add your own analysis, don't just rephrase the source
- Hedge everything — "maybe", "perhaps", "it could be argued" dilutes authority
- Write filler conclusions that repeat the introduction
- Use corporate-speak: "leverage", "synergy", "comprehensive solution"
- Over-explain basics the target audience already knows
- Treat all options as equal — make a recommendation and defend it
- Cite sources inline — no "according to [author]" or "[source] argues that" in the body
- Write a post that could be identified as a rewrite of a specific source article
