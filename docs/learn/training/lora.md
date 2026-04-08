
# LoRA 与参数高效微调

全量微调一个 8B 模型需要 80GB+ 显存，一张消费级 GPU 根本跑不动。**LoRA（Low-Rank Adaptation）** 让你用不到 1% 的参数就能微调大模型，效果接近全量微调。

## 为什么需要参数高效微调？

全量微调的资源瓶颈：

| 模型规模 | 全量微调显存 | LoRA 微调显存 | QLoRA 微调显存 |
|---------|------------|-------------|--------------|
| 1.8B | ~15GB | ~8GB | ~5GB |
| 8B | ~80GB | ~24GB | ~12GB |
| 70B | ~600GB | ~160GB | ~48GB |

大多数开发者手上只有一张 24GB 的 RTX 4090 或更小的 GPU。参数高效微调让微调从"实验室专属"变成了"人人可用"。

## LoRA 的核心原理

### 直觉理解

想象一位已经精通中菜的大厨（预训练模型），现在要学做日料（新任务）。他不需要忘掉所有中菜技能重新学习，只需要学一些"增量技巧"——刀法调整、调味方式变化。这些增量技巧就是 LoRA 学习的内容。

### 低秩分解

LoRA 的关键洞察：微调时权重的变化量是**低秩**的。

原始权重矩阵 `W` 的维度为 `d x d`（例如 4096 x 4096），微调时的变化量 `deltaW` 可以分解为两个小矩阵的乘积：

```
deltaW = A * B
其中 A 的维度为 d x r，B 的维度为 r x d
r << d（例如 r=8, d=4096）
```

参数量对比：
- 全量微调：`d * d = 4096 * 4096 = 16,777,216` 个参数
- LoRA (r=8)：`d * r + r * d = 4096 * 8 * 2 = 65,536` 个参数
- **压缩比：256 倍！**

### 训练过程

```python
# LoRA 的前向传播（伪代码）
class LoRALayer:
    def __init__(self, d, r, alpha):
        self.W = original_weight       # 冻结，不训练
        self.A = random_init(d, r)     # 可训练
        self.B = zeros(r, d)           # 可训练
        self.scaling = alpha / r

    def forward(self, x):
        # 原始输出 + LoRA 增量
        return x @ self.W + x @ self.A @ self.B * self.scaling
```

训练时只更新 A 和 B，原始权重 W 完全冻结。

## QLoRA：更进一步

QLoRA 在 LoRA 的基础上加入**量化**技术，进一步降低显存：

1. 将预训练权重量化为 4-bit（NF4 格式）
2. 在量化后的模型上应用 LoRA
3. 计算时反量化回高精度进行运算

效果：8B 模型微调只需约 12GB 显存，一张 RTX 4090 就够了。

## 关键超参数

| 超参数 | 含义 | 推荐值 | 说明 |
|--------|------|--------|------|
| `rank (r)` | 低秩矩阵的秩 | 8-64 | 越大能力越强，但参数越多 |
| `alpha` | 缩放系数 | 通常 = 2r | 控制 LoRA 增量的强度 |
| `target_modules` | 应用 LoRA 的层 | q_proj, v_proj, k_proj, o_proj | 一般应用于注意力层 |
| `dropout` | LoRA Dropout | 0.05-0.1 | 防止过拟合 |
| `lr` | 学习率 | 1e-4 ~ 2e-4 | 比全量微调大一个量级 |

**rank 选择经验：**
- 简单任务（风格迁移、单领域问答）：r=8 足够
- 中等任务（多领域微调）：r=16-32
- 复杂任务（全面能力调整）：r=64+

## 实践示例：XTuner LoRA 微调

### 配置文件

```python
# internlm3_8b_qlora.py — XTuner QLoRA 配置
from xtuner.model import SupervisedFineTune

pretrained_model_name_or_path = "internlm/internlm3-8b"

# LoRA 配置
lora_config = dict(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.05,
)

# 量化配置（QLoRA）
quantization_config = dict(
    load_in_4bit=True,
    bnb_4bit_compute_dtype="float16",
    bnb_4bit_quant_type="nf4",
)

# 训练参数
batch_size = 1
accumulative_counts = 16
lr = 2e-4
max_epochs = 3
```

### 训练与合并

```bash
# 启动 QLoRA 微调
xtuner train internlm3_8b_qlora.py

# 合并 LoRA adapter 到基座模型
xtuner convert merge \
    internlm/internlm3-8b \
    work_dirs/internlm3_8b_qlora/epoch_3.pth \
    merged_model/ \
    --max-shard-size 2GB
```

合并后的模型可以直接用于推理，和全量微调的模型使用方式完全一致。

## LoRA 的进阶技巧

### LoRA 组合与切换

LoRA 的一个优势是 adapter 可以动态加载和切换：

```python
from peft import PeftModel

# 加载基座模型
base_model = AutoModelForCausalLM.from_pretrained("internlm/internlm3-8b")

# 加载不同任务的 LoRA adapter
medical_model = PeftModel.from_pretrained(base_model, "path/to/medical-lora")
legal_model = PeftModel.from_pretrained(base_model, "path/to/legal-lora")
```

一个基座模型 + 多个轻量级 adapter = 多个专业模型，大幅节省存储和部署成本。

## 书生生态中的 LoRA

- **XTuner**：一站式支持 LoRA / QLoRA / 全量微调，内置 InternLM 系列模型的配置模板
- 书生社区提供大量 LoRA 微调教程和最佳实践
- **InternLM3** 的各类专业版本（代码、数学等）也是通过微调技术在基座模型上优化而来

## 下一步

- [SFT 有监督微调](/docs/learn/sft) — LoRA 最常用的场景就是 SFT
- [RLHF 与 DPO](/docs/learn/rlhf) — LoRA 同样可以用于对齐阶段

## 进阶实践（Intern-S1-Pro 专题）

### 实战任务
1. 用同一数据集跑两组 LoRA 参数（r/alpha/dropout）并比较效果。
2. 设计“多任务 Adapter”策略：代码助手、文档写作、问答检索三类。
3. 评估 LoRA 合并与不合并在部署效率和回滚成本上的差异。

### 交付物
- 一份《LoRA 参数对比实验表》
- 一份《Adapter 管理与发布规范》

### 自检清单
- [ ] 能解释低秩分解为何节省训练成本
- [ ] 能选择适合场景的 LoRA 参数范围
- [ ] 能给出可落地的 adapter 版本管理策略
