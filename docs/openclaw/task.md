# OpenClaw 多平台 AI 助手 -- 闯关任务

## 任务说明

通关本课程需要完成以下任务。请先按照教材完成 OpenClaw 的安装和基础配置。

## 任务 1：部署 OpenClaw + 接入 Intern-S1-Pro

**要求：**

完成 OpenClaw 的安装和配置，并将 Intern-S1-Pro 设置为默认 AI 模型。

1. 安装 OpenClaw 并验证版本
2. 运行 `openclaw onboard` 完成初始化配置
3. 编辑配置文件，将 Intern-S1-Pro 设置为 AI 提供商
4. 通过命令行对话验证配置成功

```bash
# 验证命令
openclaw chat "你好，请用一句话介绍书生大模型"
```

**提交：**

- `openclaw --version` 的截图
- 配置文件中与 Intern-S1-Pro 相关的配置内容（隐藏 API Key）
- 命令行对话的截图（需包含模型回复）
- `openclaw doctor` 健康检查结果截图

## 任务 2：接入一个消息平台

**要求：**

将 OpenClaw 接入一个消息平台（Telegram 或微信），并成功通过该平台与 AI 助手对话。

**Telegram 路线：**

1. 通过 @BotFather 创建一个 Telegram Bot
2. 在 OpenClaw 配置文件中添加 Telegram 频道配置
3. 完成配对流程
4. 通过 Telegram 与 AI 助手进行至少 3 轮对话

**微信路线：**

1. 安装微信插件 `@tencent-weixin/openclaw-weixin`
2. 在配置文件中添加微信频道配置
3. 扫码登录
4. 通过微信与 AI 助手进行至少 3 轮对话

**提交：**

- 消息平台的配置内容截图（隐藏敏感 Token）
- 在消息平台中与 AI 助手对话的截图（至少 3 轮对话）
- Gateway 启动日志截图（展示平台连接成功）

## 任务 3：添加一个自定义 MCP Server 扩展

**要求：**

为 OpenClaw 添加一个 MCP Server，扩展其工具能力，并通过对话验证扩展生效。

以下方案任选其一：

**方案 A -- 使用社区 MCP Server：**

1. 从 MCP Server 生态中选择一个 Server（如 GitHub、文件系统、SQLite 等）
2. 在配置文件中注册该 Server
3. 重启 Gateway
4. 通过对话让 OpenClaw 使用该工具完成一个任务

**方案 B -- 开发自定义 MCP Server：**

1. 编写一个自定义 MCP Server（Python 或 Node.js）
2. 实现至少一个工具（如天气查询、文件搜索、数据转换等）
3. 在配置文件中注册并启用
4. 通过对话验证工具可以正常调用

**提交：**

- MCP Server 的配置内容截图
- `openclaw mcp list` 的输出截图
- 通过对话调用 MCP 工具的截图（展示工具被成功调用并返回结果）
- 如果是自定义 Server，提交完整的 Server 源码
