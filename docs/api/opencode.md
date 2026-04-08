# OpenCode 接入指南

OpenCode 是开源的 AI 编程终端工具（GitHub 139K Stars），支持 75+ LLM 提供商，100% 开源且不锁定任何单一模型。通过配置 OpenAI 兼容端点，可以接入 Intern-S1-Pro 作为编程助手。

## 安装

```bash
# 一键安装
curl -fsSL https://opencode.ai/install | bash

# 或通过包管理器
npm i -g opencode-ai@latest
brew install anomalyco/tap/opencode
```

验证安装：

```bash
opencode --version
```

## 配置 Intern-S1-Pro

在项目根目录创建 `opencode.json`：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "intern": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Intern-S1-Pro",
      "options": {
        "baseURL": "https://chat.intern-ai.org.cn/v1",
        "apiKey": "your-api-key"
      },
      "models": {
        "intern-s1-pro": {
          "name": "Intern-S1-Pro",
          "limit": {
            "context": 128000,
            "output": 8192
          }
        }
      }
    }
  },
  "model": "intern/intern-s1-pro"
}
```

也可以放在全局配置目录 `~/.config/opencode/opencode.json`，对所有项目生效。

## 获取 API Key

前往 [书生大模型平台](https://internlm.intern-ai.org.cn/api/document) 注册获取 API Key。

## 使用

```bash
# 启动交互式终端
opencode

# 非交互模式（脚本友好）
opencode -p "用 Python 实现一个快速排序算法"
```

## 内置 Agent

OpenCode 提供两个内置 Agent：

| Agent | 权限 | 用途 |
|-------|------|------|
| build | 完全访问（读写文件、执行命令） | 日常开发、代码生成、调试 |
| plan | 只读（不修改文件） | 代码探索、架构分析、方案设计 |

## 常用命令

| 命令 | 说明 |
|------|------|
| `/models` | 切换模型 |
| `/connect` | 配置新的模型提供商 |
| `/compact` | 压缩上下文（接近 token 上限时使用） |
| `/plan` | 切换到 plan Agent（只读模式） |

## MCP Server 支持

OpenCode 支持 MCP Server，可以扩展 AI 的能力：

```json
{
  "mcp": {
    "servers": {
      "my-tools": {
        "type": "stdio",
        "command": "npx",
        "args": ["-y", "my-mcp-server"]
      }
    }
  }
}
```

## 与 Claude Code 的对比

| 特性 | OpenCode | Claude Code |
|------|----------|-------------|
| 开源 | MIT 开源 | 闭源 |
| 模型支持 | 75+ 提供商 | Anthropic 系列 |
| MCP 支持 | 支持 | 支持 |
| 桌面应用 | 有（Beta） | 有 |
| 架构 | Client/Server | 单进程 |

两者均可接入 Intern-S1-Pro，选择取决于个人偏好。

## 参考

- [OpenCode 官网](https://opencode.ai)
- [GitHub 仓库](https://github.com/anomalyco/opencode)
