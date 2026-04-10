# InternSVG 矢量图形 AI

> 本文档 AI + 社区共建中

## 先看成果：AI 生成的矢量图形

在开始学习之前，先看看 InternSVG 能做什么。以下三个成果均由 InternSVG-8B 模型一次生成，无需手动修改。

**成果一：一套 App 图标**

一句 prompt 生成 10 个统一风格的扁平化图标（首页、搜索、设置、用户、通知、消息、收藏、日历、相机、音乐），线条粗细一致、配色统一、viewBox 对齐，可直接用于移动端项目。

**成果二：数据可视化图表**

输入一段文本描述的数据（"2023 年各季度销售额分别为 120 万、185 万、 210 万、175 万"），InternSVG 直接输出一张带坐标轴、数据标注和图例的柱状图 SVG。矢量格式意味着放到论文里放大多少倍都不会模糊。

**成果三：SVG 动画**

给一个静态的齿轮图标加上旋转动画，InternSVG 自动补全 CSS `@keyframes`，输出的 SVG 文件在浏览器中直接播放，无需任何前端代码。

这三个场景对应本课程的三个实战项目。学完本课程，你将能独立完成这些任务。

---

## 课程简介

InternSVG 是书生生态推出的统一多模态 SVG 系统，首次将文本生成、图片转换、理解与编辑等多种 SVG 任务整合到一个多模态大语言模型中。该项目已被 ICLR 2026 接收，代表了矢量图形 AI 的前沿水平。

本课程将带你从 SVG 基础出发，理解 InternSVG 的架构设计，并通过三个完整的实战项目掌握文本生成 SVG、图片转 SVG、SVG 编辑与动画生成等核心能力。

## 你将学到

- SVG 与位图的本质区别，以及 SVG 在现代设计中的优势
- InternSVG 的模型架构与训练策略
- 使用 LMDeploy 完整部署 InternSVG 模型服务（含显存不足时的替代方案）
- 使用 InternSVG 从文本描述生成高质量矢量图形
- 将位图图片转换为可编辑的 SVG 代码
- 对已有 SVG 进行编辑、配色调整和动画添加
- 在科学可视化场景（分子结构、实验数据图表、论文配图）中应用 SVG 生成

---

## 第一部分：SVG 基础与矢量图形优势

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
| 版本管理 | 文本格式，可 Git diff | 二进制文件，无法 diff |

**一个完整的 SVG 示例：**

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
  <!-- 背景圆形 -->
  <circle cx="100" cy="100" r="90" fill="#1a1a2e" />
  <!-- 装饰环 -->
  <circle cx="100" cy="100" r="70" fill="none" stroke="#e94560" stroke-width="3" />
  <!-- 中心文字 -->
  <text x="100" y="108" text-anchor="middle" fill="#eaeaea" font-size="28" font-family="Arial, sans-serif" font-weight="bold">
    SVG
  </text>
  <!-- 底部小字 -->
  <text x="100" y="135" text-anchor="middle" fill="#a8a8a8" font-size="10" font-family="Arial, sans-serif">
    Scalable Vector Graphics
  </text>
</svg>
```

将上面的代码保存为 `demo.svg`，用浏览器打开即可看到效果。无论放大到多少倍，文字和圆形边缘都保持锐利。这正是 SVG 的核心优势。

**为什么 AI 生成 SVG 很难？**

传统的图像生成模型（如 Stable Diffusion）输出的是像素矩阵，而 SVG 要求输出结构化的代码。SVG 代码可以很长（复杂插画可达数千 token），且必须语法正确才能渲染。这对模型的长序列生成能力和代码理解能力提出了很高的要求。具体来说：

1. **语法严格性** -- SVG 是 XML 的子集，标签必须正确闭合，属性值必须合法，一个字符错误就会导致整个图形无法渲染
2. **序列长度** -- 一个中等复杂度的 SVG 插画可能包含 2000-5000 个 token，远超一般文本生成任务
3. **空间推理** -- 模型需要理解坐标系、相对位置、大小比例等空间概念
4. **风格一致性** -- 批量生成时，需要保持颜色、线条粗细、设计语言的统一

这些挑战正是 InternSVG 要解决的核心问题。

---

## 第二部分：InternSVG 架构与设计

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

这意味着模型不需要逐字符拼出 `<path d="M 10 20 L 30 40" />`，而是可以用更少的 token 表达同样的内容，显著提升生成效率和准确率。

**SAgoge 数据集**

InternSVG 配套构建了 SAgoge，这是目前规模最大、覆盖最全的多模态 SVG 数据集：

| 数据类别 | 说明 | 典型 token 长度 |
|---------|------|---------------|
| 图标 | 简单的 icon 级别 SVG | 100-500 |
| 长序列插画 | 复杂的设计插画 | 2000-8000 |
| 科学图表 | 化学结构、流程图等 | 500-3000 |
| 动态动画 | 包含 CSS/SMIL 动画的 SVG | 500-5000 |

**两阶段训练策略**

1. **第一阶段**：在短序列、简单的静态 SVG（图标等）上训练，让模型学会基础的 SVG 语法和空间关系
2. **第二阶段**：扩展到长序列插画和复杂动画，提升模型处理复杂场景的能力

这种课程式学习策略（curriculum learning）使模型先掌握基础再挑战复杂任务，比直接在全量数据上训练效果更好。

---

## 第三部分：环境搭建与模型部署

### 目标

完成 InternSVG 的环境搭建，通过 LMDeploy 部署模型服务，确保后续实战项目可以顺利运行。

### 内容

**硬件要求**

| 部署方式 | 最低显存 | 推荐显存 | 说明 |
|---------|---------|---------|------|
| FP16 全精度 | 24 GB | 40 GB+ | A100/A800/华为昇腾 Atlas 800T A2 |
| INT4 量化 | 10 GB | 16 GB+ | RTX 4090 / RTX 3090 等消费级显卡 |
| CPU 推理 | -- | 32 GB 内存 | 速度较慢，仅用于体验测试 |

### 步骤 1：创建环境并安装依赖

```bash
# 创建 conda 环境
conda create -n internsvg python=3.10 -y
conda activate internsvg

# 安装 PyTorch（CUDA 12.1 示例，根据你的 CUDA 版本调整）
pip install torch==2.4.0 torchvision==0.19.0 --index-url https://download.pytorch.org/whl/cu121

# 克隆 InternSVG 项目
git clone https://github.com/hmwang2002/InternSVG.git
cd InternSVG

# 安装项目依赖
pip install -r requirements.txt

# 安装额外依赖
pip install git+https://github.com/openai/CLIP.git
pip install deepspeed==0.16.9
pip install av==14.4.0
```

### 步骤 2：下载模型权重

```bash
# 安装 huggingface-cli（如果尚未安装）
pip install -U huggingface_hub

# 如果在国内环境，推荐使用 hf-mirror 加速下载
export HF_ENDPOINT=https://hf-mirror.com

# 下载模型权重（约 16 GB）
huggingface-cli download InternSVG/InternSVG-8B --local-dir ./models/InternSVG-8B

# 验证下载完整性：检查目录结构
ls -lh ./models/InternSVG-8B/
# 应该看到 config.json, tokenizer.json, model-*.safetensors 等文件
```

### 步骤 3：安装 LMDeploy 并启动 API 服务

```bash
# 安装 LMDeploy
pip install lmdeploy>=0.6.0

# 启动 API 服务（单卡部署，FP16）
lmdeploy serve api_server ./models/InternSVG-8B \
  --model-name InternSVG \
  --backend pytorch \
  --chat-template internvl2_5 \
  --server-port 23333
```

启动成功后，你会看到类似以下的日志输出：

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:23333 (Press CTRL+C to quit)
```

### 步骤 4：验证服务是否正常

打开一个新终端，运行以下命令测试：

```bash
curl http://localhost:23333/v1/models
```

预期返回：

```json
{
  "object": "list",
  "data": [
    {
      "id": "InternSVG",
      "object": "model",
      ...
    }
  ]
}
```

看到模型名称 `InternSVG` 出现在返回结果中，说明服务已经正常运行。

### 步骤 5：安装 Python 客户端依赖

后续实战项目需要用 Python 调用 API，安装 OpenAI SDK：

```bash
pip install openai
```

### 显存不足时的替代方案

**方案 A：INT4 量化部署（推荐，10 GB 显存即可）**

```bash
# 安装量化支持
pip install auto-gptq

# 使用 INT4 量化启动
lmdeploy serve api_server ./models/InternSVG-8B \
  --model-name InternSVG \
  --backend pytorch \
  --chat-template internvl2_5 \
  --server-port 23333 \
  --quant-policy 4
```

INT4 量化会略微降低生成质量，但对于图标和简单图形的生成影响不大。

**方案 B：多卡并行（适用于有多张小显存卡的情况）**

```bash
# 双卡并行，每张卡分担一半模型
CUDA_VISIBLE_DEVICES=0,1 lmdeploy serve api_server ./models/InternSVG-8B \
  --model-name InternSVG \
  --backend pytorch \
  --chat-template internvl2_5 \
  --server-port 23333 \
  --tp 2
```

**方案 C：使用 InternSVG 官方提供的在线 Demo**

如果你没有 GPU 资源，可以先使用 InternSVG 项目提供的在线 Demo 体验核心功能，熟悉 prompt 写法后再考虑本地部署。

---

## 第四部分：文本生成 SVG

### 目标

掌握通过文本描述生成 SVG 图形的完整流程，理解 prompt 工程对生成质量的影响。

### 内容

InternSVG 支持通过自然语言描述生成对应的 SVG 代码。以下是使用 Python OpenAI SDK 调用已部署服务的完整代码。

**基础调用：生成一个图标**

```python
"""
InternSVG 基础调用示例：生成一个闪电图标
前提：已按第三部分启动 LMDeploy API 服务（端口 23333）
"""

from openai import OpenAI

# 连接到本地部署的 InternSVG 服务
client = OpenAI(
    api_key="EMPTY",
    base_url="http://localhost:23333/v1",
)

# 发送生成请求
response = client.chat.completions.create(
    model="InternSVG",
    messages=[
        {
            "role": "user",
            "content": "Generate an SVG icon of a lightning bolt in flat design style, "
                       "using a bright yellow color (#FFD700) on a dark blue circular "
                       "background (#1a1a2e). Use a 100x100 viewBox."
        }
    ],
    temperature=0.0,
    max_tokens=4000,
)

# 提取生成的 SVG 代码
svg_code = response.choices[0].message.content
print("Generated SVG code:")
print(svg_code)

# 保存为 SVG 文件
with open("lightning.svg", "w", encoding="utf-8") as f:
    f.write(svg_code)
print("Saved to lightning.svg -- open in browser to view.")
```

**Prompt 工程技巧**

生成质量高度依赖 prompt 的写法。以下是经过验证的 prompt 模板：

```
Generate an SVG [图形类型]: [具体描述].
Style: [风格].
Colors: [配色方案].
ViewBox: [尺寸].
```

好的 prompt 示例：

| Prompt | 效果 |
|--------|------|
| `Generate an SVG icon of a home, minimal line art, stroke #333333 stroke-width 2, no fill, 64x64 viewBox` | 生成线条清晰、风格统一的图标 |
| `Generate an SVG illustration of a mountain landscape with sunset, flat design, warm colors #FF6B35 #F7C59F #004E89, 400x300 viewBox` | 生成层次分明的扁平风插画 |
| `Generate an SVG badge with text "CERTIFIED" in center, hexagonal shape, gold #FFD700 border, dark #1a1a2e background` | 生成可用于证书的徽章 |

不好的 prompt 示例：

| Prompt | 问题 |
|--------|------|
| `Draw something cool` | 太模糊，模型不知道画什么 |
| `Generate a photo-realistic portrait` | SVG 不适合照片级图像 |
| `Make an SVG` | 没有任何具体描述 |

---

## 实战项目一：为 App 生成一套统一风格图标

### 项目目标

为一个移动端 App 生成 10 个统一风格的图标，要求线条粗细一致、配色统一、viewBox 对齐，可直接导入设计工具或项目中使用。

### 完整代码

```python
"""
实战项目一：批量生成 App 图标套件
生成 10 个统一风格的扁平化图标，保存为独立 SVG 文件
"""

import os
from openai import OpenAI

# 连接到 InternSVG 服务
client = OpenAI(api_key="EMPTY", base_url="http://localhost:23333/v1")

# 创建输出目录
output_dir = "app_icons"
os.makedirs(output_dir, exist_ok=True)

# 统一的风格描述（关键：保持一致性）
STYLE = (
    "minimal line art style, single color stroke #333333, "
    "stroke-width 2, no fill, rounded line-cap and line-join, "
    "64x64 viewBox, centered in the viewBox with 8px padding"
)

# 10 个图标的描述
icons = [
    ("home", "a house with a chimney"),
    ("search", "a magnifying glass"),
    ("settings", "a gear/cog wheel with 6 teeth"),
    ("user", "a person silhouette (head and shoulders)"),
    ("notification", "a bell"),
    ("message", "a chat bubble with three dots inside"),
    ("favorite", "a five-pointed star"),
    ("calendar", "a calendar page showing the number 15"),
    ("camera", "a camera with a circular lens"),
    ("music", "a musical note (eighth note)"),
]

# 逐个生成
for i, (name, description) in enumerate(icons):
    prompt = f"Generate an SVG icon of {description}, {STYLE}."

    print(f"[{i+1}/{len(icons)}] Generating {name} icon...")

    response = client.chat.completions.create(
        model="InternSVG",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=4000,
    )

    svg_code = response.choices[0].message.content

    # 保存文件
    filepath = os.path.join(output_dir, f"{name}.svg")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg_code)

    print(f"    Saved to {filepath}")

print(f"\nAll {len(icons)} icons generated in '{output_dir}/' directory.")
print("Open any .svg file in browser to preview.")
```

### 验证方法

1. 用浏览器逐个打开生成的 SVG 文件，检查图形是否正确
2. 把所有图标并排放在一个 HTML 页面中，检查风格是否统一：

```html
<!DOCTYPE html>
<html>
<head><title>Icon Preview</title></head>
<body style="display: flex; gap: 20px; flex-wrap: wrap; padding: 40px; background: #f5f5f5;">
  <img src="app_icons/home.svg" width="64" height="64" alt="home" />
  <img src="app_icons/search.svg" width="64" height="64" alt="search" />
  <img src="app_icons/settings.svg" width="64" height="64" alt="settings" />
  <img src="app_icons/user.svg" width="64" height="64" alt="user" />
  <img src="app_icons/notification.svg" width="64" height="64" alt="notification" />
  <img src="app_icons/message.svg" width="64" height="64" alt="message" />
  <img src="app_icons/favorite.svg" width="64" height="64" alt="favorite" />
  <img src="app_icons/calendar.svg" width="64" height="64" alt="calendar" />
  <img src="app_icons/camera.svg" width="64" height="64" alt="camera" />
  <img src="app_icons/music.svg" width="64" height="64" alt="music" />
</body>
</html>
```

3. 将 HTML 文件保存为 `preview.html`，用浏览器打开即可看到完整的图标集预览

### 调优建议

- 如果某个图标风格偏离，在 prompt 中增加约束：`"consistent with the other icons in this set, same stroke width and padding"`
- 如果图标太简单，增加描述细节：`"a gear with 8 teeth and a small circle in the center"`
- 如果图标位置偏移，明确要求居中：`"centered at (32, 32)"`

---

## 第五部分：图片转 SVG

### 目标

学会将位图图片转换为可编辑的 SVG 矢量代码，理解适用范围和局限性。

### 内容

InternSVG 的多模态能力允许它接收一张图片作为输入，输出对应的 SVG 代码。这在将位图 Logo、图标或简单插画矢量化时非常实用。

**完整的图片转 SVG 代码**

```python
"""
图片转 SVG：将一张 PNG 图片转换为可编辑的 SVG 代码
支持 PNG、JPEG、WebP 等常见图片格式
"""

import base64
import sys
from pathlib import Path
from openai import OpenAI

def image_to_svg(image_path: str, output_path: str = None) -> str:
    """
    将图片转换为 SVG 代码

    Args:
        image_path: 输入图片路径（PNG/JPEG/WebP）
        output_path: 输出 SVG 路径，默认为输入文件名 + .svg

    Returns:
        生成的 SVG 代码字符串
    """
    # 检查输入文件
    input_file = Path(image_path)
    if not input_file.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    # 确定输出路径
    if output_path is None:
        output_path = input_file.with_suffix(".svg")

    # 确定 MIME 类型
    suffix_to_mime = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }
    mime_type = suffix_to_mime.get(input_file.suffix.lower(), "image/png")

    # 读取图片并编码为 base64
    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")

    print(f"Input: {image_path} ({input_file.stat().st_size / 1024:.1f} KB)")

    # 调用 InternSVG API
    client = OpenAI(api_key="EMPTY", base_url="http://localhost:23333/v1")

    response = client.chat.completions.create(
        model="InternSVG",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{image_b64}"
                        },
                    },
                    {
                        "type": "text",
                        "text": (
                            "Convert this image to SVG code. "
                            "Preserve the original colors, shapes, and proportions "
                            "as accurately as possible. Use clean SVG elements "
                            "(rect, circle, path, etc.) rather than embedded bitmaps."
                        ),
                    },
                ],
            }
        ],
        temperature=0.0,
        max_tokens=8000,
    )

    svg_code = response.choices[0].message.content

    # 保存 SVG 文件
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_code)

    print(f"Output: {output_path}")
    print(f"SVG code length: {len(svg_code)} characters")

    return svg_code


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python img2svg.py <image_path> [output_path]")
        print("Example: python img2svg.py logo.png logo.svg")
        sys.exit(1)

    img_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else None
    image_to_svg(img_path, out_path)
```

**适用场景与局限**

| 适用程度 | 场景 | 说明 |
|---------|------|------|
| 非常适合 | 图标、Logo | 轮廓清晰，颜色少，转换效果最佳 |
| 适合 | 简单插画、几何图形 | 扁平化设计、卡通风格效果好 |
| 可以处理 | 科学图表、流程图 | 结构化内容，模型能理解层次关系 |
| 不适合 | 照片、人脸、风景 | 像素级细节无法用矢量准确表达 |

核心原则：位图图片越简洁、轮廓越清晰，转换效果越好。

---

## 实战项目二：用文本生成数据可视化图表

### 项目目标

通过文本描述生成一张带坐标轴、数据标注和图例的柱状图 SVG，可直接用于报告或论文。

### 完整代码

```python
"""
实战项目二：文本生成数据可视化图表
输入数据描述，生成完整的柱状图 SVG
"""

from openai import OpenAI

client = OpenAI(api_key="EMPTY", base_url="http://localhost:23333/v1")

# 数据描述 prompt
data_prompt = """Generate an SVG bar chart with the following specifications:

Data:
- Q1 2024: 120 (million yuan)
- Q2 2024: 185 (million yuan)
- Q3 2024: 210 (million yuan)
- Q4 2024: 175 (million yuan)

Chart requirements:
- ViewBox: 500x350
- Title: "2024 Quarterly Revenue" at the top center, font-size 18, color #333333
- X-axis: quarter labels (Q1, Q2, Q3, Q4), font-size 12
- Y-axis: scale from 0 to 250, with gridlines at 50, 100, 150, 200, 250, light gray #e0e0e0 dashed lines
- Bars: width 60, spacing 30, colors gradient from #3498DB (Q1) to #2C3E50 (Q4)
- Data labels: show the value on top of each bar, font-size 11
- Background: white
- Add a subtle border: 1px solid #e0e0e0
"""

print("Generating bar chart SVG...")

response = client.chat.completions.create(
    model="InternSVG",
    messages=[{"role": "user", "content": data_prompt}],
    temperature=0.0,
    max_tokens=8000,
)

svg_code = response.choices[0].message.content

# 保存 SVG
with open("revenue_chart.svg", "w", encoding="utf-8") as f:
    f.write(svg_code)

print("Saved to revenue_chart.svg")
print(f"SVG code: {len(svg_code)} characters")
```

**进阶：生成饼图**

```python
"""
生成饼图 SVG
"""

from openai import OpenAI

client = OpenAI(api_key="EMPTY", base_url="http://localhost:23333/v1")

pie_prompt = """Generate an SVG pie chart with the following data:

Data (market share):
- Product A: 35%
- Product B: 25%
- Product C: 20%
- Product D: 12%
- Others: 8%

Requirements:
- ViewBox: 400x400
- Pie radius: 120, centered at (200, 200)
- Colors: #2ecc71, #3498db, #e74c3c, #f39c12, #95a5a6
- Labels: show percentage and product name next to each slice
- Title: "Market Share Distribution" at top, font-size 16, color #333
- Add a legend box at the bottom with color squares and labels
"""

response = client.chat.completions.create(
    model="InternSVG",
    messages=[{"role": "user", "content": pie_prompt}],
    temperature=0.0,
    max_tokens=8000,
)

svg_code = response.choices[0].message.content

with open("market_share_pie.svg", "w", encoding="utf-8") as f:
    f.write(svg_code)

print("Saved to market_share_pie.svg")
```

### 验证方法

1. 用浏览器打开生成的 SVG 文件，检查图表元素是否完整
2. 验证数据标注是否正确对应输入数据
3. 尝试放大浏览器页面到 200%、400%，确认文字和线条保持清晰

---

## 第六部分：SVG 编辑与动画

### 目标

掌握使用 InternSVG 对已有 SVG 进行编辑和添加动画的方法。

### 内容

InternSVG 不仅能生成 SVG，还能理解和编辑已有的 SVG 代码。你可以通过自然语言指令来修改配色、调整布局或添加动画效果。

**编辑配色**

```python
"""
SVG 编辑示例：修改配色方案
"""

from openai import OpenAI

client = OpenAI(api_key="EMPTY", base_url="http://localhost:23333/v1")

# 原始 SVG
original_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
  <circle cx="100" cy="100" r="80" fill="#FF0000" />
  <rect x="60" y="60" width="80" height="80" rx="10" fill="#00FF00" />
  <polygon points="100,30 130,90 70,90" fill="#0000FF" />
</svg>"""

response = client.chat.completions.create(
    model="InternSVG",
    messages=[
        {
            "role": "user",
            "content": (
                f"Here is an SVG:\n\n{original_svg}\n\n"
                "Please change the color scheme to a professional blue-gray palette. "
                "Use #2C3E50 for the circle, #3498DB for the rectangle, "
                "and #1ABC9C for the triangle. Keep all shapes and positions unchanged."
            ),
        }
    ],
    temperature=0.0,
    max_tokens=4000,
)

edited_svg = response.choices[0].message.content
with open("edited_colors.svg", "w", encoding="utf-8") as f:
    f.write(edited_svg)
print("Color scheme updated. Saved to edited_colors.svg")
```

**添加 CSS 动画**

```python
"""
SVG 动画示例：为图形添加旋转和缩放动画
"""

from openai import OpenAI

client = OpenAI(api_key="EMPTY", base_url="http://localhost:23333/v1")

static_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
  <circle cx="100" cy="100" r="80" fill="#1a1a2e" />
  <rect x="70" y="70" width="60" height="60" rx="8" fill="#e94560"
        transform="rotate(0, 100, 100)" />
</svg>"""

response = client.chat.completions.create(
    model="InternSVG",
    messages=[
        {
            "role": "user",
            "content": (
                f"Here is an SVG:\n\n{static_svg}\n\n"
                "Add two CSS animations:\n"
                "1. The red rectangle should rotate 360 degrees continuously, "
                "   3 seconds per revolution, smooth linear timing.\n"
                "2. The background circle should have a subtle pulse effect "
                "   (scale 1.0 to 1.05 and back), 2 seconds, infinite.\n"
                "Use <style> block inside the SVG for the CSS animations."
            ),
        }
    ],
    temperature=0.0,
    max_tokens=4000,
)

animated_svg = response.choices[0].message.content
with open("animated.svg", "w", encoding="utf-8") as f:
    f.write(animated_svg)
print("Animation added. Open animated.svg in browser to see the effect.")
```

用浏览器打开 `animated.svg`，你将看到矩形持续旋转、背景圆形微微脉动的效果。

**将动画 SVG 转为视频**

InternSVG 项目提供了将动画 SVG 转为 MP4 视频的工具：

```bash
cd InternSVG
python utils/svg_animate.py \
  --input animated.svg \
  --output animated.mp4 \
  --width 448 \
  --height 448
```

**常用编辑指令参考**

| 指令 | 用途 |
|------|------|
| `Change all fill colors to shades of blue` | 统一配色 |
| `Make this icon larger and add a drop shadow` | 增加视觉效果 |
| `Simplify this SVG by removing unnecessary groups and transforms` | 代码清理 |
| `Add a fade-in animation that plays once over 1 second` | 入场动画 |
| `Convert the stroke style from solid to dashed` | 线型变更 |
| `Add a dark mode variant with inverted colors` | 深色模式适配 |

---

## 实战项目三：PNG Logo 转 SVG 并改配色

### 项目目标

将一张 PNG 格式的 Logo 转换为可编辑的 SVG，然后通过自然语言指令修改配色方案，生成深色模式和浅色模式两个版本。

### 完整代码

```python
"""
实战项目三：PNG Logo 转 SVG + 配色变换
Step 1: 将 PNG 转为 SVG
Step 2: 基于 SVG 生成浅色模式版本
Step 3: 基于 SVG 生成深色模式版本
"""

import base64
from pathlib import Path
from openai import OpenAI

client = OpenAI(api_key="EMPTY", base_url="http://localhost:23333/v1")


def png_to_svg(image_path: str) -> str:
    """Step 1: PNG 转 SVG"""
    with open(image_path, "rb") as f:
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
                        "text": (
                            "Convert this logo image to clean SVG code. "
                            "Use vector elements (path, circle, rect, etc.), "
                            "not embedded bitmaps. Preserve the original colors "
                            "and proportions accurately."
                        ),
                    },
                ],
            }
        ],
        temperature=0.0,
        max_tokens=8000,
    )

    return response.choices[0].message.content


def recolor_svg(svg_code: str, instruction: str) -> str:
    """通用配色变换函数"""
    response = client.chat.completions.create(
        model="InternSVG",
        messages=[
            {
                "role": "user",
                "content": (
                    f"Here is an SVG:\n\n{svg_code}\n\n{instruction}\n\n"
                    "Keep all shapes, sizes, and positions exactly the same. "
                    "Only change colors."
                ),
            }
        ],
        temperature=0.0,
        max_tokens=8000,
    )
    return response.choices[0].message.content


# --- 主流程 ---

# 准备输入图片（替换为你自己的 Logo 路径）
input_logo = "my_logo.png"

if not Path(input_logo).exists():
    print(f"Please place your logo at: {input_logo}")
    print("For testing, you can use any simple PNG icon.")
    exit(1)

# Step 1: PNG -> SVG
print("Step 1: Converting PNG to SVG...")
base_svg = png_to_svg(input_logo)
with open("logo_base.svg", "w", encoding="utf-8") as f:
    f.write(base_svg)
print(f"  Base SVG saved to logo_base.svg ({len(base_svg)} chars)")

# Step 2: 浅色模式
print("Step 2: Generating light mode variant...")
light_svg = recolor_svg(
    base_svg,
    "Create a light mode version: use dark colors (#1a1a2e, #2C3E50, #333333) "
    "for the main elements, designed to be used on a white/light background."
)
with open("logo_light.svg", "w", encoding="utf-8") as f:
    f.write(light_svg)
print("  Light mode saved to logo_light.svg")

# Step 3: 深色模式
print("Step 3: Generating dark mode variant...")
dark_svg = recolor_svg(
    base_svg,
    "Create a dark mode version: use light/bright colors (#eaeaea, #3498DB, #1ABC9C) "
    "for the main elements, designed to be used on a dark (#1a1a2e) background."
)
with open("logo_dark.svg", "w", encoding="utf-8") as f:
    f.write(dark_svg)
print("  Dark mode saved to logo_dark.svg")

print("\nDone! Generated 3 files:")
print("  logo_base.svg  -- original colors from PNG")
print("  logo_light.svg -- light mode variant")
print("  logo_dark.svg  -- dark mode variant")
```

### 验证方法

创建一个预览页面来对比三个版本：

```html
<!DOCTYPE html>
<html>
<head><title>Logo Variants Preview</title></head>
<body style="font-family: Arial, sans-serif; padding: 40px;">
  <h2>Logo Variants</h2>
  <div style="display: flex; gap: 40px;">
    <div style="padding: 30px; background: #ffffff; border: 1px solid #ddd;">
      <p>Base (from PNG)</p>
      <img src="logo_base.svg" width="200" />
    </div>
    <div style="padding: 30px; background: #ffffff; border: 1px solid #ddd;">
      <p>Light Mode</p>
      <img src="logo_light.svg" width="200" />
    </div>
    <div style="padding: 30px; background: #1a1a2e; color: #eee; border: 1px solid #333;">
      <p>Dark Mode</p>
      <img src="logo_dark.svg" width="200" />
    </div>
  </div>
</body>
</html>
```

---

## 第七部分：AGI4S -- 科学可视化场景

### 目标

了解如何将 InternSVG 应用于科学研究中的可视化需求，包括分子结构、实验数据图表和论文配图。

### 内容

SVG 格式在科学出版中有天然优势：矢量格式意味着论文中的图表在任何缩放比例下都保持清晰，且文件体积远小于高分辨率位图。InternSVG 可以辅助研究者快速生成规范的科学图表。

**场景一：分子结构 SVG**

```python
"""
科学可视化：生成分子结构示意图
适用于化学/生物学论文配图
"""

from openai import OpenAI

client = OpenAI(api_key="EMPTY", base_url="http://localhost:23333/v1")

molecule_prompt = """Generate an SVG diagram of a water molecule (H2O) with the following specifications:

Structure:
- One oxygen atom (large circle, red #e74c3c, radius 25) at center
- Two hydrogen atoms (smaller circles, blue #3498db, radius 15) connected to oxygen
- Bond angle approximately 104.5 degrees
- Covalent bonds shown as thick lines (stroke-width 4, color #555)

Labels:
- "O" label on oxygen atom, white text, font-size 16, bold
- "H" labels on hydrogen atoms, white text, font-size 12, bold
- Bond angle "104.5 deg" label with an arc indicator

Style:
- ViewBox: 300x250
- Clean scientific illustration style
- White background
- Add a title "Water Molecule (H2O)" at top, font-size 14, color #333
"""

response = client.chat.completions.create(
    model="InternSVG",
    messages=[{"role": "user", "content": molecule_prompt}],
    temperature=0.0,
    max_tokens=8000,
)

svg_code = response.choices[0].message.content
with open("water_molecule.svg", "w", encoding="utf-8") as f:
    f.write(svg_code)
print("Saved to water_molecule.svg")
```

**场景二：实验数据折线图**

```python
"""
科学可视化：实验数据折线图
适用于论文中展示实验结果趋势
"""

from openai import OpenAI

client = OpenAI(api_key="EMPTY", base_url="http://localhost:23333/v1")

experiment_prompt = """Generate an SVG line chart for experimental results:

Data (two groups):
Group A (Treatment): [2.1, 3.4, 5.8, 7.2, 8.9, 9.5] at time points [0, 1, 2, 3, 4, 5] hours
Group B (Control):   [2.0, 2.3, 2.8, 3.1, 3.4, 3.6] at time points [0, 1, 2, 3, 4, 5] hours

Chart requirements:
- ViewBox: 500x350
- Title: "Cell Growth Rate Over Time" at top, font-size 16
- X-axis label: "Time (hours)", font-size 12
- Y-axis label: "Growth Rate (OD600)", font-size 12, rotated 90 degrees
- Group A: solid line, color #e74c3c, circle markers at data points
- Group B: dashed line, color #3498db, square markers at data points
- Gridlines: light gray dashed lines
- Legend: top-right corner with line samples and labels
- Error bars are NOT needed for this chart
- Scientific publication style: clean, minimal, no decorative elements
"""

response = client.chat.completions.create(
    model="InternSVG",
    messages=[{"role": "user", "content": experiment_prompt}],
    temperature=0.0,
    max_tokens=8000,
)

svg_code = response.choices[0].message.content
with open("experiment_chart.svg", "w", encoding="utf-8") as f:
    f.write(svg_code)
print("Saved to experiment_chart.svg")
```

**场景三：论文流程图**

```python
"""
科学可视化：研究方法流程图
适用于论文 Methods 部分
"""

from openai import OpenAI

client = OpenAI(api_key="EMPTY", base_url="http://localhost:23333/v1")

flowchart_prompt = """Generate an SVG flowchart for a machine learning pipeline:

Nodes (top to bottom):
1. "Raw Data" (rounded rectangle, fill #ecf0f1, border #bdc3c7)
2. "Data Preprocessing" (rounded rectangle, fill #d5f4e6, border #27ae60)
3. Split into two parallel branches:
   - Left: "Training Set (80%)" (rectangle, fill #d6eaf8, border #3498db)
   - Right: "Test Set (20%)" (rectangle, fill #fdebd0, border #e67e22)
4. Left branch continues: "Model Training" (rounded rectangle, fill #d5f4e6, border #27ae60)
5. Both branches merge: "Evaluation" (rounded rectangle, fill #fadbd8, border #e74c3c)
6. "Results" (rounded rectangle, fill #ecf0f1, border #bdc3c7)

Arrows: solid lines with arrowheads, color #555, stroke-width 2
ViewBox: 400x500
Font: sans-serif, size 12, color #333
Style: clean, publication-ready
"""

response = client.chat.completions.create(
    model="InternSVG",
    messages=[{"role": "user", "content": flowchart_prompt}],
    temperature=0.0,
    max_tokens=8000,
)

svg_code = response.choices[0].message.content
with open("ml_pipeline.svg", "w", encoding="utf-8") as f:
    f.write(svg_code)
print("Saved to ml_pipeline.svg")
```

**科学可视化的 Prompt 要点**

1. **明确标注单位** -- 坐标轴标签必须带单位（如 "Time (hours)"），这是论文配图的基本要求
2. **指定出版风格** -- 加上 "scientific publication style" 或 "clean, minimal"，避免花哨装饰
3. **使用专业配色** -- 推荐 ColorBrewer 系列配色，对色盲友好
4. **标注数据来源** -- 可以在图表底部加上 caption 或 source 标注

---

## 第八部分：SArena 评测与多卡部署

### 目标

了解如何使用 SArena 基准评测 SVG 生成质量，以及生产环境下的多卡并行部署方案。

### 内容

**SArena 评测框架**

InternSVG 配套发布了 SArena 评测基准，覆盖以下维度：

- **Text-to-SVG**：文本生成 SVG 的质量评测
- **Image-to-SVG**：图片转 SVG 的还原度评测
- **SVG 编辑**：编辑指令的执行准确度

运行评测：

```bash
cd InternSVG

python evaluate.py \
  --text2svg_test_dir ./data/test/text2svg \
  --img2svg_test_dir ./data/test/img2svg \
  --temperature 0.0 \
  --max_tokens 4000
```

如果模型不支持某个任务，将对应的测试目录参数设为空字符串即可跳过。

**多卡并行部署（生产环境推荐）**

对于需要更高吞吐量的场景（如批量生成、对外提供 API 服务），可以使用 LMDeploy 的代理模式进行多卡并行：

```bash
# 第一步：启动负载均衡代理
lmdeploy serve proxy \
  --server-name 0.0.0.0 \
  --server-port 10010 \
  --routing-strategy "min_expected_latency" &

# 第二步：在 GPU 0 上启动 worker
CUDA_VISIBLE_DEVICES=0 lmdeploy serve api_server ./models/InternSVG-8B \
  --proxy-url http://0.0.0.0:10010 \
  --model-name InternSVG \
  --backend pytorch \
  --chat-template internvl2_5 \
  --server-port 23334 &

# 第三步：在 GPU 1 上启动 worker
CUDA_VISIBLE_DEVICES=1 lmdeploy serve api_server ./models/InternSVG-8B \
  --proxy-url http://0.0.0.0:10010 \
  --model-name InternSVG \
  --backend pytorch \
  --chat-template internvl2_5 \
  --server-port 23335 &

# 验证代理是否正常
curl http://localhost:10010/v1/models
```

然后将客户端请求发送到代理地址 `http://0.0.0.0:10010` 即可自动负载均衡。客户端代码只需修改 `base_url`：

```python
client = OpenAI(
    api_key="EMPTY",
    base_url="http://localhost:10010/v1",  # 改为代理地址
)
```

---

## 常见问题与排错

### Q1: SVG 输出有语法错误，浏览器无法渲染

**症状**：浏览器打开 SVG 文件显示空白或报错。

**排查步骤**：

```python
"""
SVG 语法检查与修复工具
"""

import re
from xml.etree import ElementTree


def validate_svg(svg_code: str) -> tuple[bool, str]:
    """检查 SVG 代码是否合法"""
    try:
        ElementTree.fromstring(svg_code)
        return True, "SVG is valid."
    except ElementTree.ParseError as e:
        return False, f"XML parse error: {e}"


def clean_svg(svg_code: str) -> str:
    """
    尝试清理常见的 SVG 语法问题：
    1. 去掉模型输出中可能包含的 markdown 代码块标记
    2. 确保只保留 <svg>...</svg> 部分
    """
    # 去掉 markdown 代码块标记
    svg_code = re.sub(r"```(?:xml|svg|html)?\n?", "", svg_code)
    svg_code = svg_code.strip()

    # 提取 <svg>...</svg> 部分
    match = re.search(r"(<svg[\s\S]*?</svg>)", svg_code)
    if match:
        svg_code = match.group(1)

    return svg_code


# 使用示例
raw_output = response.choices[0].message.content
cleaned = clean_svg(raw_output)
is_valid, message = validate_svg(cleaned)

if is_valid:
    with open("output.svg", "w", encoding="utf-8") as f:
        f.write(cleaned)
    print("SVG saved successfully.")
else:
    print(f"SVG validation failed: {message}")
    print("Try regenerating with a simpler prompt.")
```

**常见原因及解决方法**：

| 原因 | 解决方法 |
|------|---------|
| 模型输出包含 markdown 代码块标记 | 用上面的 `clean_svg` 函数清理 |
| 标签未正确闭合 | 降低 `temperature` 到 0.0，增加 `max_tokens` |
| 输出被截断（token 超限） | 增大 `max_tokens`（建议 8000 以上） |
| 包含不合法的属性值 | 在 prompt 中加上 "output valid SVG XML" |

### Q2: 生成的图形太简单或太复杂

**太简单**（只有几个基础形状）：

- 在 prompt 中增加细节描述，比如 "with fine details including..."
- 提高 `max_tokens` 允许模型输出更多内容
- 明确要求复杂度："use at least 10 distinct SVG elements"

**太复杂**（元素过多，渲染慢）：

- 在 prompt 中加入约束："use no more than 20 SVG elements, keep it simple and clean"
- 指定 "minimal/flat design style"
- 降低 `max_tokens` 限制输出长度

**控制复杂度的 prompt 模板**：

```
Generate an SVG [type] with approximately [N] elements.
Style: [simple/moderate/detailed].
Complexity: [icon-level / illustration-level / infographic-level].
```

### Q3: 模型部署显存不够怎么办

**确认当前显存**：

```bash
# NVIDIA GPU
nvidia-smi

# 华为昇腾 Atlas 800T A2
npu-smi info
```

**各显存级别的推荐方案**：

| 可用显存 | 推荐方案 | 预期效果 |
|---------|---------|---------|
| 40 GB+ | FP16 全精度部署 | 最佳质量 |
| 16-24 GB | INT8 量化 | 质量几乎无损 |
| 10-16 GB | INT4 量化 | 简单图形效果好，复杂图形略有下降 |
| 多张小卡（如 2x RTX 3090） | 张量并行 `--tp 2` | 等效于单张大卡 |
| 无 GPU | 使用官方在线 Demo 或云 GPU | -- |

**INT4 量化部署命令**：

```bash
lmdeploy serve api_server ./models/InternSVG-8B \
  --model-name InternSVG \
  --backend pytorch \
  --chat-template internvl2_5 \
  --server-port 23333 \
  --quant-policy 4
```

### Q4: 批量生成时部分图标风格不一致

- 确保每个 prompt 都包含完全相同的风格描述字符串（用变量复用，不要手动重写）
- 使用 `temperature=0.0` 保证确定性输出
- 在 prompt 中明确引用其他图标的特征："consistent with the same icon set, same stroke-width 2, same padding 8px"
- 如果仍不一致，考虑先生成一个"风格参考图标"，然后用图片输入的方式让模型参考

### Q5: 在华为昇腾 Atlas 800T A2 上部署

InternSVG 基于 InternVL3-8B 架构，支持在华为昇腾 Atlas 800T A2 上通过 torch_npu 运行。部署流程与 NVIDIA GPU 基本一致，需要额外配置昇腾环境：

```bash
# 配置昇腾运行环境
export LD_LIBRARY_PATH=/usr/local/Ascend/driver/lib64:$LD_LIBRARY_PATH
source /usr/local/Ascend/ascend-toolkit/set_env.sh

# 验证 NPU 可用
python -c "import torch; import torch_npu; print(torch.npu.is_available())"

# 后续部署步骤与 NVIDIA GPU 相同
lmdeploy serve api_server ./models/InternSVG-8B \
  --model-name InternSVG \
  --backend pytorch \
  --chat-template internvl2_5 \
  --server-port 23333
```

---

## 课程回顾与拓展方向

**本课程完成的内容**：

1. 理解了 SVG 矢量图形的基础知识和优势
2. 了解了 InternSVG 的模型架构、数据集和训练策略
3. 完成了从环境搭建到模型部署的全流程
4. 通过三个实战项目掌握了核心能力：
   - 项目一：批量生成统一风格的 App 图标
   - 项目二：从文本描述生成数据可视化图表
   - 项目三：PNG Logo 转 SVG 并生成多种配色方案
5. 学习了科学可视化场景下的 SVG 生成（分子结构、实验图表、流程图）
6. 掌握了常见问题的排查和解决方法

**拓展方向**：

- **设计系统集成**：将 InternSVG 嵌入 Figma 插件或 VS Code 扩展，实现设计工作流自动化
- **科学出版流水线**：结合 Intern-S1-Pro 的科学多模态能力，自动从论文数据生成配图
- **SVG 动画视频制作**：利用 SVG 动画能力批量生成短视频素材
- **可访问性增强**：为 SVG 图形自动添加 ARIA 标签和 `<title>`/`<desc>` 描述

---

## 参考资料

- InternSVG 论文：https://arxiv.org/abs/2510.11341
- InternSVG GitHub：https://github.com/hmwang2002/InternSVG
- InternSVG 模型权重：https://huggingface.co/InternSVG/InternSVG-8B
- SAgoge 数据集：https://huggingface.co/datasets/InternSVG/SAgoge
- LMDeploy 文档：https://lmdeploy.readthedocs.io/
- SVG 规范：https://developer.mozilla.org/en-US/docs/Web/SVG
- ColorBrewer 科学配色：https://colorbrewer2.org/
