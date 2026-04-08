
# InternVL3 多模态模型

InternVL3（书生·万象 3.0）是通用多模态大模型，10 亿至 780 亿全量级开源第一，支持图像理解、文档分析、GUI 智能体等多种视觉任务。

## 可用模型

| 模型 ID | 参数量 | 上下文长度 | 说明 |
|--------|--------|-----------|------|
| `internvl-latest` | 8B | 32K | 轻量多模态，适合快速部署 |
| `internvl-latest` | 78B | 32K | 旗舰多模态，最强性能 |

## 特性

- **全量级第一**：从 1B 到 78B 全面领先开源模型
- **GUI 智能体**：理解屏幕截图并执行操作指令
- **文档理解**：解析 PDF、表格、图表等复杂文档
- **空间推理**：3D 空间关系理解能力大幅提升

## 调用示例

### 图片理解

```python
import base64

# 读取本地图片
with open("image.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

response = client.chat.completions.create(
    model="internvl-latest",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_data}"
                    }
                },
                {
                    "type": "text",
                    "text": "请描述这张图片的内容"
                }
            ]
        }
    ],
    max_tokens=1024
)

print(response.choices[0].message.content)
```

### URL 图片

```python
response = client.chat.completions.create(
    model="internvl-latest",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://example.com/chart.png"
                    }
                },
                {
                    "type": "text",
                    "text": "请分析这张图表的数据趋势"
                }
            ]
        }
    ]
)
```

## 请求参数

与 InternLM3 基础参数相同，额外支持：

| 参数 | 类型 | 说明 |
|------|------|------|
| `messages[].content[].type` | string | `text` 或 `image_url` |
| `messages[].content[].image_url.url` | string | 图片 URL 或 base64 编码 |

> **提示：** 单次请求最多支持 5 张图片，图片总大小不超过 20MB。
