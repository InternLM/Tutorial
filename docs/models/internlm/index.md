
# InternLM 书生·浦语

InternLM 是书生大模型系列的核心语言模型产品线，经历了三代迭代，从 InternLM 到 InternLM3，持续推进大语言模型的开源创新。

## 模型系列

| 模型 | 发布时间 | 参数量 | 亮点 |
|------|---------|--------|------|
| **InternLM3** | 2025.01 | 8B | 精炼数据框架，4T 数据超越同量级，深度思考 |
| **InternLM2.5** | 2024.07 | 1.8B/7B/20B | 百万 Token 长文本，自主规划 |
| **InternLM2** | 2024.01 | 1.8B/7B/20B | 高质量语料，开源领先 |
| **InternLM** | 2023.06 | 7B/20B/104B | 首发千亿参数，中国高考超越 ChatGPT |

## 快速开始

### 使用 Transformers

```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "internlm/internlm3-8b-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    trust_remote_code=True
).cuda()

messages = [
    {"role": "user", "content": "你好，请介绍一下 InternLM。"}
]
response = model.chat(tokenizer, messages)
print(response)
```

### 使用 Ollama

```bash
# 安装并运行
ollama run internlm3:8b

# 对话
>>> 你好，介绍一下自己
```

### 使用 LMDeploy 部署

```bash
# 安装
pip install lmdeploy

# 启动 API 服务
lmdeploy serve api_server internlm/internlm3-8b-instruct --server-port 23333

# 调用
curl http://localhost:23333/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "internlm3-8b-instruct", "messages": [{"role": "user", "content": "hello"}]}'
```

## 相关资源

- [GitHub 仓库](https://github.com/InternLM/InternLM)
- [HuggingFace 模型](https://huggingface.co/internlm)
- [技术报告](https://arxiv.org/abs/2403.17297)
- [LMDeploy 部署指南](/docs/models/lmdeploy)
- [XTuner 微调指南](/docs/models/xtuner)
