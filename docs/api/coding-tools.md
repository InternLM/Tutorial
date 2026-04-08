

> 本文档 AI + 社区共建中
# AI 编程工具接入

书生大模型 API 兼容 OpenAI 接口，可以接入主流 AI 编程工具。

## 通用配置信息

| 配置项 | 值 |
|--------|-----|
| API Base URL | `https://chat.intern-ai.org.cn/api/v1` |
| 协议 | OpenAI Chat Completions |
| 推荐模型 | `intern-s1-pro`、`internvl-latest` |
| API Key | 在 [认证鉴权](/docs/api/authentication) 中获取 |

---

## Claude Code

[Claude Code](https://github.com/anthropics/claude-code) 是 Anthropic 官方 CLI 编程助手，通过 `ANTHROPIC_BASE_URL` + `ANTHROPIC_AUTH_TOKEN` 环境变量接入 Intern-S1-Pro，使用 `claude --model intern-s1-pro` 启动。

**👉 [查看 Claude Code 完整接入指南](/docs/api/claude-code)**

---

## OpenClaw

[OpenClaw](https://github.com/openclaw/openclaw) 是开源个人 AI Agent，通过 `models.providers` 配置即可接入 Intern-S1-Pro。

**👉 [查看 OpenClaw 完整接入指南](/docs/api/openclaw)**

---

## OpenCode

[OpenCode](https://github.com/opencode-ai/opencode) 是开源终端 AI 编程助手，原生支持 OpenAI 兼容 API，可直接配置 InternLM 作为 Provider。

---

## 其他工具

任何支持 OpenAI 兼容 API 的工具都可以接入 InternLM：

```bash
export OPENAI_API_KEY="your-api-key"
export OPENAI_BASE_URL="https://chat.intern-ai.org.cn/api/v1"
```

---

## 下一步

- 查看 [认证鉴权](/docs/api/authentication) 获取 API Key
- 了解 [InternLM3](/docs/api/models/internlm3) 和 [InternVL](/docs/api/models/internvl3) 的模型详情
- 查看 [快速开始](/docs/api/quickstart) 了解 API 基础用法
