# InternVL-U 统一多模态

## 课程简介

InternVL-U 是书生系列推出的统一多模态大模型，仅 4B 参数即可在一个模型中实现图像理解、文生图和图像编辑三大能力。它采用 InternViT + Qwen3 + MMDiT 的融合架构，打破了传统多模态模型「理解与生成分离」的范式。本课程带你完成模型部署、三大能力实战、API 服务搭建，覆盖 A100 和华为昇腾 Atlas 800T A2 双平台。

## 你将学到

- 理解 InternVL-U 的架构设计和创新点
- 在 A100 和华为昇腾 Atlas 800T A2 上部署模型
- 使用 InternVL-U 进行图像理解（描述、OCR、VQA）
- 使用 InternVL-U 进行文生图（参数控制与质量优化）
- 使用 InternVL-U 进行图像编辑（风格转换、内容修改）
- 搭建 FastAPI 服务对外提供 API

## 架构与原理

### 目标

理解 InternVL-U 的模型架构、三大核心组件及其协作方式。

### 内容

**统一多模态的意义：**

传统方案中，图像理解（如 BLIP）和图像生成（如 Stable Diffusion）是两个独立模型，无法在同一个推理过程中既理解又生成。InternVL-U 将两者统一：同一个模型，同一套参数，根据输入类型自动切换工作模式。

**三大组件：**

```
输入(文本/图像)
     |
     v
[InternViT] -- 视觉编码器，将图像转为视觉 Token
     |
     v
[Qwen3 LLM] -- 语言模型骨干，负责推理和文本生成
     |
     v
[MMDiT]     -- 多模态扩散模块，负责图像生成和编辑
     |
     v
输出(文本/图像)
```

- **InternViT**：书生系列的视觉编码器，将输入图像编码为视觉特征向量。支持动态分辨率输入，不限制图像尺寸。
- **Qwen3 LLM**：大语言模型骨干，处理文本推理、多轮对话、指令理解。当任务是图像理解时，直接输出文本结果。
- **MMDiT（Multi-Modal Diffusion Transformer）**：当任务是图像生成或编辑时，LLM 将语义理解传递给 MMDiT，由它通过扩散过程生成图像。

**工作模式切换：**

| 输入 | 输出 | 工作模式 | 使用组件 |
|------|------|----------|----------|
| 图像 + 文字问题 | 文字回答 | 图像理解 | InternViT + Qwen3 |
| 文字描述 | 图像 | 文生图 | Qwen3 + MMDiT |
| 图像 + 编辑指令 | 编辑后图像 | 图像编辑 | InternViT + Qwen3 + MMDiT |

三种模式共享同一套参数，无需切换模型。

## 环境准备与模型部署

### 目标

在 A100 或华为昇腾 Atlas 800T A2 平台上完成模型部署。

### 内容

**硬件要求：**

| 平台 | 设备 | 显存/HBM | 说明 |
|------|------|----------|------|
| NVIDIA | A100-SXM4-80GB | 80 GB | 原生 CUDA 支持 |
| 华为昇腾 | Atlas 800T A2 | 64 GB HBM | 需 torch_npu 适配 |

InternVL-U 4B 模型在 bf16 精度下约需 12-15 GB 显存，两个平台均可流畅运行。

**A100 平台部署：**

```bash
# 创建虚拟环境
conda create -n internvl-u python=3.11 -y
conda activate internvl-u

# 安装基础依赖
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
pip install transformers accelerate pillow

# 安装 InternVL-U 依赖
pip install flash-attn --no-build-isolation

# 下载模型（国内使用 ModelScope 镜像）
pip install modelscope
python -c "
from modelscope import snapshot_download
snapshot_download('OpenGVLab/InternVL-U-4B', local_dir='./InternVL-U-4B')
"
```

**华为昇腾 Atlas 800T A2 部署：**

```bash
# 确认昇腾环境
source /usr/local/Ascend/ascend-toolkit/set_env.sh
export LD_LIBRARY_PATH=/usr/local/Ascend/driver/lib64:$LD_LIBRARY_PATH

# 确认 NPU 可用
python -c "import torch; import torch_npu; print(torch.npu.is_available())"

# 安装依赖（昇腾环境不支持 flash_attn，需使用 SDPA 替代）
pip install transformers accelerate pillow

# 下载模型
python -c "
from modelscope import snapshot_download
snapshot_download('OpenGVLab/InternVL-U-4B', local_dir='./InternVL-U-4B')
"
```

昇腾平台的 flash_attn 兼容性说明：InternVL-U 的扩散路径默认依赖 flash_attn（仅支持 CUDA）。在昇腾平台上，需要使用 PyTorch 原生的 SDPA（Scaled Dot Product Attention）作为替代实现，功能完全等价，性能差异约 30-50%。

**模型加载验证：**

```python
# test_load.py
import torch
from transformers import AutoModel, AutoTokenizer

device = "cuda" if torch.cuda.is_available() else "npu"
model_path = "./InternVL-U-4B"

tokenizer = AutoTokenizer.from_pretrained(
    model_path, trust_remote_code=True
)
model = AutoModel.from_pretrained(
    model_path,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
).to(device).eval()

print(f"模型已加载到 {device}")
print(f"模型参数量: {sum(p.numel() for p in model.parameters()) / 1e9:.2f}B")
```

## 图像理解

### 目标

使用 InternVL-U 完成图像描述、OCR 文字识别和视觉问答（VQA）任务。

### 内容

**图像描述：**

```python
# image_understanding.py
import torch
from PIL import Image
from transformers import AutoModel, AutoTokenizer

device = "cuda" if torch.cuda.is_available() else "npu"
model_path = "./InternVL-U-4B"

tokenizer = AutoTokenizer.from_pretrained(
    model_path, trust_remote_code=True
)
model = AutoModel.from_pretrained(
    model_path,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
).to(device).eval()


def describe_image(image_path: str, prompt: str = "请详细描述这张图片的内容。") -> str:
    """对图像进行描述"""
    image = Image.open(image_path).convert("RGB")
    response = model.chat(
        tokenizer=tokenizer,
        pixel_values=model.extract_pixel_values(image).to(device),
        question=prompt,
        generation_config={"max_new_tokens": 512, "temperature": 0.7},
    )
    return response


# 示例调用
result = describe_image("example.jpg")
print(result)
```

**OCR 文字识别：**

```python
def ocr_image(image_path: str) -> str:
    """识别图像中的文字"""
    image = Image.open(image_path).convert("RGB")
    response = model.chat(
        tokenizer=tokenizer,
        pixel_values=model.extract_pixel_values(image).to(device),
        question="请识别并输出这张图片中的所有文字内容，保持原始排版格式。",
        generation_config={"max_new_tokens": 1024, "temperature": 0.1},
    )
    return response


# OCR 使用低温度以提高准确性
result = ocr_image("document.png")
print(result)
```

**视觉问答（VQA）：**

```python
def visual_qa(image_path: str, question: str) -> str:
    """基于图像内容回答问题"""
    image = Image.open(image_path).convert("RGB")
    response = model.chat(
        tokenizer=tokenizer,
        pixel_values=model.extract_pixel_values(image).to(device),
        question=question,
        generation_config={"max_new_tokens": 256, "temperature": 0.5},
    )
    return response


# 示例
answer = visual_qa("chart.png", "这张图表显示的趋势是什么？最高值出现在哪个月份？")
print(answer)
```

**理解能力的参数调优建议：**

| 任务 | temperature | max_new_tokens | 说明 |
|------|-------------|----------------|------|
| 详细描述 | 0.7 | 512 | 适度创造性，生成丰富描述 |
| OCR | 0.1 | 1024 | 极低温度，保证文字准确 |
| VQA | 0.5 | 256 | 平衡准确与流畅 |
| 分类/判断 | 0.1 | 64 | 精确输出，简短回答 |

## 文生图与图像编辑

### 目标

使用 InternVL-U 生成图像和编辑已有图像。

### 内容

**文生图：**

```python
# image_generation.py
import torch
from transformers import AutoModel, AutoTokenizer

device = "cuda" if torch.cuda.is_available() else "npu"
model_path = "./InternVL-U-4B"

tokenizer = AutoTokenizer.from_pretrained(
    model_path, trust_remote_code=True
)
model = AutoModel.from_pretrained(
    model_path,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
).to(device).eval()


def generate_image(
    prompt: str,
    width: int = 512,
    height: int = 512,
    num_inference_steps: int = 50,
    guidance_scale: float = 7.5,
    seed: int = 42,
) -> "Image":
    """根据文本描述生成图像"""
    torch.manual_seed(seed)
    image = model.generate_image(
        tokenizer=tokenizer,
        prompt=prompt,
        width=width,
        height=height,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
    )
    return image


# 生成示例
image = generate_image(
    prompt="一只橘猫坐在窗台上，窗外是雨天的城市天际线，水彩画风格",
    width=512,
    height=512,
    num_inference_steps=50,
    guidance_scale=7.5,
    seed=42,
)
image.save("generated_cat.png")
print("图像已保存: generated_cat.png")
```

**文生图参数说明：**

| 参数 | 范围 | 说明 |
|------|------|------|
| width / height | 256-1024 | 图像尺寸，建议 512x512 起步 |
| num_inference_steps | 20-100 | 扩散步数，越多质量越好但越慢 |
| guidance_scale | 1.0-20.0 | 引导强度，7.5 为默认平衡值 |
| seed | 任意整数 | 随机种子，固定种子可复现结果 |

**图像编辑：**

```python
# image_editing.py
from PIL import Image


def edit_image(
    image_path: str,
    instruction: str,
    num_inference_steps: int = 50,
    guidance_scale: float = 7.5,
) -> "Image":
    """根据指令编辑图像"""
    source_image = Image.open(image_path).convert("RGB")
    edited = model.edit_image(
        tokenizer=tokenizer,
        image=source_image,
        instruction=instruction,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
    )
    return edited


# 风格转换
result = edit_image(
    "photo.jpg",
    instruction="将这张照片转换为油画风格，保持构图不变",
)
result.save("photo_oil_painting.png")

# 内容修改
result = edit_image(
    "landscape.jpg",
    instruction="将画面中的白天改为黄昏，天空变成橙红色渐变",
)
result.save("landscape_sunset.png")

# 元素添加
result = edit_image(
    "room.jpg",
    instruction="在桌子上添加一束鲜花",
)
result.save("room_with_flowers.png")
```

**性能参考（512x512 图像生成）：**

| 平台 | 设备 | 生成耗时 | 说明 |
|------|------|----------|------|
| NVIDIA | A100-SXM4-80GB | ~3.5 秒 | 使用 flash_attn |
| 华为昇腾 | Atlas 800T A2 | ~5.5 秒 | 使用 SDPA 替代 |

## API 服务搭建

### 目标

基于 FastAPI 封装 InternVL-U 的三大能力，对外提供 HTTP API 服务。

### 内容

```python
# api_server.py
import io
import base64
import torch
from PIL import Image
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModel, AutoTokenizer

app = FastAPI(title="InternVL-U API", version="1.0.0")

# 模型加载（启动时执行一次）
device = "cuda" if torch.cuda.is_available() else "npu"
model_path = "./InternVL-U-4B"

tokenizer = AutoTokenizer.from_pretrained(
    model_path, trust_remote_code=True
)
model = AutoModel.from_pretrained(
    model_path,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
).to(device).eval()


def image_to_base64(image: Image.Image) -> str:
    """将 PIL Image 转为 base64 字符串"""
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def base64_to_image(b64_string: str) -> Image.Image:
    """将 base64 字符串转为 PIL Image"""
    data = base64.b64decode(b64_string)
    return Image.open(io.BytesIO(data)).convert("RGB")


# ===== 请求模型 =====

class UnderstandRequest(BaseModel):
    image: str  # base64 编码的图像
    question: str
    max_tokens: int = 512
    temperature: float = 0.7


class GenerateRequest(BaseModel):
    prompt: str
    width: int = 512
    height: int = 512
    steps: int = 50
    guidance_scale: float = 7.5
    seed: int = 42


class EditRequest(BaseModel):
    image: str  # base64 编码的图像
    instruction: str
    steps: int = 50
    guidance_scale: float = 7.5


# ===== API 端点 =====

@app.get("/health")
async def health():
    return {"status": "ok", "device": device, "model": model_path}


@app.post("/understand")
async def understand(req: UnderstandRequest):
    """图像理解：输入图像和问题，返回文字回答"""
    try:
        image = base64_to_image(req.image)
        response = model.chat(
            tokenizer=tokenizer,
            pixel_values=model.extract_pixel_values(image).to(device),
            question=req.question,
            generation_config={
                "max_new_tokens": req.max_tokens,
                "temperature": req.temperature,
            },
        )
        return {"answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate")
async def generate(req: GenerateRequest):
    """文生图：输入文字描述，返回生成的图像"""
    try:
        torch.manual_seed(req.seed)
        image = model.generate_image(
            tokenizer=tokenizer,
            prompt=req.prompt,
            width=req.width,
            height=req.height,
            num_inference_steps=req.steps,
            guidance_scale=req.guidance_scale,
        )
        return {"image": image_to_base64(image)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/edit")
async def edit(req: EditRequest):
    """图像编辑：输入图像和编辑指令，返回编辑后的图像"""
    try:
        source = base64_to_image(req.image)
        edited = model.edit_image(
            tokenizer=tokenizer,
            image=source,
            instruction=req.instruction,
            num_inference_steps=req.steps,
            guidance_scale=req.guidance_scale,
        )
        return {"image": image_to_base64(edited)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**启动服务：**

```bash
pip install fastapi uvicorn
python api_server.py
```

**API 调用示例：**

```python
# call_api.py
import httpx
import base64

API_URL = "http://localhost:8000"


def test_understand():
    """测试图像理解"""
    with open("test.jpg", "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode()

    resp = httpx.post(f"{API_URL}/understand", json={
        "image": image_b64,
        "question": "这张图片里有什么？",
    })
    print("理解结果:", resp.json()["answer"])


def test_generate():
    """测试文生图"""
    resp = httpx.post(f"{API_URL}/generate", json={
        "prompt": "一座雪山倒映在湖面上，日出时分，摄影作品",
        "width": 512,
        "height": 512,
    })
    image_data = base64.b64decode(resp.json()["image"])
    with open("api_generated.png", "wb") as f:
        f.write(image_data)
    print("生成图像已保存: api_generated.png")


def test_edit():
    """测试图像编辑"""
    with open("input.jpg", "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode()

    resp = httpx.post(f"{API_URL}/edit", json={
        "image": image_b64,
        "instruction": "将背景从白天改为星空",
    })
    image_data = base64.b64decode(resp.json()["image"])
    with open("api_edited.png", "wb") as f:
        f.write(image_data)
    print("编辑图像已保存: api_edited.png")


if __name__ == "__main__":
    test_understand()
    test_generate()
    test_edit()
```

**生产部署建议：**

- 使用 `gunicorn` 配合 `uvicorn` worker 实现多进程
- 添加请求速率限制，防止显存溢出
- 实现请求队列，避免并发推理冲突
- 添加健康检查端点，配合负载均衡使用

## 参考资料

- [InternVL 项目主页](https://github.com/OpenGVLab/InternVL)
- [InternVL-U 论文](https://arxiv.org/abs/2501.12368)
- [ModelScope 模型下载](https://modelscope.cn/models/OpenGVLab/InternVL-U-4B)
- [FastAPI 文档](https://fastapi.tiangolo.com)
- [torch_npu 文档](https://gitee.com/ascend/pytorch)
