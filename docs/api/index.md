> 本文档 AI + 社区共建中

# 书生大模型 API 文档

书生大模型 API 由上海人工智能实验室提供，兼容 OpenAI 和 Anthropic 协议，支持 Intern-S1-Pro、Intern-S1 等模型，开箱即用。

## 概览

| 配置项 | 说明 |
|--------|------|
| **Base URL** | `https://chat.intern-ai.org.cn/api/v1` |
| **获取方式** | 访问 [internlm.intern-ai.org.cn](https://internlm.intern-ai.org.cn/api/tokens) → 注册 → 获取 API Key |
| **支持模型** | `intern-s1-pro`, `intern-s1`, `internvl-latest` 等 |
| **兼容性** | OpenAI / Anthropic 协议兼容 |

书生大模型 API 同时兼容 OpenAI 和 Anthropic 协议接口，支持以下能力：

- **Chat Completions** — 多轮对话、文本生成（Intern-S1 / Intern-S1-Pro）
- **多模态理解** — 图片理解、文档分析（`internvl-latest`）
- **Function Calling** — 工具调用、Agent 场景


## 快速导航

| 文档 | 说明 |
|------|------|
| [快速开始](/docs/api/quickstart) | 5 分钟完成第一次 API 调用 |
| [认证鉴权](/docs/api/authentication) | API Key 获取与管理 |
| [Claude Code 接入](/docs/api/claude-code) | 在 Claude Code 中使用 Intern-S1-Pro |
| [OpenClaw 接入](/docs/api/openclaw) | 在 OpenClaw 中使用 Intern-S1-Pro |
| [更多 AI 编程工具](/docs/api/coding-tools) | OpenCode 等其他工具配置 |

## 兼容性

书生大模型 API 兼容 OpenAI SDK 和 Anthropic 协议，只需修改 `base_url` 和 `api_key` 即可使用：

### OpenAI 协议

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",
    base_url="https://chat.intern-ai.org.cn/api/v1"
)

response = client.chat.completions.create(
    model="intern-s1-pro",
    messages=[{"role": "user", "content": "你好"}]
)
print(response.choices[0].message.content)
```

### Anthropic 协议

```python
from anthropic import Anthropic

client = Anthropic(
    api_key="your-api-key",
    base_url="https://chat.intern-ai.org.cn"
)

message = client.messages.create(
    model="intern-s1-pro",
    max_tokens=1024,
    messages=[{"role": "user", "content": "你好"}]
)
print(message.content[0].text)
```
