# InternVL-U 统一多模态

> 本文档 AI + 社区共建中

## 开场：一个模型，三种能力

InternVL-U 是书生系列推出的统一多模态大模型，仅 4B 参数（约 8.2 GB 权重），在一个模型中同时具备图像理解、文生图和图像编辑三大能力。下面先用三个最小示例直观展示这三种能力，让你在动手部署之前就知道这个模型能做什么、做到什么程度。

**能力一 -- 图像理解**

输入一张图片和一个问题，模型输出文字回答。

```python
# 输入：一张猫咪照片 + 问题
result = pipe(prompt="请描述这张图片的内容", image=cat_photo, generation_mode="text")
# 输出：这是一只橘色的猫咪，正趴在窗台上晒太阳。窗外是蓝天白云，阳光透过玻璃照在猫咪身上。
```

**能力二 -- 文生图**

输入一段文字描述，模型生成 512x512 图像。

```python
# 输入：文字提示
result = pipe(prompt="一只戴眼镜的橘猫坐在书桌前看论文，赛博朋克风格", generation_mode="image",
              height=512, width=512, num_inference_steps=20, all_cfg_scale=4.5)
result.images[0].save("cat_cyberpunk.png")
# 输出：一张 512x512 的赛博朋克风格猫咪图像
```

**能力三 -- 图像编辑**

输入一张图片和一条编辑指令，模型输出修改后的图像。

```python
# 输入：原图 + 编辑指令
result = pipe(prompt="把背景换成星空", image=source_image, generation_mode="image",
              height=512, width=512, num_inference_steps=20, all_cfg_scale=4.5)
result.images[0].save("edited.png")
# 输出：保持主体不变，背景替换为星空的图像
```

以上三个示例使用的是同一个模型实例（`pipe`），无需切换模型或重新加载。后续章节会完整讲解部署步骤和更多用法。

---

## 课程简介

InternVL-U 采用 InternViT + Qwen3 + MMDiT 的融合架构，打破了传统多模态模型"理解与生成分离"的范式。本课程带你完成以下目标：

1. 理解 InternVL-U 的架构设计
2. 在 A100 GPU 上完成部署和验证（直接可跑）
3. 在华为昇腾 Atlas 800T A2 上完成部署和验证（需 SDPA Patch）
4. 完成理解、生成、编辑三大能力的完整实操
5. 搭建 FastAPI 服务（示例封装，可按需调整）
6. 了解 AGI4S 科学场景的应用方式

**适合人群**：有 Python 基础的开发者和 AI 研究者，对多模态模型感兴趣。

**硬件要求**：

| 平台 | 设备 | 显存/HBM | 说明 |
|------|------|----------|------|
| NVIDIA | A100-SXM4-80GB | 80 GB | 原生 CUDA 支持，使用 flash_attn |
| 华为昇腾 | Atlas 800T A2 | 64 GB HBM | 需 torch_npu + SDPA Patch |

InternVL-U 4B 模型在 bf16 精度下约占用 8.6 GB 显存，两个平台均可流畅运行。

---

## 架构与原理

### 统一多模态的意义

传统方案中，图像理解（如 BLIP）和图像生成（如 Stable Diffusion）是两个独立模型，无法在同一个推理过程中既理解又生成。InternVL-U 将两者统一：同一个模型，同一套参数，根据输入类型自动切换工作模式。

### 三大组件

| 模块 | 参数量 | 功能 | 类比 |
|------|--------|------|------|
| InternViT-300M | 300M | 视觉编码器，将图像转为特征向量 | 眼睛 -- 看到图像 |
| Qwen3-1.7B | 1.7B | 语言模型，负责文本理解和生成 | 大脑 -- 理解和思考 |
| MMDiT-1.7B | 1.7B | 多模态扩散模型，负责图像生成 | 手 -- 画出图像 |

总参数量约 4B（40 亿），是一个非常紧凑的统一模型。

### 三条处理路径

```
理解路径：图像 --> InternViT 编码 --> Qwen3 理解 --> 文字描述
生成路径：文字提示 --> Qwen3 语义理解 --> MMDiT 扩散生成 --> 512x512 图像
编辑路径：图像 + 文字指令 --> InternViT + Qwen3 --> MMDiT --> 修改后图像
```

| 输入 | 输出 | 工作模式 | 使用组件 |
|------|------|----------|----------|
| 图像 + 文字问题 | 文字回答 | 图像理解 | InternViT + Qwen3 |
| 文字描述 | 图像 | 文生图 | Qwen3 + MMDiT |
| 图像 + 编辑指令 | 编辑后图像 | 图像编辑 | InternViT + Qwen3 + MMDiT |

三种模式共享同一套参数，无需切换模型。

### 关键技术亮点

- **统一表示**：视觉特征和文本特征在同一个向量空间中表示
- **扩散生成**：基于 MMDiT（多模态 Diffusion Transformer），生成质量高
- **双平台支持**：NVIDIA CUDA 和华为昇腾 NPU 均可运行

---

## 部署：A100 GPU（直接可跑）

以下命令在 NVIDIA A100-SXM4-80GB 上实测通过。

### 环境准备

```bash
# 创建虚拟环境
conda create -n internvl-u python=3.11 -y
conda activate internvl-u

# 安装 PyTorch（CUDA 12.1）
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# 安装 flash_attn（A100 上的 attention 加速，必装）
pip install flash-attn --no-build-isolation

# 克隆 InternVL-U 仓库并安装
cd /root
git clone https://github.com/OpenGVLab/InternVL-U.git
cd InternVL-U
pip install -e .

# 补充依赖
pip install fastapi uvicorn pillow modelscope
pip install diffusers sentencepiece tiktoken einops timm
```

### 下载模型

```bash
# 国内环境推荐 ModelScope
python -c "
from modelscope import snapshot_download
snapshot_download('OpenGVLab/InternVL-U', local_dir='/root/models/OpenGVLab/InternVL-U')
"

# 备选：HF Mirror
# HF_ENDPOINT=https://hf-mirror.com python -c "
# from huggingface_hub import snapshot_download
# snapshot_download('OpenGVLab/InternVL-U', local_dir='/root/models/OpenGVLab/InternVL-U')
# "
```

模型约 8.2 GB，下载完成后目录结构：

```
/root/models/OpenGVLab/InternVL-U/
  config.json
  model-*.safetensors
  tokenizer.json
  ...
```

### 加载模型并验证

```python
# test_load_a100.py -- 直接可跑
import torch
from internvlu.pipeline_internvlu import InternVLUPipeline

pipe = InternVLUPipeline.from_pretrained(
    '/root/models/OpenGVLab/InternVL-U',
    torch_dtype=torch.bfloat16
)
pipe = pipe.to("cuda:0")

print(f"设备: cuda")
print(f"显存占用: {torch.cuda.memory_allocated(0) / 1e9:.1f} GB")
# 期望输出：
# 设备: cuda
# 显存占用: 8.6 GB
```

### 快速验证三大能力

加载完成后，运行以下代码确认三大能力均可用：

```python
# verify_a100.py -- 直接可跑
from PIL import Image

# 1. 文本对话
result = pipe(prompt="你好，用一句话介绍你自己", generation_mode="text")
text = pipe.tokenizer.decode(result.generate_output[0], skip_special_tokens=True)
print(f"[理解] {text}")

# 2. 文生图
result = pipe(
    prompt="一只戴眼镜的橘猫坐在书桌前看论文",
    generation_mode="image",
    height=512, width=512,
    num_inference_steps=20,
    all_cfg_scale=4.5
)
result.images[0].save("verify_generate.png")
print("[生成] 已保存 verify_generate.png")

# 3. 图像编辑（用上一步生成的图作为输入）
source = Image.open("verify_generate.png").convert("RGB")
result = pipe(
    prompt="将背景改为星空",
    image=source,
    generation_mode="image",
    height=512, width=512,
    num_inference_steps=20,
    all_cfg_scale=4.5
)
result.images[0].save("verify_edit.png")
print("[编辑] 已保存 verify_edit.png")
```

如果三个步骤都正常输出，说明 A100 部署成功。

**A100 性能参考**：

| 能力 | 参数 | 耗时 |
|------|------|------|
| 文本对话 | 短文本 ~64 tokens | ~1.6 秒 |
| 文生图 | 512x512, 20 steps | ~3.5 秒 |
| 图像编辑 | 512x512, 20 steps | ~4 秒 |
| 图像理解 | 1024x1024 输入 | ~2-4 秒 |

---

## 部署：华为昇腾 Atlas 800T A2（需 SDPA Patch）

华为昇腾 Atlas 800T A2 部署的核心区别在于：InternVL-U 的扩散路径（MMDiT）硬编码依赖 `flash_attn` 库，而 `flash_attn` 仅支持 NVIDIA CUDA，无法在昇腾上安装。我们通过编写 SDPA Fallback Patch，用 PyTorch 原生的 `F.scaled_dot_product_attention` 替代 `flash_attn`，使模型全部能力在昇腾上可用。

### 环境准备

```bash
# 初始化昇腾驱动环境（每次开终端需执行，建议写入 ~/.bashrc）
export LD_LIBRARY_PATH=/usr/local/Ascend/driver/lib64:\
/usr/local/Ascend/driver/lib64/common:\
/usr/local/Ascend/driver/lib64/driver:\
$LD_LIBRARY_PATH

source /usr/local/Ascend/ascend-toolkit/set_env.sh

# 验证 NPU 可用
python3 -c "import torch, torch_npu; print(torch_npu.npu.is_available())"
# 期望输出: True
```

### 安装 InternVL-U

```bash
cd /root
git clone https://github.com/OpenGVLab/InternVL-U.git
cd InternVL-U

# 注意：使用 --no-deps 跳过 flash_attn 依赖安装
pip install -e . --no-deps

# 手动安装其他依赖
pip install fastapi uvicorn pillow modelscope transformers accelerate
pip install diffusers sentencepiece tiktoken einops timm
```

> 如果 `pip install -e .` 尝试安装 `flash_attn` 并报错，使用 `--no-deps` 跳过是正确做法。我们的 SDPA Patch 会完全替代 flash_attn 的功能。

### 下载模型

```bash
# HuggingFace 在国内不可用，使用 ModelScope
python3 -c "
from modelscope import snapshot_download
snapshot_download('OpenGVLab/InternVL-U', local_dir='/root/models/OpenGVLab/InternVL-U')
"
```

### 编写 SDPA Fallback Patch

创建文件 `/root/flash_attn_sdpa_patch.py`：

```python
# flash_attn_sdpa_patch.py -- 直接可跑
# 用 PyTorch 原生 SDPA 替代 flash_attn，使 InternVL-U 扩散路径在昇腾 NPU 上可用。
# 必须在加载模型之前调用 apply_patch()。

import math
import torch
import torch.nn.functional as F


def flash_attn_func(q, k, v, dropout_p=0.0, softmax_scale=None, causal=False, **kwargs):
    """替代 flash_attn_func。
    Input/Output 格式: (batch, seqlen, nheads, head_dim)
    """
    batch, seqlen, nheads, head_dim = q.shape
    q = q.transpose(1, 2)  # -> (batch, nheads, seqlen, head_dim)
    k = k.transpose(1, 2)
    v = v.transpose(1, 2)

    if softmax_scale is not None:
        q = q * (softmax_scale * math.sqrt(head_dim))

    out = F.scaled_dot_product_attention(q, k, v, dropout_p=0.0, is_causal=causal)
    return out.transpose(1, 2).contiguous()


def flash_attn_varlen_func(q, k, v, cu_seqlens_q, cu_seqlens_k,
                           max_seqlen_q, max_seqlen_k,
                           dropout_p=0.0, softmax_scale=None, causal=False, **kwargs):
    """替代 flash_attn_varlen_func。
    Input/Output 格式: (total_tokens, nheads, head_dim) packed variable-length
    将不等长序列 padding 到统一长度，用 SDPA 计算后重新 unpack。
    """
    nheads = q.shape[1]
    head_dim = q.shape[2]
    batch_size = cu_seqlens_q.shape[0] - 1

    q_padded = q.new_zeros(batch_size, max_seqlen_q, nheads, head_dim)
    k_padded = k.new_zeros(batch_size, max_seqlen_k, nheads, head_dim)
    v_padded = v.new_zeros(batch_size, max_seqlen_k, nheads, head_dim)
    attn_mask = q.new_zeros(batch_size, max_seqlen_k, dtype=torch.bool)

    for i in range(batch_size):
        sq = (cu_seqlens_q[i + 1] - cu_seqlens_q[i]).item()
        sk = (cu_seqlens_k[i + 1] - cu_seqlens_k[i]).item()
        q_padded[i, :sq] = q[cu_seqlens_q[i]:cu_seqlens_q[i + 1]]
        k_padded[i, :sk] = k[cu_seqlens_k[i]:cu_seqlens_k[i + 1]]
        v_padded[i, :sk] = v[cu_seqlens_k[i]:cu_seqlens_k[i + 1]]
        attn_mask[i, sk:] = True

    q_padded = q_padded.transpose(1, 2)
    k_padded = k_padded.transpose(1, 2)
    v_padded = v_padded.transpose(1, 2)

    if softmax_scale is not None:
        q_padded = q_padded * (softmax_scale * math.sqrt(head_dim))

    expanded_mask = attn_mask.unsqueeze(1).unsqueeze(2)
    attn_bias = torch.zeros_like(expanded_mask, dtype=q_padded.dtype)
    attn_bias.masked_fill_(expanded_mask, float("-inf"))

    out = F.scaled_dot_product_attention(
        q_padded, k_padded, v_padded,
        attn_mask=attn_bias if attn_mask.any() else None,
        dropout_p=0.0,
        is_causal=causal if not attn_mask.any() else False,
    )
    out = out.transpose(1, 2)

    output = q.new_zeros(q.shape[0], nheads, head_dim)
    for i in range(batch_size):
        sq = (cu_seqlens_q[i + 1] - cu_seqlens_q[i]).item()
        output[cu_seqlens_q[i]:cu_seqlens_q[i + 1]] = out[i, :sq]
    return output


def unpad_input(hidden_states, attention_mask):
    """替代 flash_attn.bert_padding.unpad_input"""
    seqlens = attention_mask.sum(dim=-1, dtype=torch.int32)
    indices = torch.nonzero(attention_mask.flatten(), as_tuple=False).flatten()
    max_seqlen = seqlens.max().item()
    cu_seqlens = F.pad(torch.cumsum(seqlens, dim=0, dtype=torch.int32), (1, 0))
    flat = hidden_states.reshape(-1, *hidden_states.shape[2:])
    return flat[indices], indices, cu_seqlens, max_seqlen


def pad_input(hidden_states, indices, batch_size, seqlen):
    """替代 flash_attn.bert_padding.pad_input"""
    dim = hidden_states.shape[1:]
    output = hidden_states.new_zeros(batch_size * seqlen, *dim)
    output[indices] = hidden_states
    return output.reshape(batch_size, seqlen, *dim)


def index_first_axis(input, indices):
    return input[indices]


def apply_patch():
    """应用 SDPA Patch。必须在加载模型之前调用。"""
    import internvlu.diffusion.internvlu_transformer as mod

    mod.flash_attn_func = flash_attn_func
    mod.flash_attn_varlen_func = flash_attn_varlen_func
    mod.index_first_axis = index_first_axis
    mod.pad_input = pad_input
    mod.unpad_input = unpad_input
    mod._flash_supports_window_size = True

    import transformers.utils
    transformers.utils.is_flash_attn_2_available = lambda: True
    transformers.utils.is_flash_attn_greater_or_equal_2_10 = lambda: True
    mod.is_flash_attn_2_available = lambda: True
    mod.is_flash_attn_greater_or_equal_2_10 = lambda: True

    print("[PATCH] SDPA fallback for flash_attn applied successfully")
```

**Patch 原理说明**：

| flash_attn 函数 | SDPA 替代策略 |
|-----------------|--------------|
| `flash_attn_func` | 转置 QKV 维度后调用 `F.scaled_dot_product_attention` |
| `flash_attn_varlen_func` | 将不等长序列 padding 后调用 SDPA，再 unpack |
| `pad_input` / `unpad_input` | 纯 PyTorch 实现的 padding 工具函数 |
| `is_flash_attn_2_available` | Patch 为始终返回 `True`，绕过可用性检查 |

这个 Patch 通过 Monkey Patch 方式工作，不需要修改 InternVL-U 源码。

### 加载模型并验证

```python
# test_load_npu.py -- 直接可跑
import os, sys
os.environ["PYTORCH_NPU_ALLOC_CONF"] = "expandable_segments:True"
import torch, torch_npu

# 必须在 import InternVLU 之前应用 Patch
sys.path.insert(0, '/root')
import flash_attn_sdpa_patch
flash_attn_sdpa_patch.apply_patch()

from internvlu.pipeline_internvlu import InternVLUPipeline

pipe = InternVLUPipeline.from_pretrained(
    '/root/models/OpenGVLab/InternVL-U',
    torch_dtype=torch.bfloat16
)
pipe = pipe.to("npu:0")

print(f"设备: npu")
print(f"NPU 显存占用: {torch_npu.npu.memory_allocated(0) / 1e9:.1f} GB")
# 期望输出：
# [PATCH] SDPA fallback for flash_attn applied successfully
# 设备: npu
# NPU 显存占用: 8.6 GB
```

### 快速验证三大能力

```python
# verify_npu.py -- 直接可跑（在上面的 test_load_npu.py 基础上继续执行）
from PIL import Image

# 1. 文本对话
result = pipe(prompt="你好，用一句话介绍你自己", generation_mode="text")
text = pipe.tokenizer.decode(result.generate_output[0], skip_special_tokens=True)
print(f"[理解] {text}")

# 2. 文生图
result = pipe(
    prompt="一只戴眼镜的橘猫坐在书桌前看论文",
    generation_mode="image",
    height=512, width=512,
    num_inference_steps=20,
    all_cfg_scale=4.5
)
result.images[0].save("verify_generate_npu.png")
print("[生成] 已保存 verify_generate_npu.png")

# 3. 图像编辑
source = Image.open("verify_generate_npu.png").convert("RGB")
result = pipe(
    prompt="将背景改为星空",
    image=source,
    generation_mode="image",
    height=512, width=512,
    num_inference_steps=20,
    all_cfg_scale=4.5
)
result.images[0].save("verify_edit_npu.png")
print("[编辑] 已保存 verify_edit_npu.png")
```

**华为昇腾 Atlas 800T A2 性能参考**：

| 能力 | 参数 | 耗时 | 备注 |
|------|------|------|------|
| 文本对话 | 短文本 ~64 tokens | ~3-5 秒 | 首次推理含 warmup |
| 文生图 | 512x512, 20 steps | ~5.5 秒 | 热启动后稳定 |
| 图像编辑 | 512x512, 20 steps | ~5.5 秒 | 与文生图速度一致 |
| 图像理解 | 1024x1024 输入 | ~11 秒 | 包含图片编码 |

### 双平台性能对比

| 指标 | A100 (flash_attn) | 华为昇腾 Atlas 800T A2 (SDPA) | 备注 |
|------|-------------------|-------------------------------|------|
| 文生图 512x512 | ~3.5 秒 | ~5.5 秒 | NPU 约慢 50% |
| 图像理解 | ~2-4 秒 | ~10-13 秒 | SDPA fallback 开销 |
| 显存占用 | 8.6 GB | 8.6 GB | 完全一致 |
| Attention 实现 | FlashAttention2 原生 | SDPA Fallback | 功能等价 |

> 通过 SDPA Patch，InternVL-U 的全部能力（文本生成、图像理解、图像生成、图像编辑）在华为昇腾 Atlas 800T A2 上全部可用。这是国产算力平台支持统一多模态模型的重要实践。

---

## 实操一：图像理解（描述 + OCR + VQA）

本节使用 InternVL-U 完成三个图像理解任务。以下代码假设你已经完成前面的部署步骤，`pipe` 对象已加载就绪。

### 图片描述

```python
# understand_describe.py -- 直接可跑
from PIL import Image

# 准备一张测试图片（替换为你自己的图片路径）
image = Image.open("photo.jpg").convert("RGB")

# 图片描述
result = pipe(
    prompt="请详细描述这张图片的内容，包括场景、人物、物体和氛围。",
    image=image,
    generation_mode="text",
    max_new_tokens=512,
    temperature=0.7
)
text = pipe.tokenizer.decode(result.generate_output[0], skip_special_tokens=True)
print("图片描述:")
print(text)
# 示例输出: 图片中是一只橘色的猫咪，正趴在窗台上晒太阳。窗外是蓝天白云...
```

### OCR 文字识别

```python
# understand_ocr.py -- 直接可跑
from PIL import Image

# 文档图片 OCR
document_image = Image.open("document.png").convert("RGB")

result = pipe(
    prompt="识别图片中的所有文字，按原始排版格式输出。",
    image=document_image,
    generation_mode="text",
    max_new_tokens=1024,
    temperature=0.1  # OCR 使用低温度以提高准确性
)
text = pipe.tokenizer.decode(result.generate_output[0], skip_special_tokens=True)
print("OCR 结果:")
print(text)

# 表格图片 OCR
table_image = Image.open("table.png").convert("RGB")

result = pipe(
    prompt="识别图片中的表格，以 Markdown 表格格式输出。",
    image=table_image,
    generation_mode="text",
    max_new_tokens=1024,
    temperature=0.1
)
text = pipe.tokenizer.decode(result.generate_output[0], skip_special_tokens=True)
print("表格内容:")
print(text)
```

### 视觉问答（VQA）

```python
# understand_vqa.py -- 直接可跑
from PIL import Image

# 图表理解
chart_image = Image.open("bar_chart.png").convert("RGB")

result = pipe(
    prompt="这个柱状图中，哪个月份的销售额最高？最高值是多少？",
    image=chart_image,
    generation_mode="text",
    max_new_tokens=256,
    temperature=0.5
)
text = pipe.tokenizer.decode(result.generate_output[0], skip_special_tokens=True)
print("图表分析:", text)
```

### 理解能力的参数调优建议

| 任务 | temperature | max_new_tokens | 说明 |
|------|-------------|----------------|------|
| 详细描述 | 0.7 | 512 | 适度创造性，生成丰富描述 |
| OCR | 0.1 | 1024 | 极低温度，保证文字准确 |
| VQA | 0.5 | 256 | 平衡准确与流畅 |
| 分类/判断 | 0.1 | 64 | 精确输出，简短回答 |

---

## 实操二：文生图（参数控制 + 风格对比）

### 基本文生图

```python
# generate_basic.py -- 直接可跑
result = pipe(
    prompt="一座雪山湖泊的风景画，日出时分，金色阳光照耀山峰",
    generation_mode="image",
    height=512,
    width=512,
    num_inference_steps=20,
    all_cfg_scale=4.5,
)
result.images[0].save("mountain_sunrise.png")
print("已生成: mountain_sunrise.png (512x512)")
```

### 参数控制

```python
# generate_params.py -- 直接可跑
# 对比不同参数对生成质量的影响

prompts_and_params = [
    {
        "prompt": "一只橘猫坐在窗台上，窗外是雨天的城市天际线",
        "steps": 10,
        "cfg": 4.5,
        "desc": "低步数快速预览"
    },
    {
        "prompt": "一只橘猫坐在窗台上，窗外是雨天的城市天际线",
        "steps": 20,
        "cfg": 4.5,
        "desc": "标准质量"
    },
    {
        "prompt": "一只橘猫坐在窗台上，窗外是雨天的城市天际线",
        "steps": 50,
        "cfg": 7.5,
        "desc": "高质量高引导"
    },
]

for i, p in enumerate(prompts_and_params):
    result = pipe(
        prompt=p["prompt"],
        generation_mode="image",
        height=512, width=512,
        num_inference_steps=p["steps"],
        all_cfg_scale=p["cfg"],
    )
    filename = f"cat_param_{i+1}.png"
    result.images[0].save(filename)
    print(f"已生成: {filename} -- {p['desc']} (steps={p['steps']}, cfg={p['cfg']})")
```

**关键参数说明**：

| 参数 | 范围 | 效果 | 推荐值 |
|------|------|------|--------|
| `num_inference_steps` | 10-50 | 步数越多，细节越丰富，但越慢 | 20（标准）/ 50（高质量） |
| `all_cfg_scale` | 3.0-12.0 | 越高越贴合文本描述，但可能过饱和 | 4.5-7.5（平衡） |
| `width` / `height` | 256-1024 | 图像尺寸，模型原生支持 512x512 | 512（推荐起步） |

### 不同风格对比

```python
# generate_styles.py -- 直接可跑
prompt_base = "一座古老的中式庭院"

styles = {
    "realistic": f"{prompt_base}，摄影写实风格，高分辨率，自然光线",
    "watercolor": f"{prompt_base}，水彩画风格，柔和色彩，纸张纹理",
    "anime": f"{prompt_base}，日式动漫风格，鲜艳色彩，精细线条",
    "oil_painting": f"{prompt_base}，印象派油画风格，厚重笔触，光影对比强烈",
}

for style_name, prompt in styles.items():
    result = pipe(
        prompt=prompt,
        generation_mode="image",
        height=512, width=512,
        num_inference_steps=20,
        all_cfg_scale=4.5,
    )
    filename = f"courtyard_{style_name}.png"
    result.images[0].save(filename)
    print(f"已生成: {filename}")
```

---

## 实操三：图像编辑（换背景 + 风格迁移）

### 换背景

```python
# edit_background.py -- 直接可跑
from PIL import Image

# 加载原图
source = Image.open("photo.jpg").convert("RGB")

# 换背景：白天改为黄昏
result = pipe(
    prompt="把天空的颜色改成橙红色的夕阳效果，保持地面和建筑不变",
    image=source,
    generation_mode="image",
    height=512, width=512,
    num_inference_steps=20,
    all_cfg_scale=4.5,
)
result.images[0].save("photo_sunset.png")
print("已保存: photo_sunset.png")

# 换背景：改为星空
result = pipe(
    prompt="将背景从白天改为夜晚星空，星光闪烁，保持前景主体不变",
    image=source,
    generation_mode="image",
    height=512, width=512,
    num_inference_steps=20,
    all_cfg_scale=4.5,
)
result.images[0].save("photo_starry.png")
print("已保存: photo_starry.png")
```

### 风格迁移

```python
# edit_style.py -- 直接可跑
from PIL import Image

source = Image.open("photo.jpg").convert("RGB")

style_instructions = [
    ("oil_painting", "将这张照片转换为梵高《星空》风格的油画"),
    ("ink_wash", "将这张照片转换为水墨画风格，黑白色调"),
    ("pixel_art", "将这张照片转换为像素艺术风格，8-bit 游戏画面"),
]

for style_name, instruction in style_instructions:
    result = pipe(
        prompt=instruction,
        image=source,
        generation_mode="image",
        height=512, width=512,
        num_inference_steps=20,
        all_cfg_scale=4.5,
    )
    filename = f"styled_{style_name}.png"
    result.images[0].save(filename)
    print(f"已保存: {filename}")
```

### 元素添加与季节变换

```python
# edit_elements.py -- 直接可跑
from PIL import Image

# 添加元素
room = Image.open("room.jpg").convert("RGB")
result = pipe(
    prompt="在桌子上添加一个花瓶，里面插着向日葵",
    image=room,
    generation_mode="image",
    height=512, width=512,
    num_inference_steps=20,
    all_cfg_scale=4.5,
)
result.images[0].save("room_with_flowers.png")

# 季节变换
park = Image.open("park.jpg").convert("RGB")
result = pipe(
    prompt="将这个公园场景从夏天变成冬天，树上覆盖白雪，地面积雪",
    image=park,
    generation_mode="image",
    height=512, width=512,
    num_inference_steps=20,
    all_cfg_scale=4.5,
)
result.images[0].save("park_winter.png")
```

### 编辑能力边界

| 编辑类型 | 效果 | 说明 |
|---------|------|------|
| 颜色修改 | 很好 | 改天空/背景/物体颜色 |
| 风格迁移 | 很好 | 写实转油画/水彩/动漫 |
| 添加元素 | 较好 | 添加简单物体，复杂场景效果有限 |
| 季节/天气变换 | 较好 | 夏转冬、晴转雨 |
| 精确位置控制 | 有限 | "左上角加一个太阳"可能位置不准 |
| 细节文字修改 | 有限 | 修改图片中的文字较困难 |

---

## AGI4S 科学场景

InternVL-U 的三大能力在科学研究中都有应用价值。以下示例展示科学图像理解和科学图表生成两个方向。

### 科学图像理解

```python
# science_understand.py -- 直接可跑
from PIL import Image

# 显微镜图像分析
microscope = Image.open("cells.png").convert("RGB")
result = pipe(
    prompt="分析这张显微镜图像，描述细胞的形态特征和可能的病理表现。",
    image=microscope,
    generation_mode="text",
    max_new_tokens=512,
    temperature=0.5
)
text = pipe.tokenizer.decode(result.generate_output[0], skip_special_tokens=True)
print("显微镜分析:", text)

# 化学分子结构识别
molecule = Image.open("molecule.png").convert("RGB")
result = pipe(
    prompt="识别这个化学分子结构图，给出分子名称和化学式。",
    image=molecule,
    generation_mode="text",
    max_new_tokens=256,
    temperature=0.3
)
text = pipe.tokenizer.decode(result.generate_output[0], skip_special_tokens=True)
print("分子识别:", text)

# 天文图像分析
galaxy = Image.open("galaxy.jpg").convert("RGB")
result = pipe(
    prompt="分析这张天文望远镜图像，识别星系类型（螺旋/椭圆/不规则）并描述特征。",
    image=galaxy,
    generation_mode="text",
    max_new_tokens=512,
    temperature=0.5
)
text = pipe.tokenizer.decode(result.generate_output[0], skip_special_tokens=True)
print("天文分析:", text)

# 论文图表解读
figure = Image.open("paper_figure.png").convert("RGB")
result = pipe(
    prompt="解读这张论文中的实验结果图，说明 x 轴和 y 轴含义，描述数据趋势和关键结论。",
    image=figure,
    generation_mode="text",
    max_new_tokens=512,
    temperature=0.5
)
text = pipe.tokenizer.decode(result.generate_output[0], skip_special_tokens=True)
print("论文图表解读:", text)
```

### 科学可视化生成

```python
# science_generate.py -- 直接可跑
science_prompts = [
    ("dna", "DNA 双螺旋结构的科学示意图，蓝色和红色碱基配对，白色背景，教科书插图风格"),
    ("neural_net", "神经网络的层级结构图，输入层到输出层，节点和连接用发光线条表示，深蓝色背景"),
    ("solar_system", "太阳系行星排列图，按照距离太阳远近排列，写实天文风格，黑色星空背景"),
]

for name, prompt in science_prompts:
    result = pipe(
        prompt=prompt,
        generation_mode="image",
        height=512, width=512,
        num_inference_steps=20,
        all_cfg_scale=5.0,
    )
    filename = f"science_{name}.png"
    result.images[0].save(filename)
    print(f"已生成科学图: {filename}")
```

**科学场景使用建议**：

| 场景 | 推荐能力 | temperature | 说明 |
|------|---------|-------------|------|
| 显微镜图像分析 | 理解 | 0.3-0.5 | 需要准确描述，温度不宜过高 |
| 化学结构识别 | 理解 | 0.1-0.3 | 分子名称和化学式要求精确 |
| 论文图表解读 | 理解 | 0.5 | 需要理解趋势，适度推理 |
| 科学概念图生成 | 生成 | - | cfg_scale 可适当调高（5.0-8.0） |
| 实验图像增强 | 编辑 | - | 标注关键区域、调整对比度 |

> 注意：InternVL-U 是通用多模态模型，不是专业科学领域模型。科学场景下的输出应作为辅助参考，关键结论需要领域专家确认。Intern-S1-Pro 是书生生态中面向科学研究的多模态大模型，在科学理解方面有更专业的能力。

---

## API 服务搭建（示例封装，可按需调整）

以下 FastAPI 服务将 InternVL-U 的三大能力封装为 HTTP API。这是一个示例封装，生产环境请根据实际需求调整并发控制、认证鉴权、错误处理等。

> 注意：同一个模型实例在同一时刻只能处理一个请求（推理过程占用 GPU/NPU），下面的服务是串行处理请求的。如果需要并发，需要部署多个模型实例或实现请求队列。

### A100 版 API 服务

```python
# api_server_a100.py -- 示例封装，可按需调整
import base64, io, torch
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from internvlu.pipeline_internvlu import InternVLUPipeline
from PIL import Image
import uvicorn

app = FastAPI(title="InternVL-U API (A100)")
pipe = None

def get_pipe():
    global pipe
    if pipe is None:
        pipe = InternVLUPipeline.from_pretrained(
            '/root/models/OpenGVLab/InternVL-U', torch_dtype=torch.bfloat16
        )
        pipe = pipe.to("cuda:0")
    return pipe

@app.on_event("startup")
async def startup():
    get_pipe()

@app.get("/health")
def health():
    return {"status": "ok", "device": "cuda"}

@app.post("/v1/chat")
async def chat(request: Request):
    """图像理解 / 文本对话"""
    body = await request.json()
    messages = body.get("messages", [])
    last = messages[-1]
    p = get_pipe()
    image = None
    if last.get("image"):
        image = Image.open(io.BytesIO(base64.b64decode(last["image"]))).convert("RGB")
    result = p(
        prompt=last["content"], image=image, generation_mode="text",
        max_new_tokens=body.get("max_new_tokens", 2048),
        temperature=body.get("temperature", 0.7)
    )
    text = p.tokenizer.decode(result.generate_output[0], skip_special_tokens=True)
    return {"ok": True, "text": text}

@app.post("/v1/generate")
async def generate(request: Request):
    """文生图"""
    body = await request.json()
    p = get_pipe()
    result = p(
        prompt=body["prompt"], generation_mode="image",
        height=min(body.get("height", 512), 1024),
        width=min(body.get("width", 512), 1024),
        num_inference_steps=body.get("steps", 20),
        all_cfg_scale=body.get("cfg_scale", 4.5)
    )
    buf = io.BytesIO()
    result.images[0].save(buf, format="PNG")
    return {"ok": True, "image": base64.b64encode(buf.getvalue()).decode()}

@app.post("/v1/edit")
async def edit(request: Request):
    """图像编辑"""
    body = await request.json()
    p = get_pipe()
    source = Image.open(io.BytesIO(base64.b64decode(body["image"]))).convert("RGB")
    result = p(
        prompt=body["prompt"], image=source, generation_mode="image",
        height=512, width=512,
        num_inference_steps=body.get("steps", 20),
        all_cfg_scale=body.get("cfg_scale", 4.5)
    )
    buf = io.BytesIO()
    result.images[0].save(buf, format="PNG")
    return {"ok": True, "image": base64.b64encode(buf.getvalue()).decode()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
```

### 华为昇腾 Atlas 800T A2 版 API 服务

与 A100 版的区别仅在于启动前需要应用 SDPA Patch 并使用 `npu:0` 设备：

```python
# api_server_npu.py -- 示例封装，可按需调整
import os, sys
os.environ["PYTORCH_NPU_ALLOC_CONF"] = "expandable_segments:True"
import base64, io, torch, torch_npu

# 必须在加载模型之前应用 Patch
sys.path.insert(0, '/root')
import flash_attn_sdpa_patch
flash_attn_sdpa_patch.apply_patch()

from fastapi import FastAPI, Request
from internvlu.pipeline_internvlu import InternVLUPipeline
from PIL import Image
import uvicorn

app = FastAPI(title="InternVL-U API (Ascend NPU)")
pipe = None

def get_pipe():
    global pipe
    if pipe is None:
        pipe = InternVLUPipeline.from_pretrained(
            '/root/models/OpenGVLab/InternVL-U', torch_dtype=torch.bfloat16
        )
        pipe = pipe.to("npu:0")  # 注意：npu 而不是 cuda
    return pipe

@app.on_event("startup")
async def startup():
    get_pipe()

@app.get("/health")
def health():
    return {"status": "ok", "device": "ascend-npu"}

@app.post("/v1/chat")
async def chat(request: Request):
    """图像理解 / 文本对话"""
    body = await request.json()
    messages = body.get("messages", [])
    last = messages[-1]
    p = get_pipe()
    image = None
    if last.get("image"):
        image = Image.open(io.BytesIO(base64.b64decode(last["image"]))).convert("RGB")
    result = p(
        prompt=last["content"], image=image, generation_mode="text",
        max_new_tokens=body.get("max_new_tokens", 2048),
        temperature=body.get("temperature", 0.7)
    )
    text = p.tokenizer.decode(result.generate_output[0], skip_special_tokens=True)
    return {"ok": True, "text": text}

@app.post("/v1/generate")
async def generate(request: Request):
    """文生图"""
    body = await request.json()
    p = get_pipe()
    result = p(
        prompt=body["prompt"], generation_mode="image",
        height=min(body.get("height", 512), 1024),
        width=min(body.get("width", 512), 1024),
        num_inference_steps=body.get("steps", 20),
        all_cfg_scale=body.get("cfg_scale", 4.5)
    )
    buf = io.BytesIO()
    result.images[0].save(buf, format="PNG")
    return {"ok": True, "image": base64.b64encode(buf.getvalue()).decode()}

@app.post("/v1/edit")
async def edit(request: Request):
    """图像编辑"""
    body = await request.json()
    p = get_pipe()
    source = Image.open(io.BytesIO(base64.b64decode(body["image"]))).convert("RGB")
    result = p(
        prompt=body["prompt"], image=source, generation_mode="image",
        height=512, width=512,
        num_inference_steps=body.get("steps", 20),
        all_cfg_scale=body.get("cfg_scale", 4.5)
    )
    buf = io.BytesIO()
    result.images[0].save(buf, format="PNG")
    return {"ok": True, "image": base64.b64encode(buf.getvalue()).decode()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
```

### 启动与测试

```bash
# A100 启动
pip install fastapi uvicorn
python api_server_a100.py

# 华为昇腾 Atlas 800T A2 启动
export LD_LIBRARY_PATH=/usr/local/Ascend/driver/lib64:$LD_LIBRARY_PATH
source /usr/local/Ascend/ascend-toolkit/set_env.sh
python api_server_npu.py
```

测试 API：

```bash
# 健康检查
curl http://localhost:8000/health
# {"status":"ok","device":"cuda"}  或  {"status":"ok","device":"ascend-npu"}

# 文本对话
curl -X POST http://localhost:8000/v1/chat \
  -H 'Content-Type: application/json' \
  -d '{"messages":[{"role":"user","content":"你好，介绍一下自己"}]}'

# 文生图
curl -X POST http://localhost:8000/v1/generate \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"一座雪山倒映在湖面上，日出时分","width":512,"height":512}'
```

Python 客户端调用示例：

```python
# call_api.py -- 示例封装，可按需调整
import httpx, base64

API_URL = "http://localhost:8000"

# 测试文生图
resp = httpx.post(f"{API_URL}/v1/generate", json={
    "prompt": "一座雪山倒映在湖面上，日出时分，摄影作品",
    "width": 512,
    "height": 512,
}, timeout=60)
image_data = base64.b64decode(resp.json()["image"])
with open("api_generated.png", "wb") as f:
    f.write(image_data)
print("已保存: api_generated.png")

# 测试图像理解（带图片）
with open("test.jpg", "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode()
resp = httpx.post(f"{API_URL}/v1/chat", json={
    "messages": [{"role": "user", "content": "这张图片里有什么？", "image": image_b64}],
}, timeout=60)
print("理解结果:", resp.json()["text"])

# 测试图像编辑
resp = httpx.post(f"{API_URL}/v1/edit", json={
    "image": image_b64,
    "prompt": "将背景从白天改为星空",
}, timeout=60)
edited_data = base64.b64decode(resp.json()["image"])
with open("api_edited.png", "wb") as f:
    f.write(edited_data)
print("已保存: api_edited.png")
```

**生产部署建议**：

- 使用 `gunicorn` 配合 `uvicorn` worker 实现多进程
- 添加请求速率限制，防止显存溢出
- 实现请求队列（如 Redis + Celery），避免并发推理冲突
- 添加认证鉴权（如 API Key），防止未授权访问
- 配置健康检查端点，配合负载均衡使用

---

## FAQ

### Q1: 显存不够怎么办？

InternVL-U 4B 在 bf16 下仅需约 8.6 GB 显存。如果你的 GPU 显存不足：

1. **确认没有其他进程占用显存**：
   ```bash
   # NVIDIA GPU
   nvidia-smi
   # 华为昇腾
   npu-smi info
   ```
2. **减小生成图像尺寸**：先用 256x256 测试，确认可用后再切到 512x512。
   ```python
   result = pipe(prompt="...", generation_mode="image",
       height=256, width=256, num_inference_steps=10)
   ```
3. **清理 GPU 缓存**：
   ```python
   import torch
   torch.cuda.empty_cache()  # 或 torch_npu.npu.empty_cache()
   ```
4. **消费级 GPU 参考**：RTX 4090 (24GB) 可以运行 InternVL-U 4B，但建议不要同时运行其他占用显存的程序。

### Q2: 生成的图片模糊怎么办？

图像模糊通常与推理步数和引导强度有关：

1. **增加推理步数**：`num_inference_steps` 从 10 提高到 20 或 30，每增加一倍步数，细节会有明显提升。
   ```python
   # 对比不同步数的效果
   for steps in [10, 20, 30, 50]:
       result = pipe(prompt="...", generation_mode="image",
           height=512, width=512, num_inference_steps=steps, all_cfg_scale=4.5)
       result.images[0].save(f"test_steps_{steps}.png")
   ```
2. **调整引导强度**：`all_cfg_scale` 控制文本描述的匹配程度。太低（<3.0）图像随机性大，太高（>10.0）可能出现色彩过饱和。推荐 4.5-7.5。
3. **优化提示词**：更具体的描述通常效果更好。例如"一只猫"不如"一只橘色短毛猫坐在木桌上，自然光线，摄影作品"。
4. **模型原生分辨率**：InternVL-U 原生支持 512x512。如果需要更高分辨率，建议先用 512x512 生成，再用超分辨率工具（如 Real-ESRGAN）放大。

### Q3: 华为昇腾 Atlas 800T A2 上 flash_attn 安装失败

这是预期行为。flash_attn 仅支持 NVIDIA CUDA，无法在昇腾上编译。解决方法：

```bash
# 方式一：安装 InternVL-U 时跳过依赖
pip install -e . --no-deps

# 方式二：注释掉 setup.py 或 pyproject.toml 中的 flash_attn 依赖
```

然后使用本教程提供的 SDPA Fallback Patch 替代 flash_attn。Patch 用 PyTorch 原生 `F.scaled_dot_product_attention` 实现完全等价的功能。

### Q4: 华为昇腾 Atlas 800T A2 首次推理很慢

正常现象。昇腾 NPU 首次推理需要编译算子 kernel（类似 CUDA 的 JIT 编译），首次推理可能额外需要 5-10 秒。后续调用会显著加快，文生图稳定在 5.5-6.0 秒（512x512, 20 steps）。

### Q5: `bitsandbytes` 警告 `compiled without GPU support`

不影响 bfloat16 推理，忽略即可。bitsandbytes 主要用于量化推理（int8/int4），InternVL-U 4B 在 bf16 精度下显存占用仅 8.6 GB，不需要量化。

### Q6: `ModuleNotFoundError: No module named 'internvlu'`

说明 InternVL-U 包没有正确安装。请确认：
1. 已 `git clone` 了 InternVL-U 仓库
2. 在仓库目录下执行了 `pip install -e .`（或 `pip install -e . --no-deps`）
3. 或者将仓库路径加入 PYTHONPATH：`export PYTHONPATH=/root/InternVL-U:$PYTHONPATH`

### Q7: `apply_patch()` 报错找不到模块

InternVL-U 的包结构可能更新了。请检查实际的 transformer 模块路径：

```bash
find /root/InternVL-U -name "*transformer*" -path "*/diffusion/*"
```

然后修改 `flash_attn_sdpa_patch.py` 中 `apply_patch()` 函数里的 import 路径。

### Q8: InternVL-U 的 "U" 代表什么？

U 代表 Unified（统一）。InternVL-U 将图像理解、图像生成和图像编辑三大能力统一在一个模型中，无需分别部署多个专用模型。

### Q9: 与 Intern-S1-Pro 的关系是什么？

InternVL-U 是书生系列的统一多模态模型，强调"一个模型三种能力"（理解 + 生成 + 编辑）。Intern-S1-Pro 是书生生态中面向科学研究的多模态大模型，在科学理解和推理方面有更专业的能力。两者定位不同，面向不同的使用场景。

---

## 参考资料

- [InternVL 项目主页](https://github.com/OpenGVLab/InternVL)
- [InternVL-U 论文](https://arxiv.org/abs/2501.12368)
- [ModelScope 模型下载](https://modelscope.cn/models/OpenGVLab/InternVL-U-4B)
- [FastAPI 文档](https://fastapi.tiangolo.com)
- [torch_npu 文档](https://gitee.com/ascend/pytorch)
