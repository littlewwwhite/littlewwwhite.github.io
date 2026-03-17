# Progression Patterns Reference

**Scope**: Deep structural analysis — how real articles achieve progression section-by-section. Use as calibration when building your Progression Spine in Step 3. For format examples (what Spine tables look like), see `examples.md`.

---

## Example 1: 同心圆展开 — 黄东旭《如何做 AI Agent 喜欢的基础软件》

**Source**: WeChat article, late 2025
**Progression**: Inside-out, from cognitive theory to business model

| # | Section | Core layer | 升维点 |
|---|---------|-----------|--------|
| 0 | Opening | Data anchor | 90% clusters created by Agent — establishes "this is already happening" |
| 1 | Heart Model | Cognitive/ontological | What does Agent understand? (innermost layer) |
| 2 | Extensibility | Abstraction | +How to evolve without breaking understanding (VFS/9PFS) |
| 3 | Interface Design | Interaction | +How Agent talks to systems (three constraints) |
| 4 | Infra Characteristics | Runtime | +What the system must look like underneath (disposable, cheap, parallel) |
| 5 | Business Model | Economic | +What this means for pricing and survival |
| 6 | Closing | Philosophical | "Welcome to the machine" — attitude shift |

**Why it works**: Each layer answers a question that the previous layer creates. "Agent understands old patterns" → "Then systems must be extensible" → "Then interfaces need these properties" → "Then infra must support disposable workloads" → "Then business models can't sell tokens."

**Key transitions**:
- Section 2→3: "但这并不意味着生态完全不重要" + "如果说前面讨论的是 Agent 更容易理解什么，那接口设计关注的就是另一个问题"
- Section 4→5: "不过这一点，我更想放到后面商业模式变化那一节里单独展开" (foreshadowing technique)

---

## Example 2: 认知升级线 — Manus《AI 代理的上下文工程》

**Source**: manus.im blog, July 2025
**Progression**: From mechanical optimization to meta-cognitive insight

| # | Section | Cognitive level | 升维点 |
|---|---------|----------------|--------|
| 0 | Prologue | Strategic decision | Why context engineering, not fine-tuning (personal narrative) |
| 1 | KV-Cache Design | Hardware/cost | Lowest level: cache hits save money |
| 2 | Masking, Not Removing | Runtime control | +Action space management: controlling what model can do |
| 3 | File System as Context | Architecture | +Memory externalization: model writes/reads files as structured memory |
| 4 | Attention via Recitation | Cognitive manipulation | +Model manipulates its own attention by rewriting todo.md |
| 5 | Keep Wrong Turns | Learning/epistemology | +Errors as learning signal — counter-intuitive: don't hide failures |
| 6 | Don't Be Trapped by Few-Shot | Meta-cognition | +Awareness of pattern-following bias — model level self-awareness |

**Why it works**: Each section requires the reader to think at a higher abstraction level. You cannot understand "attention via recitation" without first understanding "file system as context." The progression is: bits → actions → memory → attention → learning → meta-learning.

**Key technique**: "Stochastic Graduate Descent" humor in the prologue sets a personal, self-aware tone that carries through the entire piece.

---

## Example 3: 失败→发现叙事 — @trq212《Building Claude Code: Seeing like an Agent》

**Source**: X/Twitter thread, Feb 2025
**Progression**: Each tool design is told as a failure-discovery mini-arc

| # | Section | Discovery | 升维点 |
|---|---------|-----------|--------|
| 0 | Framework | "See like an agent" — math problem + tools analogy | Framing: tool design is empathy exercise |
| 1 | AskUserQuestion | Attempt 1 (ExitPlanTool) → confused model. Attempt 2 (markdown format) → unreliable. Attempt 3 (dedicated tool) → works | +First iteration cycle: tool as structured elicitation |
| 2 | Tasks/Todos | TodoWrite → model forgot. System reminders → model felt constrained. Task Tool → agents coordinate | +Second cycle: tools must evolve with model capability |
| 3 | Search Interface | RAG → fragile. Grep → model builds own context. Skills → progressive disclosure | +Third cycle: from giving context to model discovering context |
| 4 | Guide Agent | Info in system prompt → context rot. Link to docs → too much loaded. Subagent → answers directly | +Fourth cycle: progressive disclosure at meta level |

**Why it works**: The reader doesn't receive tips — they follow a team learning over time. Each section's discovery compounds: first you learn "structured tools help," then "tools must evolve," then "models can find their own context," then "disclosure can be layered." The lesson deepens.

**Key transition technique**: "As you'll see in the next example, what works for one model may not be the best for another" — explicit forward reference.

---

## Example 4: 期望→打碎→重建 — Anthropic《Effective Harnesses for Long-Running Agents》

**Source**: anthropic.com engineering blog, Nov 2025
**Progression**: Theoretical possibility → failure evidence → engineered solution → validation

| # | Section | Expectation level | 升维点 |
|---|---------|------------------|--------|
| 0 | Opening | "Agents should be able to work indefinitely" | Sets up expectation: compaction should solve it |
| 1 | Problem | Two failure modes: one-shotting + premature completion | Expectation shattered: compaction is NOT sufficient |
| 2 | Solution design | Initializer agent + coding agent (two-part architecture) | New architecture: shift analogy (each engineer leaves clean notes) |
| 3 | Environment | Feature list + init.sh + progress.txt + git | From architecture to concrete components |
| 4 | Coding agent | Incremental progress + clean state + structured updates | From setup to runtime behavior |
| 5 | Results | Before/after comparison with real output | Evidence that the solution works |

**Why it works**: The article first makes you believe something ("compaction should handle this"), then destroys that belief with evidence ("it doesn't — here are two specific failure patterns"), then rebuilds with a deeper understanding. The reader experiences the same "expectation → disappointment → insight" cycle the engineers went through.

**Key framing**: The "shift workers with amnesia" metaphor in the opening anchors the entire article — every subsequent section is about solving this specific metaphor.

---

## Example 5: 同心圆 + 升维混合 — zjding《预测市场里，0.50 的价格是信息最少的价格》(260305)

**Source**: zjding's own blog, best progression example
**Progression**: Single-static → single-extreme → single-dynamic → multi-contract → market-level

| # | Section | Scope | 升维点 |
|---|---------|-------|--------|
| 1 | 0.50 方差最大 | Single contract, static, common range | Starting point: estimation precision |
| 2 | Low probability blind spot | Single contract, static, extreme range | +Extreme region: from "imprecise" to "invisible" |
| 3 | Election night updates | Single contract, dynamic | +Time dimension: from snapshot to stream |
| 4 | Correlated contracts | Multi-contract relationships | +Inter-contract: from single to portfolio |
| 5 | Market efficiency | Market structure | +Participant structure: from math models to social mechanism |

**Why it works**: Each section adds exactly one new dimension. The reader's mental model expands in a controlled, predictable way. The explicit transition sentences ("前两个问题都是静态的", "前三个问题都是关于单个合约的") tell the reader exactly where they are in the escalation.

---

## Summary: How to Build a Progression Spine

1. **List your sections as thesis statements**
2. **For each pair of adjacent sections, answer**: "What new dimension does section N+1 open that section N didn't have?"
3. **If the answer is empty or "another example of the same thing"** → sections are parallel, not progressive
4. **Write the 升维点 column** — it should tell a coherent escalation story when read top-to-bottom
5. **Verify the last section is the highest altitude** — most abstract, most impactful
6. **Add explicit transition sentences** between every pair of sections using one of three techniques:
   - Name what changes (显式升维声明)
   - Reference a future section (伏笔接力)
   - Use previous conclusion as next premise (结论→前提)
