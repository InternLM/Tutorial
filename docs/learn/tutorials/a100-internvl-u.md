

> 本文档 AI + 社区共建中
# 在 A100 GPU 上部署 InternVL-U

本教程基于 InternStudio 开发机实战，手把手带你在 NVIDIA A100 GPU 上完成 InternVL-U 4B 模型的全能力部署，包括文本对话、文生图、图片编辑三大功能。

## 前置条件

| 项目 | 要求 |
|------|------|
| 硬件 | NVIDIA A100（80 GB），推荐 InternStudio GPU 开发机 |
| 驱动 | CUDA 12.x + cuDNN 8.x |
| Python | 3.10+ |
| 磁盘 | >= 20 GB（模型 ~8.2 GB + 依赖） |

## Step 1：环境准备

### 1.1 验证 GPU 可用

```bash
nvidia-smi
# 确认看到 A100 设备

python3 -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
# 期望输出: True NVIDIA A100-SXM4-80GB
```

### 1.2 安装依赖

```bash
pip install fastapi uvicorn pillow modelscope transformers accelerate flash-attn
```

> **flash-attn** 是 InternVL-U 图像生成的加速组件，A100 上可直接安装。如果安装失败，可参考 [昇腾 NPU 部署教程](/zh/docs/learn/ascend-internvl-u) 中的 SDPA Fallback Patch 方案作为替代。

## Step 2：下载模型

HuggingFace 在国内网络不可用，使用 ModelScope 镜像下载：

```bash
python3 -c "
from modelscope import snapshot_download
snapshot_download('OpenGVLab/InternVL-U', local_dir='/root/models/OpenGVLab/InternVL-U')
"
```

模型约 8.2 GB，下载完成后目录结构：

```
/root/models/OpenGVLab/InternVL-U/
├── config.json
├── model-*.safetensors
├── tokenizer.json
└── ...
```

> 如果可以访问 HuggingFace，也可以使用：
> ```bash
> pip install huggingface_hub
> huggingface-cli download OpenGVLab/InternVL-U --local-dir /root/models/OpenGVLab/InternVL-U
> ```

## Step 3：验证模型加载

```python
import torch
from internvlu.pipeline_internvlu import InternVLUPipeline

pipe = InternVLUPipeline.from_pretrained(
    '/root/models/OpenGVLab/InternVL-U',
    torch_dtype=torch.bfloat16
)
pipe = pipe.to("cuda:0")

print(f"GPU 显存占用: {torch.cuda.memory_allocated(0)/1e9:.1f} GB")
# 期望输出: GPU 显存占用: 8.6 GB
```

> 注意：需要将 InternVL-U 的 `internvlu` 包放在 Python Path 中。如果你用 `git clone` 下载了完整仓库，可以 `cd InternVL-U-2` 或者 `sys.path.insert(0, '/root/InternVL-U-2')`。

## Step 4：测试三大能力

### 4.1 文本对话

```python
result = pipe(prompt="你好，用一句话介绍你自己", generation_mode="text")
text = pipe.tokenizer.decode(result.generate_output[0], skip_special_tokens=True)
print(text)
# 输出: 你好，我是书生·浦语，来自上海人工智能实验室...
```

> **注意**：pipeline 返回的是 token IDs tensor，需要用 `pipe.tokenizer.decode()` 解码为文本。

### 4.2 文生图

```python
from PIL import Image

result = pipe(
    prompt="一只穿着宇航服的猫咪在太空中漫步，背景是星云",
    generation_mode="image",
    height=512, width=512,
    num_inference_steps=30,
    all_cfg_scale=4.5
)
result.images[0].save("cat_space.png")
# 512x512 生成约 3.5 秒
```

### 4.3 图片编辑

```python
source = Image.open("input.png").convert("RGB")

result = pipe(
    prompt="把背景换成海滩",
    image=source,
    generation_mode="image",
    height=512, width=512,
    num_inference_steps=30,
    all_cfg_scale=4.5
)
result.images[0].save("edited.png")
```

## Step 5：搭建 FastAPI 服务

创建 `/root/api_server.py`，将模型封装为 REST API：

```python
#!/usr/bin/env python3
"""InternVL-U FastAPI server for A100 GPU."""
import os, sys, time, base64, io, traceback
import torch

from internvlu.pipeline_internvlu import InternVLUPipeline
from PIL import Image
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(title="InternVL-U API")
pipe = None
API_KEY = os.environ.get("API_KEY", "")

def get_pipe():
    global pipe
    if pipe is None:
        print("[INIT] Loading InternVL-U pipeline on GPU...")
        t0 = time.time()
        pipe = InternVLUPipeline.from_pretrained(
            '/root/models/OpenGVLab/InternVL-U', torch_dtype=torch.bfloat16
        )
        pipe = pipe.to("cuda:0")
        print(f"[INIT] Pipeline ready in {time.time()-t0:.1f}s, "
              f"GPU mem: {torch.cuda.memory_allocated(0)/1e9:.1f} GB")
    return pipe

@app.on_event("startup")
async def startup():
    get_pipe()

@app.middleware("http")
async def check_api_key(request: Request, call_next):
    if API_KEY and request.url.path != "/health":
        key = request.headers.get("X-API-Key", "")
        if key != API_KEY:
            return JSONResponse({"error": "Unauthorized"}, status_code=401)
    return await call_next(request)

@app.get("/health")
def health():
    return {"status": "ok", "device": "a100-gpu", "model": "InternVL-U-4B"}

@app.post("/v1/chat")
async def chat(request: Request):
    body = await request.json()
    messages = body.get("messages", [])
    if not messages:
        return JSONResponse({"error": "No messages"}, status_code=400)

    p = get_pipe()
    last = messages[-1]
    prompt = last.get("content", "")
    image = None
    if last.get("image"):
        image = Image.open(io.BytesIO(base64.b64decode(last["image"]))).convert("RGB")

    t0 = time.time()
    try:
        result = p(
            prompt=prompt, image=image, generation_mode="text",
            max_new_tokens=body.get("max_new_tokens", 2048),
            temperature=body.get("temperature", 0.7)
        )
        if hasattr(result, 'generate_output') and result.generate_output is not None:
            text = p.tokenizer.decode(result.generate_output[0], skip_special_tokens=True)
        elif isinstance(result, str):
            text = result
        else:
            text = str(result)
        print(f"[CHAT] {time.time()-t0:.1f}s, prompt={prompt[:50]}")
        return {"ok": True, "text": text}
    except Exception as e:
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/v1/generate")
async def generate(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "")
    if not prompt:
        return JSONResponse({"error": "No prompt"}, status_code=400)

    p = get_pipe()
    width = min(body.get("width", 512), 1024)
    height = min(body.get("height", 512), 1024)

    t0 = time.time()
    try:
        result = p(
            prompt=prompt, generation_mode="image",
            height=height, width=width,
            num_inference_steps=30, all_cfg_scale=4.5
        )
        if hasattr(result, 'images') and result.images:
            buf = io.BytesIO()
            result.images[0].save(buf, format="PNG")
            img_b64 = base64.b64encode(buf.getvalue()).decode()
            print(f"[GEN] {time.time()-t0:.1f}s, {width}x{height}, prompt={prompt[:50]}")
            return {"ok": True, "image": img_b64}
        return JSONResponse({"error": "No image generated"}, status_code=500)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/v1/edit")
async def edit(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "")
    image_b64 = body.get("image", "")
    if not prompt or not image_b64:
        return JSONResponse({"error": "prompt and image required"}, status_code=400)

    p = get_pipe()
    source = Image.open(io.BytesIO(base64.b64decode(image_b64))).convert("RGB")

    t0 = time.time()
    try:
        result = p(
            prompt=prompt, image=source, generation_mode="image",
            height=512, width=512,
            num_inference_steps=30, all_cfg_scale=4.5
        )
        if hasattr(result, 'images') and result.images:
            buf = io.BytesIO()
            result.images[0].save(buf, format="PNG")
            img_b64_out = base64.b64encode(buf.getvalue()).decode()
            print(f"[EDIT] {time.time()-t0:.1f}s, prompt={prompt[:50]}")
            return {"ok": True, "image": img_b64_out}
        return JSONResponse({"error": "No image generated"}, status_code=500)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
```

启动服务：

```bash
nohup python3 /root/api_server.py > /root/api_server.log 2>&1 &
```

验证：

```bash
curl http://localhost:8000/health
# {"status":"ok","device":"a100-gpu","model":"InternVL-U-4B"}

curl -X POST http://localhost:8000/v1/chat \
  -H 'Content-Type: application/json' \
  -d '{"messages":[{"role":"user","content":"hello"}]}'
# {"ok":true,"text":"Hello! How can I assist you today?..."}
```

## Step 6：配置公网访问（可选）

InternStudio 开发机没有公网 IP，需要通过 SSH 隧道暴露服务。

假设你有一台公网服务器 `YOUR_SERVER_IP`：

```bash
# 在公网服务器上执行，将 8100 端口转发到 A100 的 8000 端口
sshpass -p '<A100_PASSWORD>' \
  ssh -N -L 0.0.0.0:8100:localhost:8000 \
  -p <A100_SSH_PORT> root@<A100_SSH_HOST> \
  -o StrictHostKeyChecking=no \
  -o ServerAliveInterval=30 \
  -o ServerAliveCountMax=3 \
  -o ExitOnForwardFailure=yes
```

验证公网可达：

```bash
curl http://YOUR_SERVER_IP:8100/health
# {"status":"ok","device":"a100-gpu","model":"InternVL-U-4B"}
```

> 建议用 `nohup` 或 `tmux` 保持隧道常驻。

## 性能参考

以下数据基于 A100 80GB 实测：

| 能力 | 参数 | 耗时 | 备注 |
|------|------|------|------|
| 文本对话 | 短文本 ~64 tokens | ~1.6 秒 | FlashAttention2 加速 |
| 文生图 | 512x512, 30 steps | ~3.5 秒 | 热启动后稳定 |
| 图片编辑 | 512x512, 30 steps | ~3.5 秒 | 与生图速度一致 |
| 图像理解 | 1024x1024 输入 | ~3 秒 | 包含图片编码 |

### 与昇腾 NPU 对比

| 指标 | A100 (CUDA) | 昇腾 NPU (SDPA) |
|------|-------------|-----------------|
| 文生图 512x512 | ~3.5 秒 | ~5.5 秒 |
| 文本对话 | ~1.6 秒 | ~3-5 秒 |
| 显存占用 | 8.6 GB | 8.6 GB |
| Attention 实现 | FlashAttention2 原生 | SDPA Fallback |

> A100 使用原生 FlashAttention2，性能更优。昇腾 NPU 部署教程请参考 [在昇腾 NPU 上部署 InternVL-U](/zh/docs/learn/ascend-internvl-u)。

## 常见问题

### Q: flash-attn 安装失败

flash-attn 需要 CUDA 编译，安装时间较长（约 10 分钟）。如果失败：

```bash
# 确保 CUDA toolkit 已安装
nvcc --version

# 指定 CUDA 架构编译
TORCH_CUDA_ARCH_LIST="8.0" pip install flash-attn --no-build-isolation
```

如果仍然失败，可以使用 SDPA Fallback Patch 方案，参考 [昇腾 NPU 教程](/zh/docs/learn/ascend-internvl-u) 中的 Step 3。

### Q: CUDA Out of Memory

InternVL-U 4B 仅需 8.6 GB 显存，A100 80GB 有充足余量。如果出现 OOM：

- 检查是否有其他进程占用 GPU：`nvidia-smi`
- 确保使用 `bfloat16`：`torch_dtype=torch.bfloat16`

### Q: 生成图片质量不好

- 增加推理步数：`num_inference_steps=50`（更慢但更精细）
- 调整 CFG 引导强度：`all_cfg_scale=7.0`（更高 = 更忠实于 Prompt）
- 描述尽量具体：主体 + 风格 + 色调 + 构图 + 光影 + 背景

## 总结

A100 GPU 是部署 InternVL-U 的最佳选择：

1. **原生 FlashAttention2**：无需任何 Patch，开箱即用
2. **性能最优**：文生图 512x512 仅需 ~3.5 秒
3. **显存充裕**：8.6 GB / 80 GB，可同时部署多个模型
4. **生态成熟**：CUDA 驱动、PyTorch、所有依赖均原生支持
