

> 本文档 AI + 社区共建中
# InternLM 快速上手

本指南帮助你在本地环境中运行 InternLM3 模型。

## 环境要求

| 项目 | 最低配置 | 推荐配置 |
|------|---------|---------|
| GPU | 8GB 显存 (INT4 量化) | 16GB+ 显存 |
| Python | 3.8+ | 3.10+ |
| CUDA | 11.7+ | 12.1+ |
| 内存 | 16GB | 32GB+ |

## 方式一：Transformers（最简单）

### 安装依赖

```bash
pip install torch transformers sentencepiece
```

### 运行推理

```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "internlm/internlm3-8b-instruct"

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto",
    trust_remote_code=True
)

messages = [
    {"role": "system", "content": "你是一个有用的 AI 助手。"},
    {"role": "user", "content": "什么是大语言模型？请用简单的语言解释。"}
]

response = model.chat(tokenizer, messages)
print(response)
```

## 方式二：Ollama（最方便）

```bash
# 安装 Ollama（如果还没有）
curl -fsSL https://ollama.com/install.sh | sh

# 运行 InternLM3
ollama run internlm3:8b
```

在 Ollama 交互界面中直接输入问题即可对话。

## 方式三：LMDeploy（高性能生产部署）

```bash
# 安装
pip install lmdeploy

# 交互式对话
lmdeploy chat internlm/internlm3-8b-instruct

# 或启动 OpenAI 兼容 API 服务
lmdeploy serve api_server internlm/internlm3-8b-instruct \
    --server-port 23333 \
    --tp 1
```

详细的 LMDeploy 使用指南请参考 [LMDeploy 文档](/docs/models/lmdeploy)。

## 常见问题

### 显存不足怎么办？

使用 INT4 量化可以将显存需求从 16GB 降至 8GB：

```bash
# LMDeploy 4-bit 量化
lmdeploy chat internlm/internlm3-8b-instruct --model-format awq
```

### 如何使用多卡运行？

```bash
# 2 卡并行
lmdeploy serve api_server internlm/internlm3-8b-instruct --tp 2
```

## 下一步

- 了解 [InternVL 多模态模型](/docs/models/internvl)
- 学习 [XTuner 微调](/docs/models/xtuner)自定义模型
- 使用 [OpenCompass](/docs/models/opencompass) 评测模型效果
