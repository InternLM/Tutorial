
# 预训练：从零训练大模型

预训练是大语言模型诞生的第一步。一个模型从"一无所知"到"博览群书"，靠的就是在海量文本上进行预训练。

## 直觉理解：完形填空的超级版本

小学时你做过完形填空——根据上下文猜一个词。预训练的核心思想类似，但更简单：**给定前面的所有文字，预测下一个词**。

```
输入：今天天气真
模型预测：好（概率 0.42）、不错（概率 0.31）、差（概率 0.05）...
```

这个任务叫做 **Next Token Prediction（下一个 Token 预测）**。模型通过数万亿次这样的预测练习，逐渐学会了语法、常识、推理甚至代码编写能力。

## 核心概念

### 1. 自回归语言建模

预训练的目标函数非常直觉：最大化给定上文时下一个 Token 的概率。

```
L = -sum( log P(x_t | x_1, x_2, ..., x_{t-1}) )
```

模型一次只预测一个 Token，但通过因果注意力（Causal Attention），每个位置的 Token 可以同时计算损失，训练效率很高。

### 2. 预训练数据

预训练数据的规模和质量直接决定模型能力。典型的预训练数据组成：

| 数据来源 | 占比 | 作用 |
|---------|------|------|
| 网页（Common Crawl 等） | 60-70% | 通用知识、语言能力 |
| 书籍 | 10-15% | 深度知识、长文本理解 |
| 代码（GitHub 等） | 10-15% | 代码生成、逻辑推理 |
| 论文（arXiv 等） | 3-5% | 科学知识、数学能力 |
| 百科（Wikipedia 等） | 3-5% | 事实性知识 |

数据清洗是预训练中最耗时的工程之一，包括去重、过滤低质量文本、去除有害内容等。

### 3. 计算资源需求

预训练是一项昂贵的工程。以 InternLM3-8B 为参考：

| 项目 | 量级 |
|------|------|
| 模型参数量 | 80 亿 |
| 训练数据量 | 数万亿 Token |
| GPU 数量 | 数百张 A100/H100 |
| 训练时间 | 数周到数月 |

Scaling Laws 告诉我们：模型参数量、数据量和计算量三者之间存在幂律关系，需要协调增长才能获得最优性能。

## 实践示例：理解训练过程

虽然我们很难在本地从头预训练一个大模型，但可以理解其核心代码结构：

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# 加载预训练模型（体验推理过程）
model_name = "internlm/internlm3-8b"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)

# 预训练的本质：给定前文，预测下一个 Token
text = "人工智能的发展"
inputs = tokenizer(text, return_tensors="pt")

with torch.no_grad():
    outputs = model(**inputs)
    # outputs.logits 的最后一个位置就是对下一个 Token 的预测
    next_token_logits = outputs.logits[0, -1, :]
    next_token_id = torch.argmax(next_token_logits).item()
    print(f"预测的下一个 Token：{tokenizer.decode(next_token_id)}")
```

### 训练循环的核心逻辑

```python
# 简化的预训练循环（伪代码）
for batch in dataloader:
    input_ids = batch["input_ids"]           # [batch_size, seq_len]

    outputs = model(input_ids)
    # 将预测值与右移一位的标签对比
    logits = outputs.logits[:, :-1, :]       # 预测位置
    labels = input_ids[:, 1:]                # 目标位置

    loss = cross_entropy(logits, labels)
    loss.backward()
    optimizer.step()
```

## 书生生态中的预训练

**InternLM3** 系列是书生体系的核心语言模型，预训练过程具有以下特点：

- **高质量数据**：精心筛选的中英文混合语料，代码和学术数据占比较高
- **长上下文**：支持 32K 甚至更长的上下文窗口
- **多阶段训练**：先在通用数据上训练，再在高质量数据上退火（annealing），提升能力密度
- **开源开放**：模型权重和技术报告完全开源

预训练结束后的模型叫做 **Base Model（基座模型）**。它能接话、补全文本，但还不擅长对话和遵循指令——这就需要下一步的 **SFT（有监督微调）** 来解决。

## 下一步

- [SFT 有监督微调](/docs/learn/sft) — 如何让基座模型学会对话和遵循指令
- [Transformer 架构](/docs/learn/transformer) — 回顾预训练模型的底层架构

## 进阶实践（Intern-S1-Pro 专题）

### 实战任务
1. 设计一个小规模预训练数据清洗流程（去重、去噪、质量分层）。
2. 基于公开语料估算训练 token 总量与预算区间。
3. 写出一份“预训练风险清单”（数据偏差、版权、安全）。

### 交付物
- 一份《预训练数据流程图》
- 一份《训练预算估算表（算力/时长/成本）》

### 自检清单
- [ ] 能解释预训练目标函数的基本思想
- [ ] 能说明数据质量对模型能力上限的影响
- [ ] 能列出至少 3 个训练阶段关键风险
