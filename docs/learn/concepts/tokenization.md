

> 本文档 AI + 社区共建中
# Tokenization：模型如何理解文字

大语言模型不能直接读懂"你好"这两个字。它需要先把文本切成一个个小片段——Token，然后用数字表示它们。这个过程就是 Tokenization。

## 直觉理解

想象你要用电报发一段话。电报不能直接传汉字，你需要先把汉字转成电报码（数字），对方收到后再把数字还原成汉字。Tokenization 就是大模型的"电报编码"过程。

```
"书生大模型真厉害" → [书生, 大模型, 真, 厉害] → [3214, 8872, 156, 9431]
```

## 核心概念

### 什么是 Token

Token 是模型处理文本的基本单位。它可以是一个字、一个词，也可以是一个子词片段：

```
英文: "unhappiness" → ["un", "happiness"]      # 子词切分
中文: "人工智能"     → ["人工", "智能"]           # 常见词保留
代码: "print('hello')" → ["print", "('", "hello", "')"]
```

### 主流分词算法

| 算法 | 核心思想 | 代表模型 |
|------|---------|---------|
| BPE | 统计最高频的字符对，反复合并 | GPT 系列、InternLM |
| WordPiece | 类似 BPE，按最大似然选合并 | BERT |
| SentencePiece | 语言无关，直接处理原始字符串 | LLaMA、T5 |
| Unigram | 从大词表逐步裁剪低频 token | mBART |

BPE（Byte Pair Encoding）是目前最主流的算法。核心步骤：

1. 初始化：每个字符是一个 token
2. 统计所有相邻 token 对的出现频率
3. 合并频率最高的 token 对为新 token
4. 重复步骤 2-3，直到达到目标词表大小

### Token 数与计费

调用 LLM API 时，费用按 Token 数计算。不同语言的 Token 效率差异很大：

| 文本 | 字符数 | Token 数（约） | 比率 |
|------|--------|---------------|------|
| "Hello, how are you?" | 20 | 6 | 3.3 字符/token |
| "你好，你今天怎么样？" | 10 | 8 | 1.3 字符/token |

中文通常比英文消耗更多 Token——这也是为什么中文优化的 tokenizer 非常重要。

## 实践示例

用 Python 体验 tokenization 过程：

```python
from transformers import AutoTokenizer

# 加载 InternLM3 的 tokenizer
tokenizer = AutoTokenizer.from_pretrained(
    "internlm/internlm3-8b", trust_remote_code=True
)

text = "书生大模型是一个开源的大语言模型"
tokens = tokenizer.tokenize(text)
ids = tokenizer.encode(text)

print(f"原文: {text}")
print(f"Token: {tokens}")
print(f"Token ID: {ids}")
print(f"Token 数: {len(ids)}")
```

## 书生生态中的应用

InternLM3 使用基于 BPE 的 tokenizer，词表大小约 **92,544**。相比早期模型，它：

- 对中文分词效率更高，减少 Token 浪费
- 支持代码、数学符号等特殊字符
- 包含特殊 token（如 `<|im_start|>`）用于多轮对话格式

XTuner 微调时，tokenizer 会自动添加对话模板所需的特殊 token，确保微调数据与预训练格式一致。

## 下一步

理解了 Token 之后，推荐继续学习：

- [Embedding 与词向量](/docs/learn/embedding) — Token 如何变成模型能理解的数字向量
- [什么是大语言模型](/docs/learn/what-is-llm) — 回顾 LLM 基础概念

## 进阶实践（Intern-S1-Pro 专题）

### 实战任务
1. 选 10 条中英混合提示词，统计 token 数并分析哪些写法更省 token。
2. 设计一版“同语义短提示词”，目标是把 token 成本降低 20%。
3. 用同一任务对比“冗长 prompt”和“压缩 prompt”的输出差异。

### 交付物
- 一份《提示词 Token 成本对照表》
- 一份《Prompt 压缩策略清单》

### 自检清单
- [ ] 能解释 BPE 的基本思想与优缺点
- [ ] 能估算一次调用的大致 token 成本
- [ ] 能针对高频任务写出低成本 prompt 模板
