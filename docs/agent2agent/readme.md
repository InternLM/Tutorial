# Agent2Agent 多智能体协作

> 本文档 AI + 社区共建中

## 先看效果：3 个 Agent 协作完成一次科研调研

在开始学习协议细节之前，先看一个你学完本课就能搭出来的系统。

假设你是一位研究者，需要调研"大语言模型在蛋白质结构预测中的应用"。传统做法是自己搜论文、自己读摘要、自己写总结。如果有三个 AI Agent 帮你协作呢？

```
你的一句话请求
  "调研大语言模型在蛋白质结构预测中的应用"
     |
     v
[主控 Agent (Orchestrator)]
     |
     +---> [文献检索 Agent]  搜索 arXiv、PubMed，返回 10 篇相关论文
     |         |
     |         v
     +---> [文献分析 Agent]  阅读每篇摘要，提取方法、数据集、性能指标
     |         |
     |         v
     +---> [报告生成 Agent]  整合分析结果，生成结构化调研报告
     |
     v
  一份完整的调研报告交到你手上
```

每个 Agent 独立运行，各自有明确的职责，通过 A2A 协议互相发现、分配任务、交换结果。这不是科幻，这就是本课要带你实现的系统。

## 课程简介

Agent2Agent（A2A）是由 Google 发起的开放协议，定义了 AI Agent 之间互相发现、通信和协作的标准方式。如果说 MCP 解决的是"AI 与工具的连接"，A2A 解决的则是"AI 与 AI 的连接"。本课程讲解 A2A 协议的核心概念，带你用 Python SDK 从零实现 A2A Agent，并构建一个完整的多 Agent 科研协作系统。

## 你将学到

- 理解 A2A 协议的设计目标和核心概念
- 彻底搞清 MCP 与 A2A 的区别和互补关系
- 掌握 Agent Card、Task、Message 的数据结构
- 使用 Python SDK 实现可运行的 A2A Agent
- 搭建 3-Agent 科研协作系统（文献检索 + 分析 + 报告生成）
- 掌握错误恢复、超时处理等生产级实践

## MCP 与 A2A：彻底讲透

这是学 A2A 最容易混淆的点，我们先把它讲清楚。

### 一句话区分

- **MCP = 给 Agent 装能力**。你的 Agent 通过 MCP 连接数据库、调用 API、读取文件。
- **A2A = 让 Agent 组团**。多个 Agent 通过 A2A 互相发现、分配任务、交换结果。

### 类比理解

把 Agent 想象成一个员工：

- MCP 是这个员工的"工具箱"——锤子、螺丝刀、电钻。工具本身不会自己干活，得员工来用。
- A2A 是员工之间的"协作协议"——谁负责什么、怎么分配任务、结果怎么汇报。

一个员工可以同时带着工具箱（MCP），又参与团队协作（A2A）。两者互补，不竞争。

### 详细对比

| 维度 | MCP (Model Context Protocol) | A2A (Agent2Agent) |
|------|------|------|
| 连接对象 | AI Agent <-> 工具/数据源 | AI Agent <-> AI Agent |
| 协议角色 | Client（Agent）- Server（工具） | Peer-to-Peer（对等通信） |
| 能力暴露 | Tools / Resources / Prompts | Skills（通过 Agent Card） |
| 发现机制 | 手动配置或本地声明 | 基于 Agent Card 的服务发现 |
| 通信方式 | Stdio / HTTP+SSE | HTTP + JSON-RPC 2.0 |
| 典型场景 | 查数据库、调 API、读文件 | 多 Agent 任务分工与协作 |
| 状态管理 | 无状态（每次调用独立） | 有状态（Task 有生命周期） |
| 谁发起的 | Anthropic | Google |

### 什么时候用哪个？

**用 MCP 的场景：**
- 你的 Agent 需要查询数据库 -> MCP Tool
- 你的 Agent 需要调用第三方 API -> MCP Tool
- 你的 Agent 需要读写本地文件 -> MCP Resource

**用 A2A 的场景：**
- 一个任务太复杂，需要多个专业 Agent 分工 -> A2A
- 你想复用别人开发的 Agent 而不关心其内部实现 -> A2A
- 不同团队各自维护自己的 Agent，需要互通 -> A2A

**两者结合（最常见）：**

```
用户请求: "调研大模型在蛋白质预测中的应用"
    |
    v
[主控 Agent]  <-- 通过 A2A 调度其他 Agent
    |
    +---> [文献检索 Agent]
    |         内部通过 MCP 调用 arXiv API (MCP Tool)
    |         内部通过 MCP 查询本地论文数据库 (MCP Resource)
    |
    +---> [文献分析 Agent]
    |         内部通过 MCP 调用 Intern-S1-Pro 进行科学文本理解
    |
    +---> [报告生成 Agent]
              内部通过 MCP 写入本地 Markdown 文件 (MCP Tool)
```

A2A 负责 Agent 之间的调度，MCP 负责每个 Agent 内部的工具调用。两个协议在不同层面工作。

## A2A 协议核心概念

### Agent Card（智能体名片）

每个 Agent 通过一个 JSON 格式的 Agent Card 来描述自己：我是谁、我能做什么、怎么找到我。

```json
{
  "name": "literature-search-agent",
  "description": "科研文献检索助手，擅长在 arXiv 和 PubMed 上搜索论文并整理摘要",
  "url": "http://localhost:8001",
  "version": "1.0.0",
  "capabilities": {
    "streaming": true,
    "pushNotifications": false
  },
  "skills": [
    {
      "id": "search-papers",
      "name": "论文搜索",
      "description": "根据关键词在学术数据库中搜索相关论文，返回标题、作者、摘要"
    }
  ]
}
```

关键字段：
- `name`：Agent 的唯一标识，其他 Agent 通过名字来引用它
- `description`：能力描述，编排器根据描述来决定分配什么任务
- `url`：服务地址，其他 Agent 通过这个 URL 来调用它
- `capabilities`：支持的通信能力（流式、推送通知等）
- `skills`：技能列表，每个 Skill 描述一种可执行的任务

Agent Card 通常发布在 `/.well-known/agent.json` 路径下，方便其他 Agent 通过 HTTP GET 读取其能力声明。实际使用中，通常需要预先知道 Agent 的地址，再通过该路径获取 Card 信息。

### Task（任务）

Task 是 Agent 之间协作的基本单位。一个 Agent 向另一个 Agent 发送 Task，对方处理后返回结果。

Task 有明确的生命周期状态机：

```
submitted -> working -> completed
                    \-> failed
                    \-> canceled
```

- `submitted`：任务已提交，等待处理
- `working`：Agent 正在处理
- `completed`：处理完成，结果已返回
- `failed`：处理失败，包含错误信息
- `canceled`：被调用方主动取消

### Message 与 Part

Message 是 Task 中的通信载体，每条 Message 有 `role`（user 或 agent）和 `parts` 列表：

| Part 类型 | 说明 | 使用场景 |
|-----------|------|----------|
| TextPart | 纯文本 | 自然语言请求和响应 |
| FilePart | 文件（含 MIME 类型） | 传递 PDF、图片等 |
| DataPart | 结构化 JSON 数据 | 传递表格、统计结果 |

### 通信协议

A2A 使用 JSON-RPC 2.0 通信。核心方法：

| 方法 | 说明 |
|------|------|
| `tasks/send` | 发送任务并等待完成 |
| `tasks/sendSubscribe` | 发送任务并通过 SSE 接收流式更新 |
| `tasks/get` | 查询任务状态 |
| `tasks/cancel` | 取消正在执行的任务 |

## 环境准备

```bash
# 创建虚拟环境
python -m venv a2a-env
source a2a-env/bin/activate  # Windows: a2a-env\Scripts\activate

# 安装依赖
pip install a2a-sdk uvicorn httpx

# 验证安装
python -c "import a2a; print('a2a-sdk 安装成功')"
```

## 实战：构建科研协作多 Agent 系统

接下来是本课的核心部分——实现开头展示的 3-Agent 科研协作系统。

### 整体架构

```
                        用户请求
                           |
                           v
                  [主控 Agent :8000]
                     /     |     \
                    v      v      v
    [文献检索 Agent]  [分析 Agent]  [报告 Agent]
         :8001          :8002         :8003
```

四个 Agent 各自独立运行，通过 A2A 协议通信：

1. **文献检索 Agent（:8001）**：接收关键词，返回相关论文列表
2. **文献分析 Agent（:8002）**：接收论文列表，提取关键信息并对比分析
3. **报告生成 Agent（:8003）**：接收分析结果，生成结构化调研报告
4. **主控 Agent（:8000）**：接收用户请求，按顺序调度三个子 Agent

### 三个子 Agent（单文件实现）

以下代码基于 `a2a-sdk` 早期版本编写，类名和字段可能随 SDK 更新有所变化，请以 [官方文档](https://github.com/google/a2a-protocol) 为准。本节先用模拟数据跑通协作链路，后续再替换成真实工具（如 MCP + Intern-S1-Pro）。

为了方便运行，我们把三个子 Agent 放在一个文件里，通过命令行参数选择启动哪个。每个 Agent 有独立的类和 Agent Card，运行在不同端口。

```python
# agents.py
"""
科研协作子 Agent 集合。
用法:
  python agents.py search     # 启动文献检索 Agent (:8001)
  python agents.py analysis   # 启动文献分析 Agent (:8002)
  python agents.py report     # 启动报告生成 Agent (:8003)
"""

import sys
from datetime import datetime
from a2a.server.agent_execution import AgentExecution, RequestContext
from a2a.server.server import A2AServer
from a2a.types import (
    AgentCard, AgentCapabilities, AgentSkill,
    Message, TextPart, Role, TaskState,
)


def make_msg(text: str) -> Message:
    return Message(role=Role.agent, parts=[TextPart(type="text", text=text)])


def extract_text(request: dict) -> str:
    """从 JSON-RPC 请求中提取文本内容"""
    parts = request.get("params", {}).get("message", {}).get("parts", [])
    for part in parts:
        if part.get("type") == "text":
            return part.get("text", "")
    return ""


# --- 模拟论文数据库 ---
PAPERS = [
    {
        "title": "AlphaFold2: Protein Structure Prediction with Deep Learning",
        "authors": "Jumper et al.", "year": 2021, "citations": 15420,
        "abstract": "We present AlphaFold2, achieving atomic-level accuracy in protein structure prediction using a novel neural architecture with evolutionary and geometric constraints.",
        "keywords": ["protein structure", "deep learning", "alphafold"],
    },
    {
        "title": "ESMFold: Language Models Enable Zero-Shot Prediction of Protein Structure",
        "authors": "Lin et al.", "year": 2023, "citations": 3210,
        "abstract": "Large language models trained on protein sequences can predict 3D structures without multiple sequence alignments, with competitive accuracy and faster inference.",
        "keywords": ["protein structure", "language model", "zero-shot"],
    },
    {
        "title": "RoseTTAFold: Accurate Prediction of Protein Structures and Interactions",
        "authors": "Baek et al.", "year": 2021, "citations": 4850,
        "abstract": "A three-track neural network for protein structure prediction that simultaneously processes sequence, distance, and coordinate information.",
        "keywords": ["protein structure", "neural network", "prediction"],
    },
    {
        "title": "ProteinMPNN: Robust Protein Sequence Design with Deep Learning",
        "authors": "Dauparas et al.", "year": 2022, "citations": 2760,
        "abstract": "A message passing neural network for computational protein design that generates amino acid sequences given backbone structures.",
        "keywords": ["protein design", "deep learning", "sequence design"],
    },
    {
        "title": "Uni-Fold: Training Protein Structure Prediction Models on Diverse Data",
        "authors": "Li et al.", "year": 2022, "citations": 890,
        "abstract": "An open-source platform for training protein structure prediction models on experimental and predicted structures.",
        "keywords": ["protein structure", "training", "open source"],
    },
]


# ============================================================
# Agent 1: 文献检索
# ============================================================
class LiteratureSearchAgent(AgentExecution):
    async def execute(self, context: RequestContext, request: dict) -> None:
        query = extract_text(request)
        if not query:
            await context.send_status_update(state=TaskState.failed,
                message=make_msg("错误：未收到搜索关键词"))
            return

        await context.send_status_update(state=TaskState.working,
            message=make_msg(f"正在搜索与 '{query}' 相关的论文..."))

        # 关键词匹配 + 引用排序
        results = []
        for paper in PAPERS:
            searchable = f"{paper['title']} {paper['abstract']} {' '.join(paper['keywords'])}".lower()
            score = sum(1 for w in query.lower().split() if w in searchable)
            if score > 0:
                results.append((score, paper))
        results.sort(key=lambda x: (-x[0], -x[1]["citations"]))

        if not results:
            await context.send_status_update(state=TaskState.completed,
                message=make_msg("未找到相关论文，请尝试调整关键词。"))
            return

        lines = [f"找到 {len(results)} 篇相关论文：", ""]
        for i, (_, p) in enumerate(results, 1):
            lines.append(f"[{i}] {p['title']}")
            lines.append(f"    作者: {p['authors']} ({p['year']})  引用: {p['citations']}")
            lines.append(f"    摘要: {p['abstract'][:100]}...")
            lines.append("")

        await context.send_status_update(state=TaskState.completed,
            message=make_msg("\n".join(lines)))


# ============================================================
# Agent 2: 文献分析
# ============================================================
class LiteratureAnalysisAgent(AgentExecution):
    async def execute(self, context: RequestContext, request: dict) -> None:
        text = extract_text(request)
        if not text:
            await context.send_status_update(state=TaskState.failed,
                message=make_msg("错误：未收到待分析的论文内容"))
            return

        await context.send_status_update(state=TaskState.working,
            message=make_msg("正在分析论文内容..."))

        # 实际场景中会调用 Intern-S1-Pro 等大模型做深度分析
        paper_count = sum(1 for line in text.split("\n") if line.strip().startswith("["))
        analysis = "\n".join([
            "=== 文献分析报告 ===", "",
            f"分析论文数量: {paper_count}", "",
            "--- 研究方法分类 ---",
            "- 深度学习方法: AlphaFold2, ESMFold, RoseTTAFold, Uni-Fold",
            "- 蛋白质设计: ProteinMPNN",
            "- 语言模型方法: ESMFold (零样本预测)", "",
            "--- 技术趋势 ---",
            "1. 从多序列比对(MSA)依赖 -> 零样本预测 (ESMFold 2023)",
            "2. 从结构预测 -> 蛋白质设计 (ProteinMPNN 2022)",
            "3. 开源平台趋势 (Uni-Fold 2022)", "",
            "--- 关键发现 ---",
            "- 大语言模型能够从蛋白质序列中学习结构信息",
            "- 零样本方法在速度上有显著优势，但精度仍有提升空间",
            "- 多轨道神经网络架构展现了结构预测的新范式", "",
            "--- 引用排名 ---",
            "1. AlphaFold2 (15420) - 里程碑式工作",
            "2. RoseTTAFold (4850) - 重要替代方案",
            "3. ESMFold (3210) - 语言模型新方向",
        ])

        await context.send_status_update(state=TaskState.completed,
            message=make_msg(analysis))


# ============================================================
# Agent 3: 报告生成
# ============================================================
class ReportGenerationAgent(AgentExecution):
    async def execute(self, context: RequestContext, request: dict) -> None:
        text = extract_text(request)
        if not text:
            await context.send_status_update(state=TaskState.failed,
                message=make_msg("错误：未收到待整合的分析内容"))
            return

        await context.send_status_update(state=TaskState.working,
            message=make_msg("正在生成调研报告..."))

        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        report = "\n".join([
            "=" * 50, "科研调研报告", "=" * 50, "",
            f"生成时间: {now}",
            "主题: 大语言模型在蛋白质结构预测中的应用", "",
            "--- 一、研究概述 ---", "",
            "蛋白质结构预测是计算生物学的核心问题。深度学习方法在该领域",
            "取得了突破性进展，尤其是 AlphaFold2 标志着新阶段的到来。",
            "大语言模型的引入（如 ESMFold）进一步降低了计算成本。", "",
            "--- 二、核心分析 ---", "", text, "",
            "--- 三、结论与展望 ---", "",
            "1. 大语言模型在蛋白质结构预测中展现出巨大潜力",
            "2. 零样本预测是重要趋势，有望大幅降低计算成本",
            "3. 从结构预测到蛋白质设计的转变正在发生",
            "4. 开源工具和平台的建设对推动领域发展至关重要", "",
            "--- 四、推荐行动 ---", "",
            "- 关注 ESMFold 等语言模型方法，评估其适用性",
            "- 利用 Uni-Fold 等开源平台进行模型训练和评估",
            "- 探索蛋白质设计方向，结合 ProteinMPNN 开展应用研究", "",
            "=" * 50, "报告由多 Agent 协作系统自动生成", "=" * 50,
        ])

        await context.send_status_update(state=TaskState.completed,
            message=make_msg(report))


# ============================================================
# Agent 注册表与启动入口
# ============================================================
AGENT_CONFIGS = {
    "search": {
        "cls": LiteratureSearchAgent,
        "card": AgentCard(
            name="literature-search-agent",
            description="科研文献检索助手，根据关键词搜索学术论文并返回结果列表",
            url="http://localhost:8001", version="1.0.0",
            capabilities=AgentCapabilities(streaming=False, pushNotifications=False),
            skills=[AgentSkill(id="search-papers", name="论文搜索",
                description="根据关键词在学术数据库中搜索相关论文")],
        ),
        "port": 8001,
    },
    "analysis": {
        "cls": LiteratureAnalysisAgent,
        "card": AgentCard(
            name="literature-analysis-agent",
            description="科研文献分析助手，对论文列表进行结构化分析和对比",
            url="http://localhost:8002", version="1.0.0",
            capabilities=AgentCapabilities(streaming=False, pushNotifications=False),
            skills=[AgentSkill(id="analyze-papers", name="论文分析",
                description="对论文列表进行结构化分析，提取方法、趋势和关键发现")],
        ),
        "port": 8002,
    },
    "report": {
        "cls": ReportGenerationAgent,
        "card": AgentCard(
            name="report-generation-agent",
            description="科研报告生成助手，将分析结果整合为结构化调研报告",
            url="http://localhost:8003", version="1.0.0",
            capabilities=AgentCapabilities(streaming=False, pushNotifications=False),
            skills=[AgentSkill(id="generate-report", name="报告生成",
                description="将文献分析结果整合为结构化的调研报告")],
        ),
        "port": 8003,
    },
}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in AGENT_CONFIGS:
        print(f"用法: python agents.py <{'|'.join(AGENT_CONFIGS.keys())}>")
        sys.exit(1)

    cfg = AGENT_CONFIGS[sys.argv[1]]
    agent = cfg["cls"]()
    server = A2AServer(agent_card=cfg["card"], agent_execution=agent)
    print(f"{cfg['card'].name} 启动于 http://localhost:{cfg['port']}")
    server.start(host="0.0.0.0", port=cfg["port"])
```

### 主控 Agent（Orchestrator）

主控 Agent 单独一个文件，负责发现子 Agent、按顺序分配任务、处理错误和超时。

```python
# orchestrator.py
"""
主控 Agent：接收用户请求，按顺序调度文献检索、分析、报告三个 Agent。
启动方式: python orchestrator.py
服务地址: http://localhost:8000
"""

import asyncio
import httpx
from a2a.server.agent_execution import AgentExecution, RequestContext
from a2a.server.server import A2AServer
from a2a.types import (
    AgentCard, AgentCapabilities, AgentSkill,
    Message, TextPart, Role, TaskState,
)

AGENT_TIMEOUT = 30.0

AGENT_PIPELINE = [
    {"name": "literature-search", "url": "http://localhost:8001"},
    {"name": "literature-analysis", "url": "http://localhost:8002"},
    {"name": "report-generation", "url": "http://localhost:8003"},
]


def make_msg(text: str) -> Message:
    return Message(role=Role.agent, parts=[TextPart(type="text", text=text)])


class OrchestratorAgent(AgentExecution):
    """编排多个专业 Agent 完成复杂任务"""

    async def execute(self, context: RequestContext, request: dict) -> None:
        parts = request.get("params", {}).get("message", {}).get("parts", [])
        input_text = next((p["text"] for p in parts if p.get("type") == "text"), "")

        if not input_text:
            await context.send_status_update(state=TaskState.failed,
                message=make_msg("错误：未收到用户请求"))
            return

        # 发现可用 Agent
        await context.send_status_update(state=TaskState.working,
            message=make_msg("正在发现可用的 Agent..."))

        available = await self._discover_agents()
        if not available:
            await context.send_status_update(state=TaskState.failed,
                message=make_msg("错误：未发现可用的 Agent，请确保所有 Agent 已启动"))
            return

        names = [a["name"] for a in available]
        await context.send_status_update(state=TaskState.working,
            message=make_msg(f"发现 {len(available)} 个 Agent: {', '.join(names)}"))

        # 串行流水线：每个 Agent 的输出作为下一个的输入
        current_input = input_text
        step_results = []

        for i, agent_info in enumerate(available):
            step = i + 1
            name, url = agent_info["name"], agent_info["url"]

            await context.send_status_update(state=TaskState.working,
                message=make_msg(f"[步骤 {step}/{len(available)}] 正在调用 {name}..."))

            try:
                current_input = await self._call_agent(url, name, current_input)
                step_results.append(f"  [完成] {name}")
            except asyncio.TimeoutError:
                step_results.append(f"  [超时] {name}")
                await context.send_status_update(state=TaskState.failed,
                    message=make_msg(f"步骤 {step} 超时: {name}\n" + "\n".join(step_results)))
                return
            except Exception as e:
                step_results.append(f"  [失败] {name}: {e}")
                await context.send_status_update(state=TaskState.failed,
                    message=make_msg(f"步骤 {step} 失败: {e}\n" + "\n".join(step_results)))
                return

        summary = "\n".join(step_results)
        await context.send_status_update(state=TaskState.completed,
            message=make_msg(f"{current_input}\n\n{'=' * 40}\n协作摘要\n{'=' * 40}\n{summary}"))

    async def _discover_agents(self) -> list[dict]:
        """通过读取 Agent Card 发现可用 Agent"""
        available = []
        async with httpx.AsyncClient(timeout=5.0) as client:
            for info in AGENT_PIPELINE:
                try:
                    resp = await client.get(f"{info['url']}/.well-known/agent.json")
                    if resp.status_code == 200:
                        card = resp.json()
                        available.append({"name": card.get("name", info["name"]),
                                          "url": info["url"]})
                except Exception:
                    pass  # 该 Agent 不可用，跳过
        return available

    async def _call_agent(self, url: str, name: str, text: str) -> str:
        """调用单个 Agent 并提取文本结果"""
        payload = {
            "jsonrpc": "2.0", "method": "tasks/send", "id": f"sub-{name}",
            "params": {
                "id": f"sub-{name}",
                "message": {"role": "user", "parts": [{"type": "text", "text": text}]},
            },
        }
        async with httpx.AsyncClient(timeout=AGENT_TIMEOUT) as client:
            resp = await client.post(url, json=payload)
            data = resp.json()

        result = data.get("result", {})
        status = result.get("status", {})
        if status.get("state") == "failed":
            parts = status.get("message", {}).get("parts", [])
            err = next((p["text"] for p in parts if p.get("type") == "text"), "未知错误")
            raise RuntimeError(err)

        parts = status.get("message", {}).get("parts", [])
        return next((p["text"] for p in parts if p.get("type") == "text"), "(无文本返回)")


if __name__ == "__main__":
    card = AgentCard(
        name="research-orchestrator",
        description="科研调研编排器，协调多个 Agent 完成文献检索、分析和报告生成",
        url="http://localhost:8000", version="1.0.0",
        capabilities=AgentCapabilities(streaming=False, pushNotifications=False),
        skills=[AgentSkill(id="research-survey", name="科研调研",
            description="接收调研主题，协调多个 Agent 完成文献检索、分析和报告生成")],
    )
    agent = OrchestratorAgent()
    server = A2AServer(agent_card=card, agent_execution=agent)
    print("主控 Agent 启动于 http://localhost:8000")
    server.start(host="0.0.0.0", port=8000)
```

### 客户端：发起调研请求

```python
# research_client.py
"""
客户端：向主控 Agent 发起科研调研请求。
用法: python research_client.py [调研主题]
前提: 所有 4 个 Agent 已启动
"""

import httpx
import sys

ORCHESTRATOR_URL = "http://localhost:8000"


def main():
    # 发现主控 Agent
    try:
        resp = httpx.get(f"{ORCHESTRATOR_URL}/.well-known/agent.json", timeout=5.0)
        card = resp.json()
        print(f"已连接到: {card['name']}")
        print(f"技能: {[s['name'] for s in card['skills']]}\n")
    except Exception as e:
        print(f"无法连接到主控 Agent: {e}\n请确保已启动所有 Agent")
        sys.exit(1)

    # 发送调研请求
    topic = sys.argv[1] if len(sys.argv) > 1 else "大语言模型在蛋白质结构预测中的应用"
    print(f"发送调研请求: {topic}\n等待多 Agent 协作完成...\n")

    payload = {
        "jsonrpc": "2.0", "method": "tasks/send", "id": "research-001",
        "params": {
            "id": "research-001",
            "message": {"role": "user", "parts": [{"type": "text", "text": topic}]},
        },
    }

    try:
        resp = httpx.post(ORCHESTRATOR_URL, json=payload, timeout=120.0)
        data = resp.json()
        status = data.get("result", {}).get("status", {})
        print(f"任务状态: {status.get('state', 'unknown')}\n")
        for part in status.get("message", {}).get("parts", []):
            if part.get("type") == "text":
                print(part["text"])
    except httpx.TimeoutException:
        print("请求超时，请检查 Agent 是否正常运行")
    except Exception as e:
        print(f"请求失败: {e}")


if __name__ == "__main__":
    main()
```

### 运行步骤

打开 4 个终端窗口，按顺序启动：

```bash
# 终端 1 - 文献检索 Agent
python agents.py search

# 终端 2 - 文献分析 Agent
python agents.py analysis

# 终端 3 - 报告生成 Agent
python agents.py report

# 终端 4 - 主控 Agent
python orchestrator.py
```

然后在第 5 个终端发起请求：

```bash
python research_client.py
# 或指定主题
python research_client.py "蛋白质设计的深度学习方法"
```

你会看到主控 Agent 依次调用三个子 Agent，最终输出一份完整的调研报告。

## Agent 设计原则与最佳实践

### Agent Card 设计原则

1. **描述精确**：description 要准确反映能力边界，不夸大不模糊。编排器根据描述分配任务，描述不准会导致分配错误。
2. **Skill 粒度适中**：每个 Skill 对应一个明确的任务类型。太粗（"什么都能做"）等于没说；太细会限制复用。
3. **版本管理**：能力变更时更新版本号，让调用方知道接口是否有变化。

### 任务处理原则

1. **幂等性**：同一任务重复提交应得到相同结果
2. **超时处理**：长时间运行的任务要有超时机制，不能让调用方无限等待
3. **状态反馈**：通过 Task 状态让调用方知道执行进度
4. **错误透明**：失败时返回清晰的错误信息，而不是静默失败

### 多 Agent 系统设计模式

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| 串行流水线 | A -> B -> C，每个 Agent 处理后传给下一个 | 文献检索 -> 分析 -> 报告 |
| 并行扇出 | Orchestrator 同时调用多个 Agent | 多维度分析同一份数据 |
| 层级委托 | Agent 遇到子问题时委托给专业 Agent | 复杂决策的分层处理 |
| 投票共识 | 多个 Agent 独立处理，取多数结果 | 需要高可靠性的场景 |

本课的科研协作系统采用串行流水线模式。实际场景中可以根据需求混合使用。

### 安全注意事项

- Agent Card 中不要暴露内部实现细节（数据库地址、API Key 等）
- Agent 之间的通信应验证来源身份（生产环境建议 TLS + Token 认证）
- 限制 Agent 操作权限，遵循最小权限原则
- 对输入进行校验，防止注入攻击

## 融入 AGI4S：科研协作场景拓展

上面的示例使用了模拟数据。在真实的科研场景中，每个 Agent 内部可以通过 MCP 接入真实工具：

**文献检索 Agent** -- 通过 MCP 接入 arXiv API、PubMed API、本地论文数据库（如 PaperScope）

**文献分析 Agent** -- 调用 Intern-S1-Pro 进行科学文本理解，利用多模态能力分析论文图表

**报告生成 Agent** -- 调用大模型生成高质量总结，自动生成参考文献列表，输出 Markdown / LaTeX 格式

**更多科研协作场景：**

| 场景 | Agent 组合 | 协作模式 |
|------|-----------|----------|
| 实验设计 | 文献 Agent + 方法 Agent + 评审 Agent | 串行流水线 |
| 数据分析 | 清洗 Agent + 统计 Agent + 可视化 Agent | 串行流水线 |
| 论文写作 | 大纲 Agent + 段落 Agent + 润色 Agent | 串行流水线 |
| 交叉验证 | 多个分析 Agent 独立运行 + 汇总 Agent | 并行扇出 |

## FAQ

### Q1: Agent 之间的消息格式是什么？

A2A 使用 JSON-RPC 2.0 格式。请求和响应的结构如下：

```json
// 请求
{
  "jsonrpc": "2.0",
  "method": "tasks/send",
  "id": "request-id",
  "params": {
    "id": "task-id",
    "message": {
      "role": "user",
      "parts": [{"type": "text", "text": "你的请求内容"}]
    }
  }
}

// 响应
{
  "jsonrpc": "2.0",
  "id": "request-id",
  "result": {
    "id": "task-id",
    "status": {
      "state": "completed",
      "message": {
        "role": "agent",
        "parts": [{"type": "text", "text": "Agent 的响应内容"}]
      }
    }
  }
}
```

### Q2: 网络通信失败怎么处理？

本课的 Orchestrator 已经包含了基本的超时和异常处理。生产环境建议增加重试机制：

```python
async def _call_agent_with_retry(self, url, name, text, max_retries=3):
    """带指数退避的 Agent 调用"""
    last_error = None
    for attempt in range(max_retries):
        try:
            return await self._call_agent(url, name, text)
        except (httpx.ConnectError, httpx.TimeoutException) as e:
            last_error = e
            wait = 2 ** attempt  # 1s, 2s, 4s
            print(f"[重试] {name} 第 {attempt+1} 次失败，{wait}s 后重试")
            await asyncio.sleep(wait)
        except Exception:
            raise  # 非网络错误不重试
    raise RuntimeError(f"{name} 在 {max_retries} 次重试后仍失败: {last_error}")
```

如果某个 Agent 连续失败多次，可以加熔断机制：暂时停止调用，避免雪崩。

### Q3: 怎么调试多 Agent 系统？

**1. 单独测试每个 Agent**

先用 curl 单独调用，确认各自工作正常，再测试编排：

```bash
# 测试文献检索 Agent
curl -X POST http://localhost:8001 \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0", "method": "tasks/send", "id": "test-001",
    "params": {"id": "test-001",
      "message": {"role": "user",
        "parts": [{"type": "text", "text": "protein structure"}]}}
  }'

# 查看 Agent Card
curl http://localhost:8001/.well-known/agent.json | python -m json.tool
```

**2. 日志追踪**

给每个请求分配 trace_id，在所有 Agent 的日志中透传，方便追踪完整链路。

**3. 逐步执行**

调试阶段把 Orchestrator 的流水线改成手动触发每一步，观察中间结果是否符合预期。

### Q4: A2A Agent 可以跨语言实现吗？

可以。A2A 基于 HTTP + JSON-RPC，任何语言都能实现。文献检索用 Python，分析用 Go，报告用 Node.js，只要遵循 A2A 协议规范即可。Google 官方提供了 Python SDK（`a2a-sdk`），社区也在开发其他语言的 SDK。

### Q5: 一个 Agent 能同时是服务端和客户端吗？

可以。本课的 Orchestrator 就是这样——它有自己的 Agent Card（可以被调用），同时作为 Client 调用其他 Agent。这是 A2A Peer-to-Peer 设计的好处。

### Q6: A2A 协议的生态成熟度如何？

A2A 由 Google 于 2025 年发布，协议仍在演进中，适合学习与原型验证。用于生产前需结合官方仓库和 SDK 版本状态评估。建议关注 GitHub 仓库获取最新动态。

## 拓展方向

学完本课后，你可以继续探索：

1. **接入真实 API**：用 MCP 把文献检索 Agent 接到 arXiv API 上，实现真实的论文搜索
2. **接入大模型**：让分析 Agent 调用 Intern-S1-Pro，实现真正的科学文献理解
3. **流式支持**：设置 `streaming: true`，使用 `tasks/sendSubscribe` 实现实时进度推送
4. **持久化任务**：将 Task 状态存入数据库，支持断点续传
5. **Web UI**：用 Next.js 开发前端界面，展示多 Agent 协作的实时进度

## 参考资料

- [A2A 协议规范](https://github.com/google/a2a-protocol)
- [A2A Python SDK](https://github.com/google/a2a-python)
- [Google A2A 博客](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)
- [MCP 官方文档](https://modelcontextprotocol.io)
- [JSON-RPC 2.0 规范](https://www.jsonrpc.org/specification)
