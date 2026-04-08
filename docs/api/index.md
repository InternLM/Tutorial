
# 书生系列大模型 API 文档

欢迎使用书生大模型 API！通过 API 你可以快速将书生大模型的能力集成到你的应用中。

目前有两种途径获取书生大模型 API 服务：**社区 API** 和 **官方 API**，两者均兼容 OpenAI SDK。

## 两种 API 对比

| | 社区 API | 官方 API |
|------|----------|----------|
| **提供方** | 书生社区 (community.intern-ai.org.cn) | 上海 AI 实验室官方 |
| **Base URL** | `https://community.intern-ai.org.cn/api/v1` | `https://chat.intern-ai.org.cn/api/v1` |
| **API Key 格式** | `sk-intern-XXXXXXXX_XXXX...` | 官方平台分配 |
| **获取方式** | 登录社区 → 个人中心 → API 密钥 Tab → 创建密钥 | 访问 [internlm.intern-ai.org.cn](https://internlm.intern-ai.org.cn/api/document) → 注册 → 获取 API Key |
| **支持模型** | `intern-s1-pro`, `intern-s1`, `internlm3-latest`(别名) | `intern-s1-pro`, `intern-s1`, `internvl-latest` 等 |
| **免费额度** | 每日 10K tokens 免费体验 | 注册后获得免费额度 |
| **付费方式** | 积分购买流量包 | 官方计费方案 |
| **特点** | 社区维护，免费体验，积分流量包制 | 官方运维，更多模型，企业级服务 |
| **兼容性** | OpenAI SDK 兼容 | OpenAI SDK 兼容 |

> **如何选择？**
> - 想快速免费体验 Intern-S1 系列 → 选社区 API
> - 需要 InternVL 多模态理解，或需要企业级稳定性 → 选官方 API

## 概览

书生大模型 API 提供与 OpenAI 兼容的接口，支持以下能力：

- **Chat Completions** — 多轮对话、文本生成（Intern-S1 / Intern-S1-Pro）
- **多模态理解** — 图片理解、文档分析（官方 API: `internvl-latest`）
- **Function Calling** — 工具调用、Agent 场景

此外，社区 [Playground](/playground) 提供 InternVL-U 在线体验（对话、AI 绘画、图片编辑），使用 Cookie 登录态而非 API Key。

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

两种 API 均兼容 OpenAI SDK，只需修改 `base_url` 和 `api_key` 即可切换：

```python
from openai import OpenAI

# 社区 API
client = OpenAI(
    api_key="sk-intern-xxxxxxxx_xxxxxxxxxxxxxxxxxxxxxxxx",
    base_url="https://community.intern-ai.org.cn/api/v1"
)

# 官方 API
client = OpenAI(
    api_key="your-official-api-key",
    base_url="https://chat.intern-ai.org.cn/api/v1"
)
```
