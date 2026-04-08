
# InternVL 书生·万象

InternVL 是书生系列的多模态大模型产品线，支持图像理解、视频理解、文档分析等视觉语言任务。InternVL3 在 10 亿至 780 亿全量级上均为开源第一。

## 模型系列

| 模型 | 发布时间 | 参数量 | 亮点 |
|------|---------|--------|------|
| **InternVL3** | 2025.04 | 1B-78B | 全量级开源第一，GUI 智能体，空间推理 |
| **InternVL2.5** | 2024.12 | 1B-78B | MathVista 76.5%，OCRBench 907 |
| **InternVL2** | 2024.07 | 1B-78B | 图像/视频/文字/语音/3D 点云 |
| **InternVL1.5** | 2024.06 | 6B | 动态高分辨率，比肩 GPT-4V |

## 快速体验

```python
import torch
from transformers import AutoModel, AutoTokenizer

model = AutoModel.from_pretrained(
    "OpenGVLab/InternVL3-8B",
    torch_dtype=torch.bfloat16,
    trust_remote_code=True
).cuda()
tokenizer = AutoTokenizer.from_pretrained(
    "OpenGVLab/InternVL3-8B",
    trust_remote_code=True
)

# 图片理解
response = model.chat(tokenizer, pixel_values, "描述这张图片", history=[])
print(response)
```

## 相关资源

- [GitHub 仓库](https://github.com/OpenGVLab/InternVL)
- [HuggingFace 模型](https://huggingface.co/OpenGVLab)
- [API 调用指南](/docs/api/models/internvl3)
