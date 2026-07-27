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
