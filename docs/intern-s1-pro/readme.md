# Intern-S1-Pro 科学大模型

## 课程简介

Intern-S1-Pro 是书生生态的主力科学多模态大模型，总参数量达万亿级别（1T MoE，512 个专家），每个 token 激活 22B 参数。它在数学、物理、化学、代码等科学推理任务上达到了国际顶尖水平，同时保持了出色的通用对话能力。

本课程将介绍 Intern-S1-Pro 的技术架构和能力定位，带你通过 API 调用进行科学推理实战，并学习使用深度思考模式和 Harness 评测框架。

## 你将学到

- 书生模型家族的定位与 Intern-S1-Pro 的核心优势
- 通过 Python OpenAI SDK 接入 Intern-S1-Pro API
- 在数学、物理、化学、代码等领域进行科学推理
- 深度思考模式的原理与使用方法
- 使用 lm-evaluation-harness 框架评测模型能力

## 第 1 节：书生模型家族与 Intern-S1-Pro 定位

### 目标

理解书生模型家族的产品矩阵，明确 Intern-S1-Pro 的定位。

### 内容

**书生生态产品矩阵**

| 产品 | 定位 | 说明 |
|------|------|------|
| Intern-S1 / Intern-S1-Pro | 科学多模态大模型 | 书生主力模型，专精科学推理 |
| InternVL 系列 | 开源视觉语言模型 | 多模态理解与生成 |
| InternLM 系列 | 高性能语言大模型 | 通用对话与工具调用 |
| LMDeploy | 推理部署工具 | 高效推理与量化 |
| XTuner | 微调工具 | 高效参数微调 |

注意：Intern-S1 和 Intern-S1-Pro 是科学多模态大模型，不是推理模型。它们的核心优势在于科学领域的深度理解和精确计算。

**Intern-S1-Pro 架构**

- **语言模型基座**：基于 Qwen3 架构的 235B MoE 模型，512 个专家，每个 token 激活 8 个专家（22B 参数）
- **视觉编码器**：InternViT-6B，支持图像、化学结构式、蛋白质序列等多模态输入
- **总参数量**：约 1T（万亿级）
- **训练数据**：5 万亿 token 多模态数据，其中超过 2.5 万亿为科学领域数据

**核心技术创新**

- **STE Routing**：在路由器训练中使用稠密梯度，确保万亿规模模型稳定收敛
- **Grouped Routing**：分组路由策略，平衡专家并行负载
- **Fourier Position Encoding（FoPE）**：傅里叶位置编码，增强对物理信号和时间序列的建模能力
- **动态分词器**：针对分子式、蛋白质序列、地震波信号等科学数据的专用分词策略

**模型家族**

| 模型 | 参数量 | 说明 |
|------|--------|------|
| Intern-S1-Pro | ~1T (MoE) | 旗舰模型，科学推理能力最强 |
| Intern-S1 | ~235B (MoE) | 标准版，性能与成本平衡 |
| Intern-S1-mini | ~8B | 轻量版，适合端侧部署 |

## 第 2 节：API 接入

### 目标

学会通过 Python OpenAI SDK 调用 Intern-S1-Pro 的在线 API。

### 内容

**获取 API Key**

1. 访问 https://internlm.intern-ai.org.cn
2. 注册并登录账号
3. 在 API 页面创建 API Key

**Python OpenAI SDK 调用**

Intern-S1-Pro 的 API 兼容 OpenAI 接口协议，可以直接使用 OpenAI Python SDK 调用。

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",  # 替换为你的 API Key
    base_url="https://chat.intern-ai.org.cn/api/v1/",
)

response = client.chat.completions.create(
    model="internlm3-latest",
    messages=[
        {"role": "system", "content": "You are a helpful scientific assistant."},
        {"role": "user", "content": "请解释为什么水的比热容比大多数液体都大？"},
    ],
    temperature=0.7,
    max_tokens=2048,
)

print(response.choices[0].message.content)
```

**查看可用模型**

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://chat.intern-ai.org.cn/api/v1/",
)

models = client.models.list()
for model in models.data:
    print(model.id)
```

**cURL 调用**

```bash
curl https://chat.intern-ai.org.cn/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "model": "internlm3-latest",
    "messages": [
      {"role": "user", "content": "证明根号 2 是无理数"}
    ],
    "temperature": 0.7,
    "max_tokens": 2048
  }'
```

## 第 3 节：科学推理实战

### 目标

通过实际案例体验 Intern-S1-Pro 在数学、物理、化学和代码领域的科学推理能力。

### 内容

**数学推理**

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://chat.intern-ai.org.cn/api/v1/",
)

# 竞赛级数学题
math_problem = """
设 f(x) 是定义在 R 上的连续函数，满足：
f(x+y) = f(x) + f(y) + 2xy，对任意实数 x, y 成立。
且 f'(0) = 1。
求 f(x) 的表达式。
"""

response = client.chat.completions.create(
    model="internlm3-latest",
    messages=[{"role": "user", "content": math_problem}],
    temperature=0.1,
    max_tokens=4096,
)

print(response.choices[0].message.content)
```

**物理推理**

```python
physics_problem = """
一个质量为 m 的均匀圆盘，半径为 R，绕过圆心的竖直轴以角速度 omega 旋转。
圆盘上方 h 处有一个质量为 m0 的小球自由下落到圆盘边缘，并与圆盘发生完全非弹性碰撞。
求碰撞后系统的角速度。
"""

response = client.chat.completions.create(
    model="internlm3-latest",
    messages=[{"role": "user", "content": physics_problem}],
    temperature=0.1,
    max_tokens=4096,
)

print(response.choices[0].message.content)
```

**化学推理**

```python
chemistry_problem = """
请设计一条从苯出发合成对硝基苯甲酸的合成路线。
要求：
1. 列出每一步的反应物、试剂和条件
2. 解释每一步的反应类型
3. 说明为什么选择这个顺序（涉及基团的定位效应）
"""

response = client.chat.completions.create(
    model="internlm3-latest",
    messages=[{"role": "user", "content": chemistry_problem}],
    temperature=0.1,
    max_tokens=4096,
)

print(response.choices[0].message.content)
```

**代码生成**

```python
code_problem = """
用 Python 实现一个高效的 Trie（字典树）数据结构，支持以下操作：
1. insert(word) -- 插入一个单词
2. search(word) -- 精确查找一个单词是否存在
3. starts_with(prefix) -- 查找是否存在以给定前缀开头的单词
4. count_prefix(prefix) -- 统计以给定前缀开头的单词数量
5. delete(word) -- 删除一个单词

请写完整的实现代码和测试用例。
"""

response = client.chat.completions.create(
    model="internlm3-latest",
    messages=[{"role": "user", "content": code_problem}],
    temperature=0.1,
    max_tokens=4096,
)

print(response.choices[0].message.content)
```

## 第 4 节：深度思考模式

### 目标

掌握深度思考（Thinking）模式的使用方法，理解其与普通模式的区别。

### 内容

**什么是深度思考模式？**

Intern-S1-Pro 默认开启深度思考模式。在该模式下，模型会在正式回答之前进行内部推理（类似 "chain-of-thought"），自动分解复杂问题、验证中间步骤，从而生成更高质量的回答。

深度思考模式特别适合：
- 多步数学证明
- 复杂物理问题求解
- 需要严格逻辑推导的科学问题
- 代码算法设计

**对比普通模式与深度思考模式**

普通模式（关闭深度思考）：

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://chat.intern-ai.org.cn/api/v1/",
)

# 关闭深度思考
response_normal = client.chat.completions.create(
    model="internlm3-latest",
    messages=[
        {"role": "user", "content": "求不定积分 integral of x^2 * e^x dx"}
    ],
    temperature=0.1,
    max_tokens=4096,
    extra_body={
        "chat_template_kwargs": {"enable_thinking": False}
    },
)

print("=== 普通模式 ===")
print(response_normal.choices[0].message.content)
```

深度思考模式（默认开启）：

```python
# 开启深度思考（默认行为，也可以显式指定）
response_thinking = client.chat.completions.create(
    model="internlm3-latest",
    messages=[
        {"role": "user", "content": "求不定积分 integral of x^2 * e^x dx"}
    ],
    temperature=0.1,
    max_tokens=4096,
    extra_body={
        "chat_template_kwargs": {"enable_thinking": True}
    },
)

print("=== 深度思考模式 ===")
print(response_thinking.choices[0].message.content)
```

**完整对比脚本**

以下脚本会用同一个问题分别测试两种模式，并对比结果：

```python
import time
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://chat.intern-ai.org.cn/api/v1/",
)

question = "证明：对于任意正整数 n，n^3 - n 能被 6 整除。"

results = {}
for mode_name, enable_thinking in [("normal", False), ("thinking", True)]:
    start = time.time()
    response = client.chat.completions.create(
        model="internlm3-latest",
        messages=[{"role": "user", "content": question}],
        temperature=0.1,
        max_tokens=4096,
        extra_body={
            "chat_template_kwargs": {"enable_thinking": enable_thinking}
        },
    )
    elapsed = time.time() - start
    content = response.choices[0].message.content
    results[mode_name] = {"time": elapsed, "content": content}

print(f"Question: {question}\n")
for mode_name, result in results.items():
    print(f"=== {mode_name} mode ({result['time']:.1f}s) ===")
    print(result["content"])
    print()
```

**何时使用深度思考模式**

| 场景 | 推荐模式 |
|------|---------|
| 数学证明、竞赛题 | 深度思考 |
| 复杂科学推理 | 深度思考 |
| 日常对话、简单问答 | 普通模式（更快） |
| 文本摘要、翻译 | 普通模式 |
| 代码调试、算法设计 | 深度思考 |

深度思考模式会增加响应时间，但对于需要精确推理的任务，质量提升是显著的。

## 第 5 节：Harness 评测框架

### 目标

学会使用 lm-evaluation-harness 框架评测模型在标准基准上的表现。

### 内容

**lm-evaluation-harness 简介**

lm-evaluation-harness（简称 lm_eval）是由 EleutherAI 开发的大语言模型评测框架，支持数百个标准基准任务。它是学术界和工业界最广泛使用的评测工具之一。

**安装**

```bash
pip install lm_eval
```

**评测本地部署的模型**

如果你已通过 LMDeploy 部署了 API 服务（参见 LMDeploy 课程），可以直接对接评测：

```bash
# 确保 LMDeploy API 服务已在 localhost:23333 运行

lm_eval --model local-completions \
  --model_args model=internlm3-8b-instruct,base_url=http://localhost:23333/v1,tokenizer_backend=huggingface \
  --tasks gsm8k \
  --batch_size auto \
  --output_path ./eval_results/
```

**常用评测任务**

| 任务名 | 评测内容 | 说明 |
|--------|---------|------|
| `gsm8k` | 小学数学 | 8.5K 道数学应用题 |
| `mmlu` | 综合知识 | 57 个学科的多选题 |
| `humaneval` | 代码生成 | 164 道编程题 |
| `math` | 竞赛数学 | 高中及竞赛级数学 |
| `winogrande` | 常识推理 | 代词消歧任务 |

**评测多个任务**

```bash
lm_eval --model local-completions \
  --model_args model=internlm3-8b-instruct,base_url=http://localhost:23333/v1,tokenizer_backend=huggingface \
  --tasks gsm8k,mmlu,winogrande \
  --batch_size auto \
  --output_path ./eval_results/
```

**查看评测结果**

评测完成后，结果保存在 `--output_path` 指定的目录中，包含 JSON 格式的详细报告。你可以查看每个任务的准确率、样本级别的详细结果等。

```python
import json

with open("./eval_results/results.json", "r") as f:
    results = json.load(f)

for task, metrics in results["results"].items():
    print(f"{task}: {metrics}")
```

## 第 6 节：自行部署 Intern-S1

### 目标

了解如何在自有服务器上部署 Intern-S1 系列模型。

### 内容

除了使用在线 API，Intern-S1 系列的开源权重也支持本地部署。

**模型权重下载**

所有模型权重均托管在 HuggingFace 和 ModelScope：

```bash
# HuggingFace（国内建议使用镜像）
export HF_ENDPOINT=https://hf-mirror.com
huggingface-cli download internlm/Intern-S1 --local-dir ./models/Intern-S1
```

**使用 LMDeploy 部署**

```bash
# 部署 Intern-S1-mini（8B，单卡即可）
lmdeploy serve api_server internlm/Intern-S1-mini \
  --server-port 23333

# 部署 Intern-S1（235B MoE，需要多卡）
lmdeploy serve api_server internlm/Intern-S1 \
  --tp 8 \
  --server-port 23333
```

**使用 vLLM 部署**

```bash
vllm serve internlm/Intern-S1-mini --port 23333
```

**使用 SGLang 部署**

```bash
python -m sglang.launch_server --model-path internlm/Intern-S1-mini --port 23333
```

部署完成后，使用方式与在线 API 完全一致，只需将 `base_url` 改为本地地址即可。

## 参考资料

- Intern-S1 GitHub：https://github.com/InternLM/Intern-S1
- Intern-S1-Pro 论文：https://arxiv.org/abs/2603.25040
- Intern-S1 论文：https://arxiv.org/abs/2508.15763
- Intern-S1-Pro 模型权重：https://huggingface.co/internlm/Intern-S1-Pro
- 书生平台 API 文档：https://internlm.intern-ai.org.cn/api/document
- lm-evaluation-harness：https://github.com/EleutherAI/lm-evaluation-harness
- LMDeploy 文档：https://lmdeploy.readthedocs.io/
