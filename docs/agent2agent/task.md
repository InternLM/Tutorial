# Agent2Agent 多智能体协作 -- 闯关任务

## 任务说明

通关本课程需要完成以下 2 个任务。A2A 协议定义了 AI Agent 之间的协作方式，重点考察你实现 Agent 的能力以及设计多 Agent 系统的架构思维。

## 任务 1：实现一个 A2A Agent

**目标：** 独立实现一个 A2A Agent，包含完整的 Agent Card 定义和任务处理逻辑。

**要求：**

1. 使用 Python A2A SDK 实现 Agent
2. 编写完整的 Agent Card，包含：
   - 准确的名称和描述
   - 至少 2 个 Skill 定义
   - 能力声明（streaming、pushNotifications）
3. 实现 Task 处理逻辑：
   - 能正确解析收到的消息
   - 根据不同的输入返回不同的结果
   - 包含错误处理（输入为空、格式错误等）
4. Agent 启动后，可以通过 HTTP 访问 `/.well-known/agent.json` 获取 Agent Card
5. 可以通过 JSON-RPC 调用 `tasks/send` 提交任务并获取结果

**Agent 主题建议（任选其一或自拟）：**

- **代码分析 Agent**：接收代码片段，返回复杂度分析和改进建议
- **数据处理 Agent**：接收 CSV/JSON 数据，返回统计摘要
- **知识问答 Agent**：接收问题，从预设知识库中检索答案
- **格式转换 Agent**：接收文本，支持 Markdown/HTML/纯文本互转

**提交：**

- 代码：Agent 完整源码（含 Agent Card 定义和 Task Handler）
- 截图 1：访问 `/.well-known/agent.json` 返回的 Agent Card 内容
- 截图 2：向 Agent 发送任务并收到正确响应的过程

## 任务 2：搭建多 Agent 协作系统

**目标：** 搭建一个包含 2 个以上 Agent 的协作系统，实现任务的分发和结果聚合。

**要求：**

1. 实现至少 2 个专业 Agent，各自负责不同的任务领域
2. 实现 1 个编排 Agent（Orchestrator），负责：
   - 接收用户的复杂请求
   - 将请求拆解为子任务
   - 将子任务分发给对应的专业 Agent
   - 聚合各 Agent 的结果并返回给用户
3. 系统能完成一个端到端的完整流程（从用户输入到最终输出）
4. 记录各 Agent 的调用顺序和中间结果

**系统设计建议（任选其一或自拟）：**

- **内容生产系统**：搜索 Agent + 摘要 Agent + 编排 Agent -> 生成调研报告
- **代码质量系统**：静态分析 Agent + 测试建议 Agent + 编排 Agent -> 质量报告
- **数据分析系统**：清洗 Agent + 统计 Agent + 编排 Agent -> 分析报告

**提交：**

- 代码：所有 Agent 的完整源码 + 客户端调用代码
- 截图 1：所有 Agent 启动后的终端输出
- 截图 2：完整协作流程的执行过程（显示编排 Agent 如何分发任务和聚合结果）
- 文档：一段 300 字以内的架构说明，包含：
  - 系统中各 Agent 的职责划分
  - Agent 之间的调用关系（建议画简单的流程图）
  - 选择这种架构的理由
