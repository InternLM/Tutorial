

> 本文档 AI + 社区共建中
# 模型量化：GPTQ/AWQ/GGUF

一个 70B 参数的大模型，以 FP16 精度加载需要约 140GB 显存——这超过了绝大多数消费级显卡的容量。量化就像是给模型"瘦身"，用更低的精度表示权重，让大模型可以跑在普通 GPU 甚至 CPU 上。

## 为什么需要量化？

| 模型大小 | FP16 显存 | INT8 显存 | INT4 显存 |
|---------|----------|----------|----------|
| 7B | ~14 GB | ~7 GB | ~4 GB |
| 14B | ~28 GB | ~14 GB | ~8 GB |
| 70B | ~140 GB | ~70 GB | ~35 GB |

量化的目标：**用尽可能少的精度损失换取大幅的显存和速度收益。**

## 精度是什么？

模型权重本质上是浮点数。不同精度用不同的位数来存储一个数字：

```
FP32 (32位):  1位符号 + 8位指数 + 23位尾数  → 精度最高，占用最大
FP16 (16位):  1位符号 + 5位指数 + 10位尾数  → 训练和推理的常用精度
INT8 (8位):   256 个整数值                  → 显存减半，精度损失小
INT4 (4位):   16 个整数值                   → 显存降至 1/4，有一定精度损失
```

## 主流量化方法对比

| 方法 | 类型 | 精度 | 速度 | 特点 | 适用场景 |
|------|------|------|------|------|---------|
| **GPTQ** | 训练后量化 | INT4/INT8 | 快（GPU） | 校准数据驱动，精度较好 | GPU 推理 |
| **AWQ** | 训练后量化 | INT4 | 快（GPU） | 保护重要权重，精度更优 | GPU 推理 |
| **GGUF** | 训练后量化 | 多种 | 适中 | CPU 友好，跨平台 | CPU/混合推理 |

### GPTQ（GPU 量化首选）

GPTQ 使用一小批校准数据来优化量化过程，逐层处理模型权重：

```bash
# 使用 LMDeploy 进行 GPTQ 量化
pip install lmdeploy

# W4A16 量化（权重 INT4，激活 FP16）
lmdeploy lite auto_awq \
    internlm/internlm3-8b-instruct \
    --work-dir internlm3-8b-4bit
```

### AWQ（精度更优）

AWQ（Activation-aware Weight Quantization）的核心思想：不是所有权重都同等重要，保护少数关键权重通道可以显著提升量化质量。

```python
from awq import AutoAWQForCausalLM
from transformers import AutoTokenizer

model_path = "internlm/internlm3-8b-instruct"

# 加载模型
model = AutoAWQForCausalLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

# 执行 AWQ 量化
model.quantize(tokenizer, quant_config={"w_bit": 4, "q_group_size": 128})
model.save_quantized("internlm3-8b-awq")
```

### GGUF（CPU 部署之选）

GGUF 是 llama.cpp 生态的量化格式，最大优势是**可以在纯 CPU 上运行**：

```bash
# 使用 Ollama 直接运行 GGUF 模型
ollama run internlm3:8b

# 或者用 llama.cpp
./llama-cli -m internlm3-8b-Q4_K_M.gguf -p "你好"
```

GGUF 提供多种量化级别：

| 量化类型 | 精度 | 模型大小 (7B) | 推荐场景 |
|---------|------|-------------|---------|
| Q8_0 | 8-bit | ~7.5 GB | 精度敏感任务 |
| Q5_K_M | 5-bit | ~5.0 GB | 平衡之选 |
| Q4_K_M | 4-bit | ~4.0 GB | 日常使用推荐 |
| Q2_K | 2-bit | ~2.7 GB | 极限压缩，精度下降明显 |

## 使用 LMDeploy 量化部署

LMDeploy 是书生生态的推理部署框架，支持高效的 W4A16 量化：

```python
from lmdeploy import pipeline, TurbomindEngineConfig

# 加载 4-bit 量化模型
engine_config = TurbomindEngineConfig(model_format="awq")
pipe = pipeline("internlm/internlm3-8b-instruct-awq", backend_config=engine_config)

response = pipe(["介绍一下量化技术"])
print(response[0].text)
```

## 量化对性能的影响

以 InternLM3-8B 为例（参考值）：

| 指标 | FP16 | INT8 | INT4 (AWQ) |
|------|------|------|-----------|
| 显存占用 | 16 GB | 8 GB | 5 GB |
| 推理速度 | 基准 | ~1.2x | ~1.5x |
| MMLU 精度 | 72.1 | 71.8 | 71.2 |
| 精度损失 | - | &lt;0.5% | &lt;1.5% |

关键结论：**INT4 量化在保持 98%+ 精度的同时，显存降低 70%，速度提升 50%。**

## 如何选择？

- **有 GPU、追求精度** → AWQ 或 GPTQ
- **需要 CPU 部署** → GGUF
- **显存有限但需要好效果** → AWQ INT4
- **嵌入式/边缘设备** → GGUF Q4_K_M

## 下一步

- 学习 [Transformer 架构](/zh/learn/transformer)，理解模型权重的来源
- 了解 [评测基准](/zh/learn/evaluation-benchmarks)，衡量量化对模型能力的影响
- 探索 [AI Agent](/zh/learn/ai-agent)，用量化模型搭建轻量级智能体

## 进阶实践（Intern-S1-Pro 专题）

### 实战任务
1. 对同一模型分别做 FP16、INT8、INT4 推理测试并记录性能差异。
2. 以实际硬件为约束给出“量化方案选型表”（显存、速度、精度）。
3. 评估量化后在真实问答集上的精度下降幅度。

### 交付物
- 一份《量化性能对比表（吞吐/延迟/显存）》
- 一份《部署选型建议（GPU/CPU）》

### 自检清单
- [ ] 能解释量化为何提升部署效率
- [ ] 能在精度与成本之间做权衡
- [ ] 能给出场景化量化策略
