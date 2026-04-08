
# 书生系列大模型 API 文档

欢迎使用书生大模型 API！通过 API 你可以快速将书生大模型的能力集成到你的应用中。

书生大模型 API 由上海 AI 实验室官方提供，兼容 OpenAI SDK。

## 概览

| 配置项 | 值 |
|--------|-----|
| **提供方** | 上海 AI 实验室官方 |
| **Base URL** | `https://chat.intern-ai.org.cn/api/v1` |
| **获取方式** | 访问 [internlm.intern-ai.org.cn](https://internlm.intern-ai.org.cn/api/document) → 注册 → 获取 API Key |
| **支持模型** | `intern-s1-pro`, `intern-s1`, `internvl-latest` 等 |
| **兼容性** | OpenAI SDK 兼容 |

书生大模型 API 提供与 OpenAI 兼容的接口，支持以下能力：

- **Chat Completions** — 多轮对话、文本生成（Intern-S1 / Intern-S1-Pro）
- **多模态理解** — 图片理解、文档分析（`internvl-latest`）
- **Function Calling** — 工具调用、Agent 场景

## 快速导航

| 文档 | 说明 |
|------|------|
| [快速开始](/docs/api/quickstart) | 5 分钟完成第一次 API 调用 |
| [认证鉴权](/docs/api/authentication) | API Key 获取与管理 |
| [InternLM3 模型](/docs/api/models/internlm3) | InternLM3 系列模型参数与用法 |
| [InternVL 模型](/docs/api/models/internvl3) | InternVL 多模态模型参数与用法 |
| [Claude Code 接入](/docs/api/claude-code) | 在 Claude Code 中使用 Intern-S1-Pro |
| [OpenClaw 接入](/docs/api/openclaw) | 在 OpenClaw 中使用 Intern-S1-Pro |
| [更多 AI 编程工具](/docs/api/coding-tools) | OpenCode 等其他工具配置 |

## 兼容性

书生大模型 API 兼容 OpenAI SDK，只需修改 `base_url` 和 `api_key` 即可使用：

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",
    base_url="https://chat.intern-ai.org.cn/api/v1"
)
```
