# Calibration Examples

Use these examples only to calibrate recurring failure modes. Do not copy their structure into every article.

## 1. Metric inventory versus reasoning

### Weak

```markdown
turbopuffer

- 冷 Namespace 与热 Namespace 的 p50、p95、p99
- 不同过滤选择率下的 Recall@K
- 写入返回到查询可见的时间
- Namespace 数量和大小变化

turbovec

- 2、3、4 bit 的内存占用和 Recall@K
- Float32、PQ 和 turbovec 对照
- ARM、AVX2、AVX-512 延迟
```

The list is scan-friendly but empty: it does not say what each measurement is trying to disprove, which variable comes first, or what result would change the decision.

### Better

```markdown
这两套系统不应该共用一张 Benchmark。测 turbopuffer 时，先固定文档、Query、过滤条件和 Top-K，只改变 Namespace 的冷热状态，观察 p50 到 p99 与 Recall 的变化。这个实验先回答对象存储换缓存的真实代价；只有尾延迟出现异常，再向下检查过滤选择率、Namespace 大小和分片。

turbovec 的主问题更集中：每省一倍内存，会损失多少召回。数据集、距离度量、Query、Top-K、线程数和硬件保持不变，只改变 2、3、4 bit，并保留 Float32 与 PQ 基线。校准规模、allowlist 和增删性能应由主曲线中的异常触发，而不是一开始全部摊开。
```

The information is not merely compressed. It now has experiment order, causality, and a decision boundary.

## 2. Keep evidence classes visible

### Weak

```markdown
turbovec 把向量压到 4 bit 后几乎不损失召回，而且速度提升明显，所以适合生产环境。
```

This sentence hides the source of the claim, test conditions, and uncertainty.

### Better

```markdown
在 turbovec 0.8.0、50,000 条 384 维随机单位向量、单线程的这次运行中，4 bit 索引是 Float32 原始矩阵的 1/7.83，Recall@10 为 0.8335。它证明压缩与召回必须一起读，但随机单位向量和共享容器 CPU 都不能代表生产数据，因此还不能推出“适合生产环境”。
```

The observation is exact; the interpretation is useful; the boundary prevents overclaiming.

## 3. Genuine friction versus manufactured humanity

### Weak

```markdown
经过一番曲折和不断尝试，我终于找到了答案。这个过程让我深刻意识到，技术选型从来没有银弹。
```

Nothing inspectable happened.

### Better

```markdown
第一遍没有跑到结果：`index.write()` 的类型提示看起来接受普通路径，但 Python Binding 不接收 `pathlib.Path`，必须显式转成 `str`。这个问题不改变性能结论，却说明文章不能只读 README；至少要让示例代码真正执行一次。
```

Keep the friction because it changes the method. Do not add emotion that was not observed.

## 4. A visual must add a relationship

### Weak

A Mermaid diagram repeats three sentences as three boxes connected in a row.

### Better

Use Mermaid when the reader needs to see that turbopuffer changes where bytes live while turbovec changes how many bytes each vector occupies. The diagram earns its place because the two independent axes are easier to compare spatially than in another paragraph.

## 5. Data-first opening versus situated opening

### Weak

```markdown
在 50,000×384 的随机单位向量上，2 bit、3 bit、4 bit 索引分别为 4.77、7.06、9.35 MiB，Recall@10 分别为 0.4755、0.7010、0.8335。
```

The numbers are valid, but the reader has not yet been given a reason to care about this particular comparison.

### Better

```markdown
小说 Agent 的检索还没有贵到需要立即迁移，但向量会随章节、角色和版本不断累积。真正需要提前弄清的，不是哪款库在一张榜单上更快，而是内存开始成为约束时，我们愿意拿多少召回去换空间。

这也是我重跑 turbovec 低比特量化实验的原因。它先回答一个更窄的问题：同一批向量从 Float32 压到 2、3、4 bit 后，空间与 Recall@10 怎样一起变化。
```

The situation and decision come first. The experiment now has a job instead of acting as the hook.

## 6. Flat formatting versus real hierarchy

### Weak

Five long sections all use only `##` headings, ordinary paragraphs, and one final table. The prose may be correct, but the reader cannot see which sentence is the decision, which is a boundary, and which mechanism deserves a pause.

### Better

Keep the causal explanation in prose, bold the term that changes the model, isolate the bounded decision in a clearly authored blockquote, show the exact comparison as a table or chart, and follow the visual with interpretation. The formats differ because their semantic jobs differ.

```markdown
**真正稳定复现的是空间—召回交换，不是速度排名。**

> 我的判断：在真实小说 Query 建立评测集之前，这组随机向量结果只能决定下一步测什么，不能决定是否迁移。
```

## 7. Visual deletion versus visual coverage

### Weak

The post keeps one architecture Mermaid because it is “necessary” and removes every other visual because the surrounding paragraphs contain the same facts.

### Better

Audit the reader’s mental work. If the article asks them to understand remote storage and cache topology, compare a 2/3/4-bit trade-off, and remember the difference between “moving bytes” and “shrinking bytes,” those are three different visual jobs:

- Mermaid for the exact storage and cache path;
- a deterministic chart for the bit-width/size/recall relationship;
- a concept illustration for the two intervention levels.

None should duplicate another. Together they reduce three different kinds of cognitive load.

## 8. Diagram habit versus semantic routing

### Weak

Every technical article receives a Mermaid flowchart. A two-step explanation becomes two boxes and an arrow; benchmark results remain a table even though the article discusses a trend; a retry protocol is flattened into another left-to-right flow.

The page contains more visuals, but each was chosen from habit rather than from the relationship.

### Better

Keep the two-step explanation as prose. Use a sequence diagram for the retry protocol because message order, waiting, and ownership matter. Generate the benchmark curve with Matplotlib because the claim concerns how recall changes with bit width, and preserve both the raw data and plotting script.

Use PlantUML instead of Mermaid only when a detailed sequence, component, class, or deployment view benefits from its richer notation and the Hugo publication path can render it. The objective is not to maximize Mermaid, PlantUML, or image count; it is to minimize the reader’s effort without weakening evidence.
