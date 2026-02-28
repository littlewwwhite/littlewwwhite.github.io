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

Generate the following files by transforming the source content:

### 3a. `article.md` — Long-form platforms (Zhihu / WeChat Official Account)

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

### 3b. `dynamic.md` — Short-form platforms (Xiaohongshu / Weibo / Douyin)

Transformation rules:
- **Maximum 300 characters** total (Xiaohongshu optimal length)
- **Format**: Punchy, scannable, one core message
- **Structure**:
  1. One-line hook (bold claim or question)
  2. 2-3 emoji-bulleted key points, each ≤ 1 sentence
  3. 2-3 hashtags (e.g., `#AI #技术分享`)
- **Tone**: Casual, like a friend sharing a discovery — not a summary
- **Do NOT include images, code blocks, or links**

### 3c. `thread.md` — Twitter/X post

Transformation rules:
- **1-2 tweets**, each **strictly ≤ 280 characters**
- **If 1 tweet**: The single most compelling insight + blog link
- **If 2 tweets**: First tweet is the hook, second adds context + blog link `https://littlewwwhite.github.io/posts/<slug>/`
- **Tone**: Concise, punchy, opinionated
- **Optionally 1-2 hashtags**
- **Do NOT pad** — if the core message fits in 1 tweet, use 1 tweet

### 3d. `meta.json` — Metadata file

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
    "thread": "thread.md"
  },
  "blog_url": "https://littlewwwhite.github.io/posts/<slug>/"
}
```

## Step 4: Preview and Confirm

Display each generated version in the terminal with clear separators:

```
========================================
📄 ARTICLE (Zhihu/WeChat)
========================================
<first 500 chars of article.md>
...

========================================
📱 DYNAMIC (Xiaohongshu/Weibo/Douyin)
========================================
<full dynamic.md content>

========================================
🐦 TWEET (Twitter/X)
========================================
<full thread.md content>

========================================
```

Then ask the user:
> "Preview generated. Options:\n1. Confirm and deploy\n2. Regenerate a specific version (article/dynamic/thread)\n3. Edit manually then confirm\n4. Abort"

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
2. Inject the content from all three generated versions into the template
3. Write the result to `_dist/<slug>/preview.html`
4. Open in browser:
   ```bash
   open _dist/<slug>/preview.html
   ```

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
