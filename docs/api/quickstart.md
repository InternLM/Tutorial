

> 本文档 AI + 社区共建中
# 快速开始

本指南帮助你在 5 分钟内完成第一次 书生大模型 API 调用。

## 前置条件

- 一个有效的 API Key（[获取方法](/docs/api/authentication)）
- Python 3.8+ 或 Node.js 18+（或 cURL）

## 步骤 1：安装 SDK

### Python

```bash
pip install openai
```

### Node.js

```bash
npm install openai
```

## 步骤 2：发送第一条消息

官方 API 由上海 AI 实验室提供，支持 Intern-S1、Intern-S1-Pro 等模型，适合生产环境和企业级场景。

### Python 示例

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-official-api-key",
    base_url="https://chat.intern-ai.org.cn/api/v1"
)

response = client.chat.completions.create(
    model="intern-s1-pro",
    messages=[
        {"role": "system", "content": "你是书生大模型，一个有用的 AI 助手。"},
        {"role": "user", "content": "你好！请介绍一下自己。"}
    ],
    temperature=0.7,
    max_tokens=1024
)

print(response.choices[0].message.content)
```

### cURL 示例

```bash
curl -X POST https://chat.intern-ai.org.cn/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-official-api-key" \
  -d '{
    "model": "intern-s1-pro",
    "messages": [
      {"role": "system", "content": "你是书生大模型，一个有用的 AI 助手。"},
      {"role": "user", "content": "你好！请介绍一下自己。"}
    ],
    "temperature": 0.7,
    "max_tokens": 1024
  }'
```

### Node.js 示例

```typescript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: 'your-official-api-key',
  baseURL: 'https://chat.intern-ai.org.cn/api/v1',
});

async function main() {
  const response = await client.chat.completions.create({
    model: 'intern-s1-pro',
    messages: [
      { role: 'system', content: '你是书生大模型，一个有用的 AI 助手。' },
      { role: 'user', content: '你好！请介绍一下自己。' },
    ],
    temperature: 0.7,
    max_tokens: 1024,
  });

  console.log(response.choices[0].message.content);
}

main();
```

## 步骤 3：查看响应

成功调用后，你会收到类似如下的 JSON 响应：

```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "model": "intern-s1-pro",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "你好！我是书生大模型（InternLM），..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 28,
    "completion_tokens": 156,
    "total_tokens": 184
  }
}
```

## 可用模型一览

| 模型 | 类型 | 上下文长度 | 适用场景 |
|------|------|-----------|---------|
| `intern-s1-pro` | 语言模型 | 32K | Intern-S1-Pro，推荐使用 |
| `intern-s1` | 语言模型 | 32K | Intern-S1，科学多模态大模型 |
| `internvl-latest` | 多模态模型 | 32K | 多模态最新版本 |
| 更多模型请查阅官方文档 | | | |

## 常用参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `model` | string | *必填* | 模型名称 |
| `messages` | array | *必填* | 对话消息列表 |
| `temperature` | float | 0.7 | 控制随机性，0-2 之间 |
| `max_tokens` | int | 1024 | 最大生成 Token 数 |
| `stream` | bool | false | 是否启用流式输出 |
| `top_p` | float | 1.0 | 核采样参数 |

---

## 下一步

- 了解 [认证鉴权](/docs/api/authentication) 的详细配置
- 在 [Claude Code](/docs/api/claude-code) 中接入 Intern-S1-Pro 进行 AI 编程
- 探索流式输出、Function Calling 等高级特性
