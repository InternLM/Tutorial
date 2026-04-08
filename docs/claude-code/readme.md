# Claude Code AI 编程

## 课程简介

Claude Code 是 Anthropic 官方推出的 AI 编程终端工具，将大语言模型的能力直接融入命令行开发流程。在书生大模型实战营中，我们使用 Intern-S1-Pro 科学多模态大模型作为底层驱动，让你在终端中完成代码生成、审查、调试、重构等全流程开发工作。本课程从零开始，带你掌握 AI 辅助编程的核心技能。

## 你将学到

- 安装与配置 Claude Code，连接 Intern-S1-Pro 模型
- 使用 Claude Code 进行代码生成、审查和调试
- 开发自定义 MCP Server 扩展 AI 能力边界
- 编写 Skills 文件实现可复用的任务自动化
- 配置 Hooks 实现代码提交前的自动检查
- 了解 Agent SDK 构建自主运行的 AI 代理

## 安装与配置

### 目标

完成 Claude Code 的安装，配置 Intern-S1-Pro 模型接入，并验证基本对话功能。

### 内容

Claude Code 以 npm 全局包的形式分发，需要 Node.js 18 或更高版本。

**安装 Claude Code：**

```bash
# 确认 Node.js 版本
node --version  # 需要 v18+

# 全局安装
npm install -g @anthropic-ai/claude-code

# 验证安装
claude --version
```

**配置 Intern-S1-Pro 模型：**

Claude Code 支持通过环境变量指定自定义模型端点。将以下配置写入 shell 配置文件：

```bash
# 写入 ~/.bashrc 或 ~/.zshrc
export ANTHROPIC_BASE_URL="https://chat.intern-ai.org.cn/api/v1"
export ANTHROPIC_API_KEY="your-api-key-here"
export ANTHROPIC_MODEL="intern-s1-pro"

# 使配置生效
source ~/.bashrc
```

API Key 可在书生大模型社区个人中心获取。

**启动 Claude Code：**

```bash
# 在项目目录中启动
cd your-project
claude
```

启动后会进入交互式终端界面，你可以直接用自然语言描述需求，Claude Code 会理解项目上下文并给出代码方案。

**验证连接：**

在 Claude Code 终端中输入以下内容测试：

```
请介绍一下你自己，以及你使用的底层模型。
```

如果返回正常回复且提到 Intern-S1-Pro，说明配置成功。

## 日常开发实战

### 目标

掌握 Claude Code 在实际开发中最常用的四个场景：代码生成、代码审查、调试排错和代码重构。

### 内容

**代码生成：**

Claude Code 能根据自然语言描述生成完整的、可运行的代码。关键是把需求描述清楚。

在 Claude Code 终端中尝试以下提示：

```
创建一个 Python FastAPI 服务，提供一个 /health 接口返回服务状态，
一个 /predict 接口接收 JSON 格式的文本输入并返回文本长度和词数统计。
要求包含输入校验、错误处理和完整的类型注解。
```

Claude Code 会在当前目录生成文件，你可以直接运行验证。

**代码审查：**

让 Claude Code 审查已有代码的质量问题：

```
审查当前项目中的所有 Python 文件，重点关注：
1. 安全漏洞（SQL 注入、XSS 等）
2. 性能瓶颈
3. 未处理的异常
4. 不符合 PEP 8 的风格问题
给出具体的修改建议和代码示例。
```

**调试排错：**

遇到报错时，直接把错误信息交给 Claude Code：

```
运行 python main.py 时出现以下错误，请分析原因并修复：
Traceback (most recent call last):
  File "main.py", line 42, in process_data
    result = data["key"]["nested"]
KeyError: 'nested'
```

Claude Code 会分析代码上下文，定位问题根源，并直接修改文件。

**代码重构：**

对已有代码进行结构优化：

```
将 utils.py 中超过 50 行的函数拆分为独立模块，
保持对外接口不变，添加单元测试覆盖核心逻辑。
```

**实用技巧：**

- 使用 `/compact` 命令压缩对话历史，释放上下文窗口
- 用 `claude --resume` 恢复上一次会话
- 在提示中引用文件路径，Claude Code 会自动读取内容

## MCP Server 开发

### 目标

理解 MCP（Model Context Protocol）的基本概念，开发一个自定义 MCP Server 并接入 Claude Code。

### 内容

MCP 是一种标准化协议，让 AI 模型能够调用外部工具和数据源。Claude Code 内置了 MCP 客户端，可以连接任意 MCP Server 来扩展能力。

**MCP Server 基本结构：**

一个 MCP Server 本质上是一个提供工具（Tool）的服务，AI 可以在需要时自动调用这些工具。

以下是一个完整的 TypeScript MCP Server 示例，实现天气查询和单位换算两个工具：

```typescript
// weather-server.ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "weather-tools",
  version: "1.0.0",
});

// 工具 1：查询天气
server.tool(
  "get_weather",
  "查询指定城市的当前天气信息",
  {
    city: z.string().describe("城市名称，例如：北京、上海"),
  },
  async ({ city }) => {
    // 这里替换为真实的天气 API 调用
    const mockData: Record<string, { temp: number; condition: string }> = {
      "北京": { temp: 22, condition: "晴" },
      "上海": { temp: 25, condition: "多云" },
      "广州": { temp: 30, condition: "阵雨" },
    };
    const weather = mockData[city];
    if (!weather) {
      return {
        content: [{ type: "text", text: `未找到城市 ${city} 的天气数据` }],
      };
    }
    return {
      content: [
        {
          type: "text",
          text: `${city}：${weather.temp}°C，${weather.condition}`,
        },
      ],
    };
  }
);

// 工具 2：温度单位换算
server.tool(
  "convert_temperature",
  "在摄氏度和华氏度之间转换温度",
  {
    value: z.number().describe("温度数值"),
    from_unit: z.enum(["celsius", "fahrenheit"]).describe("原始单位"),
  },
  async ({ value, from_unit }) => {
    let result: number;
    let targetUnit: string;
    if (from_unit === "celsius") {
      result = (value * 9) / 5 + 32;
      targetUnit = "°F";
    } else {
      result = ((value - 32) * 5) / 9;
      targetUnit = "°C";
    }
    return {
      content: [
        {
          type: "text",
          text: `${value}${from_unit === "celsius" ? "°C" : "°F"} = ${result.toFixed(1)}${targetUnit}`,
        },
      ],
    };
  }
);

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Weather MCP Server 已启动");
}

main().catch(console.error);
```

**初始化项目并安装依赖：**

```bash
mkdir weather-mcp-server && cd weather-mcp-server
npm init -y
npm install @modelcontextprotocol/sdk zod
npm install -D typescript @types/node
npx tsc --init
```

在 `tsconfig.json` 中确保以下配置：

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "./dist",
    "strict": true
  }
}
```

在 `package.json` 中添加：

```json
{
  "type": "module",
  "scripts": {
    "build": "tsc",
    "start": "node dist/weather-server.js"
  }
}
```

**编译并注册到 Claude Code：**

```bash
# 编译
npm run build

# 在 Claude Code 中注册（项目级别）
claude mcp add weather-tools node dist/weather-server.js

# 验证注册成功
claude mcp list
```

注册完成后，在 Claude Code 中输入「北京今天天气怎么样」，它会自动调用你的 MCP Server。

## Skills 与 Hooks

### 目标

学会编写 Skill 文件封装常用操作，配置 Hooks 实现自动化流程。

### 内容

**Skills 是什么：**

Skills 是 Markdown 格式的指令文件，存放在项目的 `.claude/skills/` 目录下。Claude Code 会自动读取这些文件，将其作为操作指南来执行特定任务。与直接对话不同，Skill 是持久化的、可复用的。

**示例：部署 Skill**

```markdown
<!-- .claude/skills/deploy.md -->
# 部署到生产环境

## 前置检查
1. 运行 `npm run lint` 确保代码风格检查通过
2. 运行 `npm run test` 确保所有测试通过
3. 运行 `npm run build` 确保构建成功

## 部署步骤
1. 切换到 main 分支并拉取最新代码
2. 创建发布标签：`git tag v$(date +%Y%m%d%H%M%S)`
3. 执行部署命令：`vercel --prod --yes`
4. 验证线上服务状态：访问 /health 接口确认返回 200

## 异常处理
- 如果构建失败，回滚到上一个标签
- 如果部署后健康检查失败，立即通知并回滚
```

**示例：代码审查 Skill**

```markdown
<!-- .claude/skills/review.md -->
# 代码审查清单

## 审查范围
检查当前 Git diff 中的所有变更文件。

## 审查要点
1. **安全性**：检查 SQL 注入、XSS、敏感信息泄露
2. **健壮性**：错误处理是否完整，边界条件是否覆盖
3. **可读性**：命名是否清晰，注释是否必要且准确
4. **性能**：是否有 N+1 查询、不必要的循环、内存泄漏风险
5. **测试**：新增代码是否有对应测试

## 输出格式
按文件列出问题，标注严重程度（高/中/低），给出修改建议。
```

**Hooks 配置：**

Hooks 让你在特定事件触发时自动执行命令。在项目根目录的 `.claude/settings.json` 中配置：

```json
{
  "hooks": {
    "pre-commit": {
      "command": "npm run lint && npm run test",
      "description": "提交前自动运行代码检查和测试"
    },
    "post-save": {
      "command": "npx prettier --write $FILE",
      "description": "保存文件后自动格式化"
    }
  }
}
```

## Agent SDK 简介

### 目标

了解 Agent SDK 的核心概念，知道如何用它构建自主运行的 AI 代理。

### 内容

Agent SDK 是 Anthropic 提供的开发框架，用于构建能够自主规划、执行多步骤任务的 AI 代理。与直接对话不同，Agent 可以在无人干预的情况下持续工作。

**核心概念：**

- **Agent**：一个带有系统指令和工具集的自主执行单元
- **Tool**：Agent 可以调用的能力（读写文件、执行命令、调用 API 等）
- **Loop**：Agent 的执行循环 -- 思考、选择工具、执行、观察结果、继续思考

**典型应用场景：**

- 自动化代码审查：Agent 读取 PR diff，逐文件分析，输出审查报告
- 批量数据处理：Agent 遍历数据集，逐条处理，汇总结果
- 多步骤部署：Agent 执行构建、测试、部署、验证的完整流水线

**基本使用示例：**

```typescript
import { Agent } from "@anthropic-ai/agent-sdk";

const agent = new Agent({
  model: "intern-s1-pro",
  system: "你是一个代码审查助手，负责审查 Python 代码的质量和安全性。",
  tools: ["read_file", "write_file", "run_command"],
});

const result = await agent.run(
  "审查 src/ 目录下所有 Python 文件，生成审查报告保存到 review-report.md"
);

console.log(result.output);
```

Agent SDK 的完整文档可参考 Anthropic 官方文档。本课程聚焦实战应用，更深入的 Agent 开发将在后续课程中展开。

## 参考资料

- [Claude Code 官方文档](https://docs.anthropic.com/en/docs/claude-code)
- [MCP 协议规范](https://modelcontextprotocol.io)
- [Anthropic Agent SDK](https://github.com/anthropics/agent-sdk)
- [书生大模型社区](https://community.intern-ai.org.cn)
