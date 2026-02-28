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

## Don't Do This

- Summarize without synthesizing — add your own analysis, don't just rephrase the source
- Hedge everything — "maybe", "perhaps", "it could be argued" dilutes authority
- Write filler conclusions that repeat the introduction
- Use corporate-speak: "leverage", "synergy", "comprehensive solution"
- Over-explain basics the target audience already knows
- Treat all options as equal — make a recommendation and defend it
