

> 本文档 AI + 社区共建中
# RAG 基础

RAG（Retrieval-Augmented Generation，检索增强生成）是解决大语言模型知识局限性的核心技术。

## 为什么需要 RAG？

大语言模型有两个核心限制：

1. **知识截止**：模型只知道训练数据截止前的信息
2. **幻觉问题**：可能生成看似合理但不正确的内容

RAG 通过将外部知识检索与模型生成相结合来解决这些问题。

## 工作原理

```
用户问题
    │
    ▼
┌─────────────┐     ┌──────────────┐
│  向量化查询   │────→│  向量数据库    │
│  (Embedding)  │     │  (知识库检索)  │
└─────────────┘     └──────┬───────┘
                           │ 相关文档
                           ▼
                    ┌──────────────┐
                    │  组装 Prompt   │
                    │  问题 + 上下文  │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   LLM 生成    │
                    │  (InternLM)   │
                    └──────┬───────┘
                           │
                           ▼
                      最终回答
```

## 核心步骤

### 1. 文档预处理

将知识库文档切分成合适大小的块（Chunk）：

```python
# 简单的文本切分示例
def split_text(text, chunk_size=500, overlap=50):
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i + chunk_size])
    return chunks
```

### 2. 向量化存储

使用 Embedding 模型将文本块转换为向量：

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('BAAI/bge-base-zh-v1.5')
embeddings = model.encode(chunks)

# 存入向量数据库（如 FAISS、Milvus、ChromaDB）
```

### 3. 检索相关内容

```python
# 将用户问题向量化，检索最相关的 Top-K 文档
query_embedding = model.encode([user_question])
similar_docs = vector_db.search(query_embedding, top_k=3)
```

### 4. 生成回答

```python
context = "\n".join([doc.text for doc in similar_docs])

prompt = f"""基于以下参考资料回答用户问题。
如果参考资料中没有相关信息，请明确告知。

参考资料：
{context}

问题：{user_question}
"""

response = llm.chat(prompt)
```

## 关键参数

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| Chunk Size | 300-500 字 | 文本块大小 |
| Overlap | 50-100 字 | 块之间的重叠 |
| Top-K | 3-5 | 检索的文档数量 |
| Embedding 模型 | BGE-base-zh | 中文场景推荐 |

## 下一步

- 实际搭建一个 RAG 系统（实战营 L2 关卡）
- 了解更多 [InternLM 模型](/docs/models/internlm) 的能力
- 使用 [InternLM API](/docs/api/quickstart) 构建应用

## 进阶实践（Intern-S1-Pro 专题）

### 实战任务
1. 基于课程文档搭建最小 RAG 系统（切分、向量化、检索、生成）。
2. 对比不同 chunk 策略在召回率和答案完整性上的影响。
3. 增加引用来源输出，要求每段结论可追溯。

### 交付物
- 一份《RAG 架构与数据流图》
- 一份《检索质量评估报告（Recall@K / 命中率）》

### 自检清单
- [ ] 能解释 RAG 各阶段的输入输出
- [ ] 能定位“检索不到”与“回答跑偏”的根因
- [ ] 能实现带引用的可追溯回答
