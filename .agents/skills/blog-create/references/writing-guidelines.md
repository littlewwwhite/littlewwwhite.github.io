# Technical Blog Writing Guidelines

Use these rules for zjding’s Chinese technical blog. Treat the reader as an experienced engineer who wants evidence, mechanisms, and decisions rather than a lecture or a source digest.

## 1. Truthful authorial voice

Build authority from inspectable work:

- an experiment with conditions and raw results;
- a source-code or architecture trace;
- a real implementation or debugging record;
- an explicit decision tied to constraints;
- a carefully bounded inference.

Use first person only for user-supplied experience or work actually performed during the current task and preserved by artifacts. Do not write “我踩过这个坑”, “我一开始以为”, or emotional reactions unless they are true.

Keep these sentence types distinct:

| Type | Suitable language |
|---|---|
| Primary-source fact | “架构文档将对象存储作为持久层……” |
| Direct observation | “在 turbovec 0.8.0、50,000×384 数据上，本次运行得到……” |
| Hypothesis/inference | “我的猜想是……；在相似数据分布下可能成立，生产环境仍需验证。” |
| Opinion/decision | “对当前小说 Agent，我不会因此引入第二套检索系统。” |

Never present a source author’s idea as the blog author’s discovery. Place an inline primary-source anchor near consequential external claims.

A hypothesis may appear before its evidence when it is labeled as a hypothesis and the article later tests, revises, or leaves it unresolved. Do not hide uncertainty to make the prose sound decisive.

## 2. Titles, openings, and endings

### Titles

Answer “这篇文章讲什么” naturally. Prefer a concrete object plus the actual lens or decision.

Good:

- `向量检索的两笔字节账`
- `为什么我暂时不会把小说检索迁到 turbopuffer`
- `turbovec 低比特量化：压缩率必须和召回率一起读`

Avoid:

- correcting a spelling mistake as the article’s opening move;
- gimmicks built from coincidental names such as “两个 Turbo 的两条路”;
- stacked product names with no reader question;
- clickbait mystery, number stacking, or a conclusion stronger than the evidence;
- habitual `不是 X，而是 Y`.

### Openings

Begin with the most concrete source of tension available: a result, an operational problem, a failed comparison, or a decision that needs evidence. A plain direct opening is acceptable. Do not force one of a fixed set of hooks.

Avoid preambles such as `随着……的发展`, `本文将介绍`, or a meta-discussion about terminology unless terminology is the actual technical problem.

### Endings

Stop after the last useful implication or decision. The final paragraph may:

- state the bounded decision;
- explain what evidence would change it;
- crystallize the mechanism;
- give actions when the article is genuinely procedural.

Do not force a philosophical “highest altitude,” a three-item action list, a prediction, or a slogan. Do not recap the table of contents.

## 3. Paragraphs are the default

A paragraph is one complete reasoning move: a claim, the evidence or mechanism that supports it, and the consequence needed to continue. End it when the thought changes, not after every sentence.

Avoid:

- one sentence per line;
- a bare product name followed by six metric lines;
- several short paragraphs that could be joined without changing meaning;
- a paragraph that contains unrelated claims merely to hit a target length.

Short paragraphs are useful for emphasis, but emphasis disappears when every paragraph is short.

### The list test

Use bullets or numbering only when all three conditions hold:

1. items are independent;
2. items have parallel semantics;
3. the reader benefits from scanning, counting, or executing them.

If list items need explanation, causality, contrast, or prioritization, write prose. If every item repeats the same fields, use a table. If steps must be performed in order, use a numbered procedure.

Never use a list to simulate depth. “需要测试 p50、p95、p99、Recall、写入可见性……” is not analysis until the text explains which promise each measurement can disprove.

## 4. Let evidence determine depth

Technical depth is not the number of concepts mentioned. It is how far the article follows a consequential question through mechanism, evidence, interpretation, and boundary.

At least one hard anchor is normally required for evaluation or decision articles. Suitable anchors include an experiment, source trace, reproducible deployment, incident, exact configuration diff, or measured comparison.

When no hard anchor is available:

- narrow the article to explanation, architecture reading, or experiment design;
- state what remains unverified;
- do not compensate with more terminology, diagrams, or assertive prose.

Spend more words where:

- a result contradicts the initial model;
- a parameter changes the decision;
- a failure reveals a system boundary;
- evidence and official claims diverge;
- a trade-off needs interpretation.

Compress:

- well-known background;
- installation mechanics unrelated to the conclusion;
- exhaustive feature inventories;
- secondary examples that do not change the argument.

Do not give every section equal weight. Do not require a failure, turning point, counterargument, analogy, aphorism, or “show, don’t tell” scene in every article. Keep them only when the material naturally contains them and they improve understanding.

## 5. Write experiments as evidence, not theater

An experiment passage should make clear:

- what claim the test could disprove;
- what was held constant and what changed;
- what actually happened;
- what the result changes;
- what the setup cannot establish.

These elements need not appear in a fixed order or under fixed headings.

Report versions, data shape, hardware/runtime, relevant concurrency, baseline, and metric definitions when they affect interpretation. Link the runnable script and raw result when practical.

Keep a failed attempt when it changes the method or conclusion. A type mismatch, broken assumption, or deployment failure can add useful texture; routine setup noise cannot.

Never:

- fabricate a failure or surprise;
- extrapolate a synthetic dataset to production behavior;
- announce “X is faster” when the baselines use different work;
- present a single latency number without the workload;
- hide recall, quality, cost, or consistency losses behind compression or throughput gains.

## 6. Structure follows the subject

Choose the smallest structure that makes dependencies visible:

- data path for system architecture;
- causal chain for mechanism;
- chronological path for a real implementation;
- decision tree for selection;
- table plus interpretation for repeated comparisons;
- claim/evidence sequence for an essay.

Parallel sections are legitimate when the dimensions are genuinely parallel. They become weak only when they are disconnected inventory items pretending to be an argument.

Use transitions when the logical relation is not obvious. Do not insert a bridge sentence between every section by rule. Do not require the final section to be the most abstract.

Headers should help navigation and may be a judgment, question, mechanism, or concise topic label. Do not contort every header into a slogan.

## 7. Visuals must earn their place

Use:

- Mermaid for topology, branching, or event order;
- tables for exact mappings and repeated-field comparisons;
- charts for quantitative relationships;
- screenshots or generated illustrations when visual appearance itself matters;
- code for executable semantics.

Do not impose a minimum number of visuals. A paragraph is better than a diagram that only repeats the paragraph.

Generated illustrations may provide a conceptual anchor, but must not invent precise architecture, benchmark data, UI state, or source evidence. A “小黑” illustration should communicate one idea, not decorate a section.

Before publication:

- decode changed images completely;
- inspect the full canvas for cropping, black regions, illegible text, and incorrect aspect ratio;
- verify captions and relative paths;
- render Mermaid through the actual Hugo path;
- keep source attribution for reused diagrams.

## 8. Language and formatting

- Write prose in Simplified Chinese.
- Keep code, identifiers, product names, and commands in their original language.
- Prefer concrete verbs and nouns over abstract packaging.
- Use bold sparingly for the one term or result a reader might otherwise miss.
- Use blockquotes only for actual quotations or a rare sentence that benefits from isolation.
- Avoid report filler: `综上所述`, `值得注意的是`, `由此可见`, `赋能`, `闭环`, `抓手`, `深耕`, `广阔前景`.
- Avoid repetitive AI constructions: `不仅……更……`, `真正的 X 不是 A 而是 B`, `从 X 到 Y`, and symmetrical “优势/局限” sections.
- Do not ban a word mechanically when it is the precise technical term; ban the empty rhetorical habit.

No fixed word count applies. The article is finished when the promise is supported, the important boundary is stated, and further detail would not change the reader’s model or decision.

## 9. Source handling

Prefer primary sources: official documentation, source code, papers, standards, release notes, and first-party benchmark methodology.

Use inline links for claims a reader may want to verify immediately. Add `## 延伸阅读` only when a curated primary-source list provides value; do not use it as a substitute for claim-level evidence.

Quote sparingly. Paraphrase accurately, preserve uncertainty, and never remove context that changes the source’s meaning.

## 10. Final read

Read the draft once as an argument and once as a skeptical engineer.

On the argument pass, remove:

- sections that can disappear without affecting the conclusion;
- repeated conclusions;
- lists that should be paragraphs;
- ornamental transitions and slogans.

On the skeptical pass, mark:

- claims without a traceable basis;
- observations missing conditions;
- inferences written as facts;
- conclusions broader than the data;
- diagrams or images that look authoritative without being evidence.

Revise the mechanism that caused each problem rather than patching the sentence in isolation.
