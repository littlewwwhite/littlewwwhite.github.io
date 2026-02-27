---
date: 2025-11-28
categories:
- 开发工具
- 代码搜索
tags:
- ast-grep
- PageIndex
- RAG
- 代码索引
- LLM
title: 代码搜索的下一形态：ast-grep 与 PageIndex 的双向增强
---

## 问题：代码搜索的两难困境

"这个项目的用户认证流程是怎么实现的？"

这个问题看似简单，但现有工具都不太好回答：

- **向量搜索**：把代码切成 chunks，做 embedding，然后相似度匹配。问题是"相似"不等于"相关"——搜"认证"可能返回一堆包含 `auth` 字符串的注释和配置文件，而不是真正的认证逻辑。

- **ast-grep**：能精确匹配代码结构，但你得先知道要搜什么模式。`ast-grep -p 'authenticate($USER)'`？还是 `login($$$)`？还是 `verify_token($TOKEN)`？不知道代码怎么写的，就不知道怎么搜。

- **grep/ripgrep**：快，但看到的是文本行，不是代码结构。注释里的、字符串里的、真正的调用，全混在一起。

这就是困境：**向量搜索不理解结构，结构搜索需要先知道模式**。

最近在研究 [PageIndex](https://github.com/VectifyAI/PageIndex) 和 [ast-grep](https://ast-grep.github.io/) 时，我发现这两个工具的结合可能是一个有趣的方向。

## 两个工具的核心能力

### ast-grep：代码的结构化视角

ast-grep 用 Tree-sitter 解析代码，生成语法树，然后让你用代码片段作为搜索模式。

```javascript
function greet(name) {
  console.log("Hello, " + name);
}
```

在 ast-grep 眼中，这不是三行文本，而是：

```
program
└── function_declaration
    ├── name: identifier "greet"
    ├── parameters: formal_parameters
    │   └── identifier "name"
    └── body: statement_block
        └── call_expression
            ├── function: member_expression (console.log)
            └── arguments: binary_expression
```

它知道什么是函数、什么是调用、什么是参数。这是**精确提取**的基础。

### PageIndex：文档的推理导航

PageIndex 的核心思路是：不用向量相似度，而是把文档转换成层级树结构（类似"目录"），然后让 LLM 在树上推理导航。

```
Financial Report 2024
├── Executive Summary (p.1-5)
├── Financial Statements (p.6-50)
│   ├── Balance Sheet (p.6-15)
│   ├── Income Statement (p.16-30)
│   └── Cash Flow (p.31-50)
└── Risk Factors (p.51-80)
```

当你问"公司的现金流状况如何"，LLM 不是做向量搜索，而是像人类专家一样：先看目录 -> 定位到 Financial Statements -> 找到 Cash Flow -> 读取 p.31-50 的内容。

这是**推理定位**的基础。

## 方向一：ast-grep 增强 PageIndex（构建代码的语义树索引）

第一个结合方向：用 ast-grep 的结构提取能力，为代码库构建 PageIndex 风格的层级索引。

### 代码库的"目录"应该长什么样？

传统的代码索引是文件列表：

```
src/
├── auth/
│   ├── login.ts
│   ├── logout.ts
│   └── token.ts
├── api/
│   ├── users.ts
│   └── orders.ts
└── utils/
    └── helpers.ts
```

这是**物理结构**，不是**语义结构**。

用 ast-grep 提取后，可以构建这样的语义树：

```
Authentication System
├── User Login Flow
│   ├── validateCredentials(email, password) -> boolean
│   │   └── Summary: 验证用户凭证，检查密码哈希
│   ├── createSession(userId) -> Session
│   │   └── Summary: 创建用户会话，设置过期时间
│   └── handleLoginError(error) -> Response
│       └── Summary: 处理登录失败，记录日志，返回错误信息
├── Token Management
│   ├── generateToken(payload) -> JWT
│   ├── verifyToken(token) -> Payload | null
│   └── refreshToken(oldToken) -> JWT
└── Session Cleanup
    └── cleanExpiredSessions() -> void
```

每个节点不是文件名，而是**语义单元**：函数、类、模块、关键逻辑块。每个节点带有：
- 函数签名
- 摘要（从注释或代码逻辑生成）
- 源码位置（文件:行号）

### 如何用 ast-grep 提取这些结构？

ast-grep 可以精确提取代码中的结构元素：

```yaml
# 提取所有函数定义
id: extract-functions
language: typescript
rule:
  any:
    - kind: function_declaration
    - kind: method_definition
    - kind: arrow_function
```

```yaml
# 提取类定义及其方法
id: extract-classes
language: typescript
rule:
  kind: class_declaration
  has:
    kind: method_definition
```

```yaml
# 提取模块导出
id: extract-exports
language: typescript
rule:
  kind: export_statement
```

把这些结构信息组织成树，就得到了代码库的"语义目录"。

### LLM 如何在代码树上推理？

有了语义树，LLM 可以像 PageIndex 处理文档一样处理代码：

```
用户：这个项目的用户认证流程是怎么实现的？

LLM 推理过程：
1. 查看代码树顶层结构
2. 定位到 "Authentication System" 节点
3. 展开子节点，看到 "User Login Flow"
4. 进一步展开，找到 validateCredentials、createSession、handleLoginError
5. 返回这些函数的摘要和位置
```

这比向量搜索靠谱——不会被 `// TODO: add authentication` 这样的注释干扰。

## 方向二：PageIndex 增强 ast-grep（推理导航 + 精确提取）

第二个结合方向：先用 PageIndex 风格的推理定位到相关区域，再用 ast-grep 做精确的结构化查询。

### 解决"不知道搜什么模式"的问题

ast-grep 的强大在于精确匹配，但前提是你知道要搜什么模式。

结合 PageIndex 的推理能力，可以这样工作：

```
用户：找出所有 API 请求失败后的重试逻辑

步骤 1：PageIndex 风格的推理导航
-> 分析代码树，定位到 src/services/http/ 目录
-> 找到 retry.ts 和 interceptor.ts
-> 识别出关键函数 withRetry()、retryOnError()

步骤 2：ast-grep 精确提取
-> 生成搜索模式：withRetry($FUNC, $OPTIONS)
-> 在整个代码库中搜索所有调用
-> 提取重试配置的具体参数
```

### 实际工作流示例

```
用户：这个项目里，数据库事务是怎么处理的？

系统：[PageIndex 推理]
分析代码树...
-> 定位到 src/database/ 模块
-> 找到 transaction.ts
-> 识别关键模式：withTransaction、beginTransaction、commit、rollback

系统：[ast-grep 精确提取]
搜索模式：withTransaction($CALLBACK)
找到 23 处调用

搜索模式：try { $$$BODY } catch ($ERR) { rollback($$$) }
找到 5 处手动事务处理

结果：
1. 主要使用 withTransaction 包装器（23 处）
2. 5 处手动事务处理，位于：
   - src/services/order.ts:145
   - src/services/payment.ts:89
   - ...
```

### 代码审计场景

这种结合在代码审计中特别有用：

```
用户：找出所有没有错误处理的外部 API 调用

系统：[PageIndex 推理]
-> 定位到所有 HTTP 客户端调用
-> 识别模式：fetch、axios、httpClient

系统：[ast-grep 精确提取]
搜索：fetch($URL) 且不在 try-catch 块内
搜索：axios.get($URL) 且不在 try-catch 块内

结果：
发现 12 处未处理的 API 调用：
- src/api/users.ts:34 - fetch(userEndpoint)
- src/api/orders.ts:78 - axios.get(orderUrl)
- ...
```

## 技术实现思路

### 索引构建流程

```
1. 代码解析
   └── ast-grep 遍历所有文件，提取结构元素

2. 语义分组
   └── 按模块/功能聚合相关函数和类

3. 摘要生成
   └── LLM 为每个节点生成简短摘要

4. 树构建
   └── 组织成 PageIndex 风格的层级结构

5. 索引存储
   └── 树结构 + 节点内容分表存储
```

### 在线检索流程

```
1. 问题理解
   └── 识别用户意图：查找、审计、理解、迁移

2. 树导航（PageIndex 风格）
   └── LLM 在代码树上推理，定位相关节点

3. 模式生成
   └── 根据定位结果，生成 ast-grep 搜索模式

4. 精确提取（ast-grep）
   └── 在代码库中执行结构化搜索

5. 结果组装
   └── 返回代码片段 + 位置 + 上下文
```

## 挑战与思考

### 1. 如何自动生成有意义的代码层级？

文档有目录，代码没有。需要启发式规则：
- 按目录结构初步分组
- 按 import/export 关系聚合
- 按命名约定识别功能模块
- LLM 辅助生成语义分组

### 2. 跨文件依赖如何表达？

代码的调用关系是图，不是树。可能的方案：
- 树结构表达主要层级
- 额外的"引用"字段表达跨节点依赖
- 或者接受"多棵树"的表达方式

### 3. LLM 推理成本如何控制？

每次查询都让 LLM 推理，成本太高。优化方向：
- 缓存常见查询的导航路径
- 用小模型做初步筛选，大模型做精确定位
- 预计算热门节点的摘要和关联

### 4. 增量更新如何处理？

代码库频繁变更，全量重建不现实：
- 监听文件变更，增量更新受影响的节点
- 定期全量校验，修复漂移

## 与现有方案的对比

| 方案 | 优势 | 劣势 |
|------|------|------|
| 向量搜索 | 语义理解，不需要精确模式 | 相似不等于相关，结构信息丢失 |
| ast-grep | 精确匹配，理解代码结构 | 需要先知道搜什么模式 |
| LSP/ctags | 精确的定义/引用跳转 | 只能点对点，不能语义查询 |
| **ast-grep + PageIndex** | 推理导航 + 精确提取 | 实现复杂，需要 LLM 成本 |

## 可能的应用场景

1. **代码库问答**："这个项目的缓存策略是什么？"
2. **代码审计**："找出所有 SQL 拼接（潜在注入风险）"
3. **代码迁移**："找出所有需要从 v1 API 升级到 v2 的调用"
4. **新人 onboarding**："这个模块的核心流程是什么？"
5. **代码评审辅助**："这个 PR 影响了哪些关键路径？"

## 总结

ast-grep 和 PageIndex 代表了两种不同的智能：
- **ast-grep**：精确的结构理解，"我知道代码长什么样"
- **PageIndex**：推理的导航能力，"我知道去哪里找"

把它们结合起来：
- **ast-grep 增强 PageIndex**：用结构提取构建语义索引
- **PageIndex 增强 ast-grep**：用推理导航指导精确搜索

这可能是代码搜索的下一个形态：**结构化理解 + 推理导航 + 精确提取**。

当然，这还只是想法。真正实现需要解决很多工程问题。但方向是清晰的：让 AI 像人类专家一样理解代码——先看结构，再定位，最后精确提取。

---

**参考资料**

- [ast-grep 官方文档](https://ast-grep.github.io/)
- [PageIndex - 基于推理的文档检索](https://github.com/VectifyAI/PageIndex)
- [Semantic Code Indexing with AST and Tree-sitter](https://medium.com/@email2dineshkuppan/semantic-code-indexing-with-ast-and-tree-sitter-for-ai-agents-part-1-of-3-eb5237ba687a)
- [PageIndex 技术详解](https://docs.pageindex.ai/)
