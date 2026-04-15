# Intern-S1-Pro 科学大模型

> 本文档 AI + 社区共建中

## 先看效果：Intern-S1-Pro 能做什么

在讲架构和 API 之前，先看三个真实场景，感受一下 Intern-S1-Pro 的科学推理能力。

### IMO 竞赛题求解

以下是 2024 年 IMO 预选题的一个变体。直接把题目扔给 Intern-S1-Pro，看它如何拆解：

**题目**：设正整数 a, b, c 满足 gcd(a, b) = gcd(b, c) = gcd(c, a) = 1，且 a^2 + b^2 + c^2 能被 (ab + bc + ca) 整除。证明：a + b + c 是完全平方数。

Intern-S1-Pro 的回答会包含：
- 从特殊到一般的分析策略（先尝试小值找规律）
- 模运算分析（分别对 a、b、c 取模）
- 二次剩余的判定
- 严格的分情况讨论和最终证明

这类问题需要模型同时具备"直觉猜测"和"严格论证"两种能力，是检验科学推理水平的试金石。

### 复杂代码生成

给 Intern-S1-Pro 一个真实的工程需求：

**Prompt**：实现一个支持并发安全的 LRU Cache，要求支持 TTL 过期、容量驱逐、命中率统计，用 Python 实现，附带完整测试。

模型不只会给出数据结构实现，还会主动考虑：
- 线程安全（使用 threading.Lock）
- 过期清理策略（惰性删除 + 主动清理）
- 性能优化（OrderedDict 而非链表手写）
- 边界条件的测试覆盖

### 科学论文辅助推导

在 AGI4S（AI for Science）场景中，Intern-S1-Pro 可以辅助论文中的数学推导：

**Prompt**：在 Transformer 的自注意力机制中，证明当 Query 和 Key 的维度 d_k 趋于无穷时，softmax(QK^T / sqrt(d_k)) 趋近于均匀分布，并分析 sqrt(d_k) 缩放因子的必要性。

模型会给出：
- 中心极限定理在高维点积中的应用
- softmax 温度参数与概率分布集中度的关系
- 梯度消失问题的定量分析
- 与原始 Attention Is All You Need 论文的对照

这三个例子涵盖了竞赛数学、工程代码、科学推导三个维度。下面我们正式开始学习如何使用 Intern-S1-Pro。

---

## 课程简介

Intern-S1-Pro 是书生生态的主力科学多模态大模型，总参数量达万亿级别（1T MoE，512 个专家），每个 token 激活 22B 参数。它在数学、物理、化学、代码等科学推理任务上达到了国际顶尖水平，同时保持了出色的通用对话能力。

注意：Intern-S1-Pro 是科学多模态大模型，不是推理模型（reasoning model）。它的核心优势在于对科学领域的深度理解和精确计算，而非单纯的推理链生成。

本课程将带你完成以下学习路径：

1. 理解 Intern-S1-Pro 在书生模型家族中的定位
2. 从零接入 API，写出可直接运行的代码
3. 在数学、物理、化学、代码四个领域进行科学推理实战
4. 了解模型的深度分析能力及使用技巧
5. 学会用 Harness 评测框架量化模型能力

## 你将学到

- 书生模型家族的定位与 Intern-S1-Pro 的核心优势
- 通过 Python OpenAI SDK 接入 Intern-S1-Pro API（含完整可运行代码）
- 在数学、物理、化学、代码等领域进行科学推理
- 深度分析能力的使用技巧
- 使用 lm-evaluation-harness 框架评测模型能力
- 常见问题排查与最佳实践

---

## 书生模型家族与 Intern-S1-Pro 定位

### 目标

理解书生模型家族的产品矩阵，明确 Intern-S1-Pro 的定位和技术架构。

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

- **语言模型基座**：**万亿参数（~1T）MoE 架构**，每个 token 激活稀疏专家子集
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

---

## API 接入

### 目标

从零开始接入 Intern-S1-Pro API，写出可以复制粘贴直接运行的代码。

### 前置准备

**1. 获取 API Token**

1. 访问 https://internlm.intern-ai.org.cn/api/tokens
2. 登录（首次需要注册）
3. 点击「创建 Token」
4. 复制 Token 并妥善保存（只显示一次）

**2. 安装依赖**

```bash
pip install openai
```

**3. 配置环境变量**

推荐使用环境变量管理 API Key，避免硬编码在代码中：

```bash
# Linux / macOS
export INTERN_API_KEY="your-api-key-here"

# Windows PowerShell
$env:INTERN_API_KEY="your-api-key-here"

# 写入 .env 文件（推荐）
echo 'INTERN_API_KEY=your-api-key-here' >> ~/.bashrc
source ~/.bashrc
```

### Python SDK 调用（完整可运行代码）

Intern-S1-Pro 的 API 兼容 OpenAI 接口协议，可以直接使用 OpenAI Python SDK 调用。

```python
import os
import sys
from openai import OpenAI, APIError, APIConnectionError, RateLimitError

# 从环境变量读取 API Key
api_key = os.environ.get("INTERN_API_KEY")
if not api_key:
    print("Error: 请设置环境变量 INTERN_API_KEY")
    print("  export INTERN_API_KEY='your-api-key-here'")
    sys.exit(1)

client = OpenAI(
    api_key=api_key,
    base_url="https://chat.intern-ai.org.cn/api/v1/",
)

try:
    response = client.chat.completions.create(
        model="intern-s1-pro",
        messages=[
            {"role": "system", "content": "You are a helpful scientific assistant."},
            {"role": "user", "content": "请解释为什么水的比热容比大多数液体都大？"},
        ],
        temperature=0.7,
        max_tokens=2048,
    )
    print(response.choices[0].message.content)

except APIConnectionError:
    print("Error: 无法连接到 API 服务器，请检查网络连接")
except RateLimitError:
    print("Error: API 调用频率超限，请稍后重试")
except APIError as e:
    print(f"Error: API 返回错误 - {e.status_code}: {e.message}")
```

### 查看可用模型

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("INTERN_API_KEY"),
    base_url="https://chat.intern-ai.org.cn/api/v1/",
)

models = client.models.list()
for model in models.data:
    print(model.id)
```

### 流式输出

对于长回答，使用流式输出可以实时看到生成过程：

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("INTERN_API_KEY"),
    base_url="https://chat.intern-ai.org.cn/api/v1/",
)

stream = client.chat.completions.create(
    model="intern-s1-pro",
    messages=[
        {"role": "user", "content": "推导薛定谔方程的时间无关形式"},
    ],
    temperature=0.1,
    max_tokens=4096,
    stream=True,
)

for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="", flush=True)

print()  # 换行
```

### cURL 调用

```bash
curl https://chat.intern-ai.org.cn/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $INTERN_API_KEY" \
  -d '{
    "model": "intern-s1-pro",
    "messages": [
      {"role": "user", "content": "证明根号 2 是无理数"}
    ],
    "temperature": 0.7,
    "max_tokens": 2048
  }'
```

### 常见报错排查

| 错误信息 | 原因 | 解决方法 |
|---------|------|---------|
| `401 Unauthorized` | API Key 无效或已过期 | 重新生成 API Key |
| `429 Too Many Requests` | 调用频率超限 | 降低调用频率，或添加重试逻辑 |
| `Connection refused` | 网络不通或服务暂时不可用 | 检查网络，稍后重试 |
| `timeout` | 请求超时 | 减少 max_tokens 或简化 prompt |
| `model not found` | 模型名称错误 | 调用 models.list() 确认可用模型 |

---

## 科学推理实战

### 目标

通过实际案例深入体验 Intern-S1-Pro 在数学、物理、化学和代码领域的科学推理能力。每个领域选取有真正挑战性的题目。

### 数学推理：竞赛级不等式证明

以下题目来自数学竞赛经典题型，需要多步推理和技巧性变换：

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("INTERN_API_KEY"),
    base_url="https://chat.intern-ai.org.cn/api/v1/",
)

math_problem = """
（AMC/AIME 风格题）

设 a, b, c 为正实数且 abc = 1。证明：

  1/(a^3(b+c)) + 1/(b^3(c+a)) + 1/(c^3(a+b)) >= 3/2

要求：
1. 给出完整的证明过程
2. 指出用到了哪些经典不等式（如 AM-GM、Schur、SOS 等）
3. 说明等号成立的条件
4. 如果有多种证明方法，请给出至少两种
"""

response = client.chat.completions.create(
    model="intern-s1-pro",
    messages=[{"role": "user", "content": math_problem}],
    temperature=0.1,
    max_tokens=4096,
)

print(response.choices[0].message.content)
```

**预期输出要点**：模型应该能识别出这是一个齐次不等式，在 abc=1 的约束下可以用 Schur 不等式或 SOS（Sum of Squares）方法处理，并明确指出等号在 a=b=c=1 时成立。

### 物理推理：能量守恒与实际计算

这道题需要同时用到力学分析和定量计算：

```python
physics_problem = """
一根质量为 M、长度为 L 的均匀链条，竖直悬挂，下端刚好接触桌面。
现在释放链条，让它自由下落到桌面上。

(1) 当链条下落了距离 x 时（0 < x < L），求桌面对链条的支持力 N(x)。
    提示：需要考虑两部分力——已堆积链条的重力 + 正在着陆链条的冲击力。

(2) 求 N(x) 的最大值，并说明在什么位置取到最大值。

(3) 对 N(x) 从 0 到 L 积分，验证冲量定理是否成立。

要求给出详细的推导过程和最终数值表达式。
"""

response = client.chat.completions.create(
    model="intern-s1-pro",
    messages=[{"role": "user", "content": physics_problem}],
    temperature=0.1,
    max_tokens=4096,
)

print(response.choices[0].message.content)
```

**预期输出要点**：这是经典的"链条落桌"问题。支持力 N(x) = 3Mgx/L（重力贡献 Mgx/L + 冲击力贡献 2Mgx/L），最大值在 x=L 时取到，为 3Mg。积分验证冲量定理的过程是检验模型推导能力的关键。

### 化学推理：分子分析与反应机理

```python
chemistry_problem = """
阿司匹林（乙酰水杨酸）的合成是有机化学经典实验。请完成以下分析：

1. 写出从水杨酸和乙酸酐合成阿司匹林的反应方程式
2. 详细描述该反应的机理（亲核酰基取代），画出每一步的电子转移
3. 为什么用乙酸酐而不是乙酸？从热力学和动力学两个角度解释
4. 实验中加入磷酸作催化剂的作用是什么？写出催化机理
5. 产物中可能含有哪些杂质？如何用 FeCl3 检验产品纯度？

请用严格的化学语言回答，分子式和反应式要完整。
"""

response = client.chat.completions.create(
    model="intern-s1-pro",
    messages=[{"role": "user", "content": chemistry_problem}],
    temperature=0.1,
    max_tokens=4096,
)

print(response.choices[0].message.content)
```

**预期输出要点**：模型应当准确写出酰基取代的四面体中间体机理，解释乙酸酐 vs 乙酸的离去基团差异（乙酸根 vs 水），以及 FeCl3 与酚羟基的显色反应原理。

### 代码推理：算法设计与复杂度分析

```python
code_problem = """
设计并实现一个 Python 类 MedianFinder，支持以下操作：

1. add_num(num: int) -- 从数据流中添加一个整数
2. find_median() -> float -- 返回当前所有已添加整数的中位数

要求：
- add_num 的时间复杂度为 O(log n)
- find_median 的时间复杂度为 O(1)
- 使用对顶堆（max-heap + min-heap）实现
- 包含详细的复杂度分析
- 包含完整的测试用例，覆盖以下边界情况：
  - 只有一个元素
  - 偶数个元素
  - 大量重复元素
  - 负数和零
- 代码需要通过所有测试

请同时分析：为什么不能用排序数组？与平衡 BST 方案相比有什么优劣？
"""

response = client.chat.completions.create(
    model="intern-s1-pro",
    messages=[{"role": "user", "content": code_problem}],
    temperature=0.1,
    max_tokens=4096,
)

print(response.choices[0].message.content)
```

**预期输出要点**：模型应使用 Python 的 heapq 模块实现对顶堆，因为 heapq 只支持最小堆，所以最大堆需要存负数。复杂度分析应覆盖 add_num 的堆操作 O(log n) 和 find_median 的堆顶访问 O(1)。

### 跨学科推理：生物信息学

Intern-S1-Pro 的科学能力不仅限于传统理科，在生物信息学等交叉领域也有出色表现：

```python
bio_problem = """
一段 DNA 序列为：5'-ATGCGATCGATCGATCGATCG-3'

请完成以下分析：
1. 写出互补链（3'->5' 方向）
2. 转录为 mRNA 序列
3. 翻译为氨基酸序列（使用标准遗传密码表）
4. 如果第 7 位的 T 突变为 A，分析这是什么类型的突变？对蛋白质有什么影响？
5. 计算这段 DNA 的 GC 含量百分比和熔解温度 Tm（使用 2(A+T)+4(G+C) 公式）
"""

response = client.chat.completions.create(
    model="intern-s1-pro",
    messages=[{"role": "user", "content": bio_problem}],
    temperature=0.1,
    max_tokens=4096,
)

print(response.choices[0].message.content)
```

---

## 深度分析能力

### 目标

了解 Intern-S1-Pro 在复杂问题上的深度分析能力，掌握引导模型进行多步推理的技巧。

### 什么是深度分析能力

Intern-S1-Pro 具备深度分析（Thinking）能力。在该模式下，模型会在正式回答之前进行内部推理链（chain-of-thought），自动分解复杂问题、验证中间步骤，最终生成更高质量的回答。

关键点：深度分析是 Intern-S1-Pro 模型本身的内在能力，通过 API 参数控制开关，而非一个单独的模型。不存在 "intern-s1-pro-deep" 这样的模型 ID。

Intern-S1-Pro 在面对复杂科学问题时，能够自动进行多步分析和推导。你可以通过 prompt 引导模型进行更深入的分析（如"请深入分析""请逐步推导"），也可以尝试通过 `extra_body` 参数控制分析深度（具体参数以平台 API 文档为准）。

### 深度分析能力特别适合

- 多步数学证明和竞赛题
- 复杂物理问题的定量求解
- 需要严格逻辑推导的科学问题
- 代码算法设计与复杂度分析
- 跨学科综合推理

### 普通模式 vs 深度分析：完整对比

以下脚本用同一道题分别测试两种模式，对比回答质量和响应时间：

```python
import os
import sys
import time
from openai import OpenAI

api_key = os.environ.get("INTERN_API_KEY")
if not api_key:
    print("Error: 请设置环境变量 INTERN_API_KEY")
    sys.exit(1)

client = OpenAI(
    api_key=api_key,
    base_url="https://chat.intern-ai.org.cn/api/v1/",
)

# 选一道需要深度推理的题目
question = """
证明：对于任意正整数 n，
  1/1^2 + 1/2^2 + 1/3^2 + ... + 1/n^2 < 2 - 1/n

并讨论当 n 趋于无穷时，这个级数的极限值（巴塞尔问题）。
"""

print(f"题目：{question.strip()}")
print("=" * 60)

# 模式一：关闭深度分析
start = time.time()
response_normal = client.chat.completions.create(
    model="intern-s1-pro",
    messages=[{"role": "user", "content": question}],
    temperature=0.1,
    max_tokens=4096,
    extra_body={
        "chat_template_kwargs": {"enable_thinking": False}
    },
)
time_normal = time.time() - start

print(f"\n--- 普通模式（耗时 {time_normal:.1f}s）---")
print(response_normal.choices[0].message.content)

# 模式二：开启深度分析（默认行为）
start = time.time()
response_thinking = client.chat.completions.create(
    model="intern-s1-pro",
    messages=[{"role": "user", "content": question}],
    temperature=0.1,
    max_tokens=4096,
    extra_body={
        "chat_template_kwargs": {"enable_thinking": True}
    },
)
time_thinking = time.time() - start

print(f"\n--- 深度分析（耗时 {time_thinking:.1f}s）---")
print(response_thinking.choices[0].message.content)

# 输出对比总结
print("\n" + "=" * 60)
print(f"普通模式耗时：{time_normal:.1f}s")
print(f"深度分析耗时：{time_thinking:.1f}s")
print(f"额外耗时：{time_thinking - time_normal:.1f}s")
```

### 对比结果解读

通常你会观察到：

- **普通模式**：给出正确的不等式证明，但可能跳过关键步骤，巴塞尔问题部分可能只给结论
- **深度分析**：证明过程更完整（例如使用数学归纳法逐步展开），巴塞尔问题部分会介绍欧拉的经典证明方法，甚至可能提到傅里叶级数方法

两种模式的差异在简单问题上不明显，但在需要多步推理的复杂问题上会很显著。

### 通过 Prompt 引导深度分析

除了 API 参数，你也可以通过 prompt 设计来引导更深入的分析：

```python
# 引导模型进行深度分析的 prompt 模板
deep_analysis_prompt = """
请对以下问题进行深度分析：

{question}

分析要求：
1. 先梳理问题涉及的核心概念和已知条件
2. 列出可能的求解策略，并评估每种策略的可行性
3. 选择最优策略，给出完整的推导过程
4. 验证结果的正确性（代入特殊值、量纲分析等）
5. 讨论结果的物理/数学含义和推广可能
"""

question = "为什么行星轨道是椭圆形的？从牛顿万有引力定律推导开普勒第一定律。"

response = client.chat.completions.create(
    model="intern-s1-pro",
    messages=[
        {"role": "user", "content": deep_analysis_prompt.format(question=question)}
    ],
    temperature=0.1,
    max_tokens=4096,
)

print(response.choices[0].message.content)
```

### 模式选择指南

| 场景 | 推荐模式 | 原因 |
|------|---------|------|
| 数学证明、竞赛题 | 深度分析 | 需要多步严格推理 |
| 复杂物理求解 | 深度分析 | 需要建模 + 计算 + 验证 |
| 科学论文推导 | 深度分析 | 需要完整逻辑链 |
| 算法设计 + 复杂度分析 | 深度分析 | 需要方案对比和正确性论证 |
| 日常对话、简单问答 | 普通模式 | 深度分析增加延迟但无质量提升 |
| 文本摘要、翻译 | 普通模式 | 不需要推理链 |
| 知识问答（"XXX 是什么"） | 普通模式 | 检索性质的问题不需要推理 |
| 代码补全、简单 Bug 修复 | 普通模式 | 模式匹配即可，不需要深度推理 |

核心原则：如果问题的答案需要"推导"而非"检索"，就用深度分析。

---

## Harness 评测框架

### 目标

学会使用 lm-evaluation-harness 框架评测模型在标准基准上的表现，从安装到报告解读。

### lm-evaluation-harness 简介

lm-evaluation-harness（简称 lm_eval）是由 EleutherAI 开发的大语言模型评测框架，支持数百个标准基准任务。它是学术界和工业界最广泛使用的评测工具之一。

### 安装

```bash
# 基础安装
pip install lm_eval

# 如果需要运行 HumanEval 等代码评测
pip install lm_eval[code_eval]

# 验证安装
python -c "import lm_eval; print(lm_eval.__version__)"
```

如果安装遇到依赖冲突，建议使用虚拟环境：

```bash
python -m venv eval_env
source eval_env/bin/activate  # Linux/macOS
# 或 eval_env\Scripts\activate  # Windows

pip install lm_eval
```

### 评测在线 API（不需要本地部署模型）

如果你使用的是在线 API，可以直接评测：

```bash
export INTERN_API_KEY="your-api-key-here"

lm_eval --model local-chat-completions \
  --model_args model=intern-s1-pro,base_url=https://chat.intern-ai.org.cn/api/v1/,tokenizer_backend=huggingface,num_concurrent=4 \
  --tasks gsm8k \
  --batch_size 1 \
  --output_path ./eval_results/
```

注意：在线 API 评测时，`num_concurrent` 控制并发数，设置过高可能触发频率限制。

### 评测本地部署的模型

如果你已通过 LMDeploy 部署了 API 服务（参见 LMDeploy 课程），可以直接对接评测：

```bash
# 确保 LMDeploy API 服务已在 localhost:23333 运行

lm_eval --model local-completions \
  --model_args model=internlm3-8b-instruct,base_url=http://localhost:23333/v1,tokenizer_backend=huggingface \
  --tasks gsm8k \
  --batch_size auto \
  --output_path ./eval_results/
```

### 常用评测任务

| 任务名 | 评测内容 | 题量 | 难度 | 说明 |
|--------|---------|------|------|------|
| `gsm8k` | 小学数学 | 8.5K | 中等 | 数学应用题，测试基础推理 |
| `mmlu` | 综合知识 | 14K | 中等 | 57 个学科的多选题 |
| `humaneval` | 代码生成 | 164 | 较高 | Python 编程题 |
| `math` | 竞赛数学 | 5K | 高 | 高中及竞赛级数学 |
| `winogrande` | 常识推理 | 1.7K | 中等 | 代词消歧任务 |
| `arc_challenge` | 科学推理 | 1.2K | 较高 | 小学/初中科学题 |
| `hellaswag` | 常识续写 | 10K | 中等 | 场景补全 |

### 评测多个任务

```bash
lm_eval --model local-completions \
  --model_args model=internlm3-8b-instruct,base_url=http://localhost:23333/v1,tokenizer_backend=huggingface \
  --tasks gsm8k,mmlu,winogrande,arc_challenge \
  --batch_size auto \
  --output_path ./eval_results/
```

### 查看和解读评测报告

评测完成后，结果保存在 `--output_path` 指定的目录中。目录结构如下：

```
eval_results/
  results.json           # 总体结果
  samples/
    gsm8k/
      samples.jsonl      # 每道题的详细输入输出
```

用以下脚本解读结果：

```python
import json
import os

# 查找最新的结果文件
result_dir = "./eval_results/"
result_files = [f for f in os.listdir(result_dir) if f.endswith(".json")]

if not result_files:
    print("未找到评测结果文件")
else:
    # 读取结果
    with open(os.path.join(result_dir, result_files[0]), "r") as f:
        results = json.load(f)

    print("=" * 50)
    print("评测报告")
    print("=" * 50)

    # 模型信息
    if "config" in results:
        print(f"模型: {results['config'].get('model', 'N/A')}")
        print(f"评测时间: {results['config'].get('start_time', 'N/A')}")

    # 各任务分数
    print("\n各任务得分：")
    print(f"{'任务':<20} {'指标':<15} {'得分':<10}")
    print("-" * 45)

    for task_name, metrics in results.get("results", {}).items():
        for metric_name, value in metrics.items():
            if isinstance(value, (int, float)):
                if "acc" in metric_name or "em" in metric_name:
                    print(f"{task_name:<20} {metric_name:<15} {value:.4f}")

    print("\n" + "=" * 50)
```

### 常见问题

**Q: 评测 gsm8k 分数异常低怎么办？**

A: 检查是否使用了正确的 prompt 模板。lm_eval 默认使用 few-shot 格式，如果模型不支持特定格式，可以用 `--num_fewshot 0` 尝试 zero-shot。

**Q: 评测速度很慢？**

A: 本地部署时检查 GPU 利用率。API 评测时调整 `num_concurrent` 参数。另外 `--batch_size auto` 会自动选择合适的 batch size。

**Q: 某些任务报错 "task not found"？**

A: 运行 `lm_eval --tasks list` 查看所有支持的任务名称，注意大小写和下划线。

**Q: 如何只评测某个子任务？**

A: 使用 `--tasks mmlu_anatomy` 这样的子任务名，而非整个 `mmlu`。

---

## 自行部署 Intern-S1

### 目标

了解如何在自有服务器上部署 Intern-S1 系列模型。

### 模型权重下载

所有模型权重均托管在 HuggingFace 和 ModelScope：

```bash
# HuggingFace（国内建议使用镜像）
export HF_ENDPOINT=https://hf-mirror.com
huggingface-cli download internlm/Intern-S1 --local-dir ./models/Intern-S1

# ModelScope（国内直接访问）
pip install modelscope
modelscope download --model internlm/Intern-S1 --local_dir ./models/Intern-S1
```

### 使用 LMDeploy 部署

```bash
# 部署 Intern-S1-mini（8B，单卡即可）
lmdeploy serve api_server internlm/Intern-S1-mini \
  --server-port 23333

# 部署 Intern-S1（235B MoE，需要多卡）
lmdeploy serve api_server internlm/Intern-S1 \
  --tp 8 \
  --server-port 23333
```

### 使用 vLLM 部署

```bash
vllm serve internlm/Intern-S1-mini --port 23333
```

### 使用 SGLang 部署

```bash
python -m sglang.launch_server --model-path internlm/Intern-S1-mini --port 23333
```

### 验证部署

部署完成后，使用方式与在线 API 完全一致，只需将 `base_url` 改为本地地址：

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key="not-needed",  # 本地部署通常不需要 API Key
    base_url="http://localhost:23333/v1",
)

# 测试连通性
response = client.chat.completions.create(
    model="internlm/Intern-S1-mini",
    messages=[{"role": "user", "content": "你好，请做个自我介绍"}],
    max_tokens=256,
)

print(response.choices[0].message.content)
```

### 硬件需求参考

| 模型 | 最低显存 | 推荐配置 |
|------|---------|---------|
| Intern-S1-mini (8B) | 16GB | 1x A100 80GB 或 1x RTX 4090 |
| Intern-S1 (235B MoE) | 8x 80GB | 8x A100 80GB / 8x H100 |
| Intern-S1-Pro (1T MoE) | 集群部署 | 建议使用在线 API |

---

## 最佳实践

### Prompt 工程技巧

针对科学推理场景，以下 prompt 技巧可以显著提升回答质量：

**1. 明确要求输出格式**

```python
prompt = """
求解以下微分方程：y'' + 4y' + 4y = e^(-2x)

要求：
- 先写出齐次方程的通解
- 再用待定系数法求特解
- 最后写出通解
- 每一步标注所用方法名称
"""
```

**2. 要求验证结果**

```python
prompt = """
计算定积分 integral from 0 to pi of x*sin(x) dx

请在得到结果后，用分部积分法和另一种方法分别计算，交叉验证结果。
"""
```

**3. 指定分析深度**

```python
prompt = """
分析快速排序的时间复杂度。

要求分析深度：
- 最好情况、最坏情况、平均情况的时间复杂度
- 递推关系式的完整推导（用主定理或递归树）
- 与归并排序的对比（时间、空间、稳定性、缓存友好性）
- 实际工程中的优化策略（三数取中、插入排序兜底、内省排序）
"""
```

### 多轮对话进行深入探索

对于复杂的科学问题，可以通过多轮对话逐步深入：

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("INTERN_API_KEY"),
    base_url="https://chat.intern-ai.org.cn/api/v1/",
)

messages = [
    {"role": "system", "content": "你是一位严谨的科学顾问，擅长逐步引导深入分析。"},
]

# 第一轮：提出问题
messages.append({
    "role": "user",
    "content": "为什么超导体在临界温度以下电阻为零？请从 BCS 理论的角度解释。"
})

response1 = client.chat.completions.create(
    model="intern-s1-pro",
    messages=messages,
    temperature=0.1,
    max_tokens=4096,
)

answer1 = response1.choices[0].message.content
messages.append({"role": "assistant", "content": answer1})
print("第一轮回答：")
print(answer1)

# 第二轮：追问细节
messages.append({
    "role": "user",
    "content": "Cooper 对的形成过程中，晶格声子起了什么作用？能否用一个类比来解释？"
})

response2 = client.chat.completions.create(
    model="intern-s1-pro",
    messages=messages,
    temperature=0.1,
    max_tokens=4096,
)

answer2 = response2.choices[0].message.content
print("\n第二轮回答：")
print(answer2)

# 第三轮：要求定量分析
messages.append({"role": "assistant", "content": answer2})
messages.append({
    "role": "user",
    "content": "能否估算一下铝（Tc=1.2K）的 Cooper 对相干长度和超导能隙？"
})

response3 = client.chat.completions.create(
    model="intern-s1-pro",
    messages=messages,
    temperature=0.1,
    max_tokens=4096,
)

print("\n第三轮回答：")
print(response3.choices[0].message.content)
```

---

## FAQ

### 基础问题

**Q: Intern-S1-Pro 和 InternLM 是什么关系？**

A: 它们是书生生态中不同定位的产品。InternLM 是通用语言大模型，擅长对话和工具调用。Intern-S1-Pro 是科学多模态大模型，在数学、物理、化学等科学领域有显著优势。两者互补，不是替代关系。

**Q: Intern-S1-Pro 是推理模型吗？**

A: 不是。Intern-S1-Pro 是科学多模态大模型。虽然它具备强大的推理能力（通过深度分析），但它的定位是科学领域的深度理解和精确计算，而非像某些推理模型那样专注于推理链生成。

**Q: API 调用时模型 ID 填什么？**

A: 使用 `intern-s1-pro` 即可获取最新版本。你也可以通过 `client.models.list()` 查看所有可用模型。

**Q: 深度分析有单独的模型 ID 吗？**

A: 没有。深度分析是 Intern-S1-Pro 模型的内在能力，通过 `extra_body` 中的 `enable_thinking` 参数控制，不需要切换模型。

### API 相关

**Q: API 有调用频率限制吗？**

A: 有。具体限制取决于你的账户级别。如果遇到 429 错误，建议添加指数退避重试：

```python
import time
from openai import RateLimitError

max_retries = 3
for attempt in range(max_retries):
    try:
        response = client.chat.completions.create(...)
        break
    except RateLimitError:
        wait_time = 2 ** attempt  # 1s, 2s, 4s
        print(f"频率限制，等待 {wait_time}s 后重试...")
        time.sleep(wait_time)
```

**Q: 支持流式输出吗？**

A: 支持。在 `create()` 调用中添加 `stream=True` 参数即可。详见上方"流式输出"章节。

**Q: max_tokens 设多少合适？**

A: 取决于任务复杂度。简单问答 512-1024 足够，数学证明建议 2048-4096，复杂代码生成可以设到 4096-8192。设得过大不会影响简短回答，但会影响计费。

### 部署相关

**Q: Intern-S1-Pro 能本地部署吗？**

A: Intern-S1-Pro 参数量约 1T，本地部署需要大规模集群，对一般用户不太现实。建议使用在线 API。如果需要本地部署体验，可以部署 Intern-S1-mini（8B），单卡即可运行。

**Q: 国内下载模型权重很慢怎么办？**

A: 使用 HuggingFace 镜像 `export HF_ENDPOINT=https://hf-mirror.com`，或使用 ModelScope 下载。

### 评测相关

**Q: 不同评测框架的分数能直接比较吗？**

A: 不建议。不同框架的 prompt 模板、few-shot 设置、后处理方式可能不同，会导致同一模型在不同框架下分数有差异。比较时应使用同一框架、同一配置。

**Q: 我的评测分数和官方报告差很多？**

A: 检查以下几点：
1. 模型版本是否一致
2. few-shot 数量是否相同
3. 是否使用了正确的 chat template
4. temperature 和采样策略是否一致

---

## 参考资料

- Intern-S1 GitHub：https://github.com/InternLM/Intern-S1
- Intern-S1-Pro 论文：https://arxiv.org/abs/2603.25040
- Intern-S1 论文：https://arxiv.org/abs/2508.15763
- Intern-S1-Pro 模型权重：https://huggingface.co/internlm/Intern-S1-Pro
- 书生平台 API 文档：https://internlm.intern-ai.org.cn/api/document
- lm-evaluation-harness：https://github.com/EleutherAI/lm-evaluation-harness
- LMDeploy 文档：https://lmdeploy.readthedocs.io/
