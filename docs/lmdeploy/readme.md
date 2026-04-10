# LMDeploy 模型部署

> 本文档 AI + 社区共建中

## 课程简介

LMDeploy 是书生生态中的高效推理部署工具，专为大语言模型和视觉语言模型的压缩、部署与服务化而设计。它的核心推理引擎 TurboMind 在吞吐量和延迟方面均达到业界领先水平。

本课程将从零开始，带你完成从安装、本地对话、API 服务搭建，到量化压缩、多模态部署和分布式推理的全流程实战。

## 学完本课你能做到

完成本课程后，你将掌握以下实战技能：

- 用较少显存运行 8B 参数的大语言模型（量化后约 4GB，视模型和配置而定）
- 搭建 OpenAI 兼容的 API 服务，让任意应用接入大模型能力
- 通过 W4A16 量化显著降低显存占用，提升推理吞吐
- 部署 InternVL3 多模态视觉语言模型，支持图片理解
- 在华为昇腾 Atlas 800T A2 上完成模型部署

下面是量化部署前后的关键指标对比，让你对课程成果有直观认识：

| 指标 | FP16 原始模型 | W4A16 量化后 |
|------|-------------|-------------|
| 模型精度 | 16-bit 浮点 | 4-bit 整数权重 + 16-bit 激活 |
| 显存占用（InternLM3-8B） | ~14 GB | ~4 GB |
| 推理速度（参考值，RTX 4090） | ~50 tokens/s | ~120 tokens/s |
| 最低 GPU 要求 | 1x 16GB GPU | 1x 6GB GPU |
| 模型质量 | 基准线 | 接近无损（AWQ 算法保障） |

## LMDeploy 概览

### 目标

理解 LMDeploy 在模型部署流程中的定位，以及它的核心技术优势。

### 内容

**什么是 LMDeploy？**

LMDeploy 是一个用于压缩、部署和服务化大语言模型（LLM）与视觉语言模型（VLM）的 Python 工具库。它由上海人工智能实验室开发维护，是书生生态中从训练到部署链路的关键一环。

**核心引擎**

LMDeploy 提供两个推理引擎：

| 引擎 | 语言 | 特点 | 适用场景 |
|------|------|------|---------|
| TurboMind | C++ / CUDA | 极致性能优化，吞吐量业界领先 | 生产环境、对性能有要求的场景 |
| PyTorch Engine | Python | 开发友好，降低二次开发门槛 | 快速验证、研究实验、自定义开发 |

**TurboMind 的核心技术**

- **Persistent Batch（持续批处理）**：动态管理多个推理请求，无需等待整个 batch 完成即可接纳新请求，最大化 GPU 利用率
- **Paged Attention（分页注意力）**：借鉴操作系统虚拟内存思想，将 KV Cache 分页存储，避免显存碎片化，支持更长的上下文和更大的并发量
- **高效量化推理**：支持 W4A16（4-bit 权重量化）、W8A8（8-bit 全量化）、FP8 等多种精度方案
- **Prefix Caching**：对共享的 system prompt 进行 KV Cache 复用，减少重复计算

**支持的模型**

LMDeploy 支持主流大模型：

- **LLM**：InternLM 系列、Llama 系列、Qwen 系列、DeepSeek-V3、Mistral、Gemma、ChatGLM 等
- **VLM**：InternVL2/3 系列、Qwen-VL 系列、DeepSeek-VL2、LLaVA、CogVLM2 等

## 安装与快速上手

### 目标

完成 LMDeploy 的安装，启动第一次本地对话，验证环境可用。

### 内容

**第一步：创建环境并安装**

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

预期输出类似：

```
lmdeploy version: 0.7.x
```

如果能正常输出版本号，说明安装成功。

**第二步：设置模型下载镜像（国内环境必做）**

HuggingFace 在国内访问不稳定，建议使用镜像：

```bash
export HF_ENDPOINT=https://hf-mirror.com
```

建议将此行加入 `~/.bashrc`，避免每次手动设置：

```bash
echo 'export HF_ENDPOINT=https://hf-mirror.com' >> ~/.bashrc
source ~/.bashrc
```

**第三步：一行命令启动对话**

LMDeploy 提供 CLI 工具，可以直接在终端与模型交互：

```bash
lmdeploy chat internlm/internlm3-8b-instruct
```

首次运行时会自动下载模型权重（约 16GB），下载完成后进入交互式对话界面。输入问题即可得到回复，输入 `exit` 退出。

**验证对话功能**

进入对话后，尝试以下测试：

```
double enter to end input >>> 用一句话解释什么是大语言模型
```

如果模型能正常回复，说明整个部署链路已经打通。

**选择推理引擎**

指定使用 TurboMind 引擎（默认，性能更优）：

```bash
lmdeploy chat internlm/internlm3-8b-instruct --backend turbomind
```

指定使用 PyTorch 引擎（兼容性更好）：

```bash
lmdeploy chat internlm/internlm3-8b-instruct --backend pytorch
```

**Python Pipeline 调用**

除了 CLI，还可以在 Python 中使用 pipeline 接口，方便集成到自己的应用中：

```python
import lmdeploy

with lmdeploy.pipeline("internlm/internlm3-8b-instruct") as pipe:
    response = pipe(["Hi, pls intro yourself", "What is deep learning?"])
    print(response)
```

## 搭建 OpenAI 兼容 API 服务

### 目标

将模型封装为 RESTful API 服务，兼容 OpenAI 接口协议，让任意应用都能接入大模型能力。

### 内容

搭建 API 服务是将大模型从"命令行玩具"变为"生产工具"的关键一步。LMDeploy 提供的 API 服务完全兼容 OpenAI 协议，这意味着所有基于 OpenAI SDK 开发的应用无需修改代码即可切换到你自己部署的模型。

**第一步：启动 API 服务**

一行命令即可将模型打包为 API 服务：

```bash
lmdeploy serve api_server internlm/internlm3-8b-instruct --server-port 23333
```

服务启动后，终端会打印类似以下信息：

```
INFO:     Uvicorn running on http://0.0.0.0:23333
```

此时可通过 `http://localhost:23333` 访问 Swagger UI 文档，查看所有可用接口。

**第二步：验证服务状态**

打开新终端，检查服务是否正常：

```bash
# 查看可用模型列表
curl http://localhost:23333/v1/models
```

预期返回包含模型名称的 JSON 响应。

**常用启动参数**

| 参数 | 说明 | 默认值 | 示例 |
|------|------|-------|------|
| `--server-port` | 服务端口 | `23333` | `8080` |
| `--tp` | Tensor Parallelism 卡数 | `1` | `2` |
| `--session-len` | 最大上下文长度 | 模型默认 | `8192` |
| `--cache-max-entry-count` | KV Cache 占 GPU 显存的比例 | `0.8` | `0.5` |
| `--backend` | 推理引擎 | `turbomind` | `pytorch` |
| `--log-level` | 日志级别 | `INFO` | `WARNING` |

显存紧张时，降低 `--cache-max-entry-count` 可以减少 KV Cache 占用，但会限制并发数量。

**第三步：使用 curl 调用**

```bash
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

**第四步：使用 Python OpenAI SDK 调用**

先安装 OpenAI SDK：

```bash
pip install openai
```

编写调用脚本：

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

**第五步：流式输出**

对于需要实时显示生成结果的场景（如聊天界面），使用流式调用：

```python
from openai import OpenAI

client = OpenAI(api_key="EMPTY", base_url="http://localhost:23333/v1")
model_name = client.models.list().data[0].id

stream = client.chat.completions.create(
    model=model_name,
    messages=[{"role": "user", "content": "详细介绍一下 Transformer 架构"}],
    stream=True,
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
print()  # 换行
```

**使用 LMDeploy 原生客户端**

LMDeploy 也提供了原生的 Python 客户端：

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

## 量化部署

### 目标

掌握 W4A16 量化方法，将 8B 模型的显存占用从 14GB 降低到 4GB，实现低显存高效部署。

### 内容

量化是将模型权重从高精度（如 FP16）压缩到低精度（如 4-bit）的技术。通过量化，你可以在消费级显卡上运行原本只能在专业卡上运行的模型。

**量化方案对比**

LMDeploy 支持多种量化方案，各有特点：

| 方案 | 权重精度 | 激活精度 | 显存节省 | 精度影响 | 适用场景 |
|------|---------|---------|---------|---------|---------|
| FP16 | 16-bit | 16-bit | 基准线 | 无 | 显存充足、精度要求最高 |
| W8A8 | 8-bit | 8-bit | ~50% | 极小 | 兼顾精度与效率 |
| W4A16 (AWQ) | 4-bit | 16-bit | ~70% | 小 | 显存受限、推荐首选 |
| FP8 | 8-bit 浮点 | 8-bit 浮点 | ~50% | 极小 | Hopper 架构 GPU |

本课程重点讲解最实用的 W4A16 量化。

**W4A16 量化：AWQ 算法**

W4A16 表示权重（Weight）量化到 4-bit，激活值（Activation）保持 16-bit。LMDeploy 采用 AWQ（Activation-aware Weight Quantization）算法，它的核心思想是：不同的权重对模型输出的影响不同，AWQ 通过分析激活值的分布，识别出"重要"的权重通道并给予更高精度的保护，从而在大幅压缩模型的同时保持质量。

**第一步：执行量化**

```bash
export HF_MODEL=internlm/internlm3-8b-instruct
export WORK_DIR=internlm3-8b-instruct-4bit

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

量化过程大约需要 15-30 分钟（取决于 GPU 性能），完成后会在 `$WORK_DIR` 目录下生成量化后的模型文件。

参数说明：

| 参数 | 说明 | 推荐值 |
|------|------|-------|
| `--calib-dataset` | 校准数据集，用于统计激活值分布 | `wikitext2` |
| `--calib-samples` | 校准样本数，越多越精确但越慢 | `128` |
| `--calib-seqlen` | 校准序列长度 | `2048` |
| `--w-bits` | 权重量化位数 | `4` |
| `--w-group-size` | 量化分组大小，越小精度越高 | `128` |
| `--batch-size` | 校准批大小，显存不够时设为 1 | `1` |
| `--work-dir` | 量化模型输出目录 | 自定义路径 |

如果使用默认参数，可以简化为：

```bash
lmdeploy lite auto_awq internlm/internlm3-8b-instruct --work-dir internlm3-8b-instruct-4bit
```

**第二步：验证量化模型**

量化完成后，先用本地对话验证模型质量：

```bash
lmdeploy chat ./internlm3-8b-instruct-4bit --model-format awq
```

建议测试以下几类问题，对比量化前后的回答质量：

- 常识问答："地球到月球的距离是多少？"
- 逻辑推理："如果所有的猫都是动物，所有的动物都需要水，那么猫需要水吗？"
- 代码生成："用 Python 写一个快速排序"
- 中文创作："写一首关于春天的五言绝句"

**第三步：部署量化模型为 API 服务**

```bash
lmdeploy serve api_server ./internlm3-8b-instruct-4bit \
  --backend turbomind \
  --model-format awq \
  --server-port 23333
```

**量化效果详细对比**

以 InternLM3-8B-Instruct 在不同显卡上的参考表现（实际数据与模型版本、上下文长度、并发数有关）：

| 配置 | 显存占用 | 推理速度 (tokens/s) | 是否可运行 |
|------|---------|-------------------|-----------|
| FP16 / RTX 4090 (24GB) | ~14 GB | ~50 | 可以 |
| FP16 / RTX 3060 (12GB) | OOM | - | 不可以 |
| W4A16 / RTX 4090 (24GB) | ~4 GB | ~120 | 可以 |
| W4A16 / RTX 3060 (12GB) | ~4 GB | ~60 | 可以 |
| W4A16 / RTX 3060 (6GB) | ~4 GB | ~40 | 可以（需降低 cache 比例） |

关键结论：

- W4A16 量化后，显存占用降低约 70%（从 14GB 到 4GB）
- 推理吞吐通常有显著提升（具体倍数与硬件和模型有关）
- 6GB 显卡也能运行 8B 模型（需搭配 `--cache-max-entry-count 0.2`）

**低显存部署技巧**

当显存非常紧张时（6GB 或以下），使用以下参数组合：

```bash
lmdeploy serve api_server ./internlm3-8b-instruct-4bit \
  --backend turbomind \
  --model-format awq \
  --cache-max-entry-count 0.2 \
  --server-port 23333
```

`--cache-max-entry-count 0.2` 表示 KV Cache 只占用 GPU 剩余显存的 20%，代价是并发能力下降，但单个请求的推理质量不受影响。

**精度影响分析**

AWQ 量化对模型质量的影响通常很小。在常用基准测试上的表现：

| 评测维度 | FP16 | W4A16 (AWQ) | 差异 |
|---------|------|-------------|------|
| 常识推理 | 基准 | -0.5% ~ -1% | 几乎无感 |
| 数学能力 | 基准 | -1% ~ -2% | 轻微下降 |
| 代码生成 | 基准 | -0.5% ~ -1.5% | 几乎无感 |
| 中文理解 | 基准 | -0.5% ~ -1% | 几乎无感 |

对于大多数应用场景（对话、问答、翻译、摘要），W4A16 量化后的体验与 FP16 几乎一致。数学和复杂推理场景可能有轻微下降，建议根据实际需求评估。

**硬件要求**

W4A16 推理需要 NVIDIA Ampere 架构及以上的 GPU（RTX 3060 及以上、A100、H100 等），或华为昇腾 Atlas 800T A2 等国产加速卡。

## 多模态模型部署

### 目标

使用 LMDeploy 部署 InternVL3 系列视觉语言模型，实现图片理解和多模态对话。

### 内容

LMDeploy 对多模态模型（VLM）的部署流程做了高度抽象，使用方式与纯文本模型基本一致。InternVL3 是书生生态中最新的视觉语言模型系列，在多个多模态评测上达到领先水平。

**安装额外依赖**

```bash
pip install timm
```

**方式一：Python Pipeline 部署 InternVL3**

```python
from lmdeploy import pipeline
from lmdeploy.vl import load_image

# 创建 VLM pipeline（首次运行自动下载模型）
pipe = pipeline("OpenGVLab/InternVL3-8B")

# 加载图片（支持本地路径和 URL）
image = load_image("https://raw.githubusercontent.com/open-mmlab/mmdeploy/main/tests/data/tiger.jpeg")

# 单图对话
response = pipe(("Describe this image in detail.", image))
print(response)
```

**多图对话**

InternVL3 支持同时理解多张图片：

```python
from lmdeploy import pipeline
from lmdeploy.vl import load_image

pipe = pipeline("OpenGVLab/InternVL3-8B")

image1 = load_image("image1.jpg")
image2 = load_image("image2.jpg")

response = pipe(("Compare these two images and describe the differences.", [image1, image2]))
print(response)
```

**方式二：启动多模态 API 服务**

```bash
lmdeploy serve api_server OpenGVLab/InternVL3-8B --server-port 23333
```

启动后提供 OpenAI 兼容的 Vision API 接口，支持通过 base64 或 URL 传入图片。

**验证 Vision API**

使用 curl 发送包含图片的请求：

```bash
curl http://localhost:23333/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "InternVL3-8B",
    "messages": [
      {
        "role": "user",
        "content": [
          {"type": "image_url", "image_url": {"url": "https://raw.githubusercontent.com/open-mmlab/mmdeploy/main/tests/data/tiger.jpeg"}},
          {"type": "text", "text": "这张图片里有什么？请用中文描述。"}
        ]
      }
    ]
  }'
```

**使用 OpenAI SDK 调用 Vision API**

```python
import base64
from openai import OpenAI

client = OpenAI(api_key="EMPTY", base_url="http://localhost:23333/v1")

# 方式 A：通过 URL 传入图片
response = client.chat.completions.create(
    model=client.models.list().data[0].id,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": "https://example.com/photo.jpg"}},
                {"type": "text", "text": "描述这张图片的内容。"},
            ],
        }
    ],
)
print(response.choices[0].message.content)

# 方式 B：通过 base64 传入本地图片
with open("photo.jpg", "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode("utf-8")

response = client.chat.completions.create(
    model=client.models.list().data[0].id,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
                {"type": "text", "text": "这张图片里有什么？"},
            ],
        }
    ],
)
print(response.choices[0].message.content)
```

**InternVL3 模型规格选择**

| 模型 | 参数量 | 最低显存 | 适用场景 |
|------|-------|---------|---------|
| InternVL3-1B | 1B | 4 GB | 端侧部署、轻量应用 |
| InternVL3-2B | 2B | 6 GB | 消费级显卡 |
| InternVL3-8B | 8B | 16 GB | 单卡推荐、通用场景 |
| InternVL3-78B | 78B | 4x 40GB | 多卡部署、精度优先 |

## 分布式推理

### 目标

使用 Tensor Parallelism 在多卡上部署大规模模型。

### 内容

当模型参数量超过单张 GPU 的显存容量时，需要使用 Tensor Parallelism（TP）将模型切分到多张 GPU 上并行推理。

**多卡 TP 部署**

以 4 卡部署 78B 参数模型为例：

```bash
lmdeploy serve api_server OpenGVLab/InternVL3-78B \
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
CUDA_VISIBLE_DEVICES=0,1,2,3 lmdeploy serve api_server OpenGVLab/InternVL3-78B \
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

实际显存需求取决于量化精度、上下文长度和 batch size。W4A16 量化可以有效降低 TP 数量需求，例如 78B 模型量化后可以用 2 卡 80GB 运行，而非 4 卡。

## 华为昇腾 Atlas 800T A2 部署

### 目标

在华为昇腾 Atlas 800T A2 上完成 LMDeploy 的安装与模型部署。

### 内容

LMDeploy 支持在华为昇腾 Atlas 800T A2 上部署大语言模型，使用 PyTorch Engine 作为推理后端。这为国产硬件生态提供了完整的模型部署方案。

**环境要求**

| 项目 | 要求 |
|------|------|
| 硬件 | 华为昇腾 Atlas 800T A2 |
| CANN 版本 | 8.0 及以上 |
| Python | 3.10 / 3.11 |
| PyTorch | 2.5+ |
| torch_npu | 与 PyTorch 版本匹配 |

**安装步骤**

首先确保昇腾基础环境已配置：

```bash
# 加载昇腾驱动和工具包环境变量
export LD_LIBRARY_PATH=/usr/local/Ascend/driver/lib64:$LD_LIBRARY_PATH
source /usr/local/Ascend/ascend-toolkit/set_env.sh
```

安装 LMDeploy：

```bash
conda create -n lmdeploy python=3.11 -y
conda activate lmdeploy
pip install lmdeploy
```

**启动对话**

在昇腾上需要使用 PyTorch Engine（TurboMind 目前仅支持 CUDA）：

```bash
lmdeploy chat internlm/internlm3-8b-instruct --backend pytorch
```

**启动 API 服务**

```bash
lmdeploy serve api_server internlm/internlm3-8b-instruct \
  --backend pytorch \
  --server-port 23333
```

API 接口与 NVIDIA GPU 上完全一致，上层应用代码无需任何修改。

**注意事项**

- 昇腾平台目前仅支持 PyTorch Engine，不支持 TurboMind 引擎
- W4A16 (AWQ) 量化对昇腾的支持可能受限，建议使用 FP16 或 W8A8 方案
- 多卡 TP 部署可用，`--tp` 参数按照 NPU 卡数设置
- 如遇到 Flash Attention 相关错误，可尝试使用 SDPA 替代方案
- 建议关注 LMDeploy 官方文档获取最新的昇腾兼容性信息

## FAQ 常见问题

### 显存不够怎么办？

这是部署大模型最常遇到的问题。按照以下优先级尝试：

**方案一：使用 W4A16 量化**

量化是最有效的手段，可以将显存占用降低约 70%。参考本文"量化部署"章节。

**方案二：降低 KV Cache 占比**

通过 `--cache-max-entry-count` 参数限制 KV Cache 使用的显存比例：

```bash
# 将 KV Cache 占用从默认的 80% 降低到 20%
lmdeploy serve api_server internlm/internlm3-8b-instruct \
  --cache-max-entry-count 0.2 \
  --server-port 23333
```

代价是并发能力下降，但单个请求不受影响。

**方案三：缩短上下文长度**

```bash
lmdeploy serve api_server internlm/internlm3-8b-instruct \
  --session-len 2048 \
  --server-port 23333
```

将上下文从默认的 8192 缩短到 2048，可以显著减少 KV Cache 的显存开销。

**方案四：使用更小的模型**

如果以上方案仍然无法满足，考虑使用参数量更小的模型，如 InternLM3-1.8B 或 InternVL3-2B。

**方案五：多卡分布式**

如果有多张 GPU，使用 `--tp` 参数将模型切分到多卡上。

### API 并发性能怎么优化？

LMDeploy 的 API 服务默认已有良好的并发性能，以下参数可以进一步调优：

```bash
lmdeploy serve api_server internlm/internlm3-8b-instruct \
  --cache-max-entry-count 0.8 \
  --session-len 4096 \
  --server-port 23333
```

关键优化点：

- `--cache-max-entry-count 0.8`：让 KV Cache 使用更多显存，支持更多并发请求
- `--session-len`：根据实际需求设置，不要盲目使用最大值
- 生产环境建议结合 Nginx 做负载均衡，将多个 LMDeploy 实例部署在不同 GPU 上

典型并发性能参考（单卡 A100 80GB，InternLM3-8B，FP16）：

| 并发数 | 平均延迟 | 吞吐量 (tokens/s) |
|-------|---------|------------------|
| 1 | ~50ms/token | ~50 |
| 8 | ~80ms/token | ~300 |
| 16 | ~120ms/token | ~500 |
| 32 | ~200ms/token | ~600 |

### 如何切换到其他模型？

LMDeploy 支持所有 HuggingFace 格式的兼容模型。替换模型只需要修改模型路径：

```bash
# 部署 Qwen 模型
lmdeploy serve api_server Qwen/Qwen2.5-7B-Instruct --server-port 23333

# 部署 Llama 模型
lmdeploy serve api_server meta-llama/Llama-3.1-8B-Instruct --server-port 23333

# 部署本地模型
lmdeploy serve api_server /path/to/your/local/model --server-port 23333
```

注意事项：
- 不同模型的对话模板会自动适配，无需手动指定
- 如果使用量化模型，记得加上 `--model-format awq` 参数
- 部分新模型可能需要升级 LMDeploy 到最新版本才能支持

### 常见错误及解决方案

**错误：CUDA out of memory**

```
torch.cuda.OutOfMemoryError: CUDA out of memory.
```

解决方案：参考上方"显存不够怎么办"中的方案。最快的解决办法是加 `--cache-max-entry-count 0.2`。

**错误：模型下载失败**

```
ConnectionError: Couldn't connect to HuggingFace
```

解决方案：设置镜像源。

```bash
export HF_ENDPOINT=https://hf-mirror.com
```

**错误：ImportError: No module named 'xxx'**

解决方案：确保在正确的 conda 环境中，并检查依赖安装。

```bash
conda activate lmdeploy
pip install lmdeploy --upgrade
# 部署多模态模型额外安装
pip install timm
```

**错误：端口已被占用**

```
OSError: [Errno 98] Address already in use
```

解决方案：更换端口或者终止占用端口的进程。

```bash
# 查看占用端口的进程
lsof -i :23333
# 终止进程
kill -9 <PID>
# 或者直接换一个端口
lmdeploy serve api_server internlm/internlm3-8b-instruct --server-port 23334
```

**错误：量化时内存不足（RAM 不足，非显存）**

量化过程需要将整个模型加载到 CPU 内存中，8B 模型至少需要 32GB RAM。

解决方案：降低 `--batch-size` 或使用更大内存的机器。也可以直接使用社区已量化好的模型，如 `internlm/internlm3-8b-instruct-4bit`（如果可用）。

## 参考资料

- LMDeploy GitHub：https://github.com/InternLM/lmdeploy
- LMDeploy 文档：https://lmdeploy.readthedocs.io/
- LMDeploy PyPI：https://pypi.org/project/lmdeploy/
- TurboMind 引擎架构：https://lmdeploy.readthedocs.io/en/latest/inference/turbomind.html
- InternVL 部署指南：https://lmdeploy.readthedocs.io/en/latest/multi_modal/internvl.html
- AWQ 量化论文：https://arxiv.org/abs/2306.00978
- 华为昇腾 LMDeploy 适配：https://lmdeploy.readthedocs.io/en/latest/get_started/ascend/get_started.html
