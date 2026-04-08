
# Agent2Agent (A2A) 协议

> **前置知识**：建议先学习 [AI Agent 原理与架构](/zh/docs/learn/core/ai-agent) 和 [MCP 协议](/zh/docs/learn/core/mcp-protocol)

## 什么是 Agent2Agent？

Agent2Agent (A2A) 是 Google 于 2025 年 4 月发布的开放协议，解决的核心问题是：**不同厂商、不同框架构建的 AI Agent 之间如何互相通信、协作和交接任务**。

打个比方：
- **MCP** 解决的是「Agent 如何使用工具」——类似给 Agent 装上手和脚
- **A2A** 解决的是「Agent 如何与其他 Agent 对话」——类似给 Agent 装上嘴和耳朵

两者是互补关系，不是竞争关系。

## 为什么需要 A2A？

在实际企业场景中，一个复杂任务往往需要多个专业 Agent 协作：

| 场景 | 涉及的 Agent | 协作方式 |
|------|-------------|---------|
| 招聘流程 | HR Agent + 技术面试 Agent + 背调 Agent | 顺序交接 |
| 客服升级 | 一线客服 Agent + 专家 Agent + 工单 Agent | 条件路由 |
| 数据分析 | 数据采集 Agent + 清洗 Agent + 可视化 Agent | 流水线 |
| 科研协作 | 文献检索 Agent + 实验设计 Agent + 论文撰写 Agent | 迭代协作 |

如果每对 Agent 之间都要写定制的通信代码，N 个 Agent 就需要 N×(N-1) 个适配器。A2A 提供统一协议，让任何 Agent 都能「即插即用」地与其他 Agent 通信。

## A2A 核心概念

### Agent Card（智能体名片）

每个 A2A Agent 都有一张「名片」，描述自己的能力：

```json
{
  "name": "科研文献助手",
  "description": "检索、分析和总结学术论文",
  "url": "https://scholar-agent.example.com",
  "capabilities": {
    "streaming": true,
    "pushNotifications": true
  },
  "skills": [
    {
      "id": "paper-search",
      "name": "论文检索",
      "description": "根据关键词检索 arXiv、Google Scholar 等数据库"
    },
    {
      "id": "paper-summary",
      "name": "论文摘要",
      "description": "阅读论文全文并生成结构化摘要"
    }
  ]
}
```

Agent Card 通常托管在 `/.well-known/agent.json`，其他 Agent 可以自动发现。

### Task（任务）

A2A 中的核心交互单元。一个 Task 有明确的生命周期：

```
submitted → working → input-required → completed / failed / canceled
```

- **submitted**：任务已提交
- **working**：Agent 正在处理
- **input-required**：Agent 需要更多信息（支持多轮交互）
- **completed**：任务完成
- **failed / canceled**：任务失败或取消

### Message & Part

Agent 之间的对话由 Message 组成，每个 Message 包含多个 Part：

```json
{
  "role": "user",
  "parts": [
    { "type": "text", "text": "分析这篇论文的创新点" },
    { "type": "file", "file": { "name": "paper.pdf", "mimeType": "application/pdf", "bytes": "..." } }
  ]
}
```

Part 支持文本、文件和结构化 JSON 数据，灵活表达各种信息。

## A2A 通信模式

### 1. 同步请求/响应

最简单的模式，适合快速任务：

```
Client Agent → POST /tasks/send → Server Agent
              ← 200 OK (结果) ←
```

### 2. 流式响应 (SSE)

适合长时间任务，实时返回进度：

```
Client Agent → POST /tasks/sendSubscribe → Server Agent
              ← SSE: status update ←
              ← SSE: partial result ←
              ← SSE: final result   ←
```

### 3. 异步推送通知

适合耗时很长的任务（几分钟到几小时）：

```
Client Agent → POST /tasks/send → Server Agent
              ← 202 Accepted ←
              ... (Server 处理中) ...
Server Agent → POST callback URL → Client Agent (推送结果)
```

## A2A vs MCP 对比

| 维度 | MCP | A2A |
|------|-----|-----|
| 解决的问题 | Agent ↔ 工具/数据源 | Agent ↔ Agent |
| 通信对象 | 被动的工具服务 | 主动的智能体 |
| 交互模式 | 单次调用 | 多轮对话 |
| 发起方 | 总是 Agent 发起 | 双方都可发起 |
| 状态管理 | 无状态 | 有状态（Task 生命周期） |
| 典型场景 | 查数据库、调 API | 任务委派、协作决策 |
| 发起者 | Anthropic | Google |
| 标准组织 | — | Linux Foundation |

**最佳实践**：同时使用 MCP（连接工具）+ A2A（连接其他 Agent），构建完整的多 Agent 系统。

## 行业支持

A2A 已获得 50+ 技术合作伙伴支持，并已捐赠给 Linux Foundation：

- **云厂商**：Google Cloud、Salesforce、SAP
- **AI 框架**：LangChain、Cohere
- **企业应用**：Atlassian、Box、Intuit、PayPal、ServiceNow、Workday
- **数据库**：MongoDB

## 实战：用 Intern-S1-Pro 构建 A2A Agent

### 基本架构

```
用户 → 主控 Agent (Intern-S1-Pro) → A2A → 文献 Agent
                                   → A2A → 数据分析 Agent
                                   → A2A → 可视化 Agent
```

### 关键步骤

1. **定义 Agent Card**：声明你的 Agent 能力
2. **实现 Task 处理**：接收任务、处理、返回结果
3. **注册发现**：将 Agent Card 发布到可发现的位置
4. **集成 MCP**：Agent 内部用 MCP 连接工具，对外用 A2A 通信

### 代码示例（Python）

```python
from a2a import A2AServer, AgentCard, Task, Message, TextPart

# 定义 Agent Card
card = AgentCard(
    name="科研助手",
    description="基于 Intern-S1-Pro 的科研辅助 Agent",
    skills=[
        {"id": "literature-review", "name": "文献综述", "description": "生成指定领域的文献综述"}
    ]
)

# 创建 A2A Server
server = A2AServer(card)

@server.on_task
async def handle_task(task: Task) -> Task:
    user_message = task.messages[-1]
    
    # 调用 Intern-S1-Pro 处理任务
    response = await call_intern_s1_pro(user_message.parts[0].text)
    
    task.messages.append(Message(
        role="agent",
        parts=[TextPart(text=response)]
    ))
    task.status = "completed"
    return task

server.run(port=8080)
```

## 进阶实践（Intern-S1-Pro 专题）

### 实操任务

1. **搭建 A2A 服务**：用 Intern-S1-Pro 实现一个具有 A2A 接口的 Agent
2. **多 Agent 编排**：构建 2-3 个专业 Agent，通过 A2A 协作完成一个复杂任务
3. **MCP + A2A 融合**：Agent 内部用 MCP 连接工具，对外用 A2A 接收任务

### 交付物

- A2A Agent 服务代码 + Agent Card 定义
- 多 Agent 协作流程图
- 性能对比报告：单 Agent vs 多 Agent 协作

### 自检清单

- [ ] 理解 A2A 与 MCP 的互补关系
- [ ] 能解释 Task 的生命周期状态转换
- [ ] 能用 Agent Card 描述一个 Agent 的能力
- [ ] 实现了至少一个 A2A Agent 服务
- [ ] 测试了两个 Agent 之间的通信

## 延伸阅读

- [A2A 官方文档](https://a2a-protocol.org/latest/)
- [A2A GitHub 仓库](https://github.com/a2aproject/A2A)
- [Google Blog: A2A 发布公告](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)
- [AI Agent 原理与架构](/zh/docs/learn/core/ai-agent)
- [MCP 协议详解](/zh/docs/learn/core/mcp-protocol)
