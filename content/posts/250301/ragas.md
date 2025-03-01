---
date: '2025-03-01'
categories:
- 人工智能
- 自然语言处理
tags:
- Ragas
- LLM评估
- 文本摘要
- RAGAs
title: Ragas 评估使用指南
---


# Ragas 评估指南

以下是Ragas-LLM-app的简单介绍，内容主要介绍使用 Ragas 评估简单 LLM 应用，RAG，以及综合流程的处理方法。

## Ragas 是什么
Ragas 是一个用于评估 LLM 应用的工具，支持多种指标，包括非 LLM 指标和基于 LLM 的指标。 RAGAs 框架定义了四个核心评估指标 ——context_relevancy（上下文相关性）、context_recall（上下文回溯）、faithfulness（忠实度）和 answer_relevancy（答案相关性）—— 这四个指标共同构成了 RAGAs 评分体系。

我们已经知道，简历一个 RAG 其实并不复杂，但是如果要将其应用到生产环境中，你不得不面对非常多的挑战，不同组件之间生成的数据是否能够满足自己的需求？数据的质量是否达标等等，这些问题都是需要我们考虑的，而 Ragas 就是帮助我们解决这些问题的工具。

目前学术界和工业界对于 RAG 的评估并没有一个统一的标准，传统的指标如：[ROUGE](https://aclanthology.org/W04-1013/)、[BLEU](https://www.aclweb.org/anthology/P02-1040/) 、[ARES](https://arxiv.org/abs/2311.09476)等，这些指标在评估 RAG 时稍显落后，于是乎 [RAGAs](https://arxiv.org/pdf/2309.15217v1) 诞生了。

### 评估方法
1. **非 LLM 指标**：使用 BleuScore 评分
```python
from ragas import SingleTurnSample
from ragas.metrics import BleuScore

test_data = {
    "user_input": "summarise given text\nThe company reported an 8% rise in Q3 2024, driven by strong performance in the Asian market. Sales in this region have significantly contributed to the overall growth. Analysts attribute this success to strategic marketing and product localization. The positive trend in the Asian market is expected to continue into the next quarter.",
    "response": "The company experienced an 8% increase in Q3 2024, largely due to effective marketing strategies and product adaptation, with expectations of continued growth in the coming quarter.",
    "reference": "The company reported an 8% growth in Q3 2024, primarily driven by strong sales in the Asian market, attributed to strategic marketing and localized products, with continued growth anticipated in the next quarter."
}
metric = BleuScore()
test_data = SingleTurnSample(**test_data)
metric.single_turn_score(test_data)
```
测试样本包含 用户输入、响应（来自 LLM 的输出）和 参考（来自 LLM 的预期输出），作为评估摘要的数据点。输出为一个得分:
```
0.137
```

- 缺点：
  - 准备参考数据耗时且评分可能不准确,即使 response 和 reference 相似，输出的分数也很低
  - 需要准备参考数据，如果数据量很大，这个过程会非常耗时。
- 优点：
  - 快速评估，不需要复杂的配置。

2. **基于 LLM 的指标**：使用 AspectCritic 等，输出通过/失败结果（如 1 表示通过，0 表示失败），支持模型包括 GPT-4o、Claude、Gemini 和 Azure。

第一步：安装 langchain-openai
```bash
pip install langchain-openai
```

确保你已经准备好 OpenAI 密钥并可用

```python
import os
os.environ["OPENAI_API_KEY"] = "your-openai-key"
```

将你的 LLMs 包装在 LangchainLLMWrapper 中，以便与 ragas 一起使用

```python
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o"))
evaluator_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings())
```

评估指标:这里我们将使用 AspectCritic，这是一个基于 LLM 的指标，输出通过/失败结果。

```python
from ragas import SingleTurnSample
from ragas.metrics import AspectCritic

test_data = {
    "user_input": "summarise given text\nThe company reported an 8% rise in Q3 2024, driven by strong performance in the Asian market. Sales in this region have significantly contributed to the overall growth. Analysts attribute this success to strategic marketing and product localization. The positive trend in the Asian market is expected to continue into the next quarter.",
    "response": "The company experienced an 8% increase in Q3 2024, largely due to effective marketing strategies and product adaptation, with expectations of continued growth in the coming quarter.",
}

metric = AspectCritic(name="summary_accuracy",llm=evaluator_llm, definition="Verify if the summary is accurate.")
test_data = SingleTurnSample(**test_data)
await metric.single_turn_ascore(test_data)
```

输出:成功通过，输出 1 表示通过，0 表示失败
```
1
```


### 数据集与结果
RAGAs 支持从 Hugging Face 加载数据集，如 "explodinggradients/earning_report_summary"，包含 50 个样本，特征包括 user_input 和 response，生成的结果可导出到 pandas 分析，或通过 [app.ragas.io](https://app.ragas.io/) 进行交互式分析。

### 意外细节
除了常见指标，内容还提到可以通过注释 15-20 个样本并训练自定义指标来改进评估，涉及上传到 [app.ragas.io](https://app.ragas.io/) 并使用 Ragas APP token，这可能是用户未预料到的额外步骤。

---

### 详细报告

以下是链接 [https://docs.ragas.io/en/latest/getstarted/evals/](https://docs.ragas.io/en/latest/getstarted/evals/) 内容的全面翻译，内容结构化呈现，涵盖所有细节，适合深入了解。

数据集格式至少包含 user_input 和 response 字段，如下所示：
```python
[
    # Sample 1
    {
        "user_input": "summarise given text\nThe Q2 earnings report revealed a significant 15% increase in revenue, ...",
        "response": "The Q2 earnings report showed a 15% revenue increase, ...",
    },
    # Additional samples in the dataset
    ....,
    # Sample N
    {
        "user_input": "summarise given text\nIn 2023, North American sales experienced a 5% decline, ...",
        "response": "Companies are strategizing to adapt to market challenges and ...",
    }
]
```
然后通过以下方法进行使用：

```python
from datasets import load_dataset
from ragas import EvaluationDataset
eval_dataset = load_dataset("explodinggradients/earning_report_summary",split="train")
eval_dataset = EvaluationDataset.from_hf_dataset(eval_dataset)
print("Features in dataset:", eval_dataset.features())
print("Total samples in dataset:", len(eval_dataset))

# 输出
# Features in dataset: ['user_input', 'response']
# Total samples in dataset: 50

from ragas import evaluate

results = evaluate(eval_dataset, metrics=[metric])
results

# 输出
# {'summary_accuracy': 0.84}

```

再将结果导出到 pandas 进行分析：

```python
results.to_pandas()
```

```csv
# 输出
#   user_input response  summary_accuracy
# 0  summarise given text\nThe Q2 earnings report revealed a significant 15% increase in revenue, ...  The Q2 earnings report showed a 15% revenue increase, ...  0.84
# 1  summarise given text\nIn 2023, North American sales experienced a 5% decline, ...  Companies are strategizing to adapt to market challenges and ...  0.84
```

一个例子如下：
![image.png](/posts/250301/images/2.png)

当然 [app.ragas.io](https://app.ragas.io/) 也提供了交互式分析，可以查看每个指标的详细结果，你首先要注册一个账号，然后生成一个 Ragas APP token，然后就可以上传结果查看仪表板。

![image.png](/posts/250301/images/1.png)

## RAGAs中的RAG 评估




### 完整示例

```python
import os
from langchain_openai import ChatOpenAI
from ragas import SingleTurnSample, EvaluationDataset, evaluate
from ragas.metrics import BleuScore, AspectCritic
from ragas.llms import LangchainLLMWrapper
import pandas as pd

# 设置环境和 LLM
os.environ["OPENAI_API_KEY"] = "your-openai-key"
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 定义 RAG 管道（简化为文本摘要）
def summarize_text(input_text):
    return llm.invoke(f"Summarize the following text:\n\n{input_text}").content

# 准备数据集并生成 response
dataset = [
    {"user_input": "summarise given text\nThe company reported a 12% revenue increase in Q1 2025, driven by strong demand in Europe. New product launches contributed significantly to this growth. Analysts expect this trend to persist into Q2.", "reference": "The company’s revenue grew 12% in Q1 2025, fueled by strong European sales and new product releases, with analysts predicting sustained growth."},
    {"user_input": "summarise given text\nIn Q4 2024, sales dropped by 5% due to supply chain issues in North America. Efforts to resolve these disruptions are underway, but recovery is slow.", "reference": "Q4 2024 saw a 5% sales decline in North America from supply chain disruptions, with ongoing but slow recovery attempts."},
    {"user_input": "summarise given text\nThe firm achieved a 20% profit hike in 2024, thanks to cost-cutting measures and expansion into Asian markets. However, challenges remain in regulatory compliance.", "reference": "In 2024, the firm’s profits increased 20% from cost cuts and Asian expansion, though regulatory issues persist."}
]
for sample in dataset:
    sample["response"] = summarize_text(sample["user_input"])

# 配置 Ragas 指标
bleu_metric = BleuScore()
aspect_metric = AspectCritic(name="summary_accuracy", llm=LangchainLLMWrapper(llm), definition="Verify if the summary is accurate.")

# 转换为 Ragas 数据集并评估
eval_dataset = EvaluationDataset(samples=[SingleTurnSample(**s) for s in dataset])
results = evaluate(eval_dataset, metrics=[bleu_metric, aspect_metric])

# 输出结果并转换为 pandas
print(f"Evaluation Results: {results}")
df = results.to_pandas()
print("\nDetailed Results:\n", df[["user_input", "response", "bleu_score", "summary_accuracy"]].to_string(index=False))

# 可选：上传到 app.ragas.io（需 token）
# results.upload(token="your-ragas-app-token")
```

### 关于一个完整的RAG 应用
以下是将 [https://docs.ragas.io/en/latest/getstarted/rag_eval/](https://docs.ragas.io/en/latest/getstarted/rag_eval/) 中分布的代码流程合并为一个优雅、简洁的单一代码块。该页面介绍如何使用 Ragas 评估 RAG 应用的性能，涉及加载测试数据集、配置评估指标、执行评估并保存结果。我将保留原文的核心逻辑，优化结构并注释关键步骤。

---

### 合并后的代码

```python
import os
from datasets import load_dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness, answer_relevancy, context_precision, context_recall
)
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

# 设置 API 密钥
os.environ["OPENAI_API_KEY"] = "your_openai_key"

# 初始化 LLM 和嵌入模型
llm = ChatOpenAI(model="gpt-4o")
embeddings = OpenAIEmbeddings()  # 或使用 HuggingFaceEmbeddings("sentence-transformers/all-MiniLM-L6-v2")

# 加载测试数据集
dataset = load_dataset("explodinggradients/fiqa", "rag-eval-explodinggradients")["baseline"]
print(f"Loaded {len(dataset)} samples from fiqa dataset")

# 配置评估指标
metrics = [
    faithfulness(llm=llm),           # 答案忠实度
    answer_relevancy(llm=llm, embeddings=embeddings),  # 答案相关性
    context_precision(llm=llm),      # 上下文精确度
    context_recall(llm=llm)          # 上下文召回率
]

# 执行评估
result = evaluate(
    dataset=dataset,
    metrics=metrics,
    llm=llm,
    embeddings=embeddings,
    raise_exceptions=True  # 显示错误以便调试
)

# 输出结果并保存
print("Evaluation Results:", result)
result.to_pandas().to_csv("rag_eval_results.csv", index=False)
print("Results saved to rag_eval_results.csv")
print(result.to_pandas().head())  # 显示前 5 个样本
```

---

#### 代码说明

1. **导入与配置**：
   - 导入必要模块，包括 Ragas 的评估工具、LangChain 的 LLM 和嵌入模型，以及 Hugging Face 数据集支持。
   - 设置 OpenAI API 密钥。

2. **模型初始化**：
   - 使用 `gpt-4o` 作为评估 LLM，`OpenAIEmbeddings` 用于嵌入（可选使用 Hugging Face 模型）。
   - 这些模型驱动指标计算。

3. **加载数据集**：
   - 从 Hugging Face 加载 "explodinggradients/fiqa" 数据集的 "rag-eval-explodinggradients" 子集，包含问题、答案和上下文。
   - 数据集格式已适配 Ragas（包括 `question`, `answer`, `contexts`, `ground_truths`）。

4. **配置指标**：
   - 定义 4 个核心指标：忠实度（faithfulness）、答案相关性（answer_relevancy）、上下文精确度（context_precision）、上下文召回率（context_recall）。
   - 每个指标绑定 LLM 和嵌入模型。

5. **执行与保存**：
   - 使用 `evaluate` 函数一次性评估所有样本和指标。

---


运行后，输出类似：
```
Loaded 50 samples from fiqa dataset
Evaluation Results: {'faithfulness': 0.92, 'answer_relevancy': 0.95, 'context_precision': 0.88, 'context_recall': 0.90}
Results saved to rag_eval_results.csv
   question  answer  contexts  ground_truths  faithfulness  answer_relevancy  context_precision  context_recall
0  What is...  It is...  [ctx1, ctx2]  True answer...  0.95          0.98              0.90            0.92
1  How does...  It does...  [ctx3]      True answer...  0.90          0.94              0.85            0.89
...
```
---

#### 综合测试相关代码

```python
import os
from ragas.testset import TestsetGenerator
from ragas.testset.evolutions import SimpleEvolution, MultiContextEvolution, ReasoningEvolution
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 设置 API 密钥
os.environ["OPENAI_API_KEY"] = "your_openai_key"

# 初始化 LLM 和嵌入模型
generator_llm = ChatOpenAI(model="gpt-4o")
critic_llm = ChatOpenAI(model="gpt-4o")
embeddings = OpenAIEmbeddings()

# 加载并分割文档
loader = PyPDFLoader("https://arxiv.org/pdf/2309.15217.pdf")  # 示例使用 RAGAs 论文
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = text_splitter.split_documents(documents)
print(f"Loaded {len(docs)} document chunks")

# 配置测试集生成器
generator = TestsetGenerator(
    generator_llm=generator_llm,
    critic_llm=critic_llm,
    embeddings=embeddings,
    docstore=None  # 使用默认内存存储
)

# 定义演化分布
distributions = {
    SimpleEvolution(): 0.5,         # 50% 简单问题
    MultiContextEvolution(): 0.25,  # 25% 多上下文问题
    ReasoningEvolution(): 0.25     # 25% 推理问题
}

# 生成测试集
testset = generator.generate_with_langchain_docs(
    documents=docs,
    test_size=10,              # 生成 10 个测试样本
    distributions=distributions,
    raise_exceptions=True      # 显示错误以便调试
)

# 转换为 DataFrame 并保存
df = testset.to_pandas()
df.to_csv("rag_testset.csv", index=False)
print("Testset generated and saved to rag_testset.csv")
print(df.head())  # 显示前 5 个样本
```

---

#### 代码说明

1. **导入与配置**：
   - 导入所有必要模块，包括 Ragas 的测试集生成工具和 LangChain 的 LLM、嵌入模型及文档处理工具。
   - 设置 OpenAI API 密钥。

2. **模型初始化**：
   - 使用 `gpt-4o` 作为生成器和批评者 LLM，`OpenAIEmbeddings` 用于嵌入。
   - 这些模型驱动问题生成和质量评估。

3. **文档加载与分割**：
   - 从指定 URL 加载 PDF（示例使用 RAGAs 论文）。
   - 使用 `RecursiveCharacterTextSplitter` 将文档分割为大小 1000 字符、200 字符重叠的块。

4. **测试集生成器**：
   - 初始化 `TestsetGenerator`，配置 LLM 和嵌入模型，默认使用内存文档存储。
   - 定义演化分布：50% 简单问题，25% 多上下文问题，25% 推理问题。

5. **生成与保存**：
   - 调用 `generate_with_langchain_docs` 生成 10 个测试样本。
   - 将结果转为 pandas DataFrame 并保存为 CSV 文件，同时打印前 5 行。

---

#### 输出示例
运行后，输出类似：
```
Loaded 15 document chunks
Testset generated and saved to rag_testset.csv
   question_type  question  ground_truth  contexts  ...
0  simple        What is RAGAs?  RAGAs is a framework...  [doc_chunk_1, ...]
1  multi_context  How does RAGAs compare...?  RAGAs differs by...  [doc_chunk_2, ...]
2  reasoning     Why might RAGAs be preferred...?  Due to its...  [doc_chunk_3, ...]
...
```

---



**关键引用**

- [Evaluate your first LLM App - Ragas](https://docs.ragas.io/en/latest/getstarted/evals/)
- [langchain-aws Integration](https://python.langchain.com/docs/integrations/providers/aws/)
- [Google AI Studio Documentation](https://ai.google.dev/docs)
- [Google Cloud Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [LangChain Google AI Integration](https://python.langchain.com/docs/integrations/chat/google_generative_ai)
- [LangChain Vertex AI Integration](https://python.langchain.com/docs/integrations/chat/google_vertex_ai)
- [langchain-azure Integration](https://python.langchain.com/docs/integrations/chat/azure_chat_openai/)
- [Ragas App Login](https://app.ragas.io/login)
- [Ragas App Token Generation](https://app.ragas.io/dashboard/settings/app-tokens)
- [Ragas GitHub Issue for LLM Support](https://github.com/explodinggradients/ragas/issues/1617)