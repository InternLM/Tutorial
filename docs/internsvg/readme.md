# InternSVG 矢量图形 AI

## 课程简介

InternSVG 是书生生态推出的统一多模态 SVG 系统，首次将文本生成、图片转换、理解与编辑等多种 SVG 任务整合到一个多模态大语言模型中。该项目已被 ICLR 2026 接收，代表了矢量图形 AI 的前沿水平。

本课程将带你从 SVG 基础出发，理解 InternSVG 的架构设计，并通过实际操作掌握文本生成 SVG、图片转 SVG、SVG 编辑与动画生成等核心能力。

## 你将学到

- SVG 与位图的本质区别，以及 SVG 在现代设计中的优势
- InternSVG 的模型架构与训练策略
- 使用 InternSVG 从文本描述生成高质量矢量图形
- 将位图图片转换为可编辑的 SVG 代码
- 对已有 SVG 进行编辑、配色调整和动画添加
- 使用 LMDeploy 部署 InternSVG 模型服务

## SVG 基础与矢量图形优势

### 目标

理解 SVG 的基本概念，明确 SVG 相比位图的核心优势，为后续使用 InternSVG 打下基础。

### 内容

SVG（Scalable Vector Graphics）是一种基于 XML 的二维矢量图形格式。与 PNG、JPEG 等位图格式不同，SVG 用数学描述来定义图形，具有天然的可缩放性。

**SVG vs 位图对比：**

| 特性 | SVG（矢量） | PNG/JPEG（位图） |
|------|-------------|-----------------|
| 缩放 | 无损缩放，任意分辨率清晰 | 放大后出现锯齿和模糊 |
| 文件体积 | 简单图形极小（几 KB） | 随分辨率线性增长 |
| 可编辑性 | 代码级可编辑，支持动画 | 需要图形编辑软件 |
| 适用场景 | 图标、Logo、图表、插画 | 照片、复杂纹理 |
| 搜索引擎 | 文本内容可被索引 | 内容不可索引 |

一个简单的 SVG 示例：

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="40" fill="#4A90D9" />
  <text x="50" y="55" text-anchor="middle" fill="white" font-size="16">
    AI
  </text>
</svg>
```

这段代码定义了一个蓝色圆形，中间写着 "AI"。无论放大到多少倍，它都保持锐利清晰。这正是 SVG 的魅力所在。

**为什么 AI 生成 SVG 很难？**

传统的图像生成模型（如 Stable Diffusion）输出的是像素矩阵，而 SVG 要求输出结构化的代码。SVG 代码可以很长（复杂插画可达数千 token），且必须语法正确才能渲染。这对模型的长序列生成能力和代码理解能力提出了很高的要求。

## InternSVG 架构与设计

### 目标

深入理解 InternSVG 的模型架构、数据集构建和训练策略。

### 内容

**模型架构：ViT-MLP-LLM 范式**

InternSVG 采用经典的视觉-语言多模态架构：

- **视觉编码器**：InternViT-300M，负责将输入图片编码为视觉 token
- **语言模型**：Qwen2.5-7B，负责理解指令并生成 SVG 代码
- **连接层**：MLP 适配器，将视觉 token 映射到语言模型的输入空间

完整模型标识为 **InternSVG-8B**，基于 InternVL3-8B 架构构建。

**SVG 专用 token**

InternSVG 引入了 SVG 专用的特殊 token，覆盖 SVG 语法中的高频元素（如 `<path>`、`<circle>`、`<rect>` 等标签和属性）。这些 token 的嵌入通过子词（subword）初始化策略来设定，使模型能更高效地生成合法的 SVG 代码。

**SAgoge 数据集**

InternSVG 配套构建了 SAgoge，这是目前规模最大、覆盖最全的多模态 SVG 数据集：

- **图标**：简单的 icon 级别 SVG
- **长序列插画**：复杂的设计插画
- **科学图表**：化学结构、流程图等
- **动态动画**：包含 CSS/SMIL 动画的 SVG

**两阶段训练策略**

1. **第一阶段**：在短序列、简单的静态 SVG（图标等）上训练，让模型学会基础的 SVG 语法
2. **第二阶段**：扩展到长序列插画和复杂动画，提升模型处理复杂场景的能力

## 环境搭建与模型部署

### 目标

完成 InternSVG 的环境搭建，通过 LMDeploy 部署模型服务。

### 内容

**安装依赖**

```bash
# 创建 conda 环境
conda create -n internsvg python=3.9 -y
conda activate internsvg

# 克隆项目
git clone https://github.com/hmwang2002/InternSVG.git
cd InternSVG
pip install -r requirements.txt

# 安装额外依赖
pip install git+https://github.com/openai/CLIP.git
pip install deepspeed==0.16.9
pip install av==14.4.0
```

**下载模型权重**

InternSVG-8B 模型托管在 HuggingFace：

```bash
# 如果在国内环境，推荐使用 hf-mirror
export HF_ENDPOINT=https://hf-mirror.com

huggingface-cli download InternSVG/InternSVG-8B --local-dir ./models/InternSVG-8B
```

**使用 LMDeploy 部署 API 服务**

```bash
pip install lmdeploy

# 启动 API 服务（单卡部署）
lmdeploy serve api_server ./models/InternSVG-8B \
  --model-name InternSVG \
  --backend pytorch \
  --chat-template internvl2_5 \
  --server-port 23333
```

启动后，服务监听在 `http://0.0.0.0:23333`，提供 OpenAI 兼容的 API 接口。

## 文本生成 SVG

### 目标

掌握通过文本描述生成 SVG 图形的完整流程。

### 内容

InternSVG 支持通过自然语言描述生成对应的 SVG 代码。以下是使用 Python OpenAI SDK 调用已部署服务的示例。

**基础调用：生成一个图标**

```python
from openai import OpenAI

client = OpenAI(
    api_key="EMPTY",
    base_url="http://localhost:23333/v1",
)

response = client.chat.completions.create(
    model="InternSVG",
    messages=[
        {
            "role": "user",
            "content": "Generate an SVG icon of a lightning bolt in flat design style, "
                       "using a bright yellow color on a dark blue circular background."
        }
    ],
    temperature=0.0,
    max_tokens=4000,
)

svg_code = response.choices[0].message.content
print(svg_code)

# 保存为文件
with open("lightning.svg", "w") as f:
    f.write(svg_code)
```

**批量生成一组统一风格的图标**

```python
from openai import OpenAI

client = OpenAI(api_key="EMPTY", base_url="http://localhost:23333/v1")

icon_prompts = [
    "a home icon in minimal line art style, single color #333333, 64x64 viewBox",
    "a search magnifying glass icon in minimal line art style, single color #333333, 64x64 viewBox",
    "a settings gear icon in minimal line art style, single color #333333, 64x64 viewBox",
    "a user profile icon in minimal line art style, single color #333333, 64x64 viewBox",
    "a notification bell icon in minimal line art style, single color #333333, 64x64 viewBox",
    "a message chat bubble icon in minimal line art style, single color #333333, 64x64 viewBox",
]

for i, prompt in enumerate(icon_prompts):
    response = client.chat.completions.create(
        model="InternSVG",
        messages=[{"role": "user", "content": f"Generate an SVG: {prompt}"}],
        temperature=0.0,
        max_tokens=4000,
    )
    svg_code = response.choices[0].message.content
    filename = f"icon_{i+1}.svg"
    with open(filename, "w") as f:
        f.write(svg_code)
    print(f"[{i+1}/{len(icon_prompts)}] Saved {filename}")

print("All icons generated.")
```

**生成技巧**

- 设置 `temperature=0.0` 可以获得最稳定、最精确的输出
- 在 prompt 中明确指定 viewBox 尺寸、配色和风格，有助于保持一组图标的一致性
- 对于复杂插画，适当提高 `max_tokens`（建议 8000 以上）

## 图片转 SVG

### 目标

学会将位图图片转换为可编辑的 SVG 矢量代码。

### 内容

InternSVG 的多模态能力允许它接收一张图片作为输入，输出对应的 SVG 代码。这在将位图 Logo、图标或简单插画矢量化时非常实用。

**图片转 SVG 示例**

```python
import base64
from openai import OpenAI

client = OpenAI(api_key="EMPTY", base_url="http://localhost:23333/v1")

# 读取图片并编码为 base64
with open("input_logo.png", "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode("utf-8")

response = client.chat.completions.create(
    model="InternSVG",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{image_b64}"},
                },
                {
                    "type": "text",
                    "text": "Convert this image to SVG code. Preserve the original colors and shapes as accurately as possible.",
                },
            ],
        }
    ],
    temperature=0.0,
    max_tokens=4000,
)

svg_code = response.choices[0].message.content
with open("output_logo.svg", "w") as f:
    f.write(svg_code)
print("Conversion complete. Saved to output_logo.svg")
```

**适用场景与局限**

- 最适合：图标、Logo、简单插画、几何图形
- 可以处理：科学图表、流程图、简单的卡通形象
- 不适合：照片级复杂图像（人脸照片、风景照等）

位图图片越简洁、轮廓越清晰，转换效果越好。

## SVG 编辑与动画

### 目标

掌握使用 InternSVG 对已有 SVG 进行编辑和添加动画的方法。

### 内容

InternSVG 不仅能生成 SVG，还能理解和编辑已有的 SVG 代码。你可以通过自然语言指令来修改配色、调整布局或添加动画效果。

**编辑配色**

```python
from openai import OpenAI

client = OpenAI(api_key="EMPTY", base_url="http://localhost:23333/v1")

original_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="40" fill="#FF0000" />
  <rect x="30" y="30" width="40" height="40" fill="#00FF00" />
</svg>"""

response = client.chat.completions.create(
    model="InternSVG",
    messages=[
        {
            "role": "user",
            "content": f"Here is an SVG:\n\n{original_svg}\n\n"
                       f"Please change the color scheme to a professional blue-gray palette. "
                       f"Use #2C3E50 for the circle and #3498DB for the rectangle.",
        }
    ],
    temperature=0.0,
    max_tokens=4000,
)

edited_svg = response.choices[0].message.content
with open("edited.svg", "w") as f:
    f.write(edited_svg)
print("Edit complete.")
```

**添加 CSS 动画**

```python
response = client.chat.completions.create(
    model="InternSVG",
    messages=[
        {
            "role": "user",
            "content": f"Here is an SVG:\n\n{original_svg}\n\n"
                       f"Add a smooth rotation animation to the rectangle. "
                       f"It should rotate 360 degrees continuously over 3 seconds.",
        }
    ],
    temperature=0.0,
    max_tokens=4000,
)

animated_svg = response.choices[0].message.content
with open("animated.svg", "w") as f:
    f.write(animated_svg)
```

**将动画 SVG 转为视频**

InternSVG 项目提供了将动画 SVG 转为 MP4 视频的工具：

```bash
python utils/svg_animate.py \
  --input animated.svg \
  --output animated.mp4 \
  --width 448 \
  --height 448
```

**编辑指令示例**

以下是一些有效的编辑指令，供参考：

- "Change all fill colors to shades of blue"
- "Make this icon larger and add a drop shadow"
- "Simplify this SVG by removing unnecessary groups and transforms"
- "Add a fade-in animation that plays once over 1 second"
- "Convert the stroke style from solid to dashed"

## SArena 评测与进阶

### 目标

了解如何使用 SArena 基准评测 SVG 生成质量，以及进阶用法。

### 内容

**SArena 评测框架**

InternSVG 配套发布了 SArena 评测基准，覆盖以下维度：

- **Text-to-SVG**：文本生成 SVG 的质量评测
- **Image-to-SVG**：图片转 SVG 的还原度评测
- **SVG 编辑**：编辑指令的执行准确度

运行评测：

```bash
python evaluate.py \
  --text2svg_test_dir ./data/test/text2svg \
  --img2svg_test_dir ./data/test/img2svg \
  --temperature 0.0 \
  --max_tokens 4000
```

如果模型不支持某个任务，将对应的测试目录参数设为空字符串即可跳过。

**多卡并行部署**

对于需要更高吞吐量的场景，可以使用 LMDeploy 的代理模式进行多卡并行：

```bash
# 启动代理
lmdeploy serve proxy --server-name 0.0.0.0 --server-port 10010 \
  --routing-strategy "min_expected_latency" &

# 在不同 GPU 上启动多个 worker
CUDA_VISIBLE_DEVICES=0 lmdeploy serve api_server ./models/InternSVG-8B \
  --proxy-url http://0.0.0.0:10010 \
  --model-name InternSVG \
  --backend pytorch \
  --chat-template internvl2_5 \
  --server-port 23334 &

CUDA_VISIBLE_DEVICES=1 lmdeploy serve api_server ./models/InternSVG-8B \
  --proxy-url http://0.0.0.0:10010 \
  --model-name InternSVG \
  --backend pytorch \
  --chat-template internvl2_5 \
  --server-port 23335 &
```

然后将客户端请求发送到代理地址 `http://0.0.0.0:10010` 即可自动负载均衡。

## 参考资料

- InternSVG 论文：https://arxiv.org/abs/2510.11341
- InternSVG GitHub：https://github.com/hmwang2002/InternSVG
- InternSVG 模型权重：https://huggingface.co/InternSVG/InternSVG-8B
- SAgoge 数据集：https://huggingface.co/datasets/InternSVG/SAgoge
- LMDeploy 文档：https://lmdeploy.readthedocs.io/
- SVG 规范：https://developer.mozilla.org/en-US/docs/Web/SVG
