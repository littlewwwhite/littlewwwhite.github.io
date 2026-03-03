---
title: "AGENTS.md 省下的不是时间，是探索税"
date: 2026-03-04
categories:
  - AI
  - Engineering
tags:
  - AI Agent
  - Claude Code
  - 工程效率
  - Context Engineering
---

有一篇最近发表的论文测量了一件很多人只有直觉、没有数据的事：给 AI Coding Agent 一个 AGENTS.md 文件，它的执行效率会提升多少？

结论是：任务完成时间中位数减少 **28.64%**，输出 token 中位数减少 **16.58%**。

实验设计很扎实——10 个真实仓库，124 个 PR，配对受控：每个任务跑两次，一次有 AGENTS.md，一次没有，其他条件全部相同，Docker 隔离环境，去掉了所有变量。

这个数字不意外。但它背后的原因值得仔细想一想。

## Agent 每次运行都要交一笔探索税

给你一个陌生的 GitHub 仓库，让你去改一个功能。你第一件事会做什么？

读 README，看目录结构，找 `package.json` 或 `pyproject.toml` 看依赖，搜一下已有的类似实现，摸清楚命名习惯、测试风格、PR 规范……

AI Coding Agent 也会做一模一样的事。

这套"摸索过程"消耗的时间和 token 就是**探索税**：它不产出代码，但它是写出符合项目规范代码的前提条件。没有 AGENTS.md，这笔税每次运行都要重新交一遍，从零开始。

论文里的输出 token 数据最说明问题。输出 token 减少 16.58%，但输入 token（中位数）几乎没变。这意味着减少的不是写代码本身产生的 token，而是做决策时产生的 token——

> "这个项目用 CommonJS 还是 ESModule？"
> "测试文件应该放 `__tests__/` 还是和源文件同目录？"
> "函数命名应该用 camelCase 还是 snake_case？"

这些问题，人类看一眼 AGENTS.md 就解决了。Agent 没有这个文件，只能边探索边决策，每一次决策都要产生 token，然后在下一个任务里重新来一遍。

## AGENTS.md 的本质是上下文预编译

类比一下解释型语言和编译型语言。

Python 解释器每次运行脚本都要解析源码、生成字节码，这个过程是有成本的。C 编译器把这个成本前置：一次编译，之后每次执行都省去解析开销。

AGENTS.md 做的事情类似：把"理解这个项目"的成本前置到人类编写文档的阶段，而不是让 Agent 在每次任务开始时重新支付。

一次编写，摊销到所有后续运行。

这个算术很简单。假设 AGENTS.md 写好需要 2 小时（7200 秒）。每次任务节省 28 秒（论文中位数差值约 28 秒）。你需要 258 次 Agent 运行才能回本。

对于一个每天运行几十次 Agent 的团队，大概两周回本。之后每次运行都是纯利润。

## 我维护 CLAUDE.md 的真实体验

我自己的 CLAUDE.md 大概写了 200 行。我把这个体验拆开，哪类内容真正起作用。

**起作用最大的：约束式声明。**

```markdown
# Package Manager
- Always use `bun`, never `npm` or `pnpm`
- Always use `uv`, never `conda` or `pip` directly
```

这两行省掉的是什么？是 Claude 在每个新项目里先跑 `npm install` 被我打断，然后重新解释，然后跑 `bun install`——这个来回至少三轮对话。现在它直接用 bun，没有任何犹豫。

**起作用次大的：模式说明。**

```markdown
# Code Search
Use `augment-context-engine` codebase-retrieval as primary search tool,
not grep/find/ls
```

这告诉 Agent"当你需要找代码时，走这条路，不走那条路"。没有这条，Agent 会先试 grep，发现效果不够好，再换工具，每次都要走一遍试错流程。

**起作用最小的：项目描述。**

"这个项目是一个 Hugo 博客站点，技术栈是……" 这类说明对效率影响有限，因为 Agent 通过读文件结构也能得出类似结论。描述性内容不如约束性内容。

论文没有分析 AGENTS.md 的内容类型对效率的具体影响（这是他们列出的 future work 之一）。但从我的体验来看，**约定（convention）> 约束（constraint）> 描述（description）**，越接近"这件事只能这样做"的声明，Agent 就越不需要探索，效率越高。

## 反驳：过时的 AGENTS.md 比没有更坏

这个担忧是真实的。

论文的实验设计回避了这个问题——他们用的是 PR 合并时点对应版本的 AGENTS.md，保证了文档和代码状态同步。真实团队里没有这个保证。

如果你的 AGENTS.md 说"测试用 Jest"，但项目已经迁移到 Vitest，Agent 会乖乖写出错误的测试代码，比没有 AGENTS.md 时还难受——至少没有的时候它会去读 `package.json` 自己摸清楚。

所以 AGENTS.md 是一个需要当代码维护的文档，不是写完就忘的 README。

我的做法是把它纳入 PR review 流程：每次改了核心工具链或约定，顺手更新 AGENTS.md，就像更新依赖版本一样。这个额外成本不高，因为这类变更本来就不频繁。

## 这个模式会泛化

这篇论文测量的是 AGENTS.md 对 AI Coding Agent 的影响，但背后的逻辑不局限于代码场景。

任何需要 Agent 在运行时花时间"摸清楚"的东西，都可以通过预置上下文来省掉。

- **客服 Agent**：产品知识库、常见问题、话术规范——提前给，省掉 Agent 在工具调用里翻文档的 token
- **数据分析 Agent**：表结构说明、字段含义、业务规则——提前给，省掉 Agent 反复查 schema 的往返
- **代码审查 Agent**：项目 coding standard、review checklist——提前给，省掉 Agent 从零推断标准的过程

28.64% 不是一个特别神奇的数字。它说的是：**你知道但 Agent 不知道的东西，现在值这么多钱。**

把这些知识写下来。

---

## 延伸阅读

- [On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents — Lulla et al. (2026)](https://arxiv.org/abs/2601.20404)
