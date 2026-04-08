

> 本文档 AI + 社区共建中
# 文生图：AI 图像生成基础

用一句话描述就能生成一张图片——这是 AI 图像生成（Text-to-Image）的核心能力。本教程带你从原理到实战，系统掌握文生图技术。

## 什么是文生图？

**文生图（Text-to-Image Generation）** 是指输入一段文本描述（Prompt），由 AI 模型生成对应图像的技术。

```
输入: "一只穿着宇航服的猫咪在太空中漫步，背景是星云"
输出: [生成的图像]
```

### 主流技术路线

| 方案 | 代表模型 | 核心思路 |
|------|----------|----------|
| **扩散模型 (Diffusion)** | Stable Diffusion, DALL-E 3, Midjourney | 从噪声逐步"去噪"生成图像 |
| **自回归模型 (AR)** | Parti, CM3Leon | 像写文字一样逐 Token 生成图像 |
| **统一多模态模型 (UMM)** | InternVL-U, Chameleon | 理解 + 生成在一个模型里 |

## 扩散模型核心原理

扩散模型是当前最主流的图像生成技术，分两个阶段：

### 前向过程（加噪）

将一张清晰图片逐步添加高斯噪声，直到变成纯噪声：

```
清晰图片 → 轻微噪声 → 更多噪声 → ... → 纯随机噪声
```

### 反向过程（去噪）

从纯噪声出发，模型学习如何一步步去除噪声，恢复出清晰图片：

```
纯随机噪声 → 模糊轮廓 → 逐渐清晰 → ... → 生成图片
```

关键洞察：模型学习的是"给定噪声图片，预测该去除多少噪声"。加上文本条件（Prompt），模型就能朝着目标描述去噪——这就是**文本引导的图像生成**。

### 关键组件

| 组件 | 作用 | 示例 |
|------|------|------|
| **Text Encoder** | 将 Prompt 编码为向量 | CLIP, T5 |
| **UNet / DiT** | 预测噪声（核心网络） | UNet-2D, DiT (Diffusion Transformer) |
| **VAE** | 图像压缩/解压（降低计算量） | KL-VAE |
| **Scheduler** | 控制去噪步骤 | DDPM, DPM-Solver |

## Prompt 写作技巧

好的 Prompt 是高质量生图的关键。

### 基本结构

```
[主体] + [动作/姿态] + [风格] + [光影] + [背景] + [质量词]
```

### 示例对比

| Prompt | 质量 |
|--------|------|
| "一只猫" | 模糊，无细节 |
| "一只橘色短毛猫坐在窗台上，阳光照射，背景是绿色花园，高清摄影" | 清晰，有细节 |

### 关键要素

**1. 具体描述主体**
- "一位年轻女性" → "一位戴着圆框眼镜的亚洲女性，长发扎马尾"

**2. 指定画风**
- 写实摄影: "photo, realistic, 8K"
- 油画: "oil painting, impressionism"
- 水彩: "watercolor, soft edges"
- 水墨画: "Chinese ink painting, traditional"
- 赛博朋克: "cyberpunk, neon lights, dark city"
- 像素风: "pixel art, retro game style"
- 扁平插画: "flat illustration, vector style"

**3. 光影与氛围**
- "golden hour lighting"（黄金时段）
- "dramatic shadows"（戏剧性阴影）
- "soft diffused light"（柔和散射光）
- "studio lighting"（影棚灯光）

**4. 构图与视角**
- "close-up portrait"（特写肖像）
- "bird's eye view"（鸟瞰）
- "wide angle landscape"（广角风景）
- "symmetrical composition"（对称构图）

**5. 质量提升词**
- "high resolution, 4K, detailed"
- "masterpiece, best quality"

### 负面提示（Negative Prompt）

告诉模型不要生成什么：

```
negative: "blur, distortion, bad anatomy, extra fingers, low quality"
```

## 分辨率选择

| 分辨率 | 适用场景 | 生成速度 |
|--------|----------|----------|
| 256x256 | 快速预览 | 最快 |
| 512x512 | 通用推荐（速度与质量平衡） | 快 |
| 768x768 | 高质量输出 | 中等 |
| 1024x1024 | 精细创作 | 较慢 |

> InternVL-U Playground 支持 256~1024 分辨率，推荐 512x512 作为起点。

## 推理增强（Chain-of-Thought）

开启推理增强（CoT）后，模型会先分析 Prompt 的语义、构图和风格要求，再进行图像生成。这对于复杂场景特别有效：

```
Prompt: "一个机器人在图书馆里阅读，周围堆满了书，暖色灯光"

[推理过程]
- 主体：人形机器人，金属质感
- 场景：传统木质图书馆
- 构图：中景，机器人居中
- 光影：暖色台灯，柔和阴影
- 风格：写实与科幻结合

[生成结果] → 质量更高的图像
```

## InternVL-U 的文生图能力

InternVL-U 是书生团队开发的统一多模态模型（4B 参数），在**一个模型**内同时支持：

- 文本理解与对话
- 图像理解与分析
- **文生图（Text-to-Image）**
- **图片编辑（Image Editing）**

与传统扩散模型不同，InternVL-U 采用"理解 + 生成"统一架构，能更好地理解复杂 Prompt 的语义。

### 在 Playground 体验

访问 [Playground](/zh/playground) 的「文生图」Tab：

1. 输入描述文本
2. 选择分辨率（推荐 512x512）
3. 可选开启「推理增强」
4. 点击生成

## 常见问题

**Q: 为什么生成的人物手指经常有问题？**

A: 这是扩散模型的已知缺陷，因为训练数据中手指姿态变化多、细节复杂。可以在 Negative Prompt 中加入 "bad hands, extra fingers" 来缓解。

**Q: 同样的 Prompt 每次生成结果不同？**

A: 正常现象。扩散模型从随机噪声开始，不同的随机种子（seed）会产生不同结果。固定 seed 可以复现结果。

**Q: 推理增强会消耗更多配额吗？**

A: 推理增强只是让模型多一步"思考"，不会额外消耗配额。但生成时间会稍长。

## 延伸阅读

- [图片编辑：AI 编辑图像基础](/zh/docs/learn/image-editing) — 在已有图片上做修改
- [文生视频：AI 视频生成基础](/zh/docs/learn/text-to-video) — 从文字生成视频
- [视觉语言模型 (VLM)](/zh/docs/learn/vlm) — 理解图像的 AI 模型
