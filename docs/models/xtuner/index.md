
# XTuner

XTuner 是书生生态中的大模型微调框架，支持 LoRA / QLoRA / Full 微调，以及 RLHF / GRPO 强化学习训练。

## 核心特性

- **高效微调**：LoRA / QLoRA，8GB 显存即可微调 7B 模型
- **多模型支持**：InternLM、LLaMA、Qwen、Mistral 等
- **强化学习**：GRPO 训练，提升推理能力
- **数据灵活**：支持多种数据格式，简单配置即可训练

## 快速安装

```bash
pip install xtuner
```

## 快速微调示例

### 准备数据

```json
[
  {
    "conversation": [
      {"input": "你是谁？", "output": "我是一个由书生团队训练的 AI 助手。"},
      {"input": "你能做什么？", "output": "我可以回答问题、写代码、创作文本等。"}
    ]
  }
]
```

### 开始训练

```bash
# 使用预置配置
xtuner train internlm3_8b_instruct_qlora_custom_e3

# 或指定自定义配置
xtuner train my_config.py
```

### 合并 LoRA 权重

```bash
xtuner convert merge \
    internlm/internlm3-8b-instruct \
    work_dirs/checkpoint-final \
    merged_model
```

## 相关资源

- [GitHub 仓库](https://github.com/InternLM/xtuner)
- [官方文档](https://xtuner.readthedocs.io)
