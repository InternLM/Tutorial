
# AI 技术基础

从零开始系统学习 AI，为使用和开发大语言模型打下坚实基础。涵盖基础概念、核心技术、进阶应用和工程实践四大层次，当前中文 17 篇核心教程（双语共 35 篇）。

> **开发中提示**：第 7 期书生大模型实战营「Skills / MCP / Claude Code / A2A / InternVL-U / InternSVG / OpenClaw」专题内容正在完善中，教程会持续更新。

## 教程审阅结论（本轮）

本轮已完成 `/zh/docs/learn` 全量教程结构审阅，并统一补充“进阶实践（Intern-S1-Pro 专题）”模块，重点增强三类能力：

- **从概念到实操**：每篇教程新增可执行任务，避免“只看懂、做不出”  
- **从学习到交付**：每篇教程新增交付物要求，便于沉淀作品集  
- **从完成到复盘**：每篇教程新增自检清单，支持自评与同伴评审

## 详细学习法（建议 4 周）

### 第 1 周：基础理解（概念正确）

- 重点教程：什么是大语言模型、Tokenization、Embedding、Attention、Transformer
- 目标：建立统一术语与核心机制认知
- 周交付：完成 1 份《LLM 基础概念图谱》

### 第 2 周：能力构建（会调会用）

- 重点教程：Prompt Engineering、RAG、Function Calling、AI Agent
- 目标：掌握“提示词 + 检索 + 工具调用 + 任务编排”的最小闭环
- 周交付：完成 1 个可运行的 Agent Demo（含至少 2 个工具）

### 第 3 周：模型工程（会训会改）

- 重点教程：Pretraining、SFT、RLHF/DPO、LoRA、Quantization
- 目标：理解训练对齐与部署优化全链路
- 周交付：完成 1 份《微调与部署选型报告》

### 第 4 周：质量与安全（可评可控）

- 重点教程：Evaluation Benchmarks、Model Safety、VLM
- 目标：建立评测体系与安全护栏能力
- 周交付：完成 1 份《模型评测 + 安全红队报告》

## 学习验收标准

- **准确性**：关键概念解释无明显错误
- **可复现性**：至少 3 个实战任务可被他人复现
- **可交付性**：至少形成 2 份结构化文档交付物
- **可迭代性**：能根据评测结果优化 Prompt / 检索 / 工具调用策略

## 适合谁？

- **AI 新手**：没有机器学习背景，想入门大模型领域
- **开发者**：有编程经验，想深入理解 AI 技术并动手实践
- **产品经理**：想理解 AI 能力边界，做出更好的产品决策
- **学生**：正在学习 AI 相关课程，需要系统化的知识补充

## 推荐学习路径

根据你的背景和目标，选择一条适合的路径开始学习。

### 路径一：AI 入门者

适合零基础读者，从概念到实操，约 3 小时完成。

| 顺序 | 教程 | 预计时间 |
|------|------|---------|
| 1 | [什么是大语言模型](/zh/docs/learn/concepts/what-is-llm) | 15 分钟 |
| 2 | [Tokenization：模型如何理解文字](/zh/docs/learn/concepts/tokenization) | 15 分钟 |
| 3 | [Embedding 与词向量](/zh/docs/learn/concepts/embedding) | 20 分钟 |
| 4 | [注意力机制详解](/zh/docs/learn/concepts/attention-mechanism) | 25 分钟 |
| 5 | [Transformer 架构](/zh/docs/learn/concepts/transformer) | 30 分钟 |
| 6 | [Prompt Engineering](/zh/docs/learn/core/prompt-engineering) | 20 分钟 |
| 7 | [RAG 基础](/zh/docs/learn/core/rag-basics) | 25 分钟 |

### 路径二：AI 开发者

适合有编程基础的开发者，覆盖训练到部署全链路，约 4.5 小时完成。

| 顺序 | 教程 | 预计时间 |
|------|------|---------|
| 1 | [什么是大语言模型](/zh/docs/learn/concepts/what-is-llm) | 15 分钟 |
| 2 | [Transformer 架构](/zh/docs/learn/concepts/transformer) | 30 分钟 |
| 3 | [预训练：从零训练大模型](/zh/docs/learn/training/pretraining) | 25 分钟 |
| 4 | [SFT 有监督微调](/zh/docs/learn/training/sft) | 20 分钟 |
| 5 | [RLHF 与 DPO：人类偏好对齐](/zh/docs/learn/training/rlhf) | 25 分钟 |
| 6 | [LoRA 与参数高效微调](/zh/docs/learn/training/lora) | 20 分钟 |
| 7 | [视觉语言模型 (VLM)](/zh/docs/learn/multimodal/vlm) | 25 分钟 |
| 8 | [AI Agent 原理与架构](/zh/docs/learn/core/ai-agent) | 25 分钟 |
| 9 | [Function Calling 与 Tool Use](/zh/docs/learn/core/function-calling) | 20 分钟 |
| 10 | [模型量化：GPTQ/AWQ/GGUF](/zh/docs/learn/training/model-quantization) | 25 分钟 |

### 路径三：AI 产品经理

适合非技术背景的产品和决策者，理解 AI 能力边界，约 3 小时完成。

| 顺序 | 教程 | 预计时间 |
|------|------|---------|
| 1 | [什么是大语言模型](/zh/docs/learn/concepts/what-is-llm) | 15 分钟 |
| 2 | [Prompt Engineering](/zh/docs/learn/core/prompt-engineering) | 20 分钟 |
| 3 | [RAG 基础](/zh/docs/learn/core/rag-basics) | 25 分钟 |
| 4 | [AI Agent 原理与架构](/zh/docs/learn/core/ai-agent) | 25 分钟 |
| 5 | [Function Calling 与 Tool Use](/zh/docs/learn/core/function-calling) | 20 分钟 |
| 6 | [评测基准：MMLU、GSM8K、HumanEval 等](/zh/docs/learn/core/evaluation-benchmarks) | 20 分钟 |
| 7 | [模型安全：幻觉、对齐与 Red Teaming](/zh/docs/learn/core/model-safety) | 25 分钟 |

## 专题任务（开发中）

围绕 S7「Skills / MCP / Claude Code / A2A / InternVL-U / InternSVG / OpenClaw」的 7 大方向学习任务如下：

| 任务 | 学习目标 | 推荐教程 |
|------|----------|---------|
| 任务 1：MCP 协议实战 | 开发一个 MCP Server，配置 Claude Code 调用 | [MCP 协议详解](/zh/docs/learn/core/mcp-protocol)、[Function Calling](/zh/docs/learn/core/function-calling) |
| 任务 2：Skills 自定义与自进化 | 编写自定义 Skill，实现自动化工作流 | [AI Agent 原理与架构](/zh/docs/learn/core/ai-agent)、[MCP 协议详解](/zh/docs/learn/core/mcp-protocol) |
| 任务 3：A2A 多 Agent 协作 | 理解 Agent Card、Task 状态机，实现 Agent 间通信 | [Agent2Agent 协议](/zh/docs/learn/core/agent2agent)、[AI Agent 原理与架构](/zh/docs/learn/core/ai-agent) |
| 任务 4：InternVL-U 多模态实验 | 多模态理解 + 图像生成 + 图片编辑 | [视觉语言模型](/zh/docs/learn/multimodal/vlm)、[文生图](/zh/docs/learn/multimodal/text-to-image) |
| 任务 5：InternSVG 矢量图形 | SVG 生成与编辑任务 | [InternSVG](/zh/docs/learn/multimodal/internsvg)、[视觉语言模型](/zh/docs/learn/multimodal/vlm) |
| 任务 6：Claude Code 全流程 | 用 Claude Code 完成完整项目开发 | [AI Agent 原理与架构](/zh/docs/learn/core/ai-agent)、[Prompt Engineering](/zh/docs/learn/core/prompt-engineering) |
| 任务 7：OpenClaw 开源协作 | 多平台 AI 开发环境集成 | [RAG 基础](/zh/docs/learn/core/rag-basics)、[评测基准](/zh/docs/learn/core/evaluation-benchmarks) |

---

## 按分类浏览

### 基础概念

零基础入门，理解大模型的核心概念。

| 教程 | 说明 | 预计时间 |
|------|------|---------|
| [什么是大语言模型](/zh/docs/learn/concepts/what-is-llm) | LLM 的基本概念、工作原理和应用场景 | 15 分钟 |
| [Tokenization：模型如何理解文字](/zh/docs/learn/concepts/tokenization) | Token 切分、BPE 算法、词表构建 | 15 分钟 |
| [Embedding 与词向量](/zh/docs/learn/concepts/embedding) | 文本向量化、语义空间、相似度计算 | 20 分钟 |
| [注意力机制详解](/zh/docs/learn/concepts/attention-mechanism) | Self-Attention、QKV 计算、注意力可视化 | 25 分钟 |

### 应用技巧

学会高效使用大模型。

| 教程 | 说明 | 预计时间 |
|------|------|---------|
| [Prompt Engineering](/zh/docs/learn/core/prompt-engineering) | 系统提示、少样本学习、思维链 | 20 分钟 |
| [RAG 基础](/zh/docs/learn/core/rag-basics) | 检索增强生成的原理、架构与实践 | 25 分钟 |

### 模型架构

理解大模型的技术原理。

| 教程 | 说明 | 预计时间 |
|------|------|---------|
| [Transformer 架构](/zh/docs/learn/concepts/transformer) | 自注意力、多头注意力、位置编码、Decoder-Only | 30 分钟 |

### 训练与对齐

了解大模型是怎么训练出来的。

| 教程 | 说明 | 预计时间 |
|------|------|---------|
| [预训练：从零训练大模型](/zh/docs/learn/training/pretraining) | 预训练目标、数据准备、训练流程 | 25 分钟 |
| [SFT 有监督微调](/zh/docs/learn/training/sft) | 指令微调、数据格式、XTuner 实践 | 20 分钟 |
| [RLHF 与 DPO：人类偏好对齐](/zh/docs/learn/training/rlhf) | 奖励模型、PPO、DPO 直接偏好优化 | 25 分钟 |
| [LoRA 与参数高效微调](/zh/docs/learn/training/lora) | 低秩适配、QLoRA、适用场景 | 20 分钟 |

### 多模态

超越文本，理解图像、语音、视频等多模态能力。

| 教程 | 说明 | 预计时间 |
|------|------|---------|
| [视觉语言模型 (VLM)](/zh/docs/learn/multimodal/vlm) | 图文理解、InternVL 架构、应用场景 | 25 分钟 |
| [文生图：AI 图像生成基础](/zh/docs/learn/multimodal/text-to-image) | 扩散模型原理、Prompt 技巧、InternVL-U 实战 | 25 分钟 |
| [图片编辑：AI 编辑图像基础](/zh/docs/learn/multimodal/image-editing) | 局部编辑、风格迁移、IP 形象变换 | 20 分钟 |
| [文生视频：AI 视频生成基础](/zh/docs/learn/multimodal/text-to-video) | Sora/Wan2.2/DreamID-Omni、Prompt 技巧 | 25 分钟 |
| [InternSVG：AI 矢量图形生成](/zh/docs/learn/multimodal/internsvg) | 文本/图片生成、编辑和理解 SVG 矢量图形 | 20 分钟 |

### Agent 与应用

让大模型真正做事。

| 教程 | 说明 | 预计时间 |
|------|------|---------|
| [AI Agent 原理与架构](/zh/docs/learn/core/ai-agent) | Agent 架构、规划与推理、记忆机制 | 25 分钟 |
| [Function Calling 与 Tool Use](/zh/docs/learn/core/function-calling) | 工具调用、JSON Schema、实践示例 | 20 分钟 |
| [MCP 协议详解](/zh/docs/learn/core/mcp-protocol) | AI 世界的 USB 接口，让大模型连接一切工具和数据 | 25 分钟 |
| [Agent2Agent (A2A) 协议](/zh/docs/learn/core/agent2agent) | Agent 间通信与协作，Task 状态机、Agent Card | 25 分钟 |

### 部署与推理

把模型跑起来。

| 教程 | 说明 | 预计时间 |
|------|------|---------|
| [模型量化：GPTQ/AWQ/GGUF](/zh/docs/learn/training/model-quantization) | 量化原理、主流方案对比、LMDeploy 实践 | 25 分钟 |
| [在昇腾 NPU 上部署 InternVL-U](/zh/docs/learn/tutorials/ascend-internvl-u) | SDPA Patch、API 服务搭建、公网代理 | 30 分钟 |

### 评测与数据

衡量和驱动模型质量。

| 教程 | 说明 | 预计时间 |
|------|------|---------|
| [评测基准：MMLU、GSM8K、HumanEval 等](/zh/docs/learn/core/evaluation-benchmarks) | 主流 Benchmark 介绍与解读 | 20 分钟 |
| [模型安全：幻觉、对齐与 Red Teaming](/zh/docs/learn/core/model-safety) | 幻觉问题、安全对齐、红队测试 | 25 分钟 |
