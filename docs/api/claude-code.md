> 本文档 AI + 社区共建中
# Claude Code 接入 Intern-S1-Pro

[Claude Code](https://github.com/anthropics/claude-code) 是 Anthropic 官方的 AI 编程终端助手，支持通过 Anthropic 兼容 API 接入第三方模型。本指南将教你如何在 Claude Code 中使用 Intern-S1-Pro 模型。

## 第一步：获取 API Key

前往书生大模型官方平台获取 API Token：

**👉 [https://internlm.intern-ai.org.cn/api/tokens](https://internlm.intern-ai.org.cn/api/tokens)**

1. 注册并登录书生大模型平台
2. 进入 API 管理页面
3. 创建新的 API Key 并妥善保存

## 第二步：安装 Claude Code

### macOS / Linux / WSL

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

### Windows PowerShell

```powershell
irm https://claude.ai/install.ps1 | iex
```

### Windows CMD

```cmd
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

### 验证安装

```bash
claude --version
```

> 更多信息请参考 [Claude Code 官方文档](https://code.claude.com/docs/en/overview)

## 第三步：配置环境变量

在终端中设置以下环境变量，让 Claude Code 使用 Intern-S1-Pro 模型：

```bash
# 设置 API 基础地址
export ANTHROPIC_BASE_URL="https://chat.intern-ai.org.cn"

# 设置 API Token（替换为你的实际 Token）
export ANTHROPIC_AUTH_TOKEN="your-internlm-api-token"
```

> **注意：** Claude Code 使用 Anthropic 协议（非 OpenAI 协议），因此环境变量为 `ANTHROPIC_BASE_URL` 和 `ANTHROPIC_AUTH_TOKEN`。

### 推荐：使用 alias 快捷启动

不建议将环境变量写入 Shell 配置文件。推荐创建一个 alias，每次启动时自动注入环境变量：

```bash
# 在 ~/.zshrc 或 ~/.bashrc 中添加
alias iclaude='ANTHROPIC_BASE_URL="https://chat.intern-ai.org.cn" ANTHROPIC_AUTH_TOKEN="your-internlm-api-token" claude'
```

```bash
# 生效
source ~/.zshrc

# 启动
iclaude
```

之后只需输入 `iclaude` 即可启动接入书生大模型的 Claude Code。

## 第四步：启动 Claude Code

使用 `--model` 参数指定 Intern-S1-Pro 模型：

```bash
claude --model intern-s1-pro
```

启动后，你可以像平常一样使用 Claude Code 进行编程：

- 代码生成与补全
- Bug 修复与调试
- 代码重构
- 项目架构设计
- 测试用例编写

## 常用命令

```bash
# 使用 alias 启动（推荐）
iclaude

# 或手动指定环境变量
ANTHROPIC_BASE_URL="https://chat.intern-ai.org.cn" \
ANTHROPIC_AUTH_TOKEN="your-token" \
claude --model intern-s1-pro

# 直接执行单次任务
iclaude -p "帮我写一个 Python HTTP 服务器"

# 在指定目录下工作
cd /path/to/your/project && iclaude
```

## 配置文件方式

你也可以在项目根目录创建 `.claude/settings.json` 来配置默认模型：

```json
{
  "model": "intern-s1-pro"
}
```

这样在该项目目录下启动 Claude Code 时无需每次指定 `--model` 参数。

## 注意事项

- Intern-S1-Pro 是书生系列最强推理模型，擅长复杂代码推理和架构设计
- API Key 请妥善保管，不要提交到 Git 仓库
- 如遇到连接问题，请检查网络环境和 API Key 是否有效

---

## 下一步

- 查看 [OpenClaw 接入指南](/docs/api/openclaw) 了解具身智能开发
- 了解 [InternLM3 模型](/docs/api/models/internlm3) 详细参数
- 查看 [快速开始](/docs/api/quickstart) 了解 API 基础用法
