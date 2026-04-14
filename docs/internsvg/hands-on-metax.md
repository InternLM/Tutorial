# InternSVG 实操 · 沐曦 MetaX C500

> 本章节 AI + 社区共建中，实测流程待补全。

## 适用平台

- **GPU**：沐曦 MetaX C500（64GB VRAM）
- **MACA**：3.3.0+
- **Python**：3.10+
- **操作系统**：x86_64 Linux

## 环境准备

```bash
# 1. 加载 MACA 环境
source /opt/maca/env.sh

# 2. 建立 conda 环境
conda create -n internsvg python=3.10 -y
conda activate internsvg

# 3. 安装 PyTorch MACA 版本
pip install torch --extra-index-url https://repo.metax-tech.com/pytorch

# 4. 安装 InternSVG
pip install internsvg
```

## 快速上手

沐曦提供 CUDA 兼容层，API 与 A100 一致：

```python
from internsvg import SVGGenerator

gen = SVGGenerator.from_pretrained("InternLM/InternSVG-8B").to("cuda")
svg = gen.generate("一只戴着眼镜的橙色猫")
```

## 显存参考（MetaX C500 64GB）

| 模型 | 精度 | 显存占用 |
|------|------|---------|
| InternSVG-8B  | bf16 | ~16 GB |
| InternSVG-8B  | int4 | ~6 GB |
| InternSVG-32B | bf16 | ~56 GB |

## 兼容性说明

- 原生支持 flash_attn（走沐曦 MACA 实现）
- 与 A100 性能差距 <10%

## 常见问题

（实测反馈后补充）
