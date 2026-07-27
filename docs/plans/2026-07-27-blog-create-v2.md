# Blog Create v2 Design

**Goal:** Make technical posts emerge from evidence and real changes in understanding, without turning every article into the same narrative template.

## Problems in the previous design

The previous skill tried to prevent source-summary writing with more mandatory structure: visible input inventories, thinking notes, progression-spine tables, a fixed hook taxonomy, author-presence quotas, a 300-word turning point, equal section-depth requirements, action lists, and at least one visual.

Those constraints optimized for the appearance of depth. They also caused predictable failures:

- prose fragmented into headings, checklists, and sentence-like bullets;
- hypothetical benchmarks replaced actual results;
- external work was written as if it were the author’s experience;
- genuine texture became a scheduled “failure → discovery” performance;
- diagrams and illustrations appeared even when prose was clearer;
- the `.agents` and `.claude` copies drifted, so one runtime loaded an older rule set.

## Design decisions

1. Keep `.agents/skills/blog-create/` as the canonical implementation. Make the Claude entrypoint delegate to it instead of duplicating references.
2. Define the article promise from available evidence. Narrow “evaluation” to “architecture reading” when no direct test exists.
3. Maintain an internal evidence ledger separating source facts, direct observations, inferences, and decisions.
4. Prefer the smallest experiment or source trace capable of changing the provisional judgment.
5. Use paragraphs by default. Permit a list only when items are independent, parallel, and scan-worthy.
6. Allocate depth where evidence changes the model or decision. Remove fixed word, section, visual, failure, and narrative-arc quotas.
7. Cite consequential external claims inline. Never manufacture first-person experience.
8. Validate rendered assets independently from a successful Hugo build.

## Runtime files

| Path | Role |
|---|---|
| `.agents/skills/blog-create/SKILL.md` | Canonical workflow and quality gates |
| `.agents/skills/blog-create/references/writing-guidelines.md` | Prose, evidence, experiment, and visual rules |
| `.agents/skills/blog-create/references/examples.md` | Focused calibration for recurrent failure modes |
| `.agents/skills/blog-create/references/learning-log.md` | User corrections and promotion history |
| `.claude/skills/blog-create/SKILL.md` | Thin entrypoint delegating to the canonical skill |
