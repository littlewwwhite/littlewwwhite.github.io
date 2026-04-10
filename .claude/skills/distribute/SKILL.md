---
name: distribute
description: Generate platform-adapted versions of a blog post for cross-posting (Zhihu, WeChat, X, Xiaohongshu, Douyin, etc). Use when user says "/distribute", "分发", "生成社媒版本", "cross-post". Requires an already-written blog post as input.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# Distribute: Cross-Platform Content Generator

Generate platform-adapted versions from an existing Hugo blog post, preview them, and optionally cross-post.

**Prerequisite**: The blog post must already exist. Use `/publish` to deploy it first.

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

## Step 2: Generate Platform-Adapted Versions

Create output directory: `_dist/<slug>/`

Generate the following files by transforming the source content.
These 4 types align with 爱贝壳内容同步助手's content tabs (文章/动态/图文/短视频).

### 2a. `article.md` — 文章 (Zhihu / WeChat Official Account / Toutiao)

Transformation rules:
- **Strip Hugo shortcodes**: Remove all `{{< ... >}}` and `{{% ... %}}` syntax
- **Strip mermaid code blocks**: Remove ` ```mermaid ... ``` ` blocks (these platforms don't render mermaid)
- **Convert image paths to absolute URLs**: Replace relative image references like `![alt](image.png)` with `![alt](https://littlewwwhite.github.io/posts/<slug>/image.png)`
- **Preserve all Markdown formatting**: Headers, lists, code blocks, tables, bold, italic
- **Add source attribution** at the end:
  ```markdown

  ---

  > Originally published at [zjding'Log](https://littlewwwhite.github.io/posts/<slug>/)
  ```
- **Keep the full content** — do not summarize or truncate

### 2b. `dynamic.md` — 动态 (X / Weibo / Jike / Threads)

Transformation rules:
- **Maximum 280 characters** (X-compatible, works for all dynamic platforms)
- **Format**: Single punchy statement or hot take
- **Structure**: One compelling insight + blog link `https://littlewwwhite.github.io/posts/<slug>/`
- **Optionally 1-2 hashtags**
- **Tone**: Concise, opinionated, conversational
- **Do NOT pad** — shorter is better
- **Do NOT include images, code blocks, or markdown formatting**

### 2c. `imagetext.md` — 图文 (Xiaohongshu / Douyin imagetext / Weishi)

Transformation rules:
- **Maximum 800 characters** (Xiaohongshu optimal range)
- **Format**: Visual, scannable, emoji-rich
- **Structure**:
  1. One-line hook (bold claim or question)
  2. 3-5 emoji-bulleted key points, each ≤ 1 sentence
  3. Brief closing thought or call to action
  4. 3-5 hashtags (e.g., `#AI #技术分享 #编程`)
- **Tone**: Casual, like a friend sharing a discovery
- **Do NOT include code blocks or links** (Xiaohongshu strips links)
- **Designed to pair with images** — reference visual content if the source post has images

### 2d. `video.md` — 短视频文案 (Douyin / Kuaishou / Bilibili)

Transformation rules:
- **Title**: ≤ 30 characters, attention-grabbing, can use「」for emphasis
- **Description**: 100-200 characters, conversational script outline
- **Structure**:
  1. `title:` — video title
  2. `hook:` — opening line to grab attention (≤ 1 sentence)
  3. `script:` — 3-5 bullet points as talking points
  4. `cta:` — closing call to action
  5. `tags:` — 3-5 hashtags
- **Tone**: Energetic, spoken-word friendly, as if narrating to camera
- **Focus on the single most interesting angle** from the blog post

### 2e. `meta.json` — Metadata file

```json
{
  "title": "<post title>",
  "slug": "<slug>",
  "date": "<post date>",
  "source": "<relative path to source file>",
  "generated_at": "<ISO 8601 timestamp>",
  "outputs": {
    "article": "article.md",
    "dynamic": "dynamic.md",
    "imagetext": "imagetext.md",
    "video": "video.md"
  },
  "blog_url": "https://littlewwwhite.github.io/posts/<slug>/"
}
```

## Step 3: Preview and Confirm

Display each generated version in the terminal with clear separators:

```
========================================
📄 文章 (Zhihu/WeChat/Toutiao)
========================================
<first 500 chars of article.md>
...

========================================
💬 动态 (X/Weibo/Jike/Threads)
========================================
<full dynamic.md content>

========================================
📸 图文 (Xiaohongshu/Douyin imagetext)
========================================
<full imagetext.md content>

========================================
🎬 短视频 (Douyin/Kuaishou/Bilibili)
========================================
<full video.md content>

========================================
```

Then ask the user:
> "Preview generated. Options:\n1. Confirm and open browser preview\n2. Regenerate a specific version (article/dynamic/imagetext/video)\n3. Edit manually then confirm\n4. Abort"

- If user chooses 2, ask which version and what to change, then regenerate only that version
- If user chooses 3, wait for them to edit files in `_dist/<slug>/`, then proceed
- If user chooses 4, stop here

## Step 4: Generate Browser Preview

1. Read the template at `.claude/skills/distribute/references/preview-template.html`
2. Inject the content from all four generated versions into the template:
   - Replace `{{TITLE}}` with the post title
   - Replace `{{ARTICLE_CONTENT}}`, `{{DYNAMIC_CONTENT}}`, `{{IMAGETEXT_CONTENT}}`, `{{VIDEO_CONTENT}}` with HTML-escaped content for display
   - Replace `{{ARTICLE_MD_ESCAPED}}`, `{{DYNAMIC_MD_ESCAPED}}`, `{{IMAGETEXT_MD_ESCAPED}}`, `{{VIDEO_MD_ESCAPED}}` with backtick-escaped content for clipboard
   - Replace `{{BLOG_URL}}` with the blog URL
3. Write the result to `_dist/<slug>/preview.html`
4. Open in browser:
   ```bash
   open _dist/<slug>/preview.html
   ```
5. Inform the user: "Preview opened. Copy content from each tab and paste into 爱贝壳内容同步助手 to publish."

## Step 5: Cross-Post via opencli-rs (optional)

After the preview is generated, offer to publish directly to supported platforms using `opencli-rs`.

Ask the user:
> "Cross-post to platforms? Select all that apply:\n1. Twitter/X (from dynamic.md)\n2. Xiaohongshu (from imagetext.md)\n3. Skip cross-posting"

### 5a. Twitter/X

Read `_dist/<slug>/dynamic.md` and post:

```bash
opencli-rs twitter post "<content of dynamic.md>"
```

- The dynamic.md content is already ≤280 chars and optimized for Twitter
- Report success/failure to the user

### 5b. Xiaohongshu

Read `_dist/<slug>/imagetext.md` and the source post's images, then publish:

```bash
opencli-rs xiaohongshu publish \
  --title "<post title, truncated to 20 chars>" \
  --images "<comma-separated paths to post images>" \
  --topics "<hashtags from imagetext.md, without # prefix, comma-separated>" \
  "<content of imagetext.md, stripped of hashtag lines>"
```

- Extract hashtags from the imagetext.md content (lines starting with `#`)
- Strip hashtag lines from the content body before passing as `<content>`
- Use `--draft true` by default for safety; ask the user if they want to publish directly
- Images: collect all `.png`, `.jpg` files from the source post directory
- Report success/failure to the user

### 5c. Future platforms

As `opencli-rs` adds publishing support for more platforms (Weibo, WeChat, etc.), extend this step accordingly. Check available commands with:

```bash
opencli-rs <platform> --help
```

## Error Handling

- If source file not found: report and abort
- If `_dist/` directory already exists for this slug: overwrite without asking (it's ephemeral)

## Important Notes

- `_dist/` is in `.gitignore` — generated files are ephemeral and local only
- Image URLs in `article.md` use the Hugo baseURL: `https://littlewwwhite.github.io/`
- All generated content should be in the same language as the source post
- The preview template is at `.claude/skills/distribute/references/preview-template.html`
- Cross-posting requires `opencli-rs` installed with Chrome extension connected (`opencli-rs doctor` to verify)
- Twitter and Xiaohongshu cross-posting require the user to be logged in via the Chrome extension's session reuse
