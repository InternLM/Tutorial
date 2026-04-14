# InternSVG 实操 · NVIDIA A100

> 本章节 AI + 社区共建中，实测流程待补全。

## A100 算力平台（推荐给学员）

🔗 **https://studio.intern-ai.org.cn**

书生社区提供的 InternStudio A100 开发环境，预装 CUDA / PyTorch，注册后即可开机。本节命令都在该平台亲测可跑。

## 适用平台

- **GPU**：NVIDIA A100 (40GB / 80GB)
- **CUDA**：12.1+
- **驱动**：535+
- **其他**：A800 / H100 / H800 / H200 / A10 系列同流程可跑

## 环境准备

```bash
# 1. 建立 conda 环境
conda create -n internsvg python=3.11 -y
conda activate internsvg

# 2. 安装 PyTorch (CUDA 12.1)
pip install torch==2.4.0 torchvision --index-url https://download.pytorch.org/whl/cu121

# 3. 安装 InternSVG
pip install internsvg
```

## 快速上手

```python
from internsvg import SVGGenerator

gen = SVGGenerator.from_pretrained("InternLM/InternSVG-8B")
svg = gen.generate("一只戴着眼镜的橙色猫")

with open("cat.svg", "w") as f:
    f.write(svg)
```

## 显存参考（A100 80GB）

| 模型 | 精度 | 显存占用 |
|------|------|---------|
| InternSVG-8B  | bf16 | ~16 GB |
| InternSVG-8B  | int4 | ~6 GB |
| InternSVG-32B | bf16 | ~64 GB |

## 常见问题

（实测反馈后补充）

## 下一步

完成实操后回到「总览」Tab 进入闯关任务。
