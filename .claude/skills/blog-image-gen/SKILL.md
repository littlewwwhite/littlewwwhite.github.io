---
name: blog-image-gen
description: Generate diagrams, illustrations, and infographics for blog posts using Gemini image generation (Nano Banana). Saves images directly to the post's Page Bundle directory and returns the markdown image tag.
allowed-tools: Bash, Read, Write
---

# Blog Image Generator

Generate contextual images for Hugo blog posts using Google Gemini's native image generation model (Nano Banana 2 / Pro).

## Models

| Codename | Model ID | Use case |
|---|---|---|
| **Nano Banana 2** | `gemini-3.1-flash-image-preview` | Fast, diagrams, flowcharts, infographics (default) |
| **Nano Banana Pro** | `gemini-3-pro-image-preview` | High-fidelity, complex reasoning, rich text rendering |

## Setup

Requires `google-genai` and `Pillow`:

```bash
pip install google-genai pillow
```

`GEMINI_API_KEY` must be set in `~/.claude/settings.json` env block (already configured).

## Workflow

When the user asks to generate an image for a blog post:

### Step 1: Identify context

- Current post directory (e.g., `content/posts/260305/`)
- Existing images in that directory (to pick the next filename: `1.png`, `2.png`, etc.)
- The concept to visualize

### Step 2: Craft the prompt

For **diagrams and flowcharts**, structure the prompt as:

```
Clean technical diagram: [description].
Style: flat design, white background, soft colors (#4A90D9 blues, #7ED321 greens, #F5A623 oranges).
Chinese labels preferred. Clear layout with arrows showing relationships.
No decorative elements, no photorealism. Optimized for blog embedding at 800px width.
```

For **conceptual illustrations**:

```
Minimal flat illustration: [concept].
Style: geometric shapes, icon-like, white or light background.
Simple color palette (2-3 colors). No text unless essential.
Suitable for technical blog post header.
```

### Step 3: Run the generator

```bash
python3 ~/.claude/skills/blog-image-gen/generate.py \
  --prompt "YOUR PROMPT" \
  --out "/path/to/post/dir" \
  --filename "1.png" \
  [--model pro]   # optional: use Nano Banana Pro for high-quality
```

### Step 4: Insert into markdown

After generation, insert the image tag at the appropriate location in `index.md`:

```markdown
![diagram description](1.png)
```

## Prompt Engineering Tips

- **Diagrams**: Describe each node and arrow explicitly. "Box A labeled '预测市场价格' connects with arrow to Box B labeled '概率估计'"
- **Flowcharts**: Specify direction (top-to-bottom or left-to-right), number of steps, decision diamonds
- **Infographics**: List every data point or label you want rendered. The model handles text well.
- **Avoid**: Photorealistic requests (use Imagen 4 instead), complex tables (use mermaid instead)

## When to Use Image vs Mermaid

| Situation | Recommendation |
|---|---|
| Simple flowchart / graph structure | **Mermaid** (renders natively, no token cost) |
| Conceptual illustration / visual metaphor | **Gemini image** |
| Infographic with mixed text + visuals | **Gemini image** |
| Architecture diagram with custom styling | **Gemini image** |
| Data chart / table | **Markdown table** |
