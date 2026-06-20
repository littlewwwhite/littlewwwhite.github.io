---
name: distribute
description: Generate a local publishing pack from a Hugo blog post for 爱贝壳-driven cross-posting to X, WeChat Official Account, Zhihu, Douyin imagetext, and Xiaohongshu.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# Distribute: Publish Pack

Generate a deterministic publishing pack and 爱贝壳 fill plan. Do **not** treat this skill as a multi-platform rewrite engine or a direct publisher.

## First-Principles Contract

The Hugo post is the canonical artifact.

- **Long-form platforms reuse the canonical content**: X Premium, 微信公众号, 知乎, and 抖音图文 should share one mechanically transformed `longform.md`.
- **Only Xiaohongshu gets lossy adaptation by default**: 小红书 has a different consumption mode, so it gets `xhs.md` and optional card images.
- **Publishing UI is the unstable layer**: use 爱贝壳 or official web editors for platform-specific posting. Codex may assist with opening/filling, but final publish remains user-confirmed unless explicitly requested.

## Invocation

Use the one-command Bun entrypoints from the repository root:

```bash
bun run publish:pack
bun run publish:open
bun run publish:check
```

Use `publish:pack` to generate `_dist/<latest-slug>/` and `_dist/<latest-slug>/aibeike-fill-plan.json`.
Use `publish:open` to generate the pack and fill plan, then open 爱贝壳.
Use `publish:check` before changing the skill implementation.

Direct script usage:

```bash
python3 .agents/skills/distribute/scripts/generate_publish_pack.py \
  --latest

python3 .agents/skills/distribute/scripts/prepare_publish_pack.py \
  --latest

python3 .agents/skills/distribute/scripts/build_aibeike_fill_plan.py \
  --latest
```

For a Claude mirrored environment, use the same command under `.claude/skills/distribute/scripts/`.

## Outputs

```text
_dist/<slug>/
  longform.md      # X Premium / 微信公众号 / 知乎 / 抖音图文
  xhs.md           # 小红书必要适配
  manifest.json    # platform mapping and artifact metadata
  aibeike-fill-plan.json
  assets/          # extracted Mermaid sources and future rendered assets
  cards/           # optional 小红书/抖音 card images
```

## Transformation Rules

### `longform.md`

Use deterministic conversion only.

- Strip frontmatter.
- Strip Hugo shortcodes.
- Convert relative Page Bundle images to `https://littlewwwhite.github.io/posts/<slug>/<image>`.
- Extract Mermaid blocks into `assets/mermaid-N.mmd` and replace the block with a source note.
- Preserve normal Markdown, headings, lists, tables, and non-Mermaid code blocks.
- Append the canonical blog URL.

### `xhs.md`

Default generator creates a light seed from the longform content. If quality matters for a real campaign, revise this one artifact manually or with a focused model pass.

- Target 800-1500 Chinese characters when hand-tuned.
- Keep one main claim, one concrete example, and the author's own judgment.
- Avoid copying code blocks.
- Add 3-5 hashtags.

### `cards/`

Optional. Generate only when the post benefits from visual cards.

Recommended card set:

1. Title card
2. Core claim card
3. Architecture / flow card
4. Takeaway card

Use the same cards for 小红书 and 抖音图文 unless a platform-specific cover proves necessary.

## Publishing Flow

1. Generate the pack and fill plan.
2. Review `longform.md`, `xhs.md`, and `aibeike-fill-plan.json`.
3. Open 爱贝壳.
4. Paste or fill from the plan:
   - 文章: import the canonical blog URL, then target 微信公众号 / 知乎专栏 / X(Premium).
   - 动态: paste `xhs.md`, attach `cards/` images when available, then target 小红书 / 抖音(图文).
5. User confirms the final publish/sync action.

## Automation Boundary

Default automation stops before final publish.

- Safe: generate files, open 爱贝壳, copy content.
- Acceptable with review: use `aibeike-fill-plan.json` to fill 爱贝壳 forms.
- Do not default to clicking publish/sync. Only do so if the user explicitly asks for a submit mode.

## Verification

Run both mirrored test files when changing the generator:

```bash
bun run publish:check
```
