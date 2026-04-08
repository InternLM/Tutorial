

> 本文档 AI + 社区共建中
# 视觉语言模型 (VLM)

视觉语言模型（Vision-Language Model，VLM）是能够同时理解**图像和文本**的 AI 模型。它不仅能看图说话，还能根据图片回答问题、理解文档、甚至分析视频。

## 直觉理解

普通的 LLM 只能"读"文字，就像一个只有耳朵没有眼睛的人。VLM 给模型装上了"眼睛"——它先用视觉编码器"看"图片，然后把视觉信息翻译成语言模型能理解的格式，最后由 LLM "大脑"综合理解并生成回答。

```
普通 LLM:  文本 → [LLM] → 回答
VLM:      图片 → [视觉编码器] → 视觉 Token
          文本 → [文本编码器] → 文本 Token
          [视觉 Token + 文本 Token] → [LLM] → 回答
```

## 核心架构

### 三大组件

| 组件 | 功能 | 常见选择 |
|------|------|---------|
| Vision Encoder | 将图片编码为视觉特征 | ViT、InternViT、SigLIP |
| Projection Layer | 将视觉特征映射到语言空间 | MLP、Cross-Attention |
| LLM Backbone | 理解多模态信息并生成回答 | InternLM3、LLaMA、Qwen |

### 图文对齐

VLM 的关键挑战是让视觉和语言在同一个"空间"中对齐。主流方案：

```
图片 [768 维特征] → Projection → [4096 维特征] → 与文本 Token 拼接 → LLM
```

- **InternVL3** 使用 Dynamic Resolution 策略：将图片分割成多个子图，每个子图独立编码后拼接，支持任意分辨率输入
- 这避免了固定分辨率带来的信息损失，尤其对文档和细粒度图片理解很有帮助

### InternVL3 架构

```
InternVL3 架构:
├── InternViT-6B          # 60 亿参数视觉编码器
├── MLP Projection         # 视觉-语言投影层
└── InternLM3-8B          # 80 亿参数语言模型
    总参数: ~140 亿
```

InternVL3 的训练分为三个阶段：

| 阶段 | 目标 | 数据 |
|------|------|------|
| 视觉预训练 | 学习图像特征表示 | 大规模图文对数据 |
| 对齐训练 | 视觉特征与语言空间对齐 | 图文对 + 指令数据 |
| 指令微调 | 多任务能力提升 | 多模态指令数据 |

## VLM 能做什么

```python
from transformers import AutoModel, AutoTokenizer
import torch
from PIL import Image

# 加载 InternVL3
model = AutoModel.from_pretrained(
    "OpenGVLab/InternVL3-8B",
    torch_dtype=torch.bfloat16,
    trust_remote_code=True
).cuda()
tokenizer = AutoTokenizer.from_pretrained(
    "OpenGVLab/InternVL3-8B", trust_remote_code=True
)

image = Image.open("example.jpg")

# 图片问答
response = model.chat(tokenizer, image, "图片里有什么？")
print(response)
```

典型应用场景：

| 场景 | 输入 | 输出示例 |
|------|------|---------|
| 图片问答 | 图片 + 问题 | 描述图片内容、回答具体问题 |
| 文档理解 | PDF/表格截图 | 提取文字、理解表格数据 |
| OCR 增强 | 含文字图片 | 识别并理解文字含义 |
| 视频理解 | 视频帧序列 | 总结视频内容、回答时序问题 |
| 图表分析 | 统计图表 | 读取数据、分析趋势 |

## 书生生态中的应用

书生在多模态领域的布局：

- **InternVL3**：最新一代视觉语言模型，在 OCRBench、MathVista 等多个评测中达到开源 SOTA
- **InternViT**：强大的视觉编码器，可独立用于图像理解任务
- **XComposer**：专注图文创作的多模态模型，支持生成长文配图
- **LMDeploy**：支持 InternVL 系列模型的高效推理部署

## 下一步

理解了 VLM 之后，推荐继续学习：

- [Transformer 架构](/docs/learn/transformer) — VLM 的底层技术基础
- [注意力机制详解](/docs/learn/attention-mechanism) — 理解视觉和语言如何通过注意力交互
- [什么是大语言模型](/docs/learn/what-is-llm) — 回顾 LLM 基础

## 进阶实践（Intern-S1-Pro 专题）

### 实战任务
1. 选 20 张图（图表、公式、截图）做图文问答测试并记录错误类型。
2. 设计一个多模态任务链路：图片理解 + 文本推理 + 结构化输出。
3. 对比不同输入分辨率下的推理质量与延迟表现。

### 交付物
- 一份《VLM 评测样例集》
- 一份《多模态任务误差分析报告》

### 自检清单
- [ ] 能解释视觉编码器与语言模型协作机制
- [ ] 能识别 OCR 类与推理类任务的边界
- [ ] 能设计适合科学场景的图文提示模板
