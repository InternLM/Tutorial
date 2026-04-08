

> 本文档 AI + 社区共建中
# AI Agent 原理与架构

如果说大语言模型是一个"超级大脑"，那 AI Agent 就是给这个大脑装上了眼睛、手脚和工具箱——它不仅能思考，还能感知环境、做出决策并采取行动。

## 什么是 AI Agent？

AI Agent（智能体）是一个能够自主完成任务的系统。它的核心是一个**感知-决策-行动**的循环：

```
        ┌──────────────────────────┐
        │        环境 (Environment) │
        └────┬────────────────┬────┘
             │ 感知            │ 行动
             ▼                │
        ┌─────────┐    ┌─────┴─────┐
        │  观察    │    │   执行     │
        │ Observe  │    │  Execute   │
        └────┬────┘    └─────▲─────┘
             │               │
             ▼               │
        ┌──────────────────────────┐
        │     LLM 大脑 (决策中心)    │
        │  思考 → 规划 → 选择行动    │
        └──────────────────────────┘
```

## ReAct 范式

ReAct（Reasoning + Acting）是目前最经典的 Agent 设计范式，让模型交替进行**推理**和**行动**：

```python
# ReAct 循环的伪代码
def react_loop(question):
    history = []
    while not finished:
        # Thought: 模型进行推理
        thought = llm.think(question, history)

        # Action: 选择并执行工具
        action = llm.choose_action(thought)
        observation = execute_tool(action)

        # 将结果加入历史，继续循环
        history.append({
            "thought": thought,
            "action": action,
            "observation": observation
        })

    return llm.final_answer(history)
```

一个实际的 ReAct 执行过程：

```
问题：北京今天的气温是多少摄氏度？

Thought 1: 我需要查询北京的实时天气。
Action 1: search_weather(city="北京")
Observation 1: 北京今天晴，气温 22°C

Thought 2: 我已经获得了答案。
Answer: 北京今天的气温是 22 摄氏度。
```

## Agent 核心组件

一个完整的 Agent 系统由四大组件构成：

| 组件 | 作用 | 类比 |
|------|------|------|
| **LLM** | 核心推理引擎 | 大脑 |
| **Memory** | 存储上下文和历史 | 记忆 |
| **Tools** | 与外部世界交互 | 手和工具箱 |
| **Planning** | 任务分解与规划 | 思考策略 |

### Memory（记忆）

Agent 的记忆分为两类：

- **短期记忆**：当前对话的上下文（Context Window）
- **长期记忆**：持久化存储的经验和知识（向量数据库、文件等）

### Planning（规划）

面对复杂任务，Agent 会先制定计划再逐步执行：

```python
# 任务分解示例
task = "写一篇关于 Intern-S1-Pro 的技术博客"

plan = [
    "1. 搜索 Intern-S1-Pro 的最新技术资料",
    "2. 整理模型的核心特点和创新点",
    "3. 编写博客大纲",
    "4. 逐段撰写正文",
    "5. 检查和润色内容"
]
```

### Tools（工具）

工具是 Agent 的能力扩展，常见工具包括：

- **搜索引擎**：获取实时信息
- **代码执行器**：运行 Python 代码
- **文件操作**：读写本地文件
- **API 调用**：访问外部服务

## 书生生态中的 Agent

### Lagent

Lagent 是书生生态的轻量级 Agent 框架，支持快速搭建 Agent 应用：

```python
from lagent import ReAct, GPTAPI, ActionExecutor
from lagent.actions import WebBrowser, PythonInterpreter

# 配置工具
tools = ActionExecutor(
    actions=[WebBrowser(), PythonInterpreter()]
)

# 创建 ReAct Agent
agent = ReAct(
    llm=GPTAPI(model_type="internlm/internlm3-latest"),
    action_executor=tools
)

response = agent.chat("帮我计算斐波那契数列前 20 项的和")
```

### MindSearch

MindSearch 是基于 InternLM 的深度搜索引擎，它将搜索过程建模为一个多步 Agent 推理过程，能像人类研究者一样深度分析问题。

## 典型应用场景

| 场景 | Agent 能力 | 示例 |
|------|-----------|------|
| 智能客服 | 查询知识库 + 工单系统 | 自动处理退换货 |
| 代码助手 | 读写文件 + 执行代码 | Claude Code、OpenClaw、Cursor |
| 数据分析 | SQL 查询 + 可视化 | 自然语言分析数据库 |
| 研究助手 | 搜索 + 阅读 + 总结 | 文献调研、报告撰写 |

## 下一步

- 学习 [Function Calling 与 Tool Use](/zh/learn/function-calling)，掌握 Agent 调用工具的核心机制
- 了解 [RAG 基础](/zh/learn/rag-basics)，为 Agent 添加知识检索能力
- 探索 [Prompt Engineering](/zh/learn/prompt-engineering)，优化 Agent 的指令设计

## 进阶实践（Intern-S1-Pro 专题）

### 实战任务
1. 设计一个 Agent 工作流：需求拆解 -> 工具调用 -> 结果校验 -> 复盘。
2. 分别用 Agent Skills / OpenClaw / Claude Code 规划同一任务，比较流程差异。
3. 为 Agent 增加失败重试与人工接管策略，记录异常处理路径。

### 交付物
- 一份《Agent 工作流设计图》
- 一份《三种工具链协作对比报告》

### 自检清单
- [ ] 能把复杂任务拆成可执行子任务
- [ ] 能为每个工具定义清晰输入输出约束
- [ ] 能设计可观测、可回滚的执行流程
