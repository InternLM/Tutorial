
# 注意力机制详解

注意力机制（Attention）是 Transformer 架构的核心。它让模型在处理每个词时，能够"关注"到输入中所有相关的词，而不是只看附近的几个。

## 直觉理解

阅读这句话："小明把球传给了小红，**她**很开心。"

你的大脑会自动把"她"和"小红"联系起来，而不是"小明"或"球"。这就是注意力——在大量信息中，**有选择地关注最相关的部分**。

```
她 → 注意力分布
  小明: 0.05  (弱关注)
  球:   0.02  (几乎忽略)
  小红: 0.88  (强关注)
  开心: 0.05  (弱关注)
```

## 核心概念

### Q、K、V 三兄弟

Self-Attention 的核心是三个矩阵：Query（查询）、Key（键）、Value（值）。

用图书馆做类比：
- **Query**：你要搜索的问题（"有没有关于机器学习的书？"）
- **Key**：每本书的标签/索引（"机器学习入门"、"烹饪大全"）
- **Value**：书的实际内容

流程：用 Query 和每个 Key 比对，找到匹配度高的，然后取出对应的 Value。

### 计算步骤

```python
import numpy as np

def self_attention(X, W_q, W_k, W_v):
    """
    X: 输入矩阵 (seq_len, d_model)
    W_q, W_k, W_v: 权重矩阵
    """
    Q = X @ W_q   # 查询
    K = X @ W_k   # 键
    V = X @ W_v   # 值

    d_k = K.shape[-1]
    # 计算注意力分数
    scores = Q @ K.T / np.sqrt(d_k)   # 缩放防止值过大
    # Softmax 归一化
    weights = np.exp(scores) / np.exp(scores).sum(axis=-1, keepdims=True)
    # 加权求和
    output = weights @ V
    return output
```

核心公式：

```
Attention(Q, K, V) = softmax(Q·K^T / √d_k) · V
```

| 步骤 | 操作 | 含义 |
|------|------|------|
| Q·K^T | 矩阵乘法 | 计算每对 token 间的相关性 |
| / √d_k | 缩放 | 防止数值过大导致 softmax 梯度消失 |
| softmax | 归一化 | 将分数转为 0-1 的概率分布 |
| · V | 加权求和 | 根据注意力权重汇聚信息 |

### Multi-Head Attention

一个"头"只能关注一种模式。多头注意力让模型同时关注不同类型的关系：

```
Head 1: 关注语法关系 ("她" → "小红")
Head 2: 关注位置邻近 ("她" → "很开心")
Head 3: 关注主题相关 ("她" → "球"、"传")
```

```python
# 伪代码
heads = [attention(Q @ W_q_i, K @ W_k_i, V @ W_v_i) for i in range(n_heads)]
output = concat(heads) @ W_o
```

| 模型 | 隐藏维度 | 注意力头数 | 每头维度 |
|------|---------|-----------|---------|
| InternLM3-8B | 4096 | 32 | 128 |
| GPT-3 (175B) | 12288 | 96 | 128 |
| LLaMA-2 7B | 4096 | 32 | 128 |

### 为什么 Attention 如此强大

与 RNN 的对比：

| 特性 | RNN | Self-Attention |
|------|-----|---------------|
| 长距离依赖 | 困难（信息逐步衰减） | 直接连接任意两个位置 |
| 并行计算 | 不可（必须顺序处理） | 可以（矩阵运算并行） |
| 计算复杂度 | O(n) | O(n²)，但可被优化 |

## 书生生态中的应用

InternLM3 在注意力机制上的优化：

- 使用 **GQA**（Grouped Query Attention）：Key 和 Value 共享分组，降低显存占用，加速推理
- 结合 **RoPE** 位置编码，支持长上下文外推
- LMDeploy 在推理时通过 **KV Cache** 缓存已计算的 Key/Value，避免重复计算

## 下一步

理解了注意力机制后，推荐继续学习：

- [Transformer 架构](/docs/learn/transformer) — 看注意力机制如何组合成完整的 Transformer
- [Tokenization](/docs/learn/tokenization) — 回顾模型输入是如何准备的

## 进阶实践（Intern-S1-Pro 专题）

### 实战任务
1. 手工计算一个 4-token 序列的注意力分数（含 softmax），验证权重和为 1。
2. 构造“长距离依赖”句子，分析注意力如何聚焦关键信息。
3. 对比单头与多头注意力在信息覆盖上的差异。

### 交付物
- 一份《手算 Attention 过程表》
- 一份《多头注意力观察笔记》

### 自检清单
- [ ] 能解释 Q/K/V 的角色分工
- [ ] 能说明为什么多头注意力更强
- [ ] 能从注意力角度理解上下文建模能力
