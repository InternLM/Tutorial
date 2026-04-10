# OpenClaw -- 把 AI 助手带进你的聊天窗口

> 本文档 AI + 社区共建中

## 1. 课程简介

想象一下：你在 Telegram 群里发了一句"帮我搜一下 InternVL3 的论文"，几秒钟后，助手就把论文标题、摘要和链接整理好发了回来。你接着说"把上个月的实验数据 CSV 读一下，画个趋势图"，它又默默把图画好贴了出来。

这不是未来的功能预告，而是你在这门课程里即将亲手搭起来的东西。

OpenClaw 是一个开源的个人 AI 助手框架。它跑在你自己的机器上，通过消息平台（Telegram、微信、飞书等）与你交互。它不只会聊天——它能打开网页、读写文件、执行代码，还能通过 MCP 协议接入各种外部工具。

本课程的目标很明确：带你从零部署 OpenClaw，接入 Telegram，在真实对话中完成三件事——查论文、读 CSV、画图——最后再接一个 MCP Server 扩展能力。做完这些，你手里就有了一个真正能干活的 AI 助手。

我们会用 Intern-S1-Pro 作为 OpenClaw 的 AI 大脑。Intern-S1-Pro 是书生生态的科学多模态大模型，API 兼容 OpenAI 协议，配置简单，能力全面。

## 2. 你将做出什么

完成本课程后，你会拥有：

- 一个运行在自己机器上的 OpenClaw 实例
- 一个接入了 Intern-S1-Pro 的 Telegram Bot
- 在 Telegram 聊天中能做到：
  - 发一句话就能搜论文、读摘要
  - 发一个 CSV 文件就能分析数据、画图
  - 让助手执行代码、处理文件
- 一个已注册的 MCP Server，让助手的能力可以持续扩展

你不需要有 AI 应用开发经验。只要会装 Node.js、会编辑配置文件，就能跟着做完。

## 3. OpenClaw 概览

在动手之前，先花两分钟了解 OpenClaw 的基本结构。不用背，后面实操时自然会熟悉。

**OpenClaw 的四个核心模块**

```
消息平台 (Telegram/微信/...)
    |
    v
 Channel (消息适配层)
    |
    v
 Gateway (核心守护进程)
    |
    +---> AI 模型 (Intern-S1-Pro)
    +---> 内置能力 (浏览器/文件/代码执行)
    +---> MCP Server (外部工具扩展)
```

- **Gateway**：OpenClaw 的中枢，负责消息路由、会话管理和工具调度。以系统服务方式运行在你的机器上。
- **Channel**：消息平台的适配层。每个平台有自己的 Channel 实现（Telegram 基于 grammY，微信基于专用插件）。
- **Session**：每个对话的独立上下文。不同对话之间互不干扰，可以分别配置权限。
- **MCP Server**：通过标准化协议接入的外部工具。后面会详细讲。

**数据怎么走**

你在 Telegram 发一条消息，Channel 把它转成统一格式交给 Gateway，Gateway 把消息和上下文一起发给 AI 模型，模型决定要不要调用工具（比如打开网页、读文件），工具执行完把结果返回，模型生成最终回复，再通过 Channel 发回 Telegram。

整个过程你只感知到"发了一句话，收到了一个回复"。

## 4. 快速部署

### 环境要求

- Node.js 24（推荐）或 Node.js 22.16+
- npm 或 pnpm 包管理器
- 一台能联网的机器（macOS / Linux / Windows 均可）

### 安装 OpenClaw

```bash
npm install -g openclaw@latest
```

验证安装：

```bash
openclaw --version
```

看到版本号输出就说明安装成功了。

### 运行初始化向导

OpenClaw 提供了一个交互式向导，帮你完成首次配置：

```bash
openclaw onboard --install-daemon
```

向导会引导你完成四个步骤：

1. 选择模型提供商（先跳过，我们后面手动配置 Intern-S1-Pro）
2. 输入 API Key
3. 选择默认模型
4. 安装 Gateway 守护进程（以系统服务方式运行）

配置完成后，所有设置会写入 `~/.openclaw/config.yaml`。

### 从源码安装（开发者）

如果你想修改 OpenClaw 源码或参与贡献：

```bash
git clone https://github.com/nicepkg/openclaw.git
cd openclaw
pnpm install
pnpm ui:build
pnpm build
pnpm openclaw onboard --install-daemon
pnpm gateway:watch  # 开发模式，支持热重载
```

### 检查安装状态

```bash
openclaw doctor
```

这个命令会检查配置文件、API 连接、平台插件等的状态。如果有问题，它会告诉你哪里出了错以及怎么修。养成习惯，遇到问题先跑一次 `openclaw doctor`。

## 5. 配置 Intern-S1-Pro

现在给 OpenClaw 装上"大脑"。

Intern-S1-Pro 的 API 完全兼容 OpenAI 协议，配置非常简单。

### 编辑配置文件

用你喜欢的编辑器打开 `~/.openclaw/config.yaml`，写入以下内容：

```yaml
# ~/.openclaw/config.yaml

ai:
  defaultProvider: intern
  providers:
    intern:
      type: openai-compatible
      baseUrl: https://chat.intern-ai.org.cn/api/v1/
      apiKey: YOUR_API_KEY  # 替换为你的 Intern API Key
      defaultModel: intern-s1-pro
```

**获取 API Key 的方法：**

1. 访问 https://internlm.intern-ai.org.cn
2. 注册并登录
3. 在 API 管理页面创建一个新的 Key
4. 复制 Key，粘贴到上面的 `apiKey` 字段

### 配置模型参数（可选）

如果你想精细控制模型行为，可以编辑 `~/.openclaw/models.yaml`：

```yaml
# ~/.openclaw/models.yaml

models:
  default:
    provider: intern
    model: intern-s1-pro
    temperature: 0.7
    maxTokens: 4096
```

### 验证模型连接

重启 Gateway 并测试：

```bash
openclaw gateway restart
openclaw chat "你好，请介绍一下你自己"
```

如果一切正常，你应该能看到 Intern-S1-Pro 的回复。看到回复后，恭喜你，OpenClaw 已经有了一颗能思考的大脑。

如果没有回复或报错，检查以下几点：

- API Key 是否正确复制（注意不要多复制空格）
- `baseUrl` 末尾是否有 `/`
- 网络是否能访问 `chat.intern-ai.org.cn`

## 6. 接入 Telegram

为什么先从 Telegram 开始？因为它是所有平台里最容易跑通的：有官方的 Bot API，不需要额外的代理服务，配置三步就能聊上。

### 步骤 1：创建 Telegram Bot

1. 在 Telegram 中搜索 **@BotFather**，打开对话
2. 发送 `/newbot`
3. 按提示输入 Bot 的显示名称（比如"我的 AI 助手"）
4. 输入 Bot 的用户名（必须以 `bot` 结尾，比如 `my_intern_ai_bot`）
5. BotFather 会返回一个 Bot Token，格式类似：

```
123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
```

把这个 Token 保存好，不要泄露给别人。拿到 Token 就等于拿到了 Bot 的控制权。

### 步骤 2：配置 OpenClaw

编辑 `~/.openclaw/config.yaml`，添加 Telegram Channel 配置：

```yaml
# ~/.openclaw/config.yaml

ai:
  defaultProvider: intern
  providers:
    intern:
      type: openai-compatible
      baseUrl: https://chat.intern-ai.org.cn/api/v1/
      apiKey: YOUR_API_KEY

channels:
  telegram:
    enabled: true
    botToken: "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"  # 替换为你的 Token
    dmPolicy: pairing  # 安全模式：陌生人需要配对码才能对话
    groups:
      "*":
        requireMention: true  # 群聊中需要 @Bot 才响应
```

**关于 dmPolicy 的说明：**

| 模式 | 行为 | 适用场景 |
|------|------|---------|
| `pairing` | 陌生人发消息后需要你在终端审批配对码 | 个人使用（推荐） |
| `open` | 任何人都可以直接对话 | 公开服务（需谨慎） |

强烈建议保持 `pairing` 模式。`open` 模式意味着任何人都可以通过你的 Bot 调用 API 和执行工具，这会带来安全风险和费用风险。

### 步骤 3：重启 Gateway

```bash
openclaw gateway restart
```

### 步骤 4：完成配对

在 Telegram 中找到你刚创建的 Bot，发送任意消息（比如"你好"）。Bot 会返回一个配对码。

回到终端，批准配对：

```bash
openclaw pairing approve telegram <配对码>
```

配对完成后，再发一条消息试试：

```
你好，请告诉我今天星期几
```

如果收到了回复——恭喜你，你的 AI 助手已经在 Telegram 里活过来了。

### 步骤 5：在群聊中使用

把 Bot 拉进一个 Telegram 群，然后 @它 说话：

```
@my_intern_ai_bot 帮我解释一下什么是 MCP 协议
```

因为我们配置了 `requireMention: true`，Bot 只有在被 @ 的时候才会回复，不会打扰正常群聊。

## 7. 三大能力实战

OpenClaw 已经在 Telegram 里跑起来了，现在我们来用一个连贯的场景体验它的核心能力。

假设你是一个 AI 研究者，正在准备一个技术分享。你需要：先找一篇论文了解背景，再分析一份实验数据，最后把结果画成图表。

这三件事，都可以在 Telegram 对话里完成。

### 实战 1：查论文

在 Telegram 中发送：

```
请帮我打开 https://arxiv.org/abs/2412.05271 ，总结一下这篇论文的核心贡献和方法
```

OpenClaw 会通过内置的浏览器能力（基于 Chrome CDP 协议）访问 arXiv 页面，提取论文信息，然后用 Intern-S1-Pro 生成总结返回给你。

你还可以继续追问：

```
这篇论文和 InternVL2 相比有什么改进？
```

OpenClaw 会基于已经读取的内容进行对比分析。

**前置条件：** 运行 OpenClaw 的机器上需要安装 Chrome 或 Chromium。如果是无头服务器，安装 Chromium 即可：

```bash
# Ubuntu/Debian
sudo apt install chromium-browser

# macOS
brew install --cask chromium
```

### 实战 2：读 CSV 数据

假设你有一份实验数据文件 `experiment_results.csv`，先把它放到 OpenClaw 能访问的目录（默认是用户主目录）。

我们先创建一份示例数据：

```bash
cat > ~/experiment_results.csv << 'EOF'
epoch,train_loss,val_loss,accuracy,learning_rate
1,2.341,2.156,0.312,0.001
2,1.876,1.743,0.445,0.001
3,1.523,1.498,0.534,0.001
4,1.245,1.312,0.612,0.0005
5,1.034,1.187,0.678,0.0005
6,0.876,1.098,0.723,0.0005
7,0.734,1.034,0.756,0.0001
8,0.623,0.987,0.789,0.0001
9,0.534,0.956,0.812,0.0001
10,0.467,0.934,0.834,0.0001
EOF
```

然后在 Telegram 中发送：

```
请读取 ~/experiment_results.csv，告诉我每个阶段的训练趋势，哪个 epoch 开始出现过拟合迹象
```

OpenClaw 会读取文件内容，分析数据，给出专业的解读。比如它可能会指出从 epoch 4 开始 train_loss 和 val_loss 的差距逐渐拉大，有轻微过拟合趋势。

**关于文件访问权限：** OpenClaw 默认只能访问用户主目录下的文件。如果你需要访问其他路径，需要在配置中显式授权。这是一项安全设计，防止助手意外读取敏感文件。

### 实战 3：画图

接着上面的对话，继续发送：

```
把这份数据画成图表：横轴是 epoch，左纵轴画 train_loss 和 val_loss 的曲线，右纵轴画 accuracy 的曲线，保存到 ~/training_chart.png
```

OpenClaw 会生成一段 Python 绘图代码（使用 matplotlib），通过 `system.run` 执行，然后把生成的图表发回 Telegram。

如果你的机器上没有 matplotlib，OpenClaw 会先帮你安装：

```
pip install matplotlib
```

你可以对图表提出修改意见：

```
不错，但请把配色改成蓝绿色系，加上网格线，标题写"Training Progress"
```

OpenClaw 会重新生成并发回修改后的图表。

**关于代码执行权限：** 首次使用代码执行功能时，OpenClaw 会在终端中请求你确认授权。这是一项安全措施——你需要明确允许助手在你的机器上运行代码。授权后，后续使用不需要再次确认。

**三个实战做完，回头看看：** 你在 Telegram 里完成了论文调研、数据分析和图表生成，没有切换任何工具，没有打开任何网页。这就是 OpenClaw 的价值——把 AI 的能力带进你日常使用的聊天窗口。

## 8. MCP Server 扩展

到目前为止，OpenClaw 的能力来自三个内置模块：浏览器、文件操作、代码执行。但真实场景中，你可能还需要操作 GitHub、查数据库、调用内部 API。

这就是 MCP（Model Context Protocol）的用武之地。MCP 是一种标准化协议，让你可以把任意工具以统一接口暴露给 AI 模型。OpenClaw 原生支持 MCP Server。

### 最小可跑 Demo：接入 GitHub

我们来接一个 GitHub MCP Server，让 OpenClaw 具备查看仓库、Issue、PR 等能力。

**步骤 1：获取 GitHub Token**

1. 访问 https://github.com/settings/tokens
2. 创建一个 Personal Access Token（Classic），勾选 `repo` 权限
3. 复制 Token

**步骤 2：注册 MCP Server**

编辑 `~/.openclaw/config.yaml`，添加 MCP 配置：

```yaml
# ~/.openclaw/config.yaml（在已有配置基础上追加）

plugins:
  mcp:
    servers:
      github:
        command: npx
        args: ["-y", "@modelcontextprotocol/server-github"]
        env:
          GITHUB_TOKEN: "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # 替换为你的 Token
```

**步骤 3：重启并测试**

```bash
openclaw gateway restart
```

在 Telegram 中测试：

```
请查看 InternLM/InternLM 仓库最近的 5 个 Issue，列出标题和状态
```

OpenClaw 会通过 GitHub MCP Server 查询 Issue 列表并返回结果。

### 查看已注册的 MCP Server

```bash
openclaw mcp list
```

### 更多 MCP Server 示例

**文件系统 Server（限定目录访问）：**

```yaml
plugins:
  mcp:
    servers:
      filesystem:
        command: npx
        args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/projects"]
```

**SQLite 数据库 Server：**

```yaml
plugins:
  mcp:
    servers:
      sqlite:
        command: npx
        args: ["-y", "@modelcontextprotocol/server-sqlite", "--db-path", "./data.db"]
```

### 写一个自定义 MCP Server

MCP Server 的实现并不复杂。只要你的程序能通过 stdin/stdout 进行 JSON-RPC 通信，就可以作为 MCP Server 注册。

以下是一个最小示例——天气查询工具：

```python
# my_weather_server.py
import json
import sys

def handle_request(request):
    method = request.get("method", "")

    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "get_weather",
                    "description": "Get current weather for a city",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "City name in English"
                            }
                        },
                        "required": ["city"],
                    },
                }
            ]
        }
    elif method == "tools/call":
        tool_name = request["params"]["name"]
        args = request["params"]["arguments"]
        if tool_name == "get_weather":
            city = args["city"]
            # 这里接入真实天气 API 即可
            return {
                "content": [
                    {"type": "text", "text": f"Weather in {city}: 25C, sunny"}
                ]
            }
    return {}

for line in sys.stdin:
    request = json.loads(line.strip())
    response = handle_request(request)
    response["jsonrpc"] = "2.0"
    response["id"] = request.get("id")
    sys.stdout.write(json.dumps(response) + "\n")
    sys.stdout.flush()
```

注册到 OpenClaw：

```yaml
plugins:
  mcp:
    servers:
      weather:
        command: python3
        args: ["/path/to/my_weather_server.py"]
```

重启 Gateway 后，在 Telegram 中说"上海今天天气怎么样"，OpenClaw 就会调用你写的天气工具。

把 `get_weather` 里的假数据换成真实的天气 API 调用（比如 OpenWeatherMap），就是一个完整可用的天气助手了。

## 9. 其他平台接入

Telegram 是最容易上手的平台，但 OpenClaw 支持 20 多个消息平台。跑通 Telegram 之后，你可以按需接入其他平台。

### 微信

微信接入需要安装专用插件，通过扫码登录：

```bash
# 安装微信插件
openclaw plugins install "@nicepkg/openclaw-weixin"
```

编辑 `~/.openclaw/config.yaml`：

```yaml
channels:
  wechat:
    enabled: true
    apiKey: "wc_live_xxxxxxxxxxxxxxxx"  # 微信服务 API Key
    proxyUrl: "http://your-proxy:3000"  # 微信代理服务地址
```

启动并扫码登录：

```bash
openclaw channels login --channel openclaw-weixin
```

微信接入比 Telegram 复杂一些，需要额外的代理服务。适合有运维经验的同学尝试。

### 飞书

飞书接入需要先在飞书开放平台创建应用：

```yaml
channels:
  feishu:
    enabled: true
    appId: "cli_xxxxxxxxxxxxxxxx"
    appSecret: "your-app-secret"
```

### Slack

```yaml
channels:
  slack:
    enabled: true
    botToken: "xoxb-xxxxxxxxxxxx"
    appToken: "xapp-xxxxxxxxxxxx"
```

### 更多平台

OpenClaw 还支持 Discord、WhatsApp、Signal、Microsoft Teams、Matrix 等平台。每个平台的接入方式大同小异：安装对应的 Channel 插件，在配置文件中填入认证信息，重启 Gateway。

具体配置可以参考 OpenClaw 官方文档：https://docs.openclaw.ai/channels

**建议：** 先把 Telegram 跑稳、用熟，再考虑接入其他平台。多平台同时接入会增加配置复杂度和排查难度。

## 10. 安全与隐私

OpenClaw 跑在你自己的机器上，这带来了控制权，也带来了责任。以下是你需要了解的安全要点。

### 数据边界

OpenClaw 的数据流向取决于你的部署方式：

- **AI 模型请求**：你的对话内容会发送到模型提供商的 API（比如 Intern-S1-Pro 的服务器）。这是获取 AI 回复所必需的。
- **消息平台**：消息通过平台的服务器传输（Telegram 的服务器、微信的服务器等）。
- **本地能力**：文件操作和代码执行在你的本地机器上完成，不经过第三方。
- **MCP Server**：取决于具体的 Server 实现。GitHub Server 会访问 GitHub API，自定义 Server 则完全由你控制。

简单说：你可以通过部署方式控制数据边界，但不能说"数据完全不出本地"——使用云端模型和消息平台本身就需要网络通信。

### 权限控制

| 机制 | 说明 |
|------|------|
| 配对模式（Pairing） | 陌生人需要你审批后才能与 Bot 对话 |
| 会话级权限 | 可以在会话中动态开关代码执行等高权限功能 |
| 文件访问范围 | 默认限制在用户主目录内 |
| 工具授权 | 首次使用新工具时需要终端确认 |

### 安全建议

- 始终保持 `pairing` 模式，不要在公网环境下使用 `open` 模式
- 不要在配置文件中硬编码敏感信息（API Key 等），推荐使用环境变量：

```yaml
ai:
  providers:
    intern:
      apiKey: ${INTERN_API_KEY}  # 从环境变量读取
```

- 定期轮换 API Key
- 代码执行功能的权限不要开太大——默认范围通常就够用
- 如果要把 Bot 加进公开群聊，务必开启 `requireMention`
- Gateway 默认只监听本地回环地址（127.0.0.1），不会暴露到公网

### 远程访问

如果你需要从外部访问 OpenClaw Gateway（比如在服务器上部署、从手机使用）：

- **推荐方案**：使用 Tailscale Serve（仅限 tailnet 内部访问，零配置）
- **公网方案**：使用 Tailscale Funnel + 密码认证
- **备选方案**：SSH 隧道转发

不建议直接把 Gateway 端口暴露到公网。

## 11. 常见问题排查

遇到问题时，第一步永远是：

```bash
openclaw doctor
```

它会检查配置、连接、插件等各项状态，大部分问题都能定位到。

以下是一些高频问题和解决方法。

### Bot 不回复消息

**现象：** 在 Telegram 给 Bot 发消息，没有任何反应。

**排查步骤：**

1. 检查 Gateway 是否在运行：

```bash
openclaw gateway status
```

如果没有运行，启动它：

```bash
openclaw gateway start
```

2. 检查 Telegram Channel 是否启用：

```bash
openclaw doctor
```

看输出中 Telegram 相关的状态。

3. 检查是否完成了配对：

```bash
openclaw pairing list
```

如果没有配对记录，说明你还没有审批过。重新给 Bot 发消息获取配对码，然后执行 `openclaw pairing approve telegram <配对码>`。

4. 检查 Bot Token 是否正确：

去 Telegram 找 @BotFather，发送 `/mybots`，确认 Token 与配置文件中的一致。

### API Key 无效

**现象：** `openclaw chat` 报错，提示认证失败或 401。

**排查步骤：**

1. 确认 API Key 格式正确，没有多余的空格或换行
2. 确认 `baseUrl` 填写正确：

```
https://chat.intern-ai.org.cn/api/v1/
```

注意末尾的 `/` 不能漏。

3. 在浏览器或 curl 中直接测试 API：

```bash
curl https://chat.intern-ai.org.cn/api/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

如果 curl 也报错，说明 Key 本身有问题，需要去 Intern 平台重新生成。

4. 如果使用环境变量方式配置，确认环境变量已正确导出：

```bash
echo $INTERN_API_KEY
```

### MCP Server 不生效

**现象：** 配置了 MCP Server，但在对话中使用相关工具时 Bot 没有调用。

**排查步骤：**

1. 确认 Server 已注册：

```bash
openclaw mcp list
```

如果列表中没有你配置的 Server，检查 `config.yaml` 中的缩进和格式。YAML 对缩进非常敏感，一个空格的差异就可能导致解析失败。

2. 确认 Server 能独立运行：

```bash
# 以 GitHub Server 为例
npx -y @modelcontextprotocol/server-github
```

如果报错（比如 npx 找不到、网络超时），先解决 Server 本身的问题。

3. 确认环境变量已配置：

GitHub Server 需要 `GITHUB_TOKEN`，如果没有配置，Server 启动后会静默失败。

4. 重启 Gateway：

```bash
openclaw gateway restart
```

MCP Server 的注册信息在 Gateway 启动时加载。修改配置后必须重启。

### 文件权限不足

**现象：** 让 OpenClaw 读写文件时报错"Permission denied"。

**排查步骤：**

1. 确认文件路径在 OpenClaw 的访问范围内（默认是用户主目录 `~`）
2. 确认文件的系统权限允许当前用户读写：

```bash
ls -la ~/experiment_results.csv
```

3. 如果需要访问主目录之外的路径，在配置中显式授权：

```yaml
security:
  allowedPaths:
    - /home/user
    - /data/shared  # 额外授权的路径
```

### 代码执行失败

**现象：** 让 OpenClaw 运行代码时报错。

**排查步骤：**

1. 确认你已在终端中授权代码执行功能
2. 确认所需的运行环境已安装（比如 Python、pip、matplotlib）
3. 手动运行同样的命令，看是否能成功：

```bash
python3 -c "import matplotlib; print(matplotlib.__version__)"
```

4. 如果是依赖缺失，先手动安装好依赖，再让 OpenClaw 重试

### 网页浏览不可用

**现象：** 让 OpenClaw 访问网页时报错。

**排查步骤：**

1. 确认 Chrome 或 Chromium 已安装：

```bash
which chromium-browser || which chromium || which google-chrome
```

2. 如果是无头服务器（没有显示器），确认以无头模式运行。OpenClaw 默认会使用 `--headless` 参数，但某些环境可能需要额外配置。

3. 确认目标网页可以从你的机器访问。某些网站有地域限制或需要代理。

## 12. 参考资料

- OpenClaw GitHub：https://github.com/nicepkg/openclaw
- OpenClaw 官方文档：https://docs.openclaw.ai
- MCP 协议规范：https://modelcontextprotocol.io
- MCP Server 生态：https://github.com/modelcontextprotocol/servers
- Intern-S1-Pro API 文档：https://internlm.intern-ai.org.cn/api/document
- Telegram BotFather：https://t.me/BotFather
- Telegram Bot API 文档：https://core.telegram.org/bots/api
- grammY 框架（Telegram Channel 底层）：https://grammy.dev
- Tailscale（安全远程访问）：https://tailscale.com
