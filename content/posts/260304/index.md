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

有人把这件事量化了。

给 AI Coding Agent 一个 AGENTS.md 文件，任务完成时间中位数减少 **28.64%**，输出 token 中位数减少 **16.58%**。实验设计是配对受控：10 个真实仓库，124 个合并 PR，每个任务跑两次，一次有 AGENTS.md，一次没有，Docker 隔离环境，其他变量全部相同。

具体数字如下：

| 指标 | 无 AGENTS.md | 有 AGENTS.md | 降幅（中位数） |
|---|---|---|---|
| 完成时间（中位数）| 98.57 秒 | 70.34 秒 | -28.64% |
| 完成时间（均值）| 162.94 秒 | 129.91 秒 | -20.27% |
| 输出 token（中位数）| 2,925 | 2,440 | -16.58% |
| 输出 token（均值）| 5,744 | 4,591 | -20.08% |
| 输入 token（中位数）| 几乎不变 | 几乎不变 | ~0% |

最后一行是关键。输入 token 基本没动，输出 token 降了 16%。减少的不是"写代码"的部分，是"做决策"的部分。

## Agent 每次运行都要交一笔探索税

给你一个陌生的 GitHub 仓库，让你去改一个功能。第一件事是什么？

读 README，看目录结构，找 `package.json` 或 `pyproject.toml` 看依赖，搜一下已有的类似实现，摸清命名习惯、测试风格、PR 规范……

AI Coding Agent 做完全一样的事。区别是它用 token 来做，每次启动都要重新来一遍。

这套"摸索过程"消耗的时间和 token 就是**探索税**：不产出代码，但是写出符合项目规范的代码的前提。没有 AGENTS.md，这笔税每次运行都要从零开始交。

探索税的形态，具体来说是这类决策：

> "这个项目用 CommonJS 还是 ESModule？"
> "测试文件放 `__tests__/` 还是和源文件同目录？"
> "函数命名用 camelCase 还是 snake_case？"
> "这里应该抛异常还是返回 null？"

人类看一眼 AGENTS.md 就解决了。Agent 没有这个文件，只能边探索边决策，每轮对话产生 token，下次还要重来。

## AGENTS.md 是上下文预编译

Python 解释器每次运行脚本都要解析源码、生成字节码。C 编译器把这个成本前置：一次编译，之后每次执行不再重复解析。

AGENTS.md 做同样的事：把"理解这个项目"的成本从运行时移到人类编写文档的阶段。一次编写，摊销到所有后续运行。

算术很直接。论文里中位数差值约 28 秒/次（98.57 → 70.34）。假设写好 AGENTS.md 需要 2 小时，那你需要 **258 次 Agent 运行**才能回本：

```
7200 秒 ÷ 28 秒/次 ≈ 258 次
```

一个每天跑几十次 Agent 的团队，两周内全部回收。之后每次运行都是纯节省。

实验的可信度值得多说一句。研究者把每个仓库还原到 PR 合并前的精确 commit 状态，用对应时间点的 AGENTS.md 版本，保证文档和代码同步。对没有足够上下文的 PR，用本地语言模型生成标准化的 GitHub issue 格式任务描述，确保输入一致。人工检查了 50 个输出样本，确认都是"非空、非平凡的代码改动"——排除了 Agent 偷懒或乱写的干扰。这种设计下，28% 的差异很难归因于噪声。

## 什么内容最值得写进 AGENTS.md

论文没有分析 AGENTS.md 的内容类型对效率的具体影响，这是他们列出的 future work。但从我维护 CLAUDE.md 的体验来看，有效性差距非常大。

**效果最好：约束式声明。**

```markdown
# Package Manager
- Always use `bun`, never `npm` or `pnpm`
- Always use `uv`, never `conda` or `pip` directly
```

这两行省掉了什么？是 Claude 在每个项目里先跑 `npm install` 被我打断，重新解释，再跑 `bun install` 的来回。这个往返至少三轮对话，每次都要产生解释性输出。现在直接跳过。

约束声明起作用，因为它把一个需要探索才能回答的问题变成了零探索的事实。Agent 不需要去读 `package.json` 再推断，直接用。

**效果次之：路径说明。**

```markdown
# Code Search
Use `augment-context-engine` codebase-retrieval as primary search tool,
not grep/find/ls

# Testing
Run tests with `bun test`, not `npm test` or `pytest`
```

这类说明给了 Agent 明确的"走哪条路"。没有它，Agent 会先试一条路，发现效果不够好，再换，每次试错都要来回几轮。

**效果最差：项目描述。**

"这个项目是一个 Hugo 博客站点，使用 Tailwind CSS 和……" Agent 通过读文件结构能自己推断出类似结论。描述性内容减少的探索最少，因为 Agent 本来就会做这个探索。

规律是：**越接近"这件事只能这样做"的声明，消除的探索越多。**

## 过时的 AGENTS.md 比没有更坏

这是真实的风险，必须正视。

论文的实验设计回避了这个问题——用的是 PR 合并时点对应的 AGENTS.md 版本，保证文档和代码一直同步。真实团队没有这个保证。

如果 AGENTS.md 写的是"测试框架用 Jest"，但项目已经迁移到 Vitest，Agent 会照着写出不能运行的测试，而且它并不知道自己错了。比没有 AGENTS.md 更难受——至少没有的时候，它会去读 `package.json` 自己发现当前用的是什么。

AGENTS.md 必须当代码文档维护，不是写完就忘的东西。

我的做法：把它加入 PR review checklist。每次改了技术栈、包管理器、测试框架、目录结构等核心约定，顺手更新 AGENTS.md，和改 `package.json` 的 scripts 是同一个动作。这类变更在一个正常演进的项目里频率不高，额外成本可以接受。

## 同样的逻辑适用于所有 Agent 场景

这篇论文测量的是编码场景，但预置上下文减少探索的逻辑不限于这里。

- **客服 Agent**：产品知识库、退款规则、话术边界——提前给，省掉 Agent 每次在工具调用里翻文档的往返
- **数据分析 Agent**：表结构说明、字段业务含义、NULL 值语义——提前给，省掉 Agent 反复查 schema 和写错 JOIN 的来回
- **代码审查 Agent**：项目 coding standard、安全禁用项、review checklist——提前给，省掉 Agent 从零推断团队标准的过程

每个场景里，Agent 都要付"探索税"。区别只是探索的对象从代码库变成了业务规则、数据模型或审查标准。

28.64% 不是一个神奇的数字。它说的是：**你已经知道的东西，Agent 不知道，所以它要花时间去发现，这个发现过程有成本。** 把这些知识写下来，成本就消失了。

---

## 延伸阅读

- [On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents — Lulla et al. (2026)](https://arxiv.org/abs/2601.20404)
