# Blog Skill Thinking Optimization Design

**Goal:** Upgrade blog-post-creator skill to produce original-feeling posts by adding an explicit thinking stage between reading source material and writing.

**Problem:** Current skill tends to produce "rewritten summaries" rather than posts with genuine original insight, despite guidelines saying "synthesize, don't summarize."

**Solution:** Insert a structured Think stage into the workflow. Claude must output a thinking note for user review before writing. This forces digestion → extension → original thesis formation.

## Design Decisions

1. **5-step workflow**: Gather → Think → Thesis → Write → Output
2. **Think output is visible** — user confirms/supplements before writing begins
3. **Thinking depth**: 感悟 (resonance) → 延伸 (extension with cases/analogies) → 原创观点 (original thesis)
4. **Citation style**: Zero inline references in body. End-of-post "延伸阅读" section with source links only.
5. **Tone**: All opinions presented as "我认为" — the post reads as fully original work.

## Files to Change

| File | Change |
|------|--------|
| `blog-post-creator/SKILL.md` | Rewrite workflow to 5 steps, add Think stage spec |
| `blog-post-creator/references/writing-guidelines.md` | Add "Thinking Depth" and "End-of-Post References" sections |
| `blog-post-creator/references/examples.md` | Add Think note example, add 延伸阅读 to existing examples |

## Think Stage Output Format

```markdown
## 📌 Source Key Points
- Article A argues X
- Article B argues Y

## 🤔 Reflections & Extensions
- X resonates because... [extend with case/analogy]
- Pushing Y to its extreme implies...
- An angle none of the sources mention: ...

## 🎯 My Article Thesis
- Not "A and B said X" but "I believe Z"
- Z is supported by digesting A+B + my own extensions

## 📎 References for 延伸阅读
- [Title](url)
```
