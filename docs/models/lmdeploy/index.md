
# LMDeploy

LMDeploy 是书生生态中的大模型部署工具，提供高效的推理引擎和便捷的部署方案。支持 LLM 和 VLM 的推理、量化和 API 服务。

## 核心特性

- **TurboMind 推理引擎**：高性能 C++ 推理后端，支持连续批处理
- **量化部署**：AWQ / GPTQ / SmoothQuant / KV Cache 量化，大幅降低显存
- **OpenAI 兼容 API**：一行命令启动兼容 OpenAI 的 API 服务
- **多模型支持**：InternLM、LLaMA、Qwen、Mistral 等 20+ 模型架构

## 快速安装

```bash
pip install lmdeploy
```

## 快速使用

### 交互式对话

```bash
lmdeploy chat internlm/internlm3-8b-instruct
```

### 启动 API 服务

```bash
lmdeploy serve api_server internlm/internlm3-8b-instruct \
    --server-port 23333 \
    --tp 1
```

### Python API

```python
from lmdeploy import pipeline

pipe = pipeline("internlm/internlm3-8b-instruct")
response = pipe(["什么是大语言模型？"])
print(response[0].text)
```

## 量化部署

### AWQ 4-bit 量化

```bash
# 量化模型
lmdeploy lite auto_awq internlm/internlm3-8b-instruct \
    --work-dir internlm3-8b-4bit

# 使用量化模型
lmdeploy chat internlm3-8b-4bit
```

显存对比：

| 模式 | 显存占用 |
|------|---------|
| FP16 | ~16GB |
| AWQ 4-bit | ~6GB |
| AWQ 4-bit + KV8 | ~4GB |

## 相关资源

- [GitHub 仓库](https://github.com/InternLM/lmdeploy)
- [官方文档](https://lmdeploy.readthedocs.io)
- [PyPI 包](https://pypi.org/project/lmdeploy)
