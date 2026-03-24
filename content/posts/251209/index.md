---
title: "Agent 和人类工程团队犯一模一样的错"
date: 2026-03-01
categories:
  - AI
  - Engineering
tags:
  - AI Agent
  - Software Engineering
  - System Design
---

让 Claude Opus 4.5 用一条指令构建一个 claude.ai 克隆——它失败了。但失败的方式比成功更有意思。

## 1. 失败模式和人类团队一模一样

把失败拆开看，每一条都和人类工程团队犯的错一模一样：

| 失败模式 | 人为版本 | Agent 版本 |
|---------|---------|-----------|
| 试图一次做完所有事 | 雄心勃勃的规划 | Context 耗尽，代码写到一半退出 |
| 过早宣布完成 | 对进度判断乐观 | 新 session 看到部分代码就说"做完了" |
| 测试不充分 | 赶着上线 | 标记 feature 完成，没有 E2E 验证 |
| 交接混乱 | 没写交接文档 | 留下无法解释的中间状态 |

这四条都不是模型智力问题，是**流程缺失问题**。

## 2. 双 Agent 架构：本质是 Tech Lead + 开发者

Anthropic 的解决方案是把工作拆成两个角色：

**Initializer Agent** 像 Tech Lead：
- 写 `run_dev.sh` 启动脚本
- 建一个 JSON 格式的 feature list（claude.ai 克隆有 200+ feature）
- 做第一次 git commit
- 留下清晰的交接文档

**Coding Agent** 像开发者：
- 每次 session 先读 git log 和 progress 文件，搞懂当前状态
- 选**一个**未完成的 feature
- 跑基础测试确保没把东西弄坏
- 实现这个 feature
- 用清晰 message 提交
- 更新进度文档

这个架构的核心不是"两个模型"，而是**结构化的责任分工**——和人-team 的组织方式一样。

## 3. WIP Limit：Kanban 原则的 AI 版本

最关键的约束：每次只做一个 feature。

这其实是 **Kanban WIP Limit** 的 AI 实现。人类工程团队早就验证过：当每个人同时做太多任务，吞吐量反而不升，质量下降。Agent 也不例外。

> 多任务并发是幻觉。人类大脑和 LLM 都是一样：表面上能并行处理，实际上是在快速上下文切换。

一旦给 Agent 加上"一次只做一个"的约束，它的行为就从"贪多嚼不烂"变成了可预测的增量交付。

## 4. 刚性格式：JSON 作为类型系统

一个有趣的发现：模型对 JSON 文件的篡改概率明显低于 Markdown 文件。

这不是偶然。JSON 的 schema 强制性相当于给 Agent 状态加了一个"类型系统"——你不能随便往一个定义好的字段塞别的内容。Markdown 的自由度太高，容易产生状态漂移。

这让我想到更广泛的原则：**给 Agent 的工作对象加结构，就是给它加护栏**。自由文本适合探索，结构化数据适合收敛。同样的逻辑也适用于数据库 schema、配置文件、甚至是 DSL。

## 5. 反馈回路要匹配领域

文章提到用 Puppeteer 做浏览器端到端测试，结果明显变好。这个洞察可以泛化：

| 领域 | 合适的反馈回路 |
|------|-------------|
| Web 开发 | 浏览器自动化（能看到实际渲染效果） |
| 数据科学 | 可视化输出（图表、统计摘要） |
| 基础设施 | 健康度检查（服务状态、延迟测试） |
| 游戏开发 | 游戏回放（能"看到"行为，不只看代码） |

Agent 需要的不是"更多代码能力"，而是"更多感知能力"——它能看到自己行为的真实后果，而不仅仅是代码层面的逻辑正确性。

## 我的判断

1. **Agent 基础设施的核心不是算法，是流程。** 把人类工程实践拆解成 Agent 可执行的约束（WIP limit、结构化交接、自动化测试、增量交付），比单纯堆模型更有效。

2. **格式刚性是一种控制抽象。** JSON schema、typed config、强约束的中间表示——这些不是限制创造力，而是给 Agent 提供可预测的"认知抓手"。

3. **更强的模型不会让这些 harness 变得不必要。** 就像资深工程师依然需要 code review 和 CI/CD，流程纪律与能力水平无关。事实上，能力越强，越容易"聪明地把自己绕进死胡同"，流程约束反而更重要。

Agent 不是在等一个更强大的模型，它需要的是一个更懂工程流程的 Harness。

## 延伸阅读

- [Effective harnesses for long-running agents — Anthropic Engineering](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
