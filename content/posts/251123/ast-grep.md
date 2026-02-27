---
date: 2025-11-23
categories:
- 开发工具
- 代码搜索
tags:
- ast-grep
- Tree-sitter
- 代码重构
- CLI工具
title: ast-grep,具有更大想象空间的 grep 工具？
---

## 问题

"这个函数在哪被调用了？"

我敲下 `rg "getUserInfo"` 然后回车。屏幕刷出几十行结果——注释里的、字符串里的、真正的调用、还有一堆看起来像但其实不是的。

每次都这样，我花了比实际搜索更多的时间在过滤噪音上。跨行的函数调用？正则写到怀疑人生。想区分函数定义和函数调用？

然后我发现了 ast-grep。

## 它到底是什么

ast-grep 用 Tree-sitter 解析代码，生成语法树，然后让你用代码片段作为搜索模式。听起来很学术？其实很直观。

想找所有 `console.log` 调用：

```bash
ast-grep -p 'console.log($ARG)'
```

`$ARG` 是元变量，匹配任意参数。不是正则，是语法结构匹配。

这意味着：
- 注释里的 `console.log` 不会被匹配
- 字符串里的也不会
- 跨行的调用？自动处理

第一次用的时候，我盯着干净的搜索结果愣了几秒。

## 代码解析：它看到的世界

要理解 ast-grep 为什么有效，得先看看它眼中的代码长什么样。

这段 JavaScript：

```javascript
function greet(name) {
  console.log("Hello, " + name);
}
```

在 Tree-sitter 解析后变成：

```
program
└── function_declaration
    ├── name: identifier "greet"
    ├── parameters: formal_parameters
    │   └── identifier "name"
    └── body: statement_block
        └── expression_statement
            └── call_expression
                ├── function: member_expression
                │   ├── object: identifier "console"
                │   └── property: property_identifier "log"
                └── arguments
                    └── binary_expression
                        ├── left: string "Hello, "
                        ├── operator: "+"
                        └── right: identifier "name"
```

每个节点都有类型：`function_declaration`、`call_expression`、`identifier`。

当你写 `console.log($ARG)` 作为模式时，ast-grep 在树里找 `call_expression`，其中 `function` 是 `console.log`，`arguments` 可以是任意内容。

这就是为什么它能区分真正的调用和注释里的文本——注释在语法树里是 `comment` 节点，根本不会被 `call_expression` 模式匹配到。

## 和其他工具的对比

**ripgrep**：快，真的快。但它看到的是文本行，不是代码结构。ast-grep 看到的是语法树，它知道什么是函数、什么是类、什么是参数。代价是速度慢一点，但在大多数场景下仍然是亚秒级。

我的使用策略：先用 `rg` 快速扫一眼，需要精确匹配时切 ast-grep。

**Semgrep**：更偏安全审计，有污点分析、数据流追踪这些重型功能。ast-grep 更轻量，启动快，适合日常开发：找代码、写 lint 规则、批量重构。

如果你需要检测 SQL 注入的数据流，用 Semgrep。如果你想把所有 `var` 换成 `const`，ast-grep 更顺手。

## 真实案例：Bevy 0.14 迁移

Bevy 是 Rust 游戏引擎，0.14 版本有大量破坏性更新。社区用 ast-grep 写了迁移脚本。

一个典型的变更：`Timer::from_seconds(duration, false)` 改成 `Timer::from_seconds(duration, TimerMode::Once)`。

规则：

```yaml
id: timer-mode-migration
language: rust
rule:
  pattern: Timer::from_seconds($DURATION, false)
fix: Timer::from_seconds($DURATION, TimerMode::Once)
```

另一个：

```yaml
id: timer-mode-repeating
language: rust
rule:
  pattern: Timer::from_seconds($DURATION, true)
fix: Timer::from_seconds($DURATION, TimerMode::Repeating)
```

两条规则，几百个调用点，几分钟搞定。手动改？一天起步，还容易漏。

## 真实案例：React 19 forwardRef 迁移

React 19 改变了 ref 的传递方式。之前需要 `forwardRef` 包裹，现在直接作为 props 传递。

旧代码：

```jsx
const Input = forwardRef((props, ref) => {
  return <input ref={ref} {...props} />;
});
```

新代码：

```jsx
const Input = ({ ref, ...props }) => {
  return <input ref={ref} {...props} />;
};
```

迁移规则：

```yaml
id: remove-forwardref
language: tsx
rule:
  pattern: forwardRef(($PROPS, $REF) => { $$$BODY })
fix: |
  ({ $REF, ...$PROPS }) => { $$$BODY }
```

`$$$BODY` 匹配函数体内的所有语句。一条规则覆盖整个代码库的 `forwardRef` 调用。

## 结构化文档的应用

ast-grep 不只能处理代码。Tree-sitter 支持 JSON、YAML、HTML，这打开了新的可能。

**Kubernetes 配置审计** - 找所有没有指定镜像 tag 的 deployment：

```yaml
id: require-image-tag
language: yaml
rule:
  kind: block_mapping_pair
  has:
    kind: flow_node
    pattern: 'image: $IMG'
  not:
    has:
      pattern: 'image: $IMG:$TAG'
message: "镜像必须指定 tag，不要用 latest"
```

这比正则靠谱多了。正则会被 `# image: nginx` 这样的注释骗到，ast-grep 不会。

**HTML 无障碍检查** - 找所有没有 `alt` 属性的 `<img>` 标签：

```yaml
id: img-alt-required
language: html
rule:
  kind: element
  has:
    kind: tag_name
    regex: "^img$"
  not:
    has:
      kind: attribute
      has:
        kind: attribute_name
        regex: "^alt$"
message: "img 标签必须有 alt 属性"
```

**Markdown 文档规范** - 找所有一级标题（确保文档只有一个 h1）：

```yaml
id: single-h1
language: markdown
rule:
  kind: atx_heading
  has:
    kind: atx_h1_marker
```

把这些规则放进 CI，文档规范自动落地。

## 局限性与思考

ast-grep 理解语法，但不理解语义。它不知道变量的类型，不追踪数据流，不做跨文件分析。需要这些能力？还是得用 TypeScript 的类型检查、Semgrep 的污点分析、或者专门的静态分析工具。

仔细思考后会自然想到：ast-grep 是否能很好地结合其他结构化分析工具？

## 我的工作流

1. 日常搜索：`rg` 快速定位
2. 需要精确匹配：`ast-grep -p 'pattern'`
3. 批量修改：写 YAML 规则，`ast-grep scan --interactive` 逐个确认
4. CI 检查：把规则提交到仓库，`ast-grep scan` 自动 lint

## 总结

ast-grep 不是要替代 grep 或者 Semgrep。它填补的是中间地带：比文本搜索更精确，比完整静态分析更轻量。在"需要结构化精度、又要保持 CLI 速度"的场景下，它是个好工具，想象空间也很大。

试试看：`brew install ast-grep`

---

**参考资料**

- [ast-grep 官方文档](https://ast-grep.github.io/)
- [Bevy 迁移案例](https://ast-grep.github.io/blog/migrate-bevy.html)
- [React 19 迁移](https://dev.to/herrington_darkholme/migrate-to-react-19-with-ast-grep-28op)
