# Agent2Agent 多智能体协作

## 课程简介

Agent2Agent（A2A）是由 Google 发起的开放协议，定义了 AI Agent 之间互相发现、通信和协作的标准方式。如果说 MCP 解决的是「AI 与工具的连接」，A2A 解决的则是「AI 与 AI 的连接」。本课程讲解 A2A 协议的核心概念，带你用 Python SDK 实现 A2A Agent，并构建多 Agent 协作系统。

## 你将学到

- 理解 A2A 协议的设计目标和核心概念
- 掌握 Agent Card、Task、Message 的数据结构
- 理解 MCP 与 A2A 的互补关系
- 使用 Python SDK 实现 A2A Agent
- 开发 Agent 的任务处理逻辑
- 搭建多 Agent 协作系统

## A2A 协议概述

### 目标

理解 A2A 协议的设计动机、核心概念和典型应用场景。

### 内容

**为什么需要 A2A：**

随着 AI Agent 越来越多，一个复杂任务往往需要多个专业 Agent 协作完成。例如：

- 用户说「帮我调研竞品并生成分析报告」
- 这需要：搜索 Agent 收集信息 + 分析 Agent 做对比 + 写作 Agent 生成报告

如果每个 Agent 都是独立系统，它们之间如何发现彼此、分配任务、交换结果？A2A 协议就是为解决这个问题而设计的。

**核心概念：**

A2A 协议围绕三个核心概念构建：

**1. Agent Card（智能体名片）**

每个 Agent 通过一个 JSON 格式的 Agent Card 来描述自己。其他 Agent 读取这张名片就知道它能做什么、怎么调用。

```json
{
  "name": "research-agent",
  "description": "擅长信息搜索和资料整理的研究助手",
  "url": "http://localhost:8001",
  "version": "1.0.0",
  "capabilities": {
    "streaming": true,
    "pushNotifications": false
  },
  "skills": [
    {
      "id": "web-search",
      "name": "网络搜索",
      "description": "在互联网上搜索指定主题的信息并整理摘要"
    },
    {
      "id": "summarize",
      "name": "文档摘要",
      "description": "将长文档压缩为结构化摘要"
    }
  ]
}
```

Agent Card 通常发布在 `/.well-known/agent.json` 路径下，方便其他 Agent 自动发现。

**2. Task（任务）**

Task 是 Agent 之间协作的基本单位。一个 Agent 向另一个 Agent 发送 Task，对方处理后返回结果。

Task 有明确的生命周期：

```
submitted -> working -> completed
                    \-> failed
                    \-> canceled
```

**3. Message（消息）**

Message 是 Task 中的通信载体，包含具体的内容。每条 Message 有角色（user 或 agent）和一个或多个 Part（文本、文件、结构化数据等）。

**MCP 与 A2A 的互补关系：**

| 维度 | MCP | A2A |
|------|-----|-----|
| 连接对象 | AI <-> 工具/数据 | AI Agent <-> AI Agent |
| 协议角色 | Client-Server | Peer-to-Peer |
| 能力暴露 | Tools / Resources / Prompts | Skills（通过 Agent Card） |
| 典型场景 | 调用 API、读取数据库 | 多 Agent 任务分工 |
| 通信方式 | Stdio / HTTP+SSE | HTTP + JSON-RPC |

两者并不冲突。一个 A2A Agent 的内部实现完全可以使用 MCP 来调用工具。A2A 管的是 Agent 之间的协作，MCP 管的是 Agent 内部的工具调用。

## Python SDK 实现 A2A Agent

### 目标

使用 Python A2A SDK 实现一个完整的 Agent，包括 Agent Card 定义和任务处理。

### 内容

**安装依赖：**

```bash
pip install a2a-sdk uvicorn
```

**基本架构：**

一个 A2A Agent 由三部分组成：

1. **Agent Card**：声明身份和能力
2. **Task Handler**：处理收到的任务
3. **HTTP Server**：对外提供服务

**完整示例 -- 文本分析 Agent：**

```python
# text_analysis_agent.py
import json
import hashlib
from a2a.server.agent_execution import AgentExecution, RequestContext
from a2a.server.server import A2AServer
from a2a.types import (
    AgentCard,
    AgentCapabilities,
    AgentSkill,
    Task,
    TaskState,
    TaskStatus,
    Message,
    Part,
    TextPart,
    Role,
)


class TextAnalysisAgent(AgentExecution):
    """文本分析 Agent：接收文本，返回统计和分析结果"""

    async def execute(
        self, context: RequestContext, request: dict
    ) -> None:
        # 从请求中提取文本
        task_params = request.get("params", {})
        message = task_params.get("message", {})
        parts = message.get("parts", [])

        input_text = ""
        for part in parts:
            if part.get("type") == "text":
                input_text = part.get("text", "")
                break

        if not input_text:
            await context.send_status_update(
                state=TaskState.failed,
                message=self._make_message("错误：未收到文本内容"),
            )
            return

        # 执行分析
        analysis = self._analyze_text(input_text)

        # 返回结果
        await context.send_status_update(
            state=TaskState.completed,
            message=self._make_message(analysis),
        )

    def _analyze_text(self, text: str) -> str:
        """对文本进行多维度分析"""
        lines = text.split("\n")
        words = text.split()
        chars = len(text)
        chars_no_space = len(text.replace(" ", "").replace("\n", ""))

        # 词频统计（取前 10）
        word_freq: dict[str, int] = {}
        for word in words:
            clean = word.strip(".,;:!?\"'()[]{}").lower()
            if len(clean) > 1:
                word_freq[clean] = word_freq.get(clean, 0) + 1
        top_words = sorted(word_freq.items(), key=lambda x: -x[1])[:10]

        # 句子统计
        sentences = [s.strip() for s in text.replace("!", ".").replace("?", ".").split(".") if s.strip()]

        result_lines = [
            "=== 文本分析报告 ===",
            "",
            f"总字符数: {chars}",
            f"字符数(不含空格): {chars_no_space}",
            f"单词/词语数: {len(words)}",
            f"行数: {len(lines)}",
            f"句子数: {len(sentences)}",
            f"平均句长: {len(words) / max(len(sentences), 1):.1f} 词/句",
            "",
            "高频词 (Top 10):",
        ]
        for word, count in top_words:
            result_lines.append(f"  {word}: {count} 次")

        # 文本指纹
        text_hash = hashlib.md5(text.encode()).hexdigest()[:12]
        result_lines.append(f"\n文本指纹: {text_hash}")

        return "\n".join(result_lines)

    def _make_message(self, text: str) -> Message:
        return Message(
            role=Role.agent,
            parts=[TextPart(type="text", text=text)],
        )


def create_agent_card() -> AgentCard:
    """定义 Agent Card"""
    return AgentCard(
        name="text-analysis-agent",
        description="文本分析助手，提供字符统计、词频分析、文本指纹等功能",
        url="http://localhost:8001",
        version="1.0.0",
        capabilities=AgentCapabilities(
            streaming=False,
            pushNotifications=False,
        ),
        skills=[
            AgentSkill(
                id="text-analysis",
                name="文本分析",
                description="接收文本内容，返回多维度统计分析报告",
            ),
        ],
    )


def main():
    agent_card = create_agent_card()
    agent = TextAnalysisAgent()
    server = A2AServer(
        agent_card=agent_card,
        agent_execution=agent,
    )
    server.start(host="0.0.0.0", port=8001)


if __name__ == "__main__":
    main()
```

**启动 Agent：**

```bash
python text_analysis_agent.py
```

**调用 Agent（客户端代码）：**

```python
# client.py
import httpx
import json

A2A_URL = "http://localhost:8001"


def get_agent_card():
    """获取 Agent Card"""
    resp = httpx.get(f"{A2A_URL}/.well-known/agent.json")
    return resp.json()


def send_task(text: str):
    """向 Agent 发送分析任务"""
    payload = {
        "jsonrpc": "2.0",
        "method": "tasks/send",
        "id": "task-001",
        "params": {
            "id": "task-001",
            "message": {
                "role": "user",
                "parts": [{"type": "text", "text": text}],
            },
        },
    }
    resp = httpx.post(A2A_URL, json=payload)
    return resp.json()


if __name__ == "__main__":
    # 查看 Agent 能力
    card = get_agent_card()
    print(f"Agent: {card['name']}")
    print(f"Skills: {[s['name'] for s in card['skills']]}")
    print()

    # 发送分析任务
    sample = """
    人工智能正在深刻改变科学研究的方式。从蛋白质结构预测到药物发现，
    从气候模拟到材料设计，AI 已经成为科学家手中不可或缺的工具。
    书生大模型系列致力于推动 AI for Science 的发展，
    让每一位研究者都能便捷地使用最先进的 AI 技术。
    """
    result = send_task(sample)
    print(json.dumps(result, indent=2, ensure_ascii=False))
```

## 多 Agent 协作系统

### 目标

设计和实现一个包含多个 Agent 的协作系统，理解 Agent 之间的任务分发和结果聚合。

### 内容

**多 Agent 架构设计：**

一个典型的多 Agent 系统包含：

- **编排 Agent（Orchestrator）**：接收用户请求，拆解任务，分发给专业 Agent，聚合结果
- **专业 Agent**：各自负责一个领域的任务处理

```
用户请求
    |
    v
[编排 Agent]
    |
    +---> [搜索 Agent]   --> 搜索结果
    |
    +---> [分析 Agent]   --> 分析报告
    |
    +---> [写作 Agent]   --> 最终文档
    |
    v
聚合结果返回用户
```

**编排 Agent 实现：**

```python
# orchestrator.py
import httpx
import json
from a2a.server.agent_execution import AgentExecution, RequestContext
from a2a.server.server import A2AServer
from a2a.types import (
    AgentCard,
    AgentCapabilities,
    AgentSkill,
    Message,
    TextPart,
    Role,
    TaskState,
)


class OrchestratorAgent(AgentExecution):
    """编排 Agent：接收复杂请求，拆解并分发给专业 Agent"""

    def __init__(self, agent_registry: dict[str, str]):
        """
        agent_registry: Agent 名称到 URL 的映射
        例如: {"text-analysis": "http://localhost:8001",
               "translation": "http://localhost:8002"}
        """
        self.registry = agent_registry

    async def execute(
        self, context: RequestContext, request: dict
    ) -> None:
        task_params = request.get("params", {})
        message = task_params.get("message", {})
        parts = message.get("parts", [])

        input_text = ""
        for part in parts:
            if part.get("type") == "text":
                input_text = part.get("text", "")
                break

        results = []

        # 依次调用已注册的 Agent
        for agent_name, agent_url in self.registry.items():
            try:
                result = await self._call_agent(
                    agent_url, agent_name, input_text
                )
                results.append(f"--- {agent_name} ---\n{result}")
            except Exception as e:
                results.append(f"--- {agent_name} ---\n调用失败: {e}")

        combined = "\n\n".join(results)
        await context.send_status_update(
            state=TaskState.completed,
            message=Message(
                role=Role.agent,
                parts=[TextPart(type="text", text=combined)],
            ),
        )

    async def _call_agent(
        self, url: str, name: str, text: str
    ) -> str:
        """调用单个 Agent"""
        payload = {
            "jsonrpc": "2.0",
            "method": "tasks/send",
            "id": f"sub-{name}",
            "params": {
                "id": f"sub-{name}",
                "message": {
                    "role": "user",
                    "parts": [{"type": "text", "text": text}],
                },
            },
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload)
            data = resp.json()

        # 提取 Agent 返回的文本
        result = data.get("result", {})
        status = result.get("status", {})
        msg = status.get("message", {})
        resp_parts = msg.get("parts", [])
        for part in resp_parts:
            if part.get("type") == "text":
                return part["text"]
        return "(无文本返回)"


def main():
    agent_card = AgentCard(
        name="orchestrator",
        description="多 Agent 编排器，将复杂任务拆解并分发给专业 Agent 协作完成",
        url="http://localhost:8000",
        version="1.0.0",
        capabilities=AgentCapabilities(
            streaming=False, pushNotifications=False
        ),
        skills=[
            AgentSkill(
                id="orchestrate",
                name="任务编排",
                description="接收复杂请求，协调多个专业 Agent 完成任务",
            ),
        ],
    )

    agent = OrchestratorAgent(
        agent_registry={
            "text-analysis": "http://localhost:8001",
            # 添加更多 Agent...
        }
    )

    server = A2AServer(
        agent_card=agent_card,
        agent_execution=agent,
    )
    server.start(host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
```

**运行多 Agent 系统：**

```bash
# 终端 1：启动文本分析 Agent
python text_analysis_agent.py

# 终端 2：启动编排 Agent
python orchestrator.py

# 终端 3：发送请求
python client.py
```

## Agent 设计原则与最佳实践

### 目标

掌握设计高质量 A2A Agent 的原则和常见模式。

### 内容

**Agent Card 设计原则：**

1. **描述精确**：description 要准确反映 Agent 的能力边界，不夸大不模糊
2. **Skill 粒度适中**：每个 Skill 对应一个明确的任务类型，不要过于宽泛
3. **版本管理**：Agent 能力变更时更新版本号，便于客户端适配

**任务处理原则：**

1. **幂等性**：同一任务重复提交应得到相同结果
2. **超时处理**：长时间运行的任务要有超时机制
3. **状态反馈**：通过 Task 状态让调用方知道执行进度
4. **错误透明**：失败时返回清晰的错误信息，而不是静默失败

**多 Agent 系统设计模式：**

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| 串行流水线 | A -> B -> C，每个 Agent 处理后传给下一个 | 文本翻译 -> 校对 -> 排版 |
| 并行扇出 | Orchestrator 同时调用多个 Agent | 多维度分析同一份数据 |
| 层级委托 | Agent 遇到子问题时委托给专业 Agent | 复杂决策的分层处理 |
| 投票共识 | 多个 Agent 独立处理，取多数结果 | 需要高可靠性的场景 |

**安全注意事项：**

- Agent Card 中不要暴露内部实现细节
- Agent 之间的通信应验证来源身份
- 限制 Agent 的操作权限，遵循最小权限原则
- 对输入进行校验，防止注入攻击

## 参考资料

- [A2A 协议规范](https://github.com/google/a2a-protocol)
- [A2A Python SDK](https://github.com/google/a2a-python)
- [Google A2A 博客](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)
- [MCP 官方文档](https://modelcontextprotocol.io)
