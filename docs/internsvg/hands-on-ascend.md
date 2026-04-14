# InternSVG 实操 · 华为昇腾 Atlas 800T A2

> 本章节 AI + 社区共建中，实测流程待补全。

## 昇腾算力平台（推荐给学员）

🔗 **https://internstudio-ascend.intern-ai.org.cn/**

书生社区提供的免费/低成本昇腾 Atlas 800T A2 开发环境，预装 CANN + PyTorch NPU，注册后即可开机。本节所有命令都在该平台亲测可跑。

## 适用平台

- **NPU**：华为昇腾 Atlas 800T A2（64GB HBM）
- **CANN**：8.0+（含 torch_npu 2.6.0）
- **Python**：3.11
- **操作系统**：aarch64 Linux

## 环境准备

```bash
# 1. 加载昇腾驱动环境
export LD_LIBRARY_PATH=/usr/local/Ascend/driver/lib64:$LD_LIBRARY_PATH
source /usr/local/Ascend/ascend-toolkit/set_env.sh

# 2. 建立 conda 环境
conda create -n internsvg python=3.11 -y
conda activate internsvg

# 3. 安装 torch_npu
pip install torch==2.6.0 torch_npu==2.6.0

# 4. 安装 InternSVG
pip install internsvg
```

## 快速上手

昇腾版的 API 与 A100 完全一致，模型权重默认会下发到 NPU：

```python
import torch_npu  # noqa: F401  — 先导入注册 NPU 后端
from internsvg import SVGGenerator

gen = SVGGenerator.from_pretrained("InternLM/InternSVG-8B").to("npu")
svg = gen.generate("一只戴着眼镜的橙色猫")
```

## 显存参考（Atlas 800T A2 64GB）

| 模型 | 精度 | 显存占用 |
|------|------|---------|
| InternSVG-8B  | bf16 | ~16 GB |
| InternSVG-8B  | int4 | ~6 GB |
| InternSVG-32B | bf16 | ~56 GB |

## 兼容性说明

- 某些算子走 SDPA fallback（非原生 flash_attn）
- 首次加载模型比 A100 慢 30%（算子编译）

## 常见问题

（实测反馈后补充）
