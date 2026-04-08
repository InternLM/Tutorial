

> 本文档 AI + 社区共建中
# Transformer 架构

Transformer 是现代大语言模型的基础架构，由 Google 在 2017 年的论文 "Attention Is All You Need" 中提出。

## 为什么要了解 Transformer？

当你使用 InternLM、GPT、LLaMA 等大模型时，它们的"大脑"都是基于 Transformer 构建的。理解 Transformer 能帮助你：

- 更好地理解模型的能力和局限
- 更高效地编写 Prompt
- 理解量化、KV Cache 等优化技术
- 为微调和部署打下基础

## 核心思想：注意力机制

Transformer 的核心是**自注意力（Self-Attention）**机制。

### 直觉理解

想象你在读一句话：

> "小明把苹果给了小红，**她**很开心。"

你的大脑会自动将"她"与"小红"关联。这就是注意力——模型在处理每个词时，会"关注"句子中所有其他词，并计算它们的相关性。

### 数学表示

自注意力的计算公式：

```
Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) * V
```

其中：
- **Q (Query)**：当前词的"提问"向量
- **K (Key)**：所有词的"标签"向量
- **V (Value)**：所有词的"内容"向量
- **d_k**：向量维度（用于缩放）

## Transformer 的组件

### 1. Embedding + 位置编码

将 Token 转换为数字向量，并注入位置信息（因为注意力本身不感知顺序）。

### 2. 多头注意力（Multi-Head Attention）

多个注意力"头"并行工作，每个头关注不同维度的语义关系：

- 头 1 可能关注语法结构
- 头 2 可能关注语义相似性
- 头 3 可能关注指代关系

### 3. 前馈网络（FFN）

每个注意力层后接一个前馈网络，做非线性变换：

```
FFN(x) = max(0, xW1 + b1)W2 + b2
```

### 4. 残差连接 + LayerNorm

保证深层网络的梯度稳定传播：

```
output = LayerNorm(x + Sublayer(x))
```

## Decoder-Only 架构

InternLM 等现代 LLM 采用 **Decoder-Only** 架构（只有解码器）：

- 使用因果注意力（Causal Attention）：每个 Token 只能看到它之前的 Token
- 自回归生成：逐个 Token 预测下一个

```
输入：  [我] [爱] [AI]
预测：  [爱] [AI] [技术]

第1步：[我] → 预测 [爱]
第2步：[我][爱] → 预测 [AI]
第3步：[我][爱][AI] → 预测 [技术]
```

## 关键参数

| 参数 | InternLM3-8B | 说明 |
|------|-------------|------|
| 层数 | 32 | Transformer 层数 |
| 注意力头数 | 32 | 多头注意力的头数 |
| 隐藏维度 | 4096 | 每个 Token 的向量维度 |
| 词表大小 | 92544 | 支持的 Token 种类数 |

## 进一步阅读

- 原论文：[Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- 下一篇：[Prompt Engineering](/docs/learn/prompt-engineering)

## 进阶实践（Intern-S1-Pro 专题）

### 实战任务
1. 画出 Decoder-Only Transformer 的完整数据流图（输入到输出）。
2. 估算一个 8B 级模型的主要参数构成（Embedding、Attention、FFN）。
3. 结合实际任务说明在哪些场景需要更长上下文。

### 交付物
- 一份《Transformer 架构图（标注版）》
- 一份《参数规模与能力关系说明》

### 自检清单
- [ ] 能解释每个核心模块在做什么
- [ ] 能区分 Encoder-Decoder 与 Decoder-Only 的应用差异
- [ ] 能把架构理解映射到推理性能问题
