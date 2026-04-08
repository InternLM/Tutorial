

> 本文档 AI + 社区共建中
# SFT 有监督微调

SFT（Supervised Fine-Tuning，有监督微调）是将预训练的基座模型"教会"对话和遵循指令的关键步骤。

## 直觉理解：从"学霸"到"好老师"

预训练好的基座模型像一个读过无数书的学霸——他知识渊博，但如果你问他一个问题，他可能不会好好回答，而是开始"续写"你的话。

```
用户：请解释量子力学
基座模型：是物理学的一个重要分支，研究微观粒子的运动规律。量子力学的发展始于...
（像百科全书一样续写，而不是在"对话"）
```

SFT 就是请一批"教师"示范标准对话，让模型学会：**收到指令 -> 给出高质量回答**。

## 核心概念

### 1. 指令数据格式

SFT 的训练数据是"指令-回答"对，通常遵循以下格式：

```json
{
  "instruction": "请用通俗的语言解释量子力学",
  "input": "",
  "output": "量子力学是研究极小粒子（如电子、光子）行为规律的物理学分支。在这个微观世界里，粒子的行为和我们日常生活中的物体很不一样..."
}
```

有些任务需要额外的输入上下文：

```json
{
  "instruction": "将以下英文翻译为中文",
  "input": "The quick brown fox jumps over the lazy dog.",
  "output": "那只敏捷的棕色狐狸跳过了那只懒狗。"
}
```

### 2. 对话模板

现代 LLM 使用特定的对话模板区分不同角色。以 InternLM 为例：

```
<|im_start|>system
你是一个有帮助的AI助手。<|im_end|>
<|im_start|>user
请解释量子力学<|im_end|>
<|im_start|>assistant
量子力学是...<|im_end|>
```

SFT 时只对 **assistant** 部分的 Token 计算损失，让模型学习生成回答，而不是模仿用户提问。

### 3. 全量微调 vs 参数高效微调

| 方式 | 训练参数 | 显存需求 | 效果 | 适用场景 |
|------|---------|---------|------|---------|
| 全量微调 | 全部参数 | 极高（8B 模型约需 80GB+） | 最佳 | 资源充足、追求最佳效果 |
| LoRA | 约 0.1-1% 参数 | 较低（8B 模型约需 24GB） | 接近全量 | 资源有限、快速实验 |
| QLoRA | 约 0.1-1% 参数 | 更低（8B 模型约需 12GB） | 接近 LoRA | 消费级 GPU |

详细的参数高效微调方法参见 [LoRA 与参数高效微调](/docs/learn/lora)。

## 实践示例：使用 XTuner 微调 InternLM

[XTuner](https://github.com/InternLM/xtuner) 是书生生态的微调工具，支持全量微调和 LoRA/QLoRA。

### 准备配置文件

```python
# internlm3_8b_chat_sft.py — XTuner 配置示例（简化版）
from xtuner.dataset import process_hf_dataset
from xtuner.model import SupervisedFineTune

# 模型
pretrained_model_name_or_path = "internlm/internlm3-8b"

# 训练参数
batch_size = 1
accumulative_counts = 16
lr = 2e-5
max_epochs = 3

# 数据集（Alpaca 格式）
dataset = dict(
    type=process_hf_dataset,
    dataset=dict(type="json", data_files="my_sft_data.json"),
    max_length=2048,
)

# 微调方式：全量微调
model = dict(
    type=SupervisedFineTune,
    llm=dict(type="AutoModelForCausalLM", pretrained_model_name_or_path=pretrained_model_name_or_path),
)
```

### 启动训练

```bash
# 使用 XTuner 启动 SFT
xtuner train internlm3_8b_chat_sft.py

# 合并 adapter（如果使用 LoRA）
xtuner convert merge \
    internlm/internlm3-8b \
    work_dirs/internlm3_8b_chat_sft/epoch_3.pth \
    merged_model/
```

## 微调的注意事项

| 常见问题 | 原因 | 解决方案 |
|---------|------|---------|
| 灾难性遗忘 | 微调数据分布与预训练差异大 | 混入通用数据、降低学习率 |
| 过拟合 | 数据量太少或训练轮数太多 | 早停、增加数据多样性 |
| 回答质量不稳定 | 训练数据质量参差不齐 | 人工审核数据、统一格式 |
| 回答过短/过长 | 训练数据长度分布不均 | 控制数据中回答的长度分布 |

## 书生生态中的 SFT

- **InternLM3-8B-Instruct**：基于 InternLM3-8B 基座模型，经过大规模高质量 SFT 数据微调
- **XTuner**：一站式微调框架，内置多种对话模板和数据处理流水线
- 书生社区提供开源的 SFT 数据集和微调教程，帮助开发者快速上手

SFT 让模型学会了对话，但模型的回答可能仍存在"说废话"、"不够安全"等问题。这就需要进一步的 **对齐（Alignment）** 技术。

## 下一步

- [RLHF 与 DPO：人类偏好对齐](/docs/learn/rlhf) — 如何让模型的回答更符合人类偏好
- [LoRA 与参数高效微调](/docs/learn/lora) — 用更少的资源完成微调

## 进阶实践（Intern-S1-Pro 专题）

### 实战任务
1. 构建一个 100 条指令数据的小样本集（问答、总结、改写三类）。
2. 设计并对比两种对话模板，观察回答风格与可控性差异。
3. 输出一份 SFT 数据质量检查规则（重复、冲突、低质样本）。

### 交付物
- 一份《SFT 数据样例集（JSON/JSONL）》
- 一份《SFT 训练配置与参数说明》

### 自检清单
- [ ] 能写出符合规范的指令数据格式
- [ ] 能说明 SFT 与预训练目标的差异
- [ ] 能识别常见数据污染与风格漂移问题
