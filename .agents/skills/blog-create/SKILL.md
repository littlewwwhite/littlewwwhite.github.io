---
name: blog-create
description: Create, restructure, or deeply revise evidence-led technical blog posts from ideas, notes, URLs, source code, experiments, screenshots, or existing drafts. Use for “写篇技术博客”, “把这些资料写成文章”, “优化这篇博客”, “发博客”, “new post”, or a full blog quality review. Do not use for isolated copy edits, translation, image-only work, or publishing an already-finished post without content changes.
---

# Blog Create

Create a technically honest article, not a polished inventory of source material. Let evidence produce the article’s claims, and let the places where understanding changes determine its depth.

## Read first

Before outlining or writing:

1. Read `references/writing-guidelines.md` completely.
2. Read `references/learning-log.md` completely. Its newer corrections override older examples.
3. Read `references/examples.md` when calibrating paragraph/list boundaries, evidence language, or experiment narration.

## Core contract

- Put truth before narrative. Never invent a failure, emotion, experiment, personal history, or change of mind to make the article feel human.
- Put argument before coverage. Do not preserve every source point merely because it was collected.
- Enter through a concrete situation, event, tension, judgment, or thought. Do not greet the reader with a benchmark table, specification list, or detached headline number.
- Use paragraphs as the default unit of thought. Use lists, tables, code, and diagrams only for the jobs they perform better than prose.
- Design reading rhythm as well as argument. Use emphasis, quotations or judgment blocks, indentation, code, tables, diagrams, charts, and illustrations when they create real hierarchy.
- Match the article’s promise to its evidence. Architecture reading is not a product benchmark; a synthetic test is not production validation.
- Allocate depth unevenly. Slow down where evidence changes the model or the decision; compress background and mechanical detail.
- Keep facts, direct observations, hypotheses/inferences, and opinions distinguishable.

## Workflow

### 1. Define the article promise

Reduce the task to:

- one question the article will answer;
- one provisional judgment or decision;
- the strongest scope the available evidence can support;
- the main uncertainty that remains.

Choose the article mode from the evidence, not from a fixed template:

| Mode | Minimum honest basis |
|---|---|
| Architecture/source reading | Primary documentation, source code, paper, or design artifacts |
| Experiment/evaluation | Reproducible test or first-hand operational observation with stated conditions |
| Engineering field note | A real implementation, debugging path, migration, or decision made during the task or supplied by the user |
| Opinion/decision essay | A clear position plus evidence and a serious boundary or countercase |

If the user asks for an evaluation but no direct test exists, either run the smallest useful experiment or narrow the promise to “architecture reading and experiment design.” Do not fill the gap with confidence.

Ask a question only when the missing answer would materially change the conclusion, evidence plan, or publication target. Do not require the user to approve an inventory, thinking note, or outline by default.

### 2. Build an evidence ledger

Keep this ledger internal unless the user asks to see it:

| Claim | Type | Evidence | Boundary |
|---|---|---|---|
| What the article may say | Source fact / direct observation / hypothesis or inference / opinion | URL, code path, command, raw result, screenshot, or user statement | Version, environment, dataset, uncertainty |

Use the ledger to prevent three common errors:

1. turning an official claim into a personal observation;
2. turning one local result into a universal judgment;
3. turning an unresolved hypothesis into a factual sentence.

For externally derived major claims, place a lightweight inline anchor near the claim: a deep documentation link, paper section, source-code path, original diagram, or raw result. An end-of-post reading list may supplement inline evidence; it does not replace it.

### 3. Generate a hard anchor when the promise needs one

For an experiment, benchmark, or tool evaluation, prefer the smallest test capable of disproving the provisional judgment.

Record enough context to reproduce and interpret it:

- package/model/version and relevant commit;
- hardware/runtime and meaningful thread or concurrency settings;
- dataset or input construction;
- baseline and metric definition;
- exact command or script;
- raw results, not only a rounded summary;
- limitations and plausible confounders.

Run the real library or inspect the real source whenever practical. Preserve useful artifacts beside the post. If the experiment fails, retain the failure only when it changes the method, interpretation, or conclusion.

Do not:

- manufacture a failed attempt because the article needs a “turning point”;
- call random or synthetic data representative of business traffic;
- compare systems at different layers with one undifferentiated benchmark;
- add a long list of future metrics in place of an experiment.

When no experiment is justified, use another hard anchor: a source trace, production incident, deployment observation, exact configuration diff, or a carefully bounded worked example.

### 4. Find the real cognitive movement

Identify:

- the initial question or assumption;
- the evidence that adds the most information;
- what changed in the mental model or decision;
- what still cannot be concluded.

Use that movement as the article’s backbone only if it actually happened. Otherwise choose the order the subject requires: causal dependency, system data path, decision criteria, chronological implementation, or an exact comparison.

Parallel sections are not automatically wrong. Keep them when the subject is genuinely parallel and the reader benefits from comparison; use a table when the fields repeat exactly. Do not force every article into “failure → discovery,” “expectation → reversal,” or an ever-higher abstraction ladder.

### 5. Choose the entry, page rhythm, and visual coverage

Before drafting, make three internal decisions.

**Opening seed:** choose the most truthful concrete entry available:

- a situation or operational problem the user actually faces;
- something that happened during the supplied work or this task;
- a comparison, contradiction, or decision that needs resolving;
- the author’s bounded opinion, doubt, or thought about the subject.

The first paragraph must establish why the question matters before presenting dense measurements. Do not open with a table, a specification inventory, or an isolated string of percentages and latency numbers. When a number is itself the incident, first frame what happened and why it was surprising or consequential, then give the measurement.

**Page rhythm:** decide where the reader needs continuous reasoning and where a different visual weight would help. A long article rendered almost entirely as headings plus plain paragraphs is unfinished even when the prose is correct. Look for honest uses of:

- bold anchors inside dense paragraphs;
- a blockquote for a sourced quotation, a clearly labeled author judgment, a decisive question, or an important boundary;
- indentation or nested structure when hierarchy is real;
- code, tables, charts, diagrams, screenshots, or illustrations for their native jobs.

Do not distribute these formats evenly or add them decoratively. Use contrast: dense reasoning beside a compact visual, a key judgment isolated after evidence, or a code block followed by interpretation.

**Visual coverage:** inventory the relationships the article asks the reader to hold in working memory. For each architecture, data path, message exchange, pipeline, state change, quantitative trade-off, repeated comparison, decision branch, abstract mechanism, or UI state, decide first whether a visual would materially reduce mental simulation. If prose already makes a simple relationship immediately clear, keep prose.

When a visual is justified, choose it by semantic job rather than habit:

- Mermaid for lightweight flow, topology, branching, state, or event-order diagrams that the site can render directly;
- PlantUML for a detailed sequence, component, class, or deployment view only when its extra notation is useful and the publication pipeline supports it;
- a sequence diagram for ordered messages, ownership, waiting, retry, or lifecycle behavior;
- a pipeline diagram for stages, transformations, queues, fan-out, or failure paths;
- a deterministic Matplotlib chart for measured trends, distributions, trade-offs, or uncertainty, with data and generation code preserved;
- a table for exact repeated fields, a screenshot for concrete UI state, and a concept illustration for intuition or a memory anchor.

These choices are alternatives, not a checklist. Do not add Mermaid to every article, turn a two-step explanation into a flowchart, or use a diagram where a sentence or small table is clearer. Conversely, do not leave a genuinely temporal, spatial, or quantitative relationship buried in prose merely to minimize the visual count. Use the project’s `blog-img` skill when a concept diagram, explainer poster, annotated screenshot, or other custom visual is the best fit.

### 6. Outline only what the argument needs

Give each section one job in the argument. Remove a section when it merely:

- repeats a source’s table of contents;
- introduces terminology that can be explained in one sentence at first use;
- contains a second shallow example of a point already proven;
- exists only to satisfy a preferred article shape;
- postpones the actual evidence.

Let section lengths differ. A background section may be one compact paragraph; an experiment that changes the conclusion may need several paragraphs, a table, and a limitation note.

Do not output a formal outline or “progression spine” unless it helps the user make a real choice.

### 7. Write from evidence toward judgment

Follow `references/writing-guidelines.md`.

In particular:

- Keep related sentences in the same paragraph until one reasoning move is complete.
- Convert metric dumps and sentence-like bullet lists into causal prose.
- Use a list only when the items are independent, parallel, and meant to be scanned or executed.
- Use a table for exact repeated-field comparison, code for executable behavior, Matplotlib or another deterministic chart for quantitative relationships, and the least complex supported diagram notation that makes topology, sequence, state, or pipeline structure materially clearer than prose.
- Use bold, blockquotes, indentation, captions, and whitespace to expose hierarchy and reading rhythm; do not let the entire article collapse into one typographic voice.
- Use first person only for experience supplied by the user or work actually performed during this task and backed by artifacts. Never invent feelings or prior production experience.
- State source facts, direct observations, and inferences with different levels of certainty.
- Preserve useful small frictions and associations only when they change the reader’s model. Do not add “human texture” on a schedule.
- Use no fixed article length, paragraph count, number of sections, number of visuals, number of failures, or required word count for a turning point.

### 8. Review the draft against its promise

Revise before output if any answer is unsatisfactory:

#### Evidence integrity

- Does each major judgment have a source, observation, calculation, or explicit reasoning chain?
- Can the reader tell what is official, what was observed here, and what is inferred?
- Does the conclusion stay within the test’s environment and dataset?
- If the hard anchor disappeared, would the article collapse into a generic source summary?

#### Prose integrity

- Does the opening begin with a concrete situation, event, tension, judgment, or thought before it asks the reader to absorb data?
- Do paragraph breaks follow changes in thought rather than individual sentences?
- Does every list pass the independent + parallel + scan-worthy test?
- Are there naked labels followed by metric inventories?
- Are sections split more finely than the reasoning requires?
- Is any transition sentence present only because a template demanded one?
- Does the page have deliberate hierarchy, or is nearly everything rendered with the same visual weight?

#### Depth and voice

- Is the deepest passage where the understanding or decision actually changes?
- Are background facts compressed?
- Is any “I” sentence unsupported by real work or user-provided experience?
- Was a failure, analogy, aphorism, counterargument, action list, or dramatic reversal inserted mechanically?
- Does the article make a real judgment, or only arrange facts attractively?

#### Visual and source utility

- Does every image, table, chart, Mermaid block, or PlantUML diagram do a job that prose would perform worse?
- Did the draft inspect every spatial, temporal, comparative, and quantitative relationship for a better visual form?
- Were useful concept or navigation images deleted merely because nearby prose can restate them?
- Do the visuals vary by function rather than repeat one diagram grammar throughout the post?
- Was Mermaid or another diagram syntax added by default even though a sentence or small table would be clearer?
- Are precise architectures and data charts based on deterministic sources rather than decorative image generation?
- Are important external claims anchored inline to primary evidence?

### 9. Produce and validate the Page Bundle

For this Hugo repository, create or update:

```text
content/posts/YYMMDD/
├── index.md
├── descriptive-assets.*
└── optional experiment scripts and raw results
```

Use frontmatter with `title`, `date`, `categories`, and `tags`. Keep asset paths relative to the Page Bundle.

Before declaring completion:

1. Run experiment or example scripts included with the article.
2. Run `python3 .github/scripts/validate_pngs.py content static` when PNG files changed.
3. Fully decode and visually inspect each changed image; a successful Hugo copy does not prove the image is intact or uncropped.
4. Run the repository’s production-equivalent Hugo build and confirm every diagram format enters a supported render path; never publish raw PlantUML or another unsupported source block.
5. Check changed links and verify that raw result files referenced by the article exist.
6. Inspect the rendered page when layout, captions, or diagrams changed.

Hand off to the project’s `publish` skill only when the user asks to publish or the active request clearly includes deployment.

## Output behavior

- Keep intermediate updates concise and decision-oriented.
- Do not expose internal inventories, ledgers, scorecards, or checklists unless they help the user decide something.
- Do not pause for ceremonial confirmation when the direction is already clear.
- End with the artifact, the substantive changes, the evidence added, the validation performed, and any remaining limitation.

## Learning loop

When the user corrects an article or this skill:

1. Compare the before and after behavior.
2. Identify the mechanism that produced the error, not only the bad sentence.
3. Add the concrete correction to `references/learning-log.md`.
4. Promote repeated or explicit high-priority corrections into `references/writing-guidelines.md`.
5. Remove or rewrite any older rule that conflicts with the correction. Do not merely append another rule.
