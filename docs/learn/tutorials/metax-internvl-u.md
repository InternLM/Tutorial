
# 在沐曦 C500 GPU 上部署 InternVL-U

本教程手把手带你在沐曦 MetaX C500 GPU 上完成 InternVL-U 4B 模型的全能力部署，包括文本对话、文生图、图片编辑三大功能。

得益于沐曦 MACA 框架预装的 FlashAttention2 实现，MetaX C500 无需任何额外 Patch 即可直接运行完整模型——这是相比昇腾 NPU 部署的一大优势。

## 关于沐曦 MetaX

沐曦集成电路（上海）有限公司是一家专注于高性能 GPU 芯片设计的国产半导体企业。MetaX C500 是其面向数据中心推出的 AI 推理/训练 GPU，搭配自研 MACA（MetaX Architecture for Computing Acceleration）计算框架，提供与 CUDA 高度兼容的编程接口。

**MACA 框架核心特性：**

- 提供与 CUDA 兼容的 API，代码中直接使用 `torch.cuda` 接口
- 预装主流深度学习算子库，包括 FlashAttention2、xformers 等
- 配套 `mx-smi` GPU 管理工具（类似 `nvidia-smi`）
- 支持 PyTorch、TensorFlow 等主流框架

## 获取 MetaX C500 算力

如果你还没有 MetaX C500 GPU 资源，可以通过 [Gitee AI 算力市场](https://ai.gitee.com/compute) 按需租用沐曦 C500 算力实例，支持小时级起租。

创建实例时选择镜像：**PyTorch / 2.8.0 / Python 3.12 / MACA 3.3.0.4**，该镜像已预装 MACA 框架、PyTorch 和 FlashAttention2，开箱即用。

> 联系书生社区小助手可获取算力优惠券，降低体验成本。

## 前置条件

| 项目 | 要求 |
|------|------|
| 硬件 | 沐曦 MetaX C500（64 GB VRAM，350W TDP） |
| 驱动 | MACA 3.3.0.4+（沐曦 GPU 计算框架） |
| PyTorch | 2.8.0（MACA 适配版，镜像已预装） |
| Python | 3.12（推荐使用镜像预装的 Conda 环境） |
| 操作系统 | Ubuntu 22.04 / 24.04 |
| 磁盘 | >= 30 GB（模型 ~8.2 GB + 代码 + 依赖） |
| 内存 | >= 32 GB（模型加载时需要） |

## Step 1：环境准备

### 1.1 设置 MACA 环境变量

MetaX C500 的 MACA 框架安装在 `/opt/maca`，使用前需设置环境变量：

```bash
export MACA_PATH=/opt/maca
```

> 建议将以上内容写入 `~/.bashrc`，避免每次手动执行：
>
> ```bash
> echo 'export MACA_PATH=/opt/maca' >> ~/.bashrc
> source ~/.bashrc
> ```

### 1.2 验证 GPU 状态

使用 `mx-smi`（沐曦版 `nvidia-smi`）查看 GPU 状态：

```bash
mx-smi
```

期望输出类似：

```
=================== MetaX System Management Interface Log ===================
Timestamp                                         : Wed Mar 18 06:44:43 2026

Attached GPUs                                     : 1
+---------------------------------------------------------------------------------+
| MX-SMI 2.2.9                       Kernel Mode Driver Version: 3.0.11           |
| MACA Version: 3.3.0.15             BIOS Version: 1.27.5.0                       |
|------------------+-----------------+---------------------+----------------------|
| Board       Name | GPU   Persist-M | Bus-id              | GPU-Util      sGPU-M |
| Pwr:Usage/Cap    | Temp       Perf | Memory-Usage        | GPU-Util             |
|==================+=================+=====================+======================|
| 0     MetaX C500 | 0           Off | 0000:10:00.0        | 0%          Disabled |
| 50W / 350W       | 35C          P9 | 0/65536 MiB         | Available            |
+------------------+-----------------+---------------------+----------------------+
```

确认可以看到 **MetaX C500** 设备信息，显存 65536 MiB（64 GB）。

### 1.3 验证 PyTorch 可用

MetaX C500 环境通常预装了 MACA 适配的 PyTorch。使用 Conda 环境中的 Python：

```bash
/opt/conda/bin/python3 -c "
import torch
print(f'PyTorch 版本: {torch.__version__}')
print(f'CUDA 可用: {torch.cuda.is_available()}')
print(f'GPU 设备数: {torch.cuda.device_count()}')
print(f'GPU 名称: {torch.cuda.get_device_name(0)}')
"
```

期望输出：

```
PyTorch 版本: 2.8.0+metax3.3.0.2
CUDA 可用: True
GPU 设备数: 1
GPU 名称: MetaX C500
```

> **关键点**：MACA 提供 CUDA 兼容 API，因此代码中使用 `torch.cuda` 接口即可，无需导入任何特殊库（不像昇腾需要 `torch_npu`）。这意味着几乎所有基于 CUDA 的 PyTorch 代码可以在 MetaX C500 上零修改运行。

### 1.4 检查预装的关键库

```bash
/opt/conda/bin/pip list | grep -iE "flash_attn|torch|transformers|xformers"
```

期望看到类似：

```
flash_attn         2.6.3+metax3.3.0.2torch2.8
torch              2.8.0+metax3.3.0.2
transformers       4.x.x
xformers           0.0.22+metax3.3.0.2torch2.8
```

> 注意 `flash_attn` 已预装（MACA 版本），这正是 MetaX C500 不需要 SDPA Patch 的原因。

### 1.5 创建独立 Conda 环境（推荐）

为了避免污染系统预装的 Conda 环境，建议创建一个独立的虚拟环境：

```bash
# 基于系统 Python 创建独立环境，继承 MACA 预装的 PyTorch / flash_attn
/opt/conda/bin/conda create -n internvlu --clone base -y
/opt/conda/bin/conda activate internvlu

# 后续所有 pip 命令使用该环境
which python3
# /opt/conda/envs/internvlu/bin/python3
```

> 如果 `conda create --clone` 耗时较长或磁盘空间不足，也可以直接使用系统 base 环境（`/opt/conda/bin/python3`），但需注意避免依赖冲突。

### 1.6 安装额外依赖

```bash
# 如果使用了独立环境
pip install fastapi uvicorn pillow modelscope accelerate

# 如果使用系统 base 环境
/opt/conda/bin/pip install fastapi uvicorn pillow modelscope accelerate
```

## Step 2：下载模型和代码

### 2.1 下载 InternVL-U 模型权重

HuggingFace 在国内网络不可用，使用 ModelScope 镜像下载：

```bash
/opt/conda/bin/python3 -c "
from modelscope import snapshot_download
snapshot_download('OpenGVLab/InternVL-U', local_dir='/data/models/OpenGVLab/InternVL-U')
"
```

模型约 8.2 GB，下载完成后目录结构：

```
/data/models/OpenGVLab/InternVL-U/
├── configuration.json
├── generation_decoder/        # Diffusion 解码器权重
│   ├── config.json
│   └── diffusion_pytorch_model.safetensors
├── model_index.json
├── processor/                 # 图像处理器配置
├── scheduler/                 # 扩散调度器配置
├── vae/                       # VAE 编解码器权重
│   ├── config.json
│   └── diffusion_pytorch_model.safetensors
└── vlm/                       # 视觉语言模型权重
    ├── config.json
    ├── model-00001-of-00002.safetensors
    ├── model-00002-of-00002.safetensors
    └── tokenizer.json
```

### 2.2 下载 InternVL-U 推理代码

InternVL-U 的 Pipeline 代码需要单独克隆：

```bash
cd /data
git clone https://github.com/OpenGVLab/InternVL-U.git InternVL-U-code
```

> 如果 GitHub 访问受限，可使用镜像：
>
> ```bash
> git clone https://mirror.ghproxy.com/https://github.com/OpenGVLab/InternVL-U.git InternVL-U-code
> ```

代码目录结构：

```
/data/InternVL-U-code/
├── internvlu/
│   ├── __init__.py
│   ├── pipeline_internvlu.py      # 主 Pipeline（推理入口）
│   └── diffusion/
│       └── internvlu_transformer.py  # Diffusion Transformer（使用 flash_attn）
├── requirements.txt
└── README.md
```

### 2.3 安装推理代码依赖

```bash
cd /data/InternVL-U-code
/opt/conda/bin/pip install -r requirements.txt
```

## Step 3：理解 MACA 与 FlashAttention2 的关系

在开始验证模型之前，有必要理解为什么 MetaX C500 **不需要** 昇腾教程中那样的 SDPA Fallback Patch。

### 三大平台的 FlashAttention2 支持情况

| 平台 | flash_attn 库 | 是否需要 Patch |
|------|--------------|---------------|
| NVIDIA A100 | 原生 CUDA 版本，pip 安装 | 不需要 |
| 华为昇腾 NPU | 不支持（CUDA-only），无法安装 | 需要 SDPA Patch |
| 沐曦 MetaX C500 | MACA 适配版本，环境预装 | 不需要 |

**InternVL-U 的 Diffusion 路径**（`internvlu_transformer.py`）硬编码调用了以下 `flash_attn` 函数：

- `flash_attn_func` — 标准注意力计算
- `flash_attn_varlen_func` — 变长序列注意力
- `pad_input` / `unpad_input` — 序列 padding 工具
- `is_flash_attn_2_available` — 可用性检查

在昇腾 NPU 上，这些函数全部需要用 PyTorch SDPA 手动替换。而 MetaX C500 的 MACA 框架已经提供了完整的 `flash_attn` 实现（版本 `2.6.3+metax3.3.0.2torch2.8`），所有函数调用可以直接走通。

验证 flash_attn 可用：

```bash
/opt/conda/bin/python3 -c "
import flash_attn
print(f'flash_attn 版本: {flash_attn.__version__}')
from flash_attn import flash_attn_func, flash_attn_varlen_func
print('flash_attn_func 可用: OK')
print('flash_attn_varlen_func 可用: OK')
"
```

## Step 4：验证模型加载

```python
import os, sys
os.environ["MACA_PATH"] = "/opt/maca"
sys.path.insert(0, "/data/InternVL-U-code")

import torch
from internvlu.pipeline_internvlu import InternVLUPipeline

print("正在加载 InternVL-U 模型...")
pipe = InternVLUPipeline.from_pretrained(
    '/data/models/OpenGVLab/InternVL-U',
    torch_dtype=torch.bfloat16
)
pipe = pipe.to("cuda:0")

mem_gb = torch.cuda.memory_allocated(0) / 1e9
total_gb = torch.cuda.get_device_properties(0).total_memory / 1e9
print(f"GPU 显存占用: {mem_gb:.1f} GB / {total_gb:.0f} GB")
print(f"剩余显存: {total_gb - mem_gb:.0f} GB")
print("模型加载成功!")
```

期望输出：

```
正在加载 InternVL-U 模型...
GPU 显存占用: 8.7 GB / 64 GB
剩余显存: 55 GB
模型加载成功!
```

> **启动时可能看到的警告**（均可忽略）：
>
> - `flash_attn is installed but failed to import: cannot import name '_wrapped_flash_attn_backward'` — MACA 版 flash_attn 的已知无害警告，前向推理正常
> - `FutureWarning: torch.cuda.amp.custom_fwd` — PyTorch API 迁移警告
> - `torchvision.datapoints Beta` — torchvision 内部警告

## Step 5：测试三大能力

### 5.1 文本对话

```python
result = pipe(prompt="你好，用一句话介绍你自己", generation_mode="text")
text = pipe.tokenizer.decode(result.generate_output[0], skip_special_tokens=True)
print(text)
# 输出: 你好，我是书生·浦语，来自上海人工智能实验室...
```

> **注意**：pipeline 返回的是 token IDs tensor，需要用 `pipe.tokenizer.decode()` 解码为文本。

测试多轮对话能力：

```python
# 带上下文的多轮对话
result = pipe(
    prompt="请用 Python 写一个快速排序算法",
    generation_mode="text",
    max_new_tokens=1024,
    temperature=0.7
)
text = pipe.tokenizer.decode(result.generate_output[0], skip_special_tokens=True)
print(text)
```

### 5.2 图像理解

InternVL-U 支持上传图片并进行理解分析：

```python
from PIL import Image

# 加载一张图片
img = Image.open("test_image.jpg").convert("RGB")

result = pipe(
    prompt="详细描述这张图片的内容",
    image=img,
    generation_mode="text",
    max_new_tokens=512
)
text = pipe.tokenizer.decode(result.generate_output[0], skip_special_tokens=True)
print(text)
```

### 5.3 文生图

```python
import time

t0 = time.time()
result = pipe(
    prompt="一只穿着宇航服的猫咪在太空中漫步，背景是星云和银河",
    generation_mode="image",
    height=512, width=512,
    num_inference_steps=20,
    all_cfg_scale=4.5
)
result.images[0].save("cat_space.png")
print(f"生成耗时: {time.time()-t0:.1f} 秒")
# 512x512 生成约 4~5 秒
```

尝试不同分辨率：

```python
# 高分辨率生成（更慢但更精细）
result = pipe(
    prompt="水墨画风格的山水风景，云雾缭绕",
    generation_mode="image",
    height=1024, width=1024,
    num_inference_steps=20,
    all_cfg_scale=4.5
)
result.images[0].save("landscape_1024.png")
```

> **Prompt 技巧**：描述越具体效果越好。推荐结构：主体 + 动作/姿态 + 风格 + 光影 + 背景。支持的画风包括：写实、油画、水彩、水墨、赛博朋克、像素风、扁平插画等。

### 5.4 图片编辑

```python
source = Image.open("input.png").convert("RGB")

# 局部编辑
result = pipe(
    prompt="把背景换成海滩",
    image=source,
    generation_mode="image",
    height=512, width=512,
    num_inference_steps=20,
    all_cfg_scale=4.5
)
result.images[0].save("edited_beach.png")

# 风格迁移
result = pipe(
    prompt="转为油画风格",
    image=source,
    generation_mode="image",
    height=512, width=512,
    num_inference_steps=20,
    all_cfg_scale=4.5
)
result.images[0].save("edited_oil_painting.png")
```

> **编辑类型参考**：
>
> - 局部编辑："给人物加上墨镜"、"把天空换成星空"
> - 全局风格："转为黑白照片"、"添加复古滤镜"、"变成水彩画风格"
> - 场景变换："把背景换成雪山"、"放在太空宇宙中"

## Step 6：搭建 FastAPI 服务

创建 `/data/api_server.py`，将模型封装为 REST API，供前端 Playground 或其他服务调用：

> **安全提示**：如果服务暴露在公网，**必须**通过 `API_KEY` 环境变量设置鉴权密钥，否则任何人都可以调用你的 GPU 资源。同时建议在反向代理（如 Nginx）层面配置速率限制。

```python
#!/usr/bin/env python3
"""InternVL-U FastAPI server for MetaX C500."""
import os, sys, time, base64, io, traceback, secrets
os.environ["MACA_PATH"] = "/opt/maca"
sys.path.insert(0, "/data/InternVL-U-code")

import torch
from internvlu.pipeline_internvlu import InternVLUPipeline
from PIL import Image
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(title="InternVL-U API (MetaX C500)")
pipe = None

# API Key 鉴权：如未设置，自动生成随机密钥并打印到日志
API_KEY = os.environ.get("API_KEY", "")
if not API_KEY:
    API_KEY = secrets.token_urlsafe(32)
    print(f"[WARN] API_KEY not set, auto-generated: {API_KEY}")
    print("[WARN] Set API_KEY env var for production use!")

# 输入限制常量
MAX_BASE64_SIZE = 10 * 1024 * 1024  # 10 MB base64 上限
MAX_PROMPT_LENGTH = 4096             # prompt 最大字符数
ALLOWED_IMAGE_FORMATS = {"JPEG", "PNG", "WEBP", "BMP", "GIF"}

def validate_base64_image(b64_str: str) -> Image.Image:
    """验证并解码 base64 图片，检查大小和格式。"""
    if len(b64_str) > MAX_BASE64_SIZE:
        raise ValueError(f"Image too large (max {MAX_BASE64_SIZE // 1024 // 1024} MB)")
    img = Image.open(io.BytesIO(base64.b64decode(b64_str))).convert("RGB")
    if img.format and img.format.upper() not in ALLOWED_IMAGE_FORMATS:
        raise ValueError(f"Unsupported image format: {img.format}")
    # 限制图片尺寸，防止 OOM
    if img.width > 4096 or img.height > 4096:
        raise ValueError(f"Image too large: {img.width}x{img.height} (max 4096x4096)")
    return img

def get_pipe():
    """懒加载模型，首次调用时初始化。"""
    global pipe
    if pipe is None:
        print("[INIT] Loading InternVL-U on MetaX C500...")
        t0 = time.time()
        pipe = InternVLUPipeline.from_pretrained(
            "/data/models/OpenGVLab/InternVL-U", torch_dtype=torch.bfloat16
        )
        pipe = pipe.to("cuda:0")
        mem = torch.cuda.memory_allocated(0) / 1e9
        print(f"[INIT] Ready in {time.time()-t0:.1f}s, GPU mem: {mem:.1f} GB")
    return pipe

@app.on_event("startup")
async def startup():
    """服务启动时预加载模型，避免首次请求超时。"""
    get_pipe()

@app.middleware("http")
async def check_api_key(request: Request, call_next):
    """API Key 鉴权中间件（/health 接口除外）。"""
    if request.url.path != "/health":
        key = request.headers.get("X-API-Key", "")
        if key != API_KEY:
            return JSONResponse({"error": "Unauthorized"}, status_code=401)
    return await call_next(request)

@app.get("/health")
def health():
    """健康检查接口，返回设备信息和显存使用。"""
    mem = torch.cuda.memory_allocated(0) / 1e9 if torch.cuda.is_available() else 0
    return {
        "status": "ok",
        "device": "metax-c500",
        "model": "InternVL-U-4B",
        "gpu_mem_gb": round(mem, 1)
    }

@app.post("/v1/chat")
async def chat(request: Request):
    """文本对话 + 图像理解接口。"""
    body = await request.json()
    messages = body.get("messages", [])
    if not messages:
        return JSONResponse({"error": "No messages"}, status_code=400)

    p = get_pipe()
    last = messages[-1]
    prompt = last.get("content", "")
    if len(prompt) > MAX_PROMPT_LENGTH:
        return JSONResponse({"error": f"Prompt too long (max {MAX_PROMPT_LENGTH} chars)"}, status_code=400)

    image = None
    # 支持 base64 编码的图片输入
    if last.get("image"):
        try:
            image = validate_base64_image(last["image"])
        except ValueError as e:
            return JSONResponse({"error": str(e)}, status_code=400)

    t0 = time.time()
    try:
        result = p(
            prompt=prompt, image=image, generation_mode="text",
            max_new_tokens=min(body.get("max_new_tokens", 2048), 4096),
            temperature=body.get("temperature", 0.7)
        )
        text = p.tokenizer.decode(result.generate_output[0], skip_special_tokens=True)
        return {"text": text, "latency": round(time.time()-t0, 2), "device": "metax-c500"}
    except Exception as e:
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/v1/generate")
async def generate(request: Request):
    """文生图接口。"""
    body = await request.json()
    prompt = body.get("prompt", "")
    if not prompt:
        return JSONResponse({"error": "No prompt"}, status_code=400)
    if len(prompt) > MAX_PROMPT_LENGTH:
        return JSONResponse({"error": f"Prompt too long (max {MAX_PROMPT_LENGTH} chars)"}, status_code=400)

    p = get_pipe()
    t0 = time.time()
    try:
        result = p(
            prompt=prompt, generation_mode="image",
            height=min(body.get("height", 512), 1024),
            width=min(body.get("width", 512), 1024),
            num_inference_steps=min(body.get("num_inference_steps", 20), 50),
            all_cfg_scale=body.get("all_cfg_scale", 4.5)
        )
        buf = io.BytesIO()
        result.images[0].save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        return {"image": b64, "latency": round(time.time()-t0, 2), "device": "metax-c500"}
    except Exception as e:
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/v1/edit")
async def edit(request: Request):
    """图片编辑接口。"""
    body = await request.json()
    prompt = body.get("prompt", "")
    image_b64 = body.get("image", "")
    if not prompt or not image_b64:
        return JSONResponse({"error": "Need prompt and image"}, status_code=400)
    if len(prompt) > MAX_PROMPT_LENGTH:
        return JSONResponse({"error": f"Prompt too long (max {MAX_PROMPT_LENGTH} chars)"}, status_code=400)

    try:
        source = validate_base64_image(image_b64)
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=400)

    p = get_pipe()
    t0 = time.time()
    try:
        result = p(
            prompt=prompt, image=source, generation_mode="image",
            height=min(body.get("height", 512), 1024),
            width=min(body.get("width", 512), 1024),
            num_inference_steps=min(body.get("num_inference_steps", 20), 50),
            all_cfg_scale=body.get("all_cfg_scale", 4.5)
        )
        buf = io.BytesIO()
        result.images[0].save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        return {"image": b64, "latency": round(time.time()-t0, 2), "device": "metax-c500"}
    except Exception as e:
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
```

### 启动服务

```bash
export MACA_PATH=/opt/maca
export API_KEY="your-secret-api-key"  # 设置 API 鉴权密钥
nohup /opt/conda/bin/python3 /data/api_server.py > /data/api_server.log 2>&1 &
```

查看启动日志：

```bash
tail -f /data/api_server.log
# 等待看到 "Uvicorn running on http://0.0.0.0:8000" 即启动成功
```

### 验证所有接口

**健康检查：**

```bash
curl http://localhost:8000/health
# {"status":"ok","device":"metax-c500","model":"InternVL-U-4B","gpu_mem_gb":8.7}
```

**文本对话：**

```bash
curl -X POST http://localhost:8000/v1/chat \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: your-secret-api-key' \
  -d '{"messages":[{"role":"user","content":"用一句话解释什么是大语言模型"}]}'
# {"text":"大语言模型是...","latency":1.07,"device":"metax-c500"}
```

**文生图：**

```bash
curl -X POST http://localhost:8000/v1/generate \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: your-secret-api-key' \
  -d '{"prompt":"一只可爱的柴犬坐在樱花树下","height":512,"width":512}' \
  -o response.json
# 返回 JSON 包含 base64 编码的图片
```

**图片编辑（需提供 base64 编码的源图）：**

```bash
# 将图片转为 base64
IMAGE_B64=$(base64 -w0 input.png)

curl -X POST http://localhost:8000/v1/edit \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: your-secret-api-key' \
  -d "{\"prompt\":\"把背景换成星空\",\"image\":\"$IMAGE_B64\"}" \
  -o edit_response.json
```

## Step 7：配置公网访问（可选）

如果你的 MetaX C500 服务器没有公网 IP，需要通过 SSH 隧道暴露服务。

### 方案：通过公网服务器 SSH 隧道

假设你有一台公网服务器 `YOUR_SERVER_IP`：

```bash
# 在公网服务器上执行，将 8102 端口转发到 MetaX 的 8000 端口
ssh -N -L 0.0.0.0:8102:localhost:8000 \
  -p <METAX_SSH_PORT> root@<METAX_SSH_HOST> \
  -o StrictHostKeyChecking=no \
  -o UserKnownHostsFile=/dev/null \
  -o ServerAliveInterval=30 \
  -o ServerAliveCountMax=3 \
  -o ExitOnForwardFailure=yes
```

使用 `sshpass` 实现自动重连：

```bash
# 安装 sshpass
apt install -y sshpass

# 带密码的自动重连隧道
while true; do
    echo "[$(date)] Starting SSH tunnel..."
    sshpass -p 'YOUR_PASSWORD' ssh -N \
        -L 0.0.0.0:8102:localhost:8000 \
        -p <METAX_SSH_PORT> root@<METAX_SSH_HOST> \
        -o StrictHostKeyChecking=no \
        -o UserKnownHostsFile=/dev/null \
        -o ServerAliveInterval=30 \
        -o ServerAliveCountMax=3 \
        -o ExitOnForwardFailure=yes \
        2>/dev/null
    echo "[$(date)] Tunnel disconnected, reconnecting in 5s..."
    sleep 5
done
```

> 建议将隧道脚本保存为 `.sh` 文件并用 `nohup` 后台运行。

验证公网可达：

```bash
curl http://YOUR_SERVER_IP:8102/health
# {"status":"ok","device":"metax-c500","model":"InternVL-U-4B","gpu_mem_gb":8.7}
```

### 安全组配置

如果你的公网服务器在阿里云/腾讯云等云平台上，还需要在安全组中开放 8102 端口的入站规则：

- 协议：TCP
- 端口范围：8102
- 授权对象：0.0.0.0/0（或限定 IP）

## 性能参考

以下数据基于 MetaX C500（64 GB VRAM，MACA 3.3.0）实测：

| 能力 | 参数 | 耗时 | 备注 |
|------|------|------|------|
| 文本对话 | 短文本 ~64 tokens | 1~2 秒 | 首次推理含 warmup |
| 图像理解 | 1024x1024 输入 | ~8 秒 | 包含图片编码 |
| 文生图 | 512x512, 20 steps | ~4-5 秒 | 热启动后稳定 |
| 文生图 | 1024x1024, 20 steps | ~15 秒 | 大尺寸更精细但更慢 |
| 图片编辑 | 512x512, 20 steps | ~4-5 秒 | 与生图速度一致 |
| 模型加载 | 首次启动 | ~30 秒 | 含权重加载和 GPU 初始化 |
| 显存占用 | bfloat16 | 8.7 GB | 64 GB 显存余量充足 |

### 三平台性能对比

| 指标 | A100 (CUDA) | 昇腾 NPU (SDPA) | MetaX C500 (MACA) |
|------|-------------|------------------|--------------------|
| 文生图 512x512 | ~3.5 秒 | ~5.5 秒 | ~4-5 秒 |
| 文本对话 | ~1 秒 | ~3-5 秒 | ~1-2 秒 |
| 显存占用 | 8.6 GB | 8.6 GB | 8.7 GB |
| 总显存 | 80 GB | 64 GB | 64 GB |
| Attention 实现 | FlashAttention2 原生 | SDPA Fallback | FlashAttention2 (MACA) |
| 是否需要 Patch | 否 | 是（SDPA Patch） | 否 |
| 设备接口 | `cuda:0` | `npu:0` | `cuda:0` |
| GPU 工具 | `nvidia-smi` | `npu-smi` | `mx-smi` |

> MetaX C500 的文生图性能接近 A100，文本对话速度也非常快。得益于 MACA 框架对 FlashAttention2 的原生支持，Attention 计算效率高于 SDPA Fallback 方案。

## 常见问题

### Q: 启动时出现 `_wrapped_flash_attn_backward` 相关警告

```
flash_attn is installed but failed to import: cannot import name '_wrapped_flash_attn_backward'
from 'flash_attn.flash_attn_interface'. Falling back to native PyTorch attention.
```

这是 MACA 版 `flash_attn` 的已知无害警告。尽管提示 "Falling back"，实际前向推理的 FlashAttention2 仍正常工作，不影响任何功能和性能。忽略即可。

### Q: `mx-smi` 显示 GPU 利用率很高

模型加载到 GPU 后常驻显存（约 8.7 GB / 64 GB），`mx-smi` 显示较高的 Memory-Usage 是正常现象。GPU-Util 在推理时会波动，空闲时接近 0%。

### Q: 什么是 MACA？

MACA（MetaX Architecture for Computing Acceleration）是沐曦自研的 GPU 计算框架，类似 NVIDIA 的 CUDA。它的核心特性：

- **CUDA API 兼容**：代码中 `import torch` 后直接使用 `torch.cuda`，无需修改
- **预装算子库**：包括 FlashAttention2、xformers、causal_conv1d 等主流加速库
- **开发者友好**：现有 CUDA 代码几乎可以零修改迁移

### Q: 能部署更大的模型吗？

InternVL-U 4B 仅占用 8.7 GB 显存，C500 有 64 GB VRAM，剩余 55+ GB 足够部署更大模型或多实例并发。例如可以同时加载多个 InternVL-U 实例用于负载均衡。

### Q: 与昇腾 NPU 教程相比，为什么这里不需要 SDPA Patch？

昇腾 NPU 无法安装 CUDA 原生的 `flash_attn` 库（因为 flash_attn 底层依赖 CUDA kernel），因此需要用 PyTorch 原生 `F.scaled_dot_product_attention` 手动替代全部 flash_attn 函数。

而 MetaX C500 的 MACA 框架已预装了兼容版本的 `flash_attn`（版本号 `2.6.3+metax3.3.0.2torch2.8`），其底层使用 MACA kernel 实现，对上层 Python API 完全兼容。模型可以直接调用，无需任何 Monkey Patch。

### Q: 如何监控 GPU 状态？

```bash
# 实时监控（每秒刷新）
watch -n 1 mx-smi

# 查看 GPU 进程
mx-smi  # 底部会列出占用 GPU 的进程和显存
```

### Q: 服务启动后如何查看日志？

```bash
# 查看实时日志
tail -f /data/api_server.log

# 查看最近的请求记录
grep "POST\|GET" /data/api_server.log | tail -20
```

## 总结

MetaX C500 凭借 MACA 框架的 CUDA 兼容能力，实现了 InternVL-U 的开箱即用部署。这个方案的核心优势在于：

1. **零额外适配**：MACA 预装 FlashAttention2，无需编写任何 Patch，部署流程比昇腾 NPU 更简单
2. **标准 CUDA API**：使用 `torch.cuda` 接口，代码与 NVIDIA A100 完全一致，迁移成本为零
3. **功能完整**：对话、图像理解、文生图、图片编辑四大能力全部可用
4. **性能优异**：文生图速度接近 A100（~4-5s vs ~3.5s），文本推理速度快，显著优于 SDPA Fallback 方案
5. **国产替代**：作为国产 GPU 方案，MetaX C500 展示了在 AI 推理场景下替代 NVIDIA GPU 的可行性
