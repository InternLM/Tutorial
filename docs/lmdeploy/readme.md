# LMDeploy 模型部署

## 课程简介

LMDeploy 是书生生态中的高效推理部署工具，专为大语言模型和视觉语言模型的压缩、部署与服务化而设计。它的核心推理引擎 TurboMind 在吞吐量和延迟方面均达到业界领先水平。

本课程将从零开始，带你完成从安装、本地对话、API 服务搭建，到量化压缩、多模态部署和分布式推理的全流程实战。

## 你将学到

- LMDeploy 的整体架构与核心引擎设计
- 一行命令启动本地大模型对话
- 搭建 OpenAI 兼容的 API 服务
- 使用 AWQ 量化将模型体积压缩至 1/4
- 部署多模态视觉语言模型（InternVL 系列）
- 使用 Tensor Parallelism 实现多卡分布式推理

## 第 1 节：LMDeploy 概览

### 目标

理解 LMDeploy 在模型部署流程中的定位，以及它的核心技术优势。

### 内容

**什么是 LMDeploy？**

LMDeploy 是一个用于压缩、部署和服务化大语言模型（LLM）与视觉语言模型（VLM）的 Python 工具库。它由上海人工智能实验室开发维护，是书生生态中从训练到部署链路的关键一环。

**核心引擎**

LMDeploy 提供两个推理引擎：

| 引擎 | 语言 | 特点 |
|------|------|------|
| TurboMind | C++ / CUDA | 极致性能优化，推荐生产环境使用 |
| PyTorch Engine | Python | 开发友好，降低二次开发门槛 |

**TurboMind 的核心技术**

- **Persistent Batch（持续批处理）**：动态管理多个推理请求，无需等待整个 batch 完成即可接纳新请求，最大化 GPU 利用率
- **Paged Attention（分页注意力）**：借鉴操作系统虚拟内存思想，将 KV Cache 分页存储，避免显存碎片化，支持更长的上下文和更大的并发量
- **高效量化推理**：支持 W4A16（4-bit 权重量化）、W8A8（8-bit 全量化）、FP8 等多种精度方案

**支持的模型**

LMDeploy 支持主流大模型：

- **LLM**：InternLM 系列、Llama 系列、Qwen 系列、DeepSeek-V3、Mistral、Gemma、ChatGLM 等
- **VLM**：InternVL2/3 系列、Qwen-VL 系列、DeepSeek-VL2、LLaVA、CogVLM2 等

## 第 2 节：安装与快速上手

### 目标

完成 LMDeploy 的安装，启动第一次本地对话。

### 内容

**安装**

推荐使用 conda 创建独立环境：

```bash
conda create -n lmdeploy python=3.12 -y
conda activate lmdeploy
pip install lmdeploy
```

默认安装包适配 CUDA 12。安装完成后验证：

```bash
lmdeploy version
```

**一行命令启动对话**

LMDeploy 提供 CLI 工具，可以直接在终端与模型交互：

```bash
lmdeploy chat internlm/internlm3-8b-instruct
```

首次运行时会自动从 HuggingFace 下载模型权重。如果在国内环境，建议提前设置镜像：

```bash
export HF_ENDPOINT=https://hf-mirror.com
lmdeploy chat internlm/internlm3-8b-instruct
```

指定使用 TurboMind 引擎（默认）：

```bash
lmdeploy chat internlm/internlm3-8b-instruct --backend turbomind
```

指定使用 PyTorch 引擎：

```bash
lmdeploy chat internlm/internlm3-8b-instruct --backend pytorch
```

**Python Pipeline 调用**

除了 CLI，还可以在 Python 中使用 pipeline 接口：

```python
import lmdeploy

with lmdeploy.pipeline("internlm/internlm3-8b-instruct") as pipe:
    response = pipe(["Hi, pls intro yourself", "What is deep learning?"])
    print(response)
```

## 第 3 节：搭建 OpenAI 兼容 API 服务

### 目标

将模型封装为 RESTful API 服务，兼容 OpenAI 接口协议。

### 内容

**启动 API 服务**

一行命令即可将模型打包为 API 服务：

```bash
lmdeploy serve api_server internlm/internlm3-8b-instruct --server-port 23333
```

服务启动后，可通过 `http://localhost:23333` 访问 Swagger UI 文档。

**常用启动参数**

| 参数 | 说明 | 示例 |
|------|------|------|
| `--server-port` | 服务端口 | `23333` |
| `--tp` | Tensor Parallelism 卡数 | `2` |
| `--session-len` | 最大上下文长度 | `8192` |
| `--cache-max-entry-count` | KV Cache 占 GPU 显存的比例 | `0.8` |
| `--backend` | 推理引擎 | `turbomind` 或 `pytorch` |

**使用 curl 调用**

```bash
# 查看可用模型
curl http://localhost:23333/v1/models

# 发送对话请求
curl http://localhost:23333/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "internlm3-8b-instruct",
    "messages": [
      {"role": "user", "content": "用一句话解释什么是大语言模型"}
    ],
    "temperature": 0.7
  }'
```

**使用 Python OpenAI SDK 调用**

```python
from openai import OpenAI

client = OpenAI(
    api_key="EMPTY",
    base_url="http://localhost:23333/v1",
)

model_name = client.models.list().data[0].id
print(f"Using model: {model_name}")

response = client.chat.completions.create(
    model=model_name,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "用一句话解释什么是大语言模型"},
    ],
    temperature=0.7,
)

print(response.choices[0].message.content)
```

**使用 LMDeploy 原生客户端**

```python
from lmdeploy.serve.openai.api_client import APIClient

api_client = APIClient("http://localhost:23333")
model_name = api_client.available_models[0]

for item in api_client.chat_completions_v1(
    model=model_name,
    messages=[{"role": "user", "content": "什么是 Transformer 架构？"}],
):
    print(item)
```

## 第 4 节：量化部署

### 目标

掌握 W4A16 量化方法，实现模型压缩与高效部署。

### 内容

量化是将模型权重从高精度（如 FP16）压缩到低精度（如 4-bit）的技术。它可以显著降低显存占用，同时保持模型质量。

**W4A16 量化：AWQ 算法**

W4A16 表示权重（Weight）量化到 4-bit，激活值（Activation）保持 16-bit。LMDeploy 采用 AWQ（Activation-aware Weight Quantization）算法实现。

```bash
export HF_MODEL=internlm/internlm2_5-7b-chat
export WORK_DIR=internlm2_5-7b-chat-4bit

lmdeploy lite auto_awq \
  $HF_MODEL \
  --calib-dataset wikitext2 \
  --calib-samples 128 \
  --calib-seqlen 2048 \
  --w-bits 4 \
  --w-group-size 128 \
  --batch-size 1 \
  --work-dir $WORK_DIR
```

参数说明：

| 参数 | 说明 |
|------|------|
| `--calib-dataset` | 校准数据集，用于统计激活值分布 |
| `--calib-samples` | 校准样本数 |
| `--calib-seqlen` | 校准序列长度 |
| `--w-bits` | 权重量化位数（4 或 8） |
| `--w-group-size` | 量化分组大小 |
| `--work-dir` | 量化模型输出目录 |

简化版命令（使用默认参数）：

```bash
lmdeploy lite auto_awq internlm/internlm2_5-7b-chat --work-dir internlm2_5-7b-chat-4bit
```

**部署量化模型**

量化完成后，直接启动对话或 API 服务：

```bash
# 本地对话
lmdeploy chat ./internlm2_5-7b-chat-4bit --model-format awq

# API 服务
lmdeploy serve api_server ./internlm2_5-7b-chat-4bit \
  --backend turbomind \
  --model-format awq \
  --server-port 23333
```

**量化效果对比**

以 InternLM2.5-7B-Chat 在单张 RTX 4090（24GB）上的典型表现为参考：

| 精度 | 显存占用 | 推理速度（tokens/s） |
|------|---------|---------------------|
| FP16 | ~14 GB | ~50 |
| W4A16 (AWQ) | ~4 GB | ~120 |

W4A16 量化后，显存占用降低约 70%，推理速度提升约 2.4 倍。

**硬件要求**

W4A16 推理需要 NVIDIA Ampere 架构及以上的 GPU（RTX 3060 及以上、A100、H100 等）。

## 第 5 节：多模态模型部署

### 目标

使用 LMDeploy 部署 InternVL 系列视觉语言模型。

### 内容

LMDeploy 对多模态模型（VLM）的部署流程做了高度抽象，使用方式与纯文本模型基本一致。

**安装额外依赖**

```bash
pip install timm
```

**Python Pipeline 部署 InternVL**

```python
from lmdeploy import pipeline
from lmdeploy.vl import load_image

# 创建 VLM pipeline
pipe = pipeline("OpenGVLab/InternVL2_5-8B")

# 加载图片
image = load_image("https://raw.githubusercontent.com/open-mmlab/mmdeploy/main/tests/data/tiger.jpeg")

# 单图对话
response = pipe(("Describe this image in detail.", image))
print(response)
```

**多图对话**

```python
from lmdeploy import pipeline
from lmdeploy.vl import load_image

pipe = pipeline("OpenGVLab/InternVL2_5-8B")

image1 = load_image("image1.jpg")
image2 = load_image("image2.jpg")

response = pipe(("Compare these two images and describe the differences.", [image1, image2]))
print(response)
```

**启动多模态 API 服务**

```bash
lmdeploy serve api_server OpenGVLab/InternVL2_5-8B --server-port 23333
```

启动后同样提供 OpenAI 兼容的接口，支持通过 base64 或 URL 传入图片。

**使用 OpenAI SDK 调用多模态 API**

```python
import base64
from openai import OpenAI

client = OpenAI(api_key="EMPTY", base_url="http://localhost:23333/v1")

with open("photo.jpg", "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode("utf-8")

response = client.chat.completions.create(
    model=client.models.list().data[0].id,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
                {"type": "text", "text": "Describe this image."},
            ],
        }
    ],
)
print(response.choices[0].message.content)
```

## 第 6 节：分布式推理

### 目标

使用 Tensor Parallelism 在多卡上部署大规模模型。

### 内容

当模型参数量超过单张 GPU 的显存容量时，需要使用 Tensor Parallelism（TP）将模型切分到多张 GPU 上并行推理。

**多卡 TP 部署**

以 4 卡部署 78B 参数模型为例：

```bash
lmdeploy serve api_server OpenGVLab/InternVL2_5-78B \
  --tp 4 \
  --server-port 23333
```

`--tp` 参数指定张量并行度，通常设置为 GPU 数量。

**本地多卡对话**

```bash
lmdeploy chat internlm/internlm3-8b-instruct --tp 2
```

**控制 GPU 分配**

通过环境变量指定使用哪些 GPU：

```bash
CUDA_VISIBLE_DEVICES=0,1,2,3 lmdeploy serve api_server OpenGVLab/InternVL2_5-78B \
  --tp 4 \
  --server-port 23333
```

**TP 部署建议**

| 模型规模 | 推荐 TP | 最低显存配置 |
|---------|--------|------------|
| 1B-8B | 1 | 1x 24GB GPU |
| 14B-20B | 2 | 2x 24GB GPU |
| 40B-78B | 4 | 4x 40GB GPU |
| 100B+ | 8 | 8x 80GB GPU |

实际显存需求取决于量化精度、上下文长度和 batch size。W4A16 量化可以有效降低 TP 数量需求。

## 参考资料

- LMDeploy GitHub：https://github.com/InternLM/lmdeploy
- LMDeploy 文档：https://lmdeploy.readthedocs.io/
- LMDeploy PyPI：https://pypi.org/project/lmdeploy/
- TurboMind 引擎架构：https://lmdeploy.readthedocs.io/en/latest/inference/turbomind.html
- InternVL 部署指南：https://lmdeploy.readthedocs.io/en/latest/multi_modal/internvl.html
- AWQ 量化论文：https://arxiv.org/abs/2306.00978
