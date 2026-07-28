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

Begin with a concrete situation, something that happened, a problem being faced, a comparison that feels wrong, a bounded opinion, or a thought that opens the question. The reader should first understand **why this subject has become worth thinking about**.

Do not begin by laying out a benchmark table, a row of percentages, a specification inventory, or an isolated headline number. Data is evidence, not a substitute for an opening. If a measurement is itself the event, first name the consequence or conflict it created, then show the exact number.

A plain direct opening is acceptable. Do not force one of a fixed set of hooks, and never invent a scene, prior belief, or personal experience. The situation may come from the user’s real context, a supplied artifact, a source conflict, work performed during this task, or an explicitly framed present-tense judgment.

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

## 7. Plan visual coverage, not visual decoration

Choose the representation after identifying the relationship:

| Reader needs to understand | Prefer | Boundary |
|---|---|---|
| A simple claim or one-step relation | Prose | Do not diagram what one sentence makes obvious |
| Exact mappings or repeated fields | Table | Add interpretation outside the table |
| Lightweight topology, branching, state, or event order | Mermaid | Use only when spatial layout reveals something |
| Detailed calls, ownership, waiting, retry, or lifecycle | Sequence diagram; Mermaid or PlantUML | Prefer PlantUML only when its richer notation is useful and supported by the publication pipeline |
| Stages, transformations, queues, fan-out, or failure paths | Pipeline/flow diagram | Show meaningful branches and boundaries, not a long row of boxes |
| Measured trend, distribution, trade-off, or uncertainty | Deterministic Matplotlib chart | Preserve source data and generation code; label axes, units, sample size, and conditions |
| Concrete interface, state, or before/after evidence | Screenshot | Annotate only what the reader should inspect |
| Mechanism, intuition, navigation, or a memorable anchor | Concept diagram or illustration | Never invent precise architecture or evidence |
| Executable semantics | Code | Follow it with interpretation |

Mermaid and PlantUML are not goals; they are notations for particular diagrams. A sequence diagram or pipeline diagram describes the semantic form, while Matplotlib is for quantitative evidence. Do not use one as a decorative substitute for another.

Plan visuals before the prose hardens. Mark every place where the reader must mentally simulate:

- where components or bytes live;
- what happens over time;
- how state branches or changes;
- how two or more systems map across the same dimensions;
- how a metric changes with a parameter;
- how an abstract mechanism should be pictured;
- where to look inside a UI or screenshot.

For each place, choose the native representation or consciously keep prose. A paragraph is better than a diagram that merely turns three sentences into three boxes. A visual is justified only when it improves comprehension, comparison, orientation, evidence reading, or memory.

Do not impose a universal image count or a mandatory Mermaid block. An article may legitimately need no diagram; another may need a sequence view, pipeline view, and data chart because they solve different reader problems. Re-audit both extremes: several difficult relationships left entirely in prose, and a simple article padded with diagrams.

Do not optimize visuals only by deletion. Merge genuinely duplicate diagrams, but retain or improve an image that contributes explanation, navigation, pacing, or memory even when nearby prose can paraphrase it.

Generated illustrations may provide a conceptual anchor, but must not invent precise architecture, benchmark data, UI state, or source evidence. A “小黑” illustration should communicate one idea, not decorate a section.

Before publication:

- decode changed images completely;
- inspect the full canvas for cropping, black regions, illegible text, and incorrect aspect ratio;
- verify captions and relative paths;
- render Mermaid, PlantUML, and any other diagram source through a publication path the repository actually supports;
- regenerate deterministic charts from their checked-in data and script when practical;
- keep source attribution for reused diagrams.

## 8. Language, hierarchy, and page rhythm

- Write prose in Simplified Chinese.
- Keep code, identifiers, product names, and commands in their original language.
- Prefer concrete verbs and nouns over abstract packaging.
- Use **bold** to give a dense paragraph one or two reading anchors: a decisive term, changed judgment, mechanism, or result. Do not bold whole sentences repeatedly.
- Use blockquotes for an attributed source quotation, a clearly labeled author judgment, the decisive question, or an important boundary that benefits from isolation. Do not present an author-written callout as someone else’s quotation.
- Use indentation and nested structure only when the content has real parent-child hierarchy. Do not flatten hierarchical material into a long paragraph, and do not indent merely for decoration.
- Put commands and executable behavior in code blocks; follow them with interpretation instead of leaving code to explain itself.
- Use captions to tell the reader what to notice in a figure, not to repeat the preceding paragraph.
- Alternate visual weight where the material supports it: sustained reasoning, a compact emphasized judgment, a figure or table, then interpretation. Avoid a page whose every section has the same Markdown silhouette.
- Avoid report filler: `综上所述`, `值得注意的是`, `由此可见`, `赋能`, `闭环`, `抓手`, `深耕`, `广阔前景`.
- Avoid repetitive AI constructions: `不仅……更……`, `真正的 X 不是 A 而是 B`, `从 X 到 Y`, and symmetrical “优势/局限” sections.
- Do not ban a word mechanically when it is the precise technical term; ban the empty rhetorical habit.

Formatting must expose structure already present in the thought. It cannot rescue weak reasoning, and uniform plain prose is not a virtue when it hides hierarchy.

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

On the page-rhythm pass, inspect the rendered article and mark:

- an opening that asks the reader to digest data before understanding the situation;
- long stretches with no visual or typographic change despite multiple reasoning levels;
- important judgments buried at the same weight as supporting detail;
- blockquotes, bold, indentation, or images that are decorative rather than functional;
- mechanisms, timelines, comparisons, or trade-offs still being simulated entirely in prose.

On the skeptical pass, mark:

- claims without a traceable basis;
- observations missing conditions;
- inferences written as facts;
- conclusions broader than the data;
- diagrams or images that look authoritative without being evidence.

Revise the mechanism that caused each problem rather than patching the sentence in isolation.
