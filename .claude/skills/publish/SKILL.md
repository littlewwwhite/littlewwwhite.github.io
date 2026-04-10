---
name: publish
description: Publish a blog post to Hugo via git push. Validates frontmatter, commits, and deploys. Use when user says "/publish", "发布", "deploy post". Does NOT generate social media versions — use /distribute for that.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# Publish: Hugo Blog Deployer

Validate and deploy a Hugo blog post via git push. Single responsibility: get the post live.

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

## Step 3: Deploy via Git

Execute the following commands sequentially:

```bash
cd <project-root>
git add content/
git commit -m "publish: <post-title>"
git push origin main
```

- If `git push` fails, report the error and suggest resolution
- After successful push, derive the slug from the directory name (e.g., `260410` from `content/posts/260410/index.md`)
- Inform the user:

```
Post deployed. GitHub Actions will build and publish to:
https://littlewwwhite.github.io/posts/<slug>/

To generate social media versions, run: /distribute
```

## Error Handling

- If source file not found: report and abort
- If frontmatter is severely malformed (not valid YAML): attempt to fix, show diff, ask user to confirm
- If git operations fail: report error, do NOT retry automatically

## Important Notes

- The Hugo build and deploy is handled by GitHub Actions on push to `main`
- Frontmatter must have title, date, categories (1-2), tags (2-4)
- Image paths in the post should be relative Page Bundle format (`![alt](image.png)`)
