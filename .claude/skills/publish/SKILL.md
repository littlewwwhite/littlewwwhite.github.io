---
name: publish
description: Publish a blog post to Hugo and generate platform-adapted versions for cross-posting (Zhihu, Xiaohongshu, Twitter, etc.)
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# Publish: Cross-Platform Blog Publisher

Publish a Hugo blog post and generate platform-adapted content for cross-posting across multiple platforms.

## Invocation

```
/publish [path]
```

- **With path**: Use the specified Markdown file (e.g., `/publish content/posts/250315/index.md`)
- **Without path**: Auto-detect the most recently modified post

## Step 1: Resolve Source Post

### If path is provided:
- Read the file at the given path
- Verify it exists and contains valid Markdown with YAML frontmatter

### If no path is provided:
- Auto-detect the most recent post by modification time:
  ```bash
  find content/posts -name "index.md" -exec stat -f '%m %N' {} \; | sort -rn | head -1 | cut -d' ' -f2-
  ```
- Read the detected file
- Confirm with the user: "Detected most recent post: `<title>` at `<path>`. Proceed?"

## Step 2: Validate and Fix Frontmatter

Required frontmatter fields:
- `title`: string
- `date`: YYYY-MM-DD format
- `categories`: list with 1-2 items
- `tags`: list with 2-4 items

### Validation rules:
1. If `title` is missing, infer from the first `#` heading or the filename
2. If `date` is missing, infer from the directory name (YYMMDD format) or use today's date
3. If `categories` is missing, infer from the content topic
4. If `tags` is missing, infer from the content keywords
5. If any field was auto-inferred, show the user the proposed frontmatter and ask for confirmation before writing

### Fix any issues in-place:
- Write corrected frontmatter back to the source file
- Do NOT change any body content at this stage

## Step 3: Generate Platform-Adapted Versions

Derive the slug from the directory name (e.g., `250315` from `content/posts/250315/index.md`).

Create output directory: `_dist/<slug>/`

Generate the following files by transforming the source content.
These 4 types align with 爱贝壳内容同步助手's content tabs (文章/动态/图文/短视频).

### 3a. `article.md` — 文章 (Zhihu / WeChat Official Account / Toutiao)

Transformation rules:
- **Strip Hugo shortcodes**: Remove all `{{< ... >}}` and `{{% ... %}}` syntax
- **Convert image paths to absolute URLs**: Replace relative image references like `![alt](image.png)` with `![alt](https://littlewwwhite.github.io/posts/<slug>/image.png)`
- **Preserve all Markdown formatting**: Headers, lists, code blocks, tables, bold, italic
- **Add source attribution** at the end:
  ```markdown

  ---

  > Originally published at [zjding'Log](https://littlewwwhite.github.io/posts/<slug>/)
  ```
- **Keep the full content** — do not summarize or truncate

### 3b. `dynamic.md` — 动态 (X / Weibo / Jike / Threads)

Transformation rules:
- **Maximum 280 characters** (X-compatible, works for all dynamic platforms)
- **Format**: Single punchy statement or hot take
- **Structure**: One compelling insight + blog link `https://littlewwwhite.github.io/posts/<slug>/`
- **Optionally 1-2 hashtags**
- **Tone**: Concise, opinionated, conversational
- **Do NOT pad** — shorter is better
- **Do NOT include images, code blocks, or markdown formatting**

### 3c. `imagetext.md` — 图文 (Xiaohongshu / Douyin imagetext / Weishi)

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

### 3d. `video.md` — 短视频文案 (Douyin / Kuaishou / Bilibili)

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

### 3e. `meta.json` — Metadata file

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

## Step 4: Preview and Confirm

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
> "Preview generated. Options:\n1. Confirm and deploy\n2. Regenerate a specific version (article/dynamic/imagetext/video)\n3. Edit manually then confirm\n4. Abort"

- If user chooses 2, ask which version and what to change, then regenerate only that version
- If user chooses 3, wait for them to edit files in `_dist/<slug>/`, then proceed to deploy
- If user chooses 4, stop here

## Step 5: Deploy Hugo via Git

Execute the following commands sequentially:

```bash
cd <project-root>
git add content/
git commit -m "publish: <post-title>"
git push origin main
```

- If `git push` fails, report the error and suggest resolution
- After successful push, inform the user: "Post deployed. GitHub Actions will build and publish to https://littlewwwhite.github.io/posts/<slug>/"

## Step 6: Generate Browser Preview

1. Read the template at `.claude/skills/publish/references/preview-template.html`
2. Inject the content from all four generated versions into the template:
   - Replace `{{TITLE}}` with the post title
   - Replace `{{ARTICLE_CONTENT}}`, `{{DYNAMIC_CONTENT}}`, `{{IMAGETEXT_CONTENT}}`, `{{VIDEO_CONTENT}}` with the respective content
   - Replace `{{META_JSON}}` with the meta.json content
   - Replace `{{ARTICLE_MD_ESCAPED}}`, `{{DYNAMIC_MD_ESCAPED}}`, `{{IMAGETEXT_MD_ESCAPED}}`, `{{VIDEO_MD_ESCAPED}}` with backtick-escaped content for clipboard
   - Replace `{{BLOG_URL}}` with the blog URL
3. Write the result to `_dist/<slug>/preview.html`
4. Open in browser:
   ```bash
   open _dist/<slug>/preview.html
   ```
5. Inform the user: "Preview opened. Copy content from each tab and paste into 爱贝壳内容同步助手 to publish."

## Error Handling

- If source file not found: report and abort
- If frontmatter is severely malformed (not valid YAML): attempt to fix, show diff, ask user to confirm
- If git operations fail: report error, do NOT retry automatically
- If `_dist/` directory already exists for this slug: overwrite without asking (it's ephemeral)

## Important Notes

- `_dist/` is in `.gitignore` — generated files are ephemeral and local only
- The Hugo build and deploy is handled by GitHub Actions on push to `main`
- Image URLs in `article.md` use the Hugo baseURL: `https://littlewwwhite.github.io/`
- All generated content should be in the same language as the source post
- The preview template is at `.claude/skills/publish/references/preview-template.html`
