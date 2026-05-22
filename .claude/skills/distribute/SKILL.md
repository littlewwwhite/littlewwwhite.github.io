---
name: distribute
description: Generate platform-adapted versions of a blog post for cross-posting (Zhihu, WeChat, X, Xiaohongshu, Douyin, etc). Use when user says "/distribute", "分发", "生成社媒版本", "cross-post". Requires an already-written blog post as input.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# Distribute: Cross-Platform Content Generator

Generate platform-adapted versions from an existing Hugo blog post, preview them, and optionally cross-post.

**Prerequisite**: The blog post must already exist. Use `/publish` to deploy it first.

## Three Output Tiers

Each tier maps to a distinct platform philosophy — do not collapse them into one format.

| Tier | File | Length policy | Platforms | Rationale |
|---|---|---|---|---|
| **Full** | `article.md` | 100% — entire post | 知乎 / 微信公众号 / 今日头条 | Long-form readers expect the full argument; no condensation |
| **Essence** | `essence.md` | ~30% of source char count (±10%) | 小红书 / 抖音图文 | Scroll-feed readers need standalone value in seconds; keep concrete details, drop connective tissue |
| **X Thread** | `x-thread.md` | 5–8 tweets, ≤270 char each, with image cues | X / Twitter | Thread is X's native long-form unit; each tweet standalone, images on visual tweets |
| _Optional_ | `video.md` | Short script | 抖音视频 / 快手 / Bilibili | Generate only when source has a visual or narrative spine that translates to camera |

## Invocation

```
/distribute [path]
```

- **With path**: Use the specified Markdown file
- **Without path**: Auto-detect the most recently modified post

## Step 1: Resolve Source Post

### If path is provided:
- Read the file at the given path

### If no path is provided:
- Auto-detect the most recent post by modification time:
  ```bash
  find content/posts -name "index.md" -exec stat -f '%m %N' {} \; | sort -rn | head -1 | cut -d' ' -f2-
  ```
- Read the detected file
- Confirm with the user: "Detected most recent post: `<title>` at `<path>`. Proceed?"

Derive the slug from the directory name (e.g., `260410` from `content/posts/260410/index.md`).

## Step 1.5: Render Mermaid Diagrams to PNG

Extract all mermaid code blocks from the source post and render each to PNG for social media embedding.

```bash
# Extract each mermaid block (posts may have multiple)
# For each block, create a .mmd file and render with mmdc
cd <project-root>
mkdir -p _dist/<slug>

# Example for a single block (repeat for each, incrementing index):
sed -n '/^```mermaid$/,/^```$/p' <source-file> | sed '1d;$d' > _dist/<slug>/mermaid-1.mmd
mmdc -i _dist/<slug>/mermaid-1.mmd -o _dist/<slug>/mermaid-1.png -t neutral -b white --scale 3
```

- Use `-t neutral -b white --scale 3` for clean, high-resolution output suitable for all platforms
- Name files `mermaid-1.png`, `mermaid-2.png`, etc. in order of appearance
- If `mmdc` is not installed: `bun install -g @mermaid-js/mermaid-cli`

## Step 2: Generate Platform-Adapted Versions

Create output directory: `_dist/<slug>/`

Generate **3 mandatory tiers** (`article.md`, `essence.md`, `x-thread.md`) plus `meta.json`. Generate `video.md` **only** when the source post has clear visual or narrative spine suited for camera; otherwise skip.

### Source measurement (do this first)

Before writing any tier, measure the source's "body length" — total non-whitespace UTF-8 character count of the post body excluding frontmatter, code blocks, and mermaid blocks.

**Use Python, not awk `length()`** — awk counts bytes, which inflates CJK chars by 3×. Python's character counting is correct.

```bash
python3 -c "
import re
with open('content/posts/<slug>/index.md','r',encoding='utf-8') as f: t = f.read()
t = re.sub(r'^---\n.*?\n---\n', '', t, count=1, flags=re.DOTALL)  # strip frontmatter
t = re.sub(r'\`\`\`.*?\`\`\`\n?', '', t, flags=re.DOTALL)         # strip fenced blocks
print('body_chars:', sum(1 for c in t if not c.isspace()))
"
```

The **Essence tier target = source body length × 0.30 (±10%)**. For a 4000-char source, aim for 1080–1320 chars. Verify the essence with the same Python char count, not `wc -m` (which also counts bytes ambiguously).

### 2a. `article.md` — Full (知乎 / 微信公众号 / 今日头条)

Tier: **Full**. Keep 100% of the source.

Transformation rules:
- **Strip Hugo shortcodes**: Remove all `{{< ... >}}` and `{{% ... %}}` syntax
- **Replace mermaid code blocks with rendered images**: Replace each ` ```mermaid ... ``` ` block with `![diagram](mermaid-N.png "caption text")` when the target platform benefits from a visible caption, referencing the PNG rendered in Step 1.5. Match by order of appearance (first mermaid block → `mermaid-1.png`, etc.)
- **Convert image paths to absolute URLs**: Replace relative image references like `![alt](image.png)` with `![alt](https://littlewwwhite.github.io/posts/<slug>/image.png)`. For mermaid renders, use the `_dist/<slug>/` path since they are not deployed to the blog
- **Preserve all Markdown formatting**: Headers, lists, code blocks, tables, bold, italic
- **Add source attribution** at the end:
  ```markdown

  ---

  > Originally published at [zjding'Log](https://littlewwwhite.github.io/posts/<slug>/)
  ```
- **Keep the full content** — do not summarize or truncate

### 2b. `essence.md` — Essence, ~30% length (小红书 / 抖音图文)

Tier: **Essence**. The hardest output to generate well — it's not a summary, it's a **lossy compression that preserves all the concrete details and drops only the connective tissue**.

**Length policy (HARD constraint):**
- Default target: 30% of source body length (±10% slack). Verify with the Python char count from Source measurement above (NOT `wc -m`).
- Below 20% = information stripped beyond utility (unless cap applied). Above 40% = not condensed enough — re-cut.
- **Platform cap**: Xiaohongshu posts soft-cap around **1000–1500 chars** for engagement; beyond that, readers bounce.
- **Clamping rule**: `target_chars = min(source_body × 0.30, 1500)`. For short sources (≤4000 chars), 30% lands inside the cap naturally. For long sources (>5000 chars), the cap dominates and the essence becomes a tighter compression than 30% — explicitly state this in the preview stats line: `707 chars · 5.4% of source · capped at 1500`.

**What to KEEP (high-density signals):**
- Named entities, file paths, function signatures, version numbers, latency figures
- The single counterintuitive finding the source built toward
- The author's personal experience / project / incident (first-person)
- One concrete example illustrating the main point — not three

**What to DROP (low-density connective tissue):**
- Section transitions ("看到这里我以为...", "再往前走一步...")
- Parallel explanations of the same idea
- Industry-context paragraphs that don't carry new facts
- Code blocks (Xiaohongshu strips formatting anyway — paraphrase into prose)

**Structure (3–5 paragraphs, NOT bullets):**
1. One-line hook stating a specific finding (not a question)
2. 2–3 prose paragraphs — each paragraph carries one concrete fact/example, in conversational tone
3. Personal angle or first-person judgment (if source has one)
4. One-line landing — the conclusion at the highest altitude
5. 3–5 hashtags

**Tone & style:**
- 像在群里跟朋友讲今天看到一个有意思的事——有信息量但不端着
- 用口语、短句、自然的转折（"但是"、"说白了"、"有意思的是"），不用排比句式
- Emoji ≤ 2，只用在真正需要视觉分隔的地方，绝不每段开头放 emoji
- No code blocks. No links. No markdown formatting (Xiaohongshu strips it).

**Anti-patterns (instant rejection):**
- 每段开头 emoji + 冒号的列表格式（"🧠 Anthropic：xxx"）— AI-generated tell
- 排比句式（"A 是 xxx，B 是 xxx，C 是 xxx"）
- "你知道吗"、"太厉害了"、"建议收藏" 等营销话术
- High-level category labels instead of actual content
- Repeating the same point in different words to pad length

### 2c. `x-thread.md` — X-native thread (X / Twitter)

Tier: **X Thread**. X's native long-form unit is the thread, not the single tweet. Each tweet is a standalone idea; thread builds an argument.

**File format (machine-parseable, human-readable):**

```markdown
# X Thread — <post title>

## Tweet 1/N — hook
<text, ≤270 chars>
[image: <filename relative to _dist/<slug>/ or content/posts/<slug>/>]

---

## Tweet 2/N
<text, ≤270 chars>

---

## Tweet N/N — closing
<text> https://littlewwwhite.github.io/posts/<slug>/
[image: <filename if applicable>]
```

**Structure rules:**
- **5–8 tweets total** (less = thin, more = loses thread cohesion)
- **Tweet 1 (hook)**: state the most counterintuitive finding from the post in ≤270 chars — NOT a question, NOT a teaser. The hook must work standalone for readers who never expand the thread.
- **Tweets 2 to N-1 (body)**: each one tweet = one concrete insight, with at least one named entity / number / code reference. Each tweet readable without context.
- **Tweet N (closing)**: 1-sentence high-altitude takeaway + full blog URL. Do not put the blog link in the first tweet — X downranks tweets with external links in the open.

**Image attachment rules:**
- 1–3 image attachments total across the thread (not every tweet needs one)
- Attach an image to a tweet **only when the image directly illustrates that tweet's claim** — not as decoration
- Priority for image choice:
  1. Mermaid renders from the source post (`_dist/<slug>/mermaid-*.png`) — unique to this post
  2. Project original architecture diagrams downloaded into the post bundle (`content/posts/<slug>/*.svg|*.png`)
  3. Skip if no relevant image exists; do NOT auto-attach unrelated source images
- Mark image attachment as `[image: filename]` on its own line directly under the tweet text
- The tweet text should still make sense without the image (image complements, doesn't replace)

**Length & style:**
- ≤270 chars per tweet (leave headroom for X's URL-shortening; never hit 280 exactly)
- English or Chinese, same as source
- No hashtags inside body tweets; if used, only in closing tweet (≤2)
- One idea per tweet — if you find yourself using semicolons, split into two tweets

**Anti-patterns:**
- Numbering tweets in the text itself ("1/" "2/" — let the position markers `## Tweet N/N` do that, X auto-numbers in compose)
- Padding to hit a tweet count (5 strong tweets > 8 weak ones)
- Restating the title in tweet 1
- Putting the most specific insight in the closing tweet (front-load specifics, not back-load)

### 2d. `video.md` — Short video script (抖音视频 / 快手 / Bilibili)

**Generate only if source has a visual or narrative spine that translates to camera.** Skip otherwise — not every analysis post is video material.

Transformation rules:
- **Title**: ≤ 30 characters, attention-grabbing, can use「」for emphasis
- **Description**: 100-200 characters, conversational script outline
- **Structure**:
  1. `title:` — video title
  2. `hook:` — opening line that states a specific, counterintuitive fact (not a generic question)
  3. `script:` — 3-5 bullet points, each a concrete talking point with numbers/names/specifics
  4. `cta:` — closing call to action
  5. `tags:` — 3-5 hashtags
- **Tone**: Energetic, spoken-word friendly, as if narrating to camera
- **Focus on the single most interesting angle** from the blog post
- **Each script bullet must be sayable in one breath AND contain a specific fact**

### 2e. `meta.json` — Metadata file

```json
{
  "title": "<post title>",
  "slug": "<slug>",
  "date": "<post date>",
  "source": "<relative path to source file>",
  "generated_at": "<ISO 8601 timestamp>",
  "source_body_chars": <number>,
  "outputs": {
    "article": "article.md",
    "essence": "essence.md",
    "x-thread": "x-thread.md",
    "video": "video.md or null if skipped"
  },
  "essence_chars": <number>,
  "essence_ratio": <essence_chars / source_body_chars>,
  "x_thread_count": <number of tweets>,
  "blog_url": "https://littlewwwhite.github.io/posts/<slug>/"
}
```

## Step 3: Preview and Confirm

Display each generated version in the terminal with clear separators. Always show the length stats for `essence.md` (against 30% target) and the tweet count for `x-thread.md`.

```
========================================
📄 Full · article.md (知乎/微信公众号/今日头条)
========================================
<first 500 chars of article.md>
...

========================================
✨ Essence · essence.md (小红书/抖音图文)
Length: <N> chars  |  Source: <M> chars  |  Ratio: <N/M %>  |  Target: 30% (±10%)
========================================
<full essence.md content>

========================================
🧵 X Thread · x-thread.md (X/Twitter)
Tweets: <N>  |  With images: <K>
========================================
<full x-thread.md content>

========================================
🎬 Video · video.md (抖音视频/快手/Bilibili)  [omit section if not generated]
========================================
<full video.md content>

========================================
```

Then ask the user:
> "Preview generated. Options:\n1. Confirm and open browser preview\n2. Regenerate a specific tier (article/essence/x-thread/video)\n3. Edit manually then confirm\n4. Abort"

- If user chooses 2, ask which tier and what to change, then regenerate only that one
- If user chooses 3, wait for them to edit files in `_dist/<slug>/`, then proceed
- If user chooses 4, stop here

## Step 4: Generate Browser Preview

1. Read the template at `.claude/skills/distribute/references/preview-template.html`
2. Inject content into placeholders:
   - `{{TITLE}}` → post title
   - `{{ARTICLE_CONTENT}}`, `{{ESSENCE_CONTENT}}`, `{{XTHREAD_CONTENT}}`, `{{VIDEO_CONTENT}}` → HTML-escaped content for display
   - `{{ARTICLE_MD_ESCAPED}}`, `{{ESSENCE_MD_ESCAPED}}`, `{{XTHREAD_MD_ESCAPED}}`, `{{VIDEO_MD_ESCAPED}}` → backtick-escaped content for clipboard
   - `{{BLOG_URL}}` → blog URL
   - `{{ESSENCE_STATS}}` → e.g. `707 chars · 17.7% of source · target 30%`
   - `{{XTHREAD_STATS}}` → e.g. `7 tweets · 3 with images`
3. Write to `_dist/<slug>/preview.html` and open with `open _dist/<slug>/preview.html`

If `video.md` is omitted, leave its tab content empty / hidden (template handles gracefully).

## Step 5: Cross-Post via opencli

After preview is generated, publish per-tier. Each tier has its own publishing semantics — do not mix them.

**Prerequisite**: Run `opencli doctor` to verify daemon + browser extension are connected.

Ask the user:
> "Cross-post which tier?\n1. All three (Full + Essence + X Thread)\n2. Full only (知乎/微信公众号)\n3. Essence only (小红书/抖音)\n4. X Thread only\n5. Skip cross-posting"

### 5a. Full → 知乎 / 微信公众号

**No reliable CLI exists for either platform** (Zhihu blocks automation; WeChat OA requires authenticated service-account API). Cross-post pathway:

1. Open the browser preview: `open _dist/<slug>/preview.html`
2. From the "Full" tab → click `Copy Current Tab`
3. Paste into:
   - 知乎: 写文章 → paste Markdown (Zhihu's editor auto-converts)
   - 微信公众号: 草稿箱 → 新建 → paste through a MD→公众号 converter (md2wechat etc.) OR paste directly and re-style

Surface this guidance after preview opens. Do not attempt direct API publishing.

### 5b. Essence → Xiaohongshu (and Douyin imagetext via 爱贝壳)

```bash
SLUG=<slug>
IMGDIR="content/posts/$SLUG"
DISTDIR="_dist/$SLUG"
TITLE_TRUNC="$(head -1 _dist/$SLUG/meta.json | jq -r ... )"  # or pass explicitly

# Content: strip the hashtag line
CONTENT=$(sed '/^#[A-Za-z一-鿿]/d' "$DISTDIR/essence.md")

# Topics: extract hashtags without # prefix, comma-separated
TOPICS=$(grep -o '#[^ ]*' "$DISTDIR/essence.md" | tr -d '#' | tr '\n' ',' | sed 's/,$//')

# Images: mermaid renders first (most informative), then post bundle images, max 9
IMAGES=$(printf '%s,' "$DISTDIR"/mermaid-*.png "$IMGDIR"/*.png "$IMGDIR"/*.jpg "$IMGDIR"/*.svg 2>/dev/null | sed 's/,$//')

opencli xiaohongshu publish "$CONTENT" \
  --title "<post title, ≤20 chars>" \
  --images "$IMAGES" \
  --topics "$TOPICS"
```

- Xiaohongshu allows max 9 images. SVGs may not render — prefer PNG/JPG. Skip SVG if Xiaohongshu rejects.
- For 抖音图文: no CLI; user pastes the same `essence.md` content into 抖音 web 创作中心 (or routes through 爱贝壳同步助手).

### 5c. X Thread → X / Twitter

`opencli twitter post` only posts single tweets and does not return the new tweet URL, so true automated threading is brittle. Two paths:

**Path A (recommended) — post opening tweet via CLI, chain rest manually in browser:**

```bash
SLUG=<slug>
DISTDIR="_dist/$SLUG"
IMGDIR="content/posts/$SLUG"

# Parse tweet 1 from x-thread.md (text between "## Tweet 1" and the first "---")
TWEET1=$(awk '/^## Tweet 1/{f=1;next} /^---$/{if(f)exit} f && !/^\[image:/' "$DISTDIR/x-thread.md")

# Image for tweet 1, if any (line starting with [image: ...] under Tweet 1)
IMG1=$(awk '/^## Tweet 1/{f=1;next} /^---$/{if(f)exit} f && /^\[image:/{gsub(/^\[image: */,""); gsub(/\]$/,""); print; exit}' "$DISTDIR/x-thread.md")

if [ -n "$IMG1" ]; then
  # Resolve image path: try _dist first, then post bundle
  IMG_PATH="$DISTDIR/$IMG1"; [ -f "$IMG_PATH" ] || IMG_PATH="$IMGDIR/$IMG1"
  opencli twitter post "$TWEET1" --images "$IMG_PATH"
else
  opencli twitter post "$TWEET1"
fi
```

Then prompt: "Opening tweet posted. Go to x.com, click the tweet you just posted, and chain the remaining tweets from `_dist/<slug>/x-thread.md`. X's compose UI supports native threading via the '+' button."

**Path B — full manual paste**: open preview, copy tweets one by one, paste into X compose with native threading. Slower but no CLI fragility.

Default to Path A. Surface Path B if `opencli twitter post` returns an error.

### 5d. Publish summary

After all selected tiers finish, report:

```
| Tier          | Platforms                | Status | Detail |
|---------------|--------------------------|--------|--------|
| Full          | 知乎 / 微信公众号           | manual | preview opened, copy from tab |
| Essence       | 小红书 (+ 抖音 manual)     | ✅/❌  | <opencli result>              |
| X Thread      | X                        | ✅/❌  | opening tweet posted, N-1 left to chain |
```

## Error Handling

- If source file not found: report and abort
- If `_dist/` directory already exists for this slug: overwrite without asking (it's ephemeral)
- If `opencli doctor` shows extension disconnected: ask user to check browser extension, do not attempt publishing

## Important Notes

- `_dist/` is in `.gitignore` — generated files are ephemeral and local only
- Image URLs in `article.md` use the Hugo baseURL: `https://littlewwwhite.github.io/`
- All generated content should be in the same language as the source post
- The preview template is at `.claude/skills/distribute/references/preview-template.html`
- Cross-posting requires `opencli` v1.7.0+ with Chromium browser extension connected (`opencli doctor` to verify)
- All platforms require the user to be logged in via the browser that the opencli extension is connected to
