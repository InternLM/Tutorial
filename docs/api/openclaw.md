

> 本文档 AI + 社区共建中
# OpenClaw 接入 Intern-S1-Pro

[OpenClaw](https://github.com/openclaw/openclaw) 是一款开源的个人 AI 助手，运行在你自己的设备上，数据完全私有。它支持通过 WhatsApp、Telegram、微信等消息平台作为交互入口，并具备浏览网页、读写文件、执行代码等能力。

## 为什么选择 OpenClaw？

| 特性 | 说明 |
|------|------|
| 开源免费 | MIT 协议，GitHub 15,000+ Stars |
| 隐私优先 | 数据存储在你自己的设备上 |
| 多平台 | 支持 20+ 消息平台（微信、Telegram、Slack 等） |
| 全能助手 | 浏览网页、读写文件、执行代码、语音交互 |
| 模型灵活 | 支持 Claude、OpenAI、本地模型和 Intern-S1-Pro |

## 第一步：安装 OpenClaw

```bash
# 克隆仓库
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# 安装依赖
npm install

# 复制配置文件
cp .env.example .env
```

## 第二步：获取 Intern-S1-Pro API Key

前往书生大模型官方平台获取 API Token：

**[https://internlm.intern-ai.org.cn/api/document](https://internlm.intern-ai.org.cn/api/document?lang=zh)**

1. 注册并登录书生大模型平台
2. 进入 API 管理页面
3. 创建新的 API Key 并妥善保存

## 第三步：配置模型

编辑 OpenClaw 配置文件，添加 Intern-S1-Pro 作为模型 Provider：

```yaml
# config.yaml
models:
  providers:
    - name: intern-s1-pro
      type: openai-compatible
      base_url: https://chat.intern-ai.org.cn/api/v1
      api_key: your-api-key-here
      model: intern-s1-pro
      max_tokens: 8192
```

### 可用模型

| 模型 | 说明 | 推荐场景 |
|------|------|---------|
| `intern-s1-pro` | 科学多模态大模型（推荐） | 科研、数学、编程 |
| `intern-s1` | 标准版 | 日常对话、文本处理 |
| `internvl-latest` | 多模态 | 图文理解、图像分析 |

## 第四步：连接消息平台

以 Telegram 为例：

```bash
# 设置 Telegram Bot Token
export TELEGRAM_BOT_TOKEN="your-bot-token"

# 启动 OpenClaw
npm start
```

### 支持的消息平台

| 平台 | 配置方式 |
|------|---------|
| Telegram | Bot Token |
| 微信 | ClawBot 接口 |
| WhatsApp | WhatsApp Business API |
| Slack | Slack App |
| Discord | Discord Bot |
| 飞书 | 飞书机器人 |

## 第五步：开始使用

连接完成后，你可以通过消息平台直接与 Intern-S1-Pro 对话：

```
你：帮我分析这篇论文的创新点 [上传 PDF]
OpenClaw：基于 Intern-S1-Pro 的分析...

你：把分析结果保存到 ~/research/notes.md
OpenClaw：已保存到指定路径。

你：搜索 arXiv 上关于 "视觉语言模型" 的最新论文
OpenClaw：正在浏览 arXiv...
```

## OpenClaw 核心能力

### 网页浏览

```
你：去 GitHub Trending 看看今天最火的 AI 项目
OpenClaw：[自动打开浏览器] 今天 GitHub Trending 上的 AI 项目...
```

### 文件操作

```
你：读取 ~/data/report.csv，生成数据摘要
OpenClaw：[读取文件] 这个 CSV 文件包含 1000 行数据...
```

### 代码执行

```
你：用 Python 画一个 sin 函数图
OpenClaw：[执行代码] 图片已保存到 ~/output/sin_plot.png
```

## 进阶配置

### 自定义系统提示词

```yaml
# config.yaml
system_prompt: |
  你是一个基于 Intern-S1-Pro 的科研助手。
  擅长论文分析、数学推导和代码编写。
  请用中文回复。
```

### MCP Server 集成

OpenClaw 支持 MCP 协议，可以扩展工具能力：

```yaml
mcp_servers:
  - name: database
    command: npx
    args: ["@modelcontextprotocol/server-postgres"]
    env:
      DATABASE_URL: postgresql://...
```

## 下一步

- [Claude Code 接入指南](/zh/docs/api/claude-code) — 另一个支持 Intern-S1-Pro 的 AI 编程工具
- [快速开始](/zh/docs/api/quickstart) — API 基础用法
- [MCP 协议详解](/zh/docs/learn/core/mcp-protocol) — 扩展 AI 工具能力
