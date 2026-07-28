# Writing Style Learning Log

Treat zjding’s direct edits and explicit feedback as ground truth. Newer entries override older examples. Promote a rule into the main guidelines by changing or deleting the conflicting old rule, not by stacking contradictory instructions.

## 2026-07-28 — Learn the author, not only the opening type

### Preserve the personal research trajectory

**Pattern**: “Start from a concrete situation” was satisfied by describing the novel Agent’s future vector growth and infrastructure cost. The opening was technically situated, but it removed the author’s actual experience: building a content-creation retrieval module, defaulting to Qdrant from habit, noticing a long gap in following retrieval technology, and deciding to investigate what had changed.

**Correction**: When the user supplies a real reason for writing, preserve the causal route from current work to habitual choice, personal doubt or curiosity, research action, and the question that emerged. Generic product stakes may follow, but they must not replace the author’s presence.

**Generalization boundary**: Learn the thinking pattern and degree of conversational texture, not the literal phrases. Do not require every post to say `最近在做`, `但你是知道我的`, or `于是有了这篇文章`; do not invent a default choice or research journey when none exists.

**Status**: PROMOTED to `writing-guidelines.md` §1–2, the main workflow’s author trace, and calibration example 5.

## 2026-07-28 — Opening, formatting, and visual coverage

### Choose visual grammar by relationship

**Pattern**: “Add more visuals” can overcorrect into Mermaid-by-default. Mermaid, PlantUML, sequence diagrams, pipeline diagrams, and Matplotlib plots were treated as interchangeable decoration rather than tools for different semantic jobs.

**Correction**: First decide whether prose already explains the relationship clearly. If a visual is warranted, route by meaning: sequence for messages and lifecycle, pipeline for stages and failure paths, Mermaid for lightweight supported relationship diagrams, PlantUML for richer formal diagrams when the build supports it, and Matplotlib for reproducible quantitative evidence. Do not require Mermaid or any diagram in every article.

**Status**: PROMOTED to `writing-guidelines.md` §7, the main workflow’s visual plan, and calibration example 8.

### Situation before data

**Pattern**: The evidence-led rule was interpreted as permission to place benchmark numbers at the top of the article. The result was accurate but read like a report rather than a piece of thinking.

**Correction**: Open from a real situation, event, tension, opinion, doubt, or thought. Establish why the question exists before presenting dense data. Measurements support the opening; they do not replace it.

**Status**: PROMOTED to `writing-guidelines.md` §2 and the main workflow’s entry decision.

### Deliberate page rhythm

**Pattern**: Avoiding fragmented lists overcorrected into nearly uniform headings, paragraphs, and tables. Bold anchors, hierarchy, blockquotes, captions, and other changes of visual weight were rarely used.

**Correction**: Design typographic hierarchy around the argument. Use emphasis, labeled judgment or boundary blocks, real indentation, code, captions, and whitespace when they expose existing structure. Reject both decorative formatting and visually flat long-form prose.

**Status**: PROMOTED to `writing-guidelines.md` §8 and the final page-rhythm pass.

### Visual coverage, not minimum deletion

**Pattern**: “Every visual must earn its place” and “no minimum number” were applied almost entirely as deletion rules. The revision removed redundant diagrams but also under-illustrated mechanisms, comparisons, and conceptual transitions.

**Correction**: Plan visuals by the relationships readers must understand. Count explanation, cognitive relief, navigation, and memory as legitimate visual value. Do not set a universal quota, but treat several visualizable relationships with only one or two visuals as a reason to re-audit coverage.

**Status**: PROMOTED to `writing-guidelines.md` §7 and the main workflow’s visual plan.

## 2026-07-27 — Turbopuffer / turbovec revision

### Paragraphs before lists

**Pattern**: Metric inventories and one-sentence line breaks made the article fragmented and shallow.

**Correction**: Group related metrics by the higher-level question they answer. Explain test order, causal purpose, and decision impact in prose. Reserve lists for independent, parallel, scan-worthy items.

**Status**: PROMOTED to `writing-guidelines.md` §3.

### Evidence produces depth

**Pattern**: Reading many sources and listing possible benchmarks created the appearance of research without an observed result.

**Correction**: Let a real experiment, source trace, deployment observation, or other hard anchor generate the article’s judgment. If no hard anchor exists, narrow the promise to architecture reading or experiment design.

**Status**: PROMOTED to `writing-guidelines.md` §4–5.

### Uneven depth, no narrative formula

**Pattern**: Mandatory author presence, “show, don’t tell,” fixed 300–500 word turning points, equal section depth, and required action lists turned texture into a template.

**Correction**: Slow down only where evidence changes the mental model or decision. Keep genuine failures and associations when consequential; never invent or mechanically schedule them.

**Status**: PROMOTED to `writing-guidelines.md` §4.

### Honest ownership of claims

**Pattern**: “Zero inline citations” and “write as if every insight came from your own experience” blurred source facts, task-run observations, and the author’s real history.

**Correction**: Anchor consequential external claims inline. Use first person only for user-supplied experience or work actually performed and preserved during the task.

**Status**: PROMOTED to `writing-guidelines.md` §1 and §9.

### Natural titles and openings

**Pattern**: Openings such as “先纠正一个笔误” and titles built around two products both containing “Turbo” felt amateurish and centered the writing process rather than the technical question.

**Correction**: Name the actual mechanism, decision, or cost. Begin with the most concrete result or problem available; do not force a hook taxonomy.

**Status**: PROMOTED to `writing-guidelines.md` §2.

### Visuals must explain and survive publication

**Pattern**: Decorative or redundant Mermaid/images added volume, while damaged PNGs still passed a successful Hugo build and rendered only half the canvas.

**Correction**: Add visuals only when they make a relationship materially clearer. Fully decode and visually inspect changed images, and validate Mermaid through the production render path.

**Status**: PROMOTED to `writing-guidelines.md` §7.
