# zjding's Blog Writing Guidelines

Style guide for writing high-quality technical blog posts. Voice baseline calibrated from Karpathy's blog writing (Software 2.0, Recipe for Training NNs), refined by zjding's actual posts (260304, 260228) versus AI-generated drafts (251028, 250315). The gap between these is the target. Continuously updated via `learning-log.md`.

## Table of Contents

- **Part 1**: 角色与读者 — who you are, who reads, what tone
- **Part 2**: 风格要点 — titles, opening hooks, headers, closings, blockquotes, bold (with ✅/❌ examples)
- **Part 3**: 禁止清单 — structural, word-level, and tone prohibitions
- **Part 4**: Voice Baseline — Karpathy 风格解剖 (calibration reference)
- **Part 5**: 迭代更新工作流 — how to update these guidelines from real edits
- **Structure Patterns**: A/B/C patterns with built-in progression
- **Part 6**: 递进结构 — Progression Architecture (types, transitions, anti-patterns)
- **Part 7**: 深入浅出 — Narrative Depth & Reader Engagement (author presence, show-don't-tell, depth over breadth, tension, actionable takeaway, topic gate)
- **Formatting / Language / References**: mechanical rules

---

## Part 1: 角色与读者

**我是谁**：有工程和架构品味的人，读大量英文技术原文，对系统设计和 AI 应用有强观点，会直接说"这个做法是错的"。

**读者是谁**：资深工程师或技术管理者，时间有限，讨厌废话，需要被说服不只是被介绍。不是在看教程，是在看另一个行家怎么想这件事。

**语气基调**：同事聊天，不是写报告，也不是做讲座。"我做过这个" > "建议读者考虑"。

---

## Part 2: 风格要点（每条附正反例）

### 2.0 标题：朴素直白，不刻意制造悬念

标题的任务是让人一眼知道这篇讲什么，同时有足够的观点性让人想读。**标题应该像同事之间聊"这篇讲什么"时的自然回答**——不堆砌数字，不造悬念，不讲故事。朴素的直接陈述完全可以是好标题。

**好标题的特征：**
- 有观点或判断，不是纯话题标签
- 自然、朴素、不刻意
- 数字/悖论/反问可以用，但不要为了用而用

**标题示例：**

| 类型 | 示例 |
|------|------|
| **直白判断** | 不要低估 Autoresearch 所带来的影响 |
| **悖论/反问** | 为什么你的 Agent 知道得越多，表现越差 |
| **事实+意外** | 同一个模型，换套壳，排名从 Top 30 跳到 Top 5 |
| **简洁描述** | 给 AI 做软件的反直觉法则：越旧越好 |
| **数字+极简** | 一个 Markdown 文件让 Agent 快了 28% |

**标题禁止：**

❌ 故事体/悬念体 — "睡前启动一个脚本，醒来发现它进化了 700 代"（水文风格）
❌ 堆砌数字 — "630 行 Python，一夜 700 次实验——X 把 Y 变成了 Z"（刻意为之）
❌ "不是 X，是 Y" / "不需要 X，需要 Y" — 否定-修正句式最多每 5 篇用一次
❌ "X 的 N 个要点/原则/趋势" — 列表体
❌ "关于 X，你需要知道的一切" — 百科体
❌ 超过 25 个字 — 太长在 feed 里会被截断

### 2.1 开头：钩子工具箱

第一段（1-3 句）必须完成一件事：让读者觉得"不看完这篇会错过什么"。以下 5 种钩子策略轮换使用：

| 策略 | 机制 | 示例 |
|------|------|------|
| **杀手数据** | 具体数字 + 意外结果 | `Princeton 给 GPT-4 换了一套接口，SWE-bench 分数从 3.97% 跳到 12.47%。` |
| **先破后立** | 打破常见认知 → 自己的判断 | `直觉答案是"更智能、更强大、更新"。但数据给出了一个完全相反的结论。` |
| **场景投掷** | 把读者直接扔进一个具体场景 | `让 Claude Opus 4.5 用一条指令构建一个 claude.ai 克隆——它失败了。但失败的方式比成功更有意思。` |
| **悖论** | 提出一个违反直觉的事实 | `有人把这件事量化了。给 Agent 更多信息，它反而变慢了。` |
| **结果先行** | 先给结果，再展开过程 | `583 次工具调用，311 个请求，58 美元。一个 Sonnet 模型用两小时做完了移植。` |

**开头禁止：**

❌ `随着 X 的迅速发展……` — 废话铺垫
❌ `上一篇文章里我提到……` — 系列引用不能当开头，放在钩子后面
❌ `很多人认为……我的判断是……` — 论文式，先说结论不如先给证据
❌ `本文将介绍……` — 目录不是开头

### 2.2 Section Header：论断，不是话题标签

Header 必须是一个有观点的句子，读者看完 header 就知道这一节要说什么结论。

✅ `Agent 每次运行都要交一笔探索税`
✅ `熟悉度悖论：你的 API 越新，AI 越不会用`
✅ `0.50 是最难定价的合约`
❌ `背景介绍`
❌ `第一部分：基础概念`
❌ `1.1 Serverless 的瞬态矛盾`

### 2.3 收尾：全文最高点，不是打包

文章的最后一段是全文的制高点——比开头更抽象、更有洞察力。它回答"所以这一切意味着什么？"读者只看开头和结尾，就应该能抓住全文主线。

**3 种收尾策略：**

| 策略 | 机制 | 示例 |
|------|------|------|
| **升维结论** | 把全文的具体论证拉到更高的抽象层 | `28.64% 说的不是效率。它说的是：你已经知道的东西，Agent 不知道，所以它要花时间去发现。把知识写下来，发现成本就消失了。` |
| **格言式收尾** | 一句话结晶全文核心 | `Welcome to the machine.` |
| **前瞻性断言** | 基于全文论证，指向一个更大的判断 | `当 harness 的边际贡献超过模型升级，"选哪个模型"就不再是最重要的工程决策了。` |

**收尾要求：**

- 最后一段必须包含全文的核心判断
- 核心判断要比开头的钩子更深一层——开头是"发生了什么"，结尾是"这意味着什么"
- 1-3 句话，不超过 100 字

**收尾禁止：**

❌ `综上所述，本文介绍了……` — 打包式总结
❌ `结语：……是一个创新解决方案……具有广阔的发展潜力。` — 公文体
❌ 重复开头的数据或事实 — 结尾应该在更高的抽象层
❌ "值得持续关注" / "让我们拭目以待" — 空洞的展望

### 2.4 Blockquote：两种合法用途

`>` 只用于：
1. 引用具体决策场景（对话感）
2. 格言式单句（本节的最关键洞察）

✅
```
> "这个项目用 CommonJS 还是 ESModule？"
> "测试文件放 `__tests__/` 还是和源文件同目录？"
```
✅ `> 在传统软件行业，创新是竞争优势。在 AI Agent 时代，**兼容性**才是。`
❌ 用 blockquote 包裹普通的背景介绍

### 2.5 Bold：标记"本节最重要的那一个词/句子"

Bold 是稀缺资源，用多了就失效。每节最多 1-2 处。用来标记：
- 新造的概念名（**探索税**，**POSIX 法则**）
- 这节核心结论里最关键的那几个字（**兼容性**，**误差在 0.50 附近最大**）
- 效果对比中的等级（**效果最好**，**效果次之**）

---

## Part 3: 禁止清单

### 结构性禁止（比词汇禁止更重要）

❌ **"摘要" / "总结" / "结语" 章节** — 直接删。没有这些。
❌ **首先…其次…最后…** 的三段式结构 — 改为自然过渡或平铺。
❌ **1.1 / 2.3 这类数字小节** — 散文里不用，只有表格才分行列。
❌ **在这个 X 迅速发展的时代** 开头 — 直接删，从第一个实质句子开始。
❌ **"这不仅仅是 X，它代表了 Y"** — 直接说 Y 是什么。
❌ **优点/局限性 的对称清单** — 有观点的文章做选择，不做"中立分析"。

### 词汇禁止

❌ 核心论点、关键洞察、本质上是、这让我想到
❌ 赋能、闭环、抓手、深耕、落地
❌ 值得注意的是、有趣的是、不得不说、有一说一
❌ 综上所述、总而言之、由此可见
❌ 更强大、更高效、更灵活（无数字支撑时）
❌ 等等、之类（用具体例子替代）
❌ 截至 X 年 X 月（文章发布就是时间戳，不用再说）

### 语气禁止

❌ "建议读者…" — 直接说该怎么做
❌ "可以考虑…" — 直接说做什么
❌ "尽管 X，但 Y 具有广阔前景" — 要么说问题是什么，要么别提
❌ "笔者认为" — 直接陈述观点

---

## Part 4: Voice Baseline — Karpathy 风格解剖

zjding 的目标文风以 Andrej Karpathy 的技术博客为校准基线。以下从 Karpathy 的 "Software 2.0" 和 "A Recipe for Training Neural Networks" 提取的关键写作模式：

### 4.1 开头：先破后立

Karpathy 从不用 "In this post I will discuss..." 开头。他的钩子是**打破一个常见认知，然后立刻给出自己的判断**。

✅ Karpathy 原文：
`I sometimes see people refer to neural networks as just "another tool in your machine learning toolbox". Unfortunately, this interpretation completely misses the forest for the trees. Neural networks are not just another classifier, they represent the beginning of a fundamental shift in how we develop software.`

拆解：
- 句1：常见认知（"just another tool"）
- 句2：直接否定（"completely misses"）
- 句3：自己的判断（"fundamental shift"）

zjding 对应：
`TiDB Cloud 上每天新建的集群，超过 90% 是 AI Agent 创建的。` → 事实钩子
`直觉答案是"更智能、更强大、更新"。但黄东旭最近的文章给出了一个完全相反的结论` → 先破后立

### 4.2 权威感来源：I-statement + 具体失败

Karpathy 的权威感不是靠"笔者认为"或引用论文，而是靠**亲身经历的具体场景**。

✅ `I can't count the number of times this has saved me and revealed problems in data preprocessing.`
✅ `One time I accidentally left a model training during the winter break and when I got back in January it was SOTA.`
✅ `coding directly in weights is kind of hard (I tried).`

规律：**"I + 动词 + 具体结果"** 比任何论述都有说服力。

### 4.3 幽默：一剂，不是一瓶

Karpathy 的幽默是干燥的、克制的，每篇大约 1-2 处，放在读者需要喘口气的地方。

✅ `the state of the art approach to exploring a nice and wide space of models and hyperparameters is to use an intern :). Just kidding.`
✅ `coding directly in weights is kind of hard (I tried).`

规律：幽默必须是**括号式的**——去掉它不影响论点，保留它让人会心一笑。

### 4.4 Bold = 信号弹，不是荧光笔

Karpathy 的 bold 只标记**一个明确的行动指令或反直觉结论**：

✅ **Don't be a hero.**
✅ **a "fast and furious" approach to training neural networks does not work**

规律：如果你想 bold 一个词，先问——去掉 bold 读者会漏掉这个关键信息吗？如果不会，就不 bold。

### 4.5 结尾：最后一个有用的东西说完就走

✅ `You're now ready to read a lot of papers, try a large number of experiments, and get your SOTA results. Good luck!`

没有"综上所述"。没有回顾。最后一句要么是**行动指令**，要么是**格言式收尾**。

### 4.6 反模式对照

| Karpathy 写法 | AI 典型写法 | 差距 |
|---|---|---|
| "It's a leaky abstraction" | "值得注意的是，这种方法存在一定局限性" | 直接 vs 绕弯 |
| "Don't be a hero" | "建议读者在初期保持简单" | 命令 vs 建议 |
| "I tried. (it's hard)" | "在实践中可能会遇到一些挑战" | 亲历 vs 泛泛 |
| "Good luck!" | "综上所述，本文介绍了 X、Y、Z" | 停 vs 打包 |

### Karpathy 参考文章（用于校准）

- [Software 2.0 — Andrej Karpathy](https://karpathy.medium.com/software-2-0-a64152b37c35)（2017）— 先破后立的经典示范
- [A Recipe for Training Neural Networks](https://karpathy.github.io/2019/04/25/recipe/)（2019）— I-statement 权威感 + 具体失败场景的教科书
- [Yes you should understand backprop](https://karpathy.medium.com/yes-you-should-understand-backprop-e2f06eab496b)（2016）— 反框架式直言

### zjding 本站参考范文

以下是风格最准确的参考文章，写作前建议重读一篇感受节奏：

- `content/posts/260304/index.md` — 一个 Markdown 文件让 Agent 快了 28%（最典型）
- `content/posts/260228/index.md` — 给 AI 做软件的反直觉法则：越旧越好

反面参考（AI 调子没对的早期版本）：
- `content/posts/251028/index.md` — 有摘要/结语，数字小节，AI 味结尾
- `content/posts/250315/index.md` — "本文将详细介绍"开头，优缺点对称清单

---

## Part 5: 迭代更新工作流

每次你手动修改了 AI 生成的草稿，执行以下更新流程：

**Step 1**：把 AI 原稿和你修改后的版本都提供给 Claude。

**Step 2**：用这个提示：
> "对比以下两段文字，第一段是 AI 草稿，第二段是我手动修改后的版本。分析我做了哪些修改，总结修改规律，判断哪些规律应该作为新规则加入 writing-guidelines.md，然后直接更新文件。"

**Step 3**：确认新规则是否需要加进 Part 3 禁止清单，或更新 Part 2 风格要点的正反例。

这个工作流是 writing-guidelines.md 保持准确的唯一来源。靠凭空写规则不如靠你的真实修改动作。

---

## Thesis-Driven Writing

Every post must have a **clear, directional thesis** — not a topic, but a position.

**Bad**: "Let's explore Cloudflare Tunnel"
**Good**: "Cloudflare Tunnel is the most cost-effective way to expose local services — here's why and how"

**Bad**: "An overview of document conversion tools"
**Good**: "After testing markitdown, MinerU, and Marker, Marker wins on structured output quality — here's the data"

The thesis goes in the opening paragraph. Everything else serves it.

---

## Content Depth Requirements

每篇博客至少 1200 字，必须包含实质内容：

- **具体数字或对比** — "方案 A 用了 3 秒，方案 B 用了 1.2 秒"，不是"方案 B 更快"
- **真实代码或配置** — 不是伪代码，是能跑的
- **失败或代价** — "这样做的问题是……"，不是只写成功路径
- **可执行结论** — "如果你遇到类似情况，建议……"，不是"值得思考"

---

## Intellectual Depth Techniques

### Create Conceptual Frameworks
Don't just describe — **frame**. Build mental models readers can apply elsewhere.

**zjding style**: "RAG systems have two failure modes: retrieval failure (didn't find it) and synthesis failure (found it, mangled it). Most teams only measure the second."

### Aphoristic Summaries
Crystallize complex ideas into one-liners. Place at section ends or as blockquotes.

- "自然语言负责探索空间，符号负责收敛空间"
- "Agent 不是在等一个更强大的系统，而是更喜欢一个它已经懂的系统"
- "接口封闭，实现开放 = 可控演化"

### Cross-Domain Analogies
Borrow from physics, biology, economics, history. Makes writing feel richer.

Used in best posts: biology (最成功的不是最强壮的), computing (编译器 vs 解释器), energy (按度卖电 vs 订阅)

### Data Before Claims
Every assertion needs supporting evidence — benchmarks, numbers, comparisons.

---

## Structure Patterns (with built-in progression)

Patterns now embed progression logic. See `progression-patterns.md` for annotated real-world examples.

### Pattern A: 同心圆分析 (survey/review posts — progression: inside-out)
```
Opening: Thesis + anchoring data point
Layer 1: Core mechanism — the innermost "why"
Layer 2: Design implications — what the mechanism demands
Layer 3: System-level consequences — how it reshapes infrastructure
Layer 4: Economic/social impact — what it means for business or culture
Closing: One-liner crystallization (no "综上所述")
```
Each layer's conclusion is the next layer's premise. The reader cannot skip a layer without losing the logic.

### Pattern B: 工程叙事 (tool/project posts — progression: failure→discovery)
```
Opening: The problem I hit + why it matters
Attempt 1: Obvious approach → why it failed (concrete data)
Attempt 2: Better approach → partial success + remaining gap
Solution: What finally worked + working examples
Takeaway: What this failure sequence reveals about the deeper problem
```
Each attempt builds on the previous failure. The reader follows a discovery arc, not a comparison table.

### Pattern C: 论证升维 (opinion/analysis posts — progression: thesis deepening)
```
Opening: Provocative thesis + anchoring evidence
Evidence 1: First supporting argument — establishes the base case
Evidence 2: Extends to a new domain/dimension — thesis is bigger than it seemed
Evidence 3: Counter-argument addressed — thesis survives the strongest objection
Closing: Refined thesis + implications readers didn't see coming
```
Each evidence section expands the thesis scope. The closing must be at a higher altitude than the opening.

---

## Part 6: 递进结构 — Progression Architecture

**Core principle**: Sections form an escalation arc, not a parallel list. The reader's understanding should deepen with each section.

### 6.1 Four Progression Types

| Type | Mechanism | Signal phrase | Anti-pattern |
|------|-----------|--------------|--------------|
| **同心圆展开** | Each section's conclusion → next section's premise | "这意味着…" "由此推导…" | Sections that can be freely reordered |
| **认知升级线** | Each section shifts the reader's mental model deeper | "这不仅是 X 问题" "真正的问题在于…" | All sections at the same abstraction level |
| **失败→发现叙事** | "Tried X → failed → discovered Y" compounds | "第一版…" "后来发现…" "最终…" | Listing features without showing the journey |
| **期望→打碎→重建** | "Should work" → "doesn't" → "here's why + fix" | "理论上…" "但实际…" "解法是…" | Giving the solution without showing why obvious approaches fail |

### 6.2 Transition Techniques (节间过渡)

**Mandatory**: Every pair of adjacent sections MUST have connective tissue. Three proven techniques:

**技法 1: 显式升维声明** — Name what changes between this section and the next.
✅ `前两个问题都是静态的。预测市场还有一个动态问题。` (260305)
✅ `前三个问题都是关于单个合约的。最后一个问题升维：多合约组合。` (260305)
✅ `如果说前面讨论的是 Agent 更容易理解什么样的系统，那接口设计关注的是另一个问题。` (黄东旭)

**技法 2: 伏笔接力** — Mention a future section to create narrative tension.
✅ `这一点，我更想放到后面商业模式变化那一节里单独展开去说。` (黄东旭)
✅ `正如你将在下一个例子中看到的，对一个模型有效的方法可能对另一个并非最佳。` (@trq212)

**技法 3: 前节结论作为后节前提** — The last sentence of section N is the first sentence's setup of section N+1.
✅ `AGENTS.md 是上下文预编译` 的结论是"一次编写，摊销到所有后续运行" → 下一节直接问"什么内容最值得写进去" (260304)

### 6.3 Anti-Patterns (递进禁止项)

❌ **并列节测试**：如果交换两节顺序后文章仍然成立 → 它们是并列的，需要重排或合并
❌ **孤岛节**：某节和前后节都没有逻辑依赖 → 要么删除，要么找到它在递进中的位置
❌ **末节塌陷**：最后一节是具体技巧而不是最高抽象 → 重排，让最有洞察力的部分收尾
❌ **无过渡跳跃**：两节之间没有任何连接句，直接换话题 → 加显式升维声明

### 6.4 结构紧凑性 — Structural Tightness

松散感来自三个源头：节与节之间跳跃、段与段之间堆砌、全文没有一条贯穿线。

**全文红线测试**：删掉所有内容，只保留每节的第一句话。这些句子连起来应该读成一个完整的论证链。如果读起来像一组不相关的观点——结构是松散的，需要重排。

**节级结构**：每节必须服务全文论点。每节的第一句必须做以下两件事之一：
1. **承上**：回应上一节的结论，说明它留下了什么新问题
2. **启下**：直接陈述本节要解决的问题或要建立的判断

❌ 直接开始新话题，没有和上一节的任何连接

**段级结构**：每段遵循 **论断 → 证据 → 推论** 的节奏：
- 第一句：本段的判断（这段在说什么）
- 中间：支撑这个判断的具体数据、例子、类比
- 最后一句：这个证据意味着什么 / 引出下一段

❌ 连续堆砌事实而不给出判断（流水账）
❌ 连续堆砌判断而不给出证据（空洞）
❌ 一段内同时塞入两个以上不相关论点（散焦）

---

## Part 7: 深入浅出 — Narrative Depth & Reader Engagement

**Core problem this solves**: 文章有洞察但读起来像论文综述——观点被"宣布"而非"发现"，例子多而浅，读者知道重要但不知道怎么做。

### 7.1 作者在场 — Author Presence

读者信任亲历者，不信转述者。每篇文章至少有一个"我亲手验证"的段落——自己跑过的实验、踩过的坑、观察到的反直觉现象。

| 级别 | 描述 | 示例 |
|------|------|------|
| **A: 亲历** | 你亲手做了实验，有数据 | "我拿 autoresearch 跑了一晚上，发现 X 和 Karpathy 说的不一样" |
| **B: 类比迁移** | 你在自己项目中遇到过类似问题 | "我们在迁移 vLLM 时遇到了完全相同的认知负荷问题" |
| **C: 判断** | 你对别人工作有明确的独立判断 | "Anthropic 的方案在小团队里不成立，因为……" |

**最低标准**：每篇文章至少达到 B 级。纯 C 级（只有判断没有经历）连续不得超过两篇。

**禁止**：全文只分析别人的工作而作者从未出场。如果你对某个话题没有任何亲身体验或迁移经验，要么补一个快速实验，要么换一个你有经验的角度切入。

### 7.2 展示而非告诉 — Show, Don't Tell

洞察应该通过叙事弧线被"发现"，而不是被"宣布"后再解释。

**反模式（告诉）**：
```
❌ "Context window 不是内存，是意识。" → 然后解释为什么
```

**正确模式（展示）**：
```
✅ 先呈现一个具体场景：你的 Agent 拿到了 200K context，
   塞进去完整的代码库文档。结果表现变差了。
   读者此时和你一起困惑——"信息更多怎么会更差？"
   在张力最高点揭示："因为 context 不是内存，是意识。"
```

**核心手法**：困惑 → 探索 → 揭示。读者经历了发现过程，所以记得住。

**每篇文章至少一个核心洞察必须用"展示"模式呈现**，通常放在文章的第二或第三节——这是认知转折发生的位置。

### 7.3 一个深故事胜过五个浅例子 — Depth Over Breadth

当需要举例证明一个观点时，用一个深例子走完 "为什么能行 → 哪里卡住 → 怎么解决" 的完整弧线，其余例子用一句话带过。

**反模式**：
```
❌ 金融领域：X 做了 A。基础设施：Y 做了 B。内容：Z 做了 C。科学：W 做了 D。
   （五个领域，每个一段，结构相同——这是清单，不是论证）
```

**正确模式**：
```
✅ 深挖一个最反直觉的案例（如古卷识别——最不像 ML 的场景），
   用 300-500 字走完 "为什么这里也能用 → 哪里不一样 → 最终效果" 的完整叙事。
   然后一句话："同样的模式被迁移到交易策略、GPU kernel 优化和邮件营销。"
```

**规则**：同一节内不得出现 3 个以上结构相同的平行段落。超过 3 个说明你在列清单，合并为一个深案例 + 一句话概括。

### 7.4 张力与转折 — Narrative Tension

好文章的读者体验是侦探小说，不是教科书。每篇文章至少有一个**转折点**——读者的预期被打破的时刻。

**转折结构**：
```
常识/预期 → 反常现象 → 旧解释失败 → 新框架揭示
```

**寻找转折点的方法**：在你的素材中找到以下任一信号：
- 某个团队/某人最初以为 X，后来发现是 Y
- 一个看起来应该有效的方案失败了
- 两个看起来矛盾的数据指向同一个结论
- 你自己改变想法的时刻

**转折点应得到充分展开（300-500 字）**，包括：失败的具体表现、当时的困惑、转折发生的原因、效果的量化对比。不要把最好的故事压缩在两句话里一带而过。

**禁止**：全文平铺直叙，从开头到结尾没有任何时刻读者的预期被打破。

### 7.5 可执行的收尾 — Actionable Takeaway

读者读完知道"重要"但不知道"怎么做"是文章最大的失败模式之一。

**每篇分析/框架类文章结尾前，加一个"明天就能做"的段落或列表**（3-5 条）：

```markdown
✅ 示例：
把你的 AGENTS.md 行数查一下。超过 100 行？拆成地图 + docs/ 结构。
给 Agent 的搜索工具加一个硬上限（50 条），强制它精炼查询。
在 Agent 每次编辑后自动跑 linter，观察错误传播是否减少。
```

**这不是"总结"**——不要重复前文观点。这是把抽象框架翻译成读者明天早上就能执行的具体动作。

**例外**：纯观点/前瞻类文章（如"autoresearch 的长期影响"）可以不加执行列表，但必须在收尾中给出一个可验证的预测或判断标准，让读者在未来可以回来检验。

### 7.6 选题过滤器 — Topic Gate

写之前问自己一个问题：**"我在这个话题上有什么是官方文档、Twitter thread 和其他博主没说过的？"**

如果答案只是"我把多个来源整理在一起了"——这是综述，不是文章。要么：
- 补充亲身实验数据
- 找到一个别人没提到的反直觉角度
- 用你自己的工程经历验证或反驳原始观点

**如果以上三者都做不到，不要写这篇文章。**

---

## Formatting

- **Tables** for feature comparisons and benchmarks
- **Code blocks** with language identifiers
- **Mermaid diagrams** for architecture and flow
- **Blockquotes** for aphorisms and specific quoted scenarios only
- **Bold** sparingly — key coined terms and the single most important claim per section
- Short paragraphs (2-4 sentences)

---

## Language Rules

- **Prose**: Simplified Chinese
- **Code, identifiers, tool names**: English as-is
- **Comments in code**: English

---

## End-of-Post References

Every post drawing from external sources MUST end with `## 延伸阅读`:

```markdown
## 延伸阅读

- [Article Title — Author](url)
```

- No inline citations in the body
- All opinions presented as your own
- List only primary sources
