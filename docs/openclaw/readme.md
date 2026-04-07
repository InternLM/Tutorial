# OpenClaw 多平台 AI 助手

## 课程简介

OpenClaw 是一个开源个人 AI 助手框架，你可以在自己的设备上运行，通过微信、Telegram、飞书、Slack 等 20 余个消息平台与它交互。它不仅能对话，还具备网页浏览、文件操作、代码执行等"有手有眼"的实际操作能力，并支持通过 MCP Server 扩展功能。

本课程将从零开始，带你完成 OpenClaw 的部署、接入 Intern-S1-Pro 作为大脑、对接消息平台、以及通过 MCP Server 扩展自定义能力。

## 你将学到

- OpenClaw 的架构设计与核心能力
- 快速部署 OpenClaw 并完成初始配置
- 将 Intern-S1-Pro 配置为 OpenClaw 的 AI 大脑
- 接入 Telegram、微信等消息平台
- OpenClaw 的核心能力：网页浏览、文件操作、代码执行
- 通过 MCP Server 扩展 OpenClaw 的工具能力

## 第 1 节：OpenClaw 概览

### 目标

理解 OpenClaw 的定位、架构和核心能力。

### 内容

**什么是 OpenClaw？**

OpenClaw 是一个你在自己设备上运行的个人 AI 助手。与 ChatGPT 等云端服务不同，OpenClaw 运行在你的本地机器上，数据不经过第三方服务器，你拥有完全的控制权。

**支持的消息平台**

OpenClaw 支持 20 余个消息平台，覆盖了个人和工作场景中的主流沟通工具：

| 分类 | 平台 |
|------|------|
| 即时通讯 | WhatsApp、Telegram、Signal、微信、iMessage |
| 办公协作 | Slack、Discord、Microsoft Teams、飞书、Mattermost |
| 社区 | Matrix、IRC、Nostr、Tlon |
| 其他 | Google Chat、LINE、Twitch、Zalo、WebChat |

**核心能力**

OpenClaw 不仅仅是一个聊天机器人，它具备三大实操能力：

1. **网页浏览**：通过 Chrome/Chromium CDP 协议控制浏览器，可以访问网页、填写表单、截取页面
2. **文件操作**：读写本地文件，处理图片、音频、视频，支持文件上传和转码
3. **代码执行**：通过 `system.run` 执行 Shell 命令，获取 stdout/stderr 和退出码

**架构组成**

- **Gateway**：核心守护进程，管理消息路由、会话状态和工具调度
- **Channels**：各平台的消息适配层（Telegram 基于 gramm Y、微信基于 @tencent-weixin/openclaw-weixin）
- **Sessions**：每个对话的独立上下文，支持模型切换和权限控制
- **Nodes**：不同设备（macOS/iOS/Android/Linux）的能力映射

## 第 2 节：快速部署

### 目标

完成 OpenClaw 的安装和初始化配置。

### 内容

**环境要求**

- Node.js 24（推荐）或 Node.js 22.16+
- npm 或 pnpm 包管理器
- 一个 AI 模型的 API Key（本课程使用 Intern-S1-Pro）

**安装 OpenClaw**

```bash
npm install -g openclaw@latest
```

验证安装成功：

```bash
openclaw --version
```

**初始化配置（Onboard 向导）**

OpenClaw 提供交互式向导完成初始配置：

```bash
openclaw onboard --install-daemon
```

向导会引导你完成以下步骤：

1. **选择模型提供商**：选择你要使用的 AI 模型服务
2. **输入 API Key**：OpenClaw 会立即验证 Key 的有效性
3. **选择默认模型**：根据提供商推荐模型
4. **安装 Gateway 守护进程**：以系统服务方式运行

配置完成后，OpenClaw 会将设置写入 `~/.openclaw/config.yaml`。

**从源码安装（开发者）**

如果你需要修改 OpenClaw 源码或参与开发：

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm ui:build
pnpm build
pnpm openclaw onboard --install-daemon
pnpm gateway:watch  # 开发模式，支持热重载
```

## 第 3 节：配置 Intern-S1-Pro 作为 AI 大脑

### 目标

将 Intern-S1-Pro 配置为 OpenClaw 的默认 AI 模型。

### 内容

OpenClaw 支持任何兼容 OpenAI API 协议的模型。Intern-S1-Pro 的 API 完全兼容该协议，可以无缝对接。

**编辑配置文件**

OpenClaw 使用两个核心配置文件：

- `~/.openclaw/config.yaml`：全局设置、默认提供商、偏好
- `~/.openclaw/models.yaml`：模型定义、回退链、路由规则

编辑 `~/.openclaw/config.yaml`，配置 Intern-S1-Pro：

```yaml
# ~/.openclaw/config.yaml

ai:
  defaultProvider: intern
  providers:
    intern:
      type: openai-compatible
      baseUrl: https://chat.intern-ai.org.cn/api/v1/
      apiKey: YOUR_API_KEY  # 替换为你的 Intern API Key
      defaultModel: internlm3-latest
```

**配置模型路由（可选）**

在 `~/.openclaw/models.yaml` 中，你可以配置多个模型和回退策略：

```yaml
# ~/.openclaw/models.yaml

models:
  default:
    provider: intern
    model: internlm3-latest
    temperature: 0.7
    maxTokens: 4096
```

**验证配置**

重启 Gateway 并测试：

```bash
openclaw gateway restart
openclaw chat "你好，请介绍一下你自己"
```

如果一切正常，你应该能看到 Intern-S1-Pro 的回复。

**健康检查**

```bash
openclaw doctor
```

该命令会检查配置文件、API 连接、平台插件等的状态，帮助排查问题。

## 第 4 节：接入消息平台

### 目标

将 OpenClaw 接入 Telegram 或微信，实现通过消息平台与 AI 助手对话。

### 内容

### 方案 A：接入 Telegram

**步骤 1：创建 Telegram Bot**

1. 在 Telegram 中搜索并打开 @BotFather
2. 发送 `/newbot`，按提示输入 Bot 名称和用户名
3. 保存返回的 Bot Token（格式类似 `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`）

**步骤 2：配置 OpenClaw**

编辑 `~/.openclaw/config.yaml`，添加 Telegram 频道配置：

```yaml
# ~/.openclaw/config.yaml

channels:
  telegram:
    enabled: true
    botToken: "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"  # 替换为你的 Token
    dmPolicy: pairing  # 安全模式：陌生人需要配对码才能对话
    groups:
      "*":
        requireMention: true  # 群聊中需要 @Bot 才响应
```

**步骤 3：启动并配对**

```bash
openclaw gateway restart
```

在 Telegram 中向你的 Bot 发送任意消息，Bot 会返回一个配对码。在终端中批准配对：

```bash
openclaw pairing approve telegram <pairing-code>
```

配对完成后，你就可以通过 Telegram 与 OpenClaw 对话了。

### 方案 B：接入微信

**步骤 1：安装微信插件**

```bash
openclaw plugins install "@tencent-weixin/openclaw-weixin"
```

**步骤 2：配置**

编辑 `~/.openclaw/config.yaml`：

```yaml
# ~/.openclaw/config.yaml

channels:
  wechat:
    enabled: true
    apiKey: "wc_live_xxxxxxxxxxxxxxxx"  # 替换为你的微信服务 API Key
    proxyUrl: "http://your-proxy:3000"  # 微信代理服务地址
```

**步骤 3：登录**

```bash
openclaw channels login --channel openclaw-weixin
```

按提示扫描二维码完成微信登录。

### 方案 C：接入飞书

```yaml
# ~/.openclaw/config.yaml

channels:
  feishu:
    enabled: true
    appId: "cli_xxxxxxxxxxxxxxxx"
    appSecret: "your-app-secret"
```

**安全策略说明**

OpenClaw 默认采用 pairing 模式，即陌生人发来的消息不会被处理，需要你手动批准。这是一项重要的安全措施，防止任何人通过你的 Bot 调用 API。

| 模式 | 说明 | 适用场景 |
|------|------|---------|
| `pairing` | 陌生人需配对码，审批后才能对话 | 个人使用（推荐） |
| `open` | 任何人都可以直接对话 | 公开服务（需谨慎） |

## 第 5 节：核心能力实战

### 目标

体验 OpenClaw 的网页浏览、文件操作和代码执行能力。

### 内容

OpenClaw 不只是转发消息给 AI 模型，它本身就是一个有"手"和"眼"的智能体。以下能力可以在任何已接入的消息平台中使用。

**网页浏览**

在对话中让 OpenClaw 访问网页并提取信息：

```
请帮我打开 https://arxiv.org/abs/2510.11341 ，总结一下这篇论文的核心贡献。
```

OpenClaw 会通过 CDP 协议控制 Chrome 浏览器，访问页面、提取内容，并返回总结。

**文件操作**

让 OpenClaw 读写本地文件：

```
请读取 ~/Documents/notes.txt 的内容，然后帮我翻译成英文，保存到 ~/Documents/notes_en.txt
```

**代码执行**

让 OpenClaw 执行代码并返回结果：

```
请帮我写一个 Python 脚本，统计当前目录下所有 .py 文件的总行数，然后运行它。
```

OpenClaw 会生成代码、通过 `system.run` 执行，并返回结果。

**注意事项**

- 代码执行功能有权限控制，首次使用需要在终端中确认授权
- 文件操作默认限制在用户目录内
- 网页浏览需要本地安装 Chrome/Chromium

## 第 6 节：MCP Server 扩展

### 目标

学会通过 MCP Server 为 OpenClaw 添加自定义工具能力。

### 内容

**什么是 MCP？**

MCP（Model Context Protocol）是一种标准化协议，用于将外部工具和数据源以统一接口暴露给 AI 模型。OpenClaw 支持将任意 MCP Server 注册为工具，大幅扩展助手的能力边界。

**查看已注册的 MCP Server**

```bash
openclaw mcp list
```

**添加一个 MCP Server**

以添加 GitHub MCP Server 为例，让 OpenClaw 具备操作 GitHub 仓库的能力：

```bash
openclaw mcp set github --command "npx" --args "-y @modelcontextprotocol/server-github"
```

或者直接编辑配置文件：

```yaml
# ~/.openclaw/config.yaml

plugins:
  mcp:
    servers:
      github:
        command: npx
        args: ["-y", "@modelcontextprotocol/server-github"]
        env:
          GITHUB_TOKEN: "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

配置完成后重启 Gateway：

```bash
openclaw gateway restart
```

现在你可以在对话中让 OpenClaw 操作 GitHub：

```
请查看 InternLM/lmdeploy 仓库最近的 5 个 Issue。
```

**添加文件系统 MCP Server**

```yaml
plugins:
  mcp:
    servers:
      filesystem:
        command: npx
        args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/projects"]
```

**添加数据库 MCP Server**

```yaml
plugins:
  mcp:
    servers:
      sqlite:
        command: npx
        args: ["-y", "@modelcontextprotocol/server-sqlite", "--db-path", "./data.db"]
```

**自定义 MCP Server**

你也可以开发自己的 MCP Server。一个最小的 MCP Server 只需要实现 stdio 通信协议。以下是一个 Python 示例：

```python
# my_mcp_server.py
import json
import sys

def handle_request(request):
    if request["method"] == "tools/list":
        return {
            "tools": [
                {
                    "name": "get_weather",
                    "description": "Get current weather for a city",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "city": {"type": "string", "description": "City name"}
                        },
                        "required": ["city"],
                    },
                }
            ]
        }
    elif request["method"] == "tools/call":
        city = request["params"]["arguments"]["city"]
        return {"content": [{"type": "text", "text": f"Weather in {city}: 25C, sunny"}]}
    return {}

for line in sys.stdin:
    request = json.loads(line)
    response = handle_request(request)
    response["jsonrpc"] = "2.0"
    response["id"] = request.get("id")
    sys.stdout.write(json.dumps(response) + "\n")
    sys.stdout.flush()
```

注册自定义 Server：

```yaml
plugins:
  mcp:
    servers:
      weather:
        command: python
        args: ["my_mcp_server.py"]
```

## 第 7 节：隐私安全与最佳实践

### 目标

了解 OpenClaw 的安全模型和生产部署建议。

### 内容

**安全第一原则**

OpenClaw 将所有外部消息视为不受信任的输入。以下安全机制默认启用：

1. **配对模式（Pairing）**：陌生人发来的消息需要你手动批准后才会被处理
2. **权限映射**：不同设备（Node）有不同的能力权限，macOS/iOS/Android 通过 TCC 权限系统控制
3. **会话级权限**：可以在会话中动态开关代码执行等高权限功能

**安全检查**

```bash
openclaw doctor
```

该命令会检查并报告安全配置中的潜在问题。

**远程访问**

如果需要从外部访问 OpenClaw Gateway：

- **推荐**：使用 Tailscale Serve（仅限 tailnet 内部访问）
- **公网访问**：使用 Tailscale Funnel + 密码认证
- **备选**：SSH 隧道

Gateway 默认只监听 loopback 地址，不会暴露到公网。

**最佳实践**

- 始终使用 pairing 模式，不要轻易开启 open 模式
- 定期轮换 API Key
- 不要在配置文件中硬编码敏感信息，使用环境变量
- 对代码执行功能保持警惕，只在可信环境下启用

## 参考资料

- OpenClaw GitHub：https://github.com/openclaw/openclaw
- OpenClaw 官方文档：https://docs.openclaw.ai
- MCP 协议规范：https://modelcontextprotocol.io
- Intern-S1-Pro API：https://internlm.intern-ai.org.cn/api/document
- Telegram BotFather：https://t.me/BotFather
- MCP Server 生态：https://github.com/modelcontextprotocol/servers
