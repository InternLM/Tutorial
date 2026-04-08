

> 本文档 AI + 社区共建中
# Embedding 与词向量

Token 只是文本切分后的编号，模型还需要将它们变成**有含义的数字向量**，才能进行计算和理解。这些向量就叫 Embedding。

## 直觉理解

想象一张城市地图。两个城市在地图上越近，它们在现实中也越近。Embedding 就是给每个词在一个高维空间中找一个"坐标"——意思相近的词，坐标也相近。

```
"国王" → [0.21, 0.85, -0.33, ...]   # 高维坐标
"王后" → [0.19, 0.82, -0.31, ...]   # 和"国王"很近
"苹果" → [-0.72, 0.11, 0.64, ...]   # 和"国王"很远
```

经典发现：`国王 - 男人 + 女人 ≈ 王后`，这说明 Embedding 捕捉到了语义关系。

## 核心概念

### 从独热编码到稠密向量

| 表示方式 | 维度 | "猫" 的表示 | 特点 |
|---------|------|------------|------|
| 独热编码 | 词表大小（数万） | [0,0,...,1,...,0] | 稀疏、无语义关系 |
| Embedding | 几百到几千 | [0.12, -0.34, ...] | 稠密、蕴含语义 |

### 词向量的演进

| 阶段 | 代表方法 | 特点 |
|------|---------|------|
| 静态词向量 | Word2Vec, GloVe | 每个词一个固定向量 |
| 上下文词向量 | ELMo | 同一个词在不同句中有不同向量 |
| 预训练模型 | BERT, InternLM | Transformer 编码，embedding 质量大幅提升 |
| 专用 Embedding 模型 | BGE, E5, text-embedding-3 | 专为检索/相似度优化 |

### 向量相似度

衡量两个 Embedding 有多"接近"的常用方法：

```python
import numpy as np

def cosine_similarity(a, b):
    """余弦相似度：值域 [-1, 1]，越大越相似"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
```

| 相似度方法 | 公式 | 适用场景 |
|-----------|------|---------|
| 余弦相似度 | cos(a,b) = a·b / (\|a\|\|b\|) | 最常用，忽略向量长度 |
| 欧氏距离 | \|a - b\| | 对绝对距离敏感 |
| 点积 | a·b | 计算最快 |

## Embedding 在 RAG 中的作用

RAG（检索增强生成）的核心依赖 Embedding：

```
用户问题 → Embedding → 查询向量
知识库文档 → Embedding → 文档向量集合
查询向量 vs 文档向量 → 相似度排序 → 取 Top-K → 送入 LLM 生成回答
```

Embedding 质量直接决定了"能不能检索到正确的内容"，是 RAG 系统最关键的环节。

## 实践示例

使用 Sentence Transformers 计算文本相似度：

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-base-zh-v1.5")

sentences = [
    "什么是大语言模型",
    "LLM 的基本概念",
    "今天北京天气怎么样",
]

embeddings = model.encode(sentences)

# 计算相似度
from sklearn.metrics.pairwise import cosine_similarity
sim_matrix = cosine_similarity(embeddings)

print("相似度矩阵:")
for i, s1 in enumerate(sentences):
    for j, s2 in enumerate(sentences):
        print(f"  '{s1}' vs '{s2}': {sim_matrix[i][j]:.3f}")
```

## 书生生态中的应用

书生生态与 Embedding 技术紧密相关：

- **BGE 系列**（智源 BAAI 开源）：中文 Embedding 领域的标杆模型，`bge-base-zh-v1.5` 在多个评测中领先
- **InternLM 内部 Embedding**：InternLM 的 hidden states 本身就是高质量的文本表示
- **RAG 实践**：结合 InternLM + BGE + 向量数据库，可以搭建企业级知识问答系统

## 下一步

理解了 Embedding 之后，推荐继续学习：

- [注意力机制详解](/docs/learn/attention-mechanism) — 模型如何决定"关注"哪些 Token
- [RAG 基础](/docs/learn/rag-basics) — 深入了解 Embedding 在检索增强中的应用

## 进阶实践（Intern-S1-Pro 专题）

### 实战任务
1. 用 20 段课程文本构建一个迷你向量库，完成相似度检索。
2. 设计 5 个查询问题，观察 Top-K 命中质量并调参（chunk_size、overlap、K）。
3. 对比“只靠生成”与“检索增强后生成”的答案可信度。

### 交付物
- 一份《Embedding 检索实验记录》
- 一份《参数调优建议（chunk/K）》

### 自检清单
- [ ] 能解释向量相似度与语义相关性的关系
- [ ] 能完成最小可用语义检索流程
- [ ] 能识别召回不足和语义漂移问题
