
# MCP 协议详解

> **配套视频**：[MCP：AI 世界的 USB 接口](https://c.vansin.top/video/v3/knowledge-mcp-v3.mp4)

## 什么是 MCP？

MCP（Model Context Protocol，模型上下文协议）是 Anthropic 于 2024 年 11 月开源的通信协议。它的核心理念非常简单：**给 AI 一个标准接口，让它能连接任何外部工具和数据**。

就像 USB 让所有外设都能连接电脑一样，MCP 让所有工具都能连接 AI。

## 为什么需要 MCP？

没有 MCP 之前，AI 被困在「聊天框」里：

| 能力 | 没有 MCP | 有 MCP |
|------|---------|--------|
| 数据库查询 | 不能直接查，只能让用户复制粘贴 | 直接连接数据库，实时查询 |
| 文件操作 | 只能读用户上传的文件 | 直接读写本地文件系统 |
| API 调用 | 需要用户手动转发 | 自动调用外部 API |
| 代码执行 | 只能生成代码，不能运行 | 在沙箱中运行代码并返回结果 |

MCP 的月下载量已超过 9700 万次，被 OpenAI、Google、Microsoft、Amazon 全部采纳。

## MCP 架构

### 三个角色

```
┌──────────────┐     MCP 协议     ┌──────────────┐
│  MCP Client  │ ◄─────────────► │  MCP Server  │
│  (AI 应用)   │                  │  (工具服务)  │
│              │                  │              │
│  Claude Code │                  │  数据库       │
│  Cursor      │                  │  文件系统     │
│  自定义应用   │                  │  GitHub API   │
└──────────────┘                  └──────────────┘
       ▲
       │ 调用
       ▼
┌──────────────┐
│  LLM (Host)  │
│  Intern-S1   │
└──────────────┘
```

- **Host**：运行 LLM 的应用（如 Claude Code）
- **Client**：MCP 客户端，负责与 Server 通信
- **Server**：提供工具、资源和提示的服务端

### 三种能力

| 能力 | 说明 | 示例 |
|------|------|------|
| **Tools**（工具） | 可被 AI 调用的函数 | 查数据库、发邮件、运行代码 |
| **Resources**（资源） | 可被 AI 读取的数据 | 文件内容、API 响应、配置信息 |
| **Prompts**（提示） | 预定义的提示模板 | 代码审查模板、翻译模板 |

## 开发 MCP Server

### TypeScript 实现

```typescript
import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new McpServer({
  name: "我的工具服务",
  version: "1.0.0"
});

// 注册一个工具
server.tool(
  "查询天气",
  { city: { type: "string", description: "城市名" } },
  async ({ city }) => {
    const weather = await fetchWeather(city);
    return { content: [{ type: "text", text: `${city}天气：${weather}` }] };
  }
);

// 注册一个资源
server.resource(
  "config",
  "config://app",
  async (uri) => ({
    contents: [{ uri: uri.href, text: JSON.stringify(appConfig) }]
  })
);

// 启动
const transport = new StdioServerTransport();
await server.connect(transport);
```

### Python 实现

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("我的工具服务")

@mcp.tool()
async def query_weather(city: str) -> str:
    """查询指定城市的天气"""
    weather = await fetch_weather(city)
    return f"{city}天气：{weather}"

@mcp.resource("config://app")
async def get_config() -> str:
    """获取应用配置"""
    return json.dumps(app_config)

mcp.run()
```

## 在 Claude Code 中使用 MCP

Claude Code 原生支持 MCP Server：

```bash
# 添加 MCP Server
claude mcp add weather-server -- npx weather-mcp-server

# 查看已安装的 MCP Server
claude mcp list

# 在对话中，AI 会自动发现并调用 MCP 工具
```

### 配置文件方式

```json
// .claude/settings.json
{
  "mcpServers": {
    "weather": {
      "command": "npx",
      "args": ["weather-mcp-server"],
      "env": {
        "API_KEY": "your-key"
      }
    },
    "database": {
      "command": "python",
      "args": ["db_mcp_server.py"],
      "env": {
        "DB_URL": "postgresql://..."
      }
    }
  }
}
```

## 用 Intern-S1-Pro 构建 MCP 应用

### 场景：科研论文助手

```
用户 → Claude Code (Intern-S1-Pro)
         ├── MCP: arXiv Server  → 搜索和下载论文
         ├── MCP: PDF Parser    → 解析论文 PDF
         ├── MCP: Database      → 存储笔记和标注
         └── MCP: Citation      → 生成引用格式
```

### 关键配置

```bash
# 设置 Claude Code 使用 Intern-S1-Pro
export ANTHROPIC_BASE_URL="https://chat.intern-ai.org.cn/api"
export ANTHROPIC_AUTH_TOKEN="your-api-key"

# 启动 Claude Code 并选择模型
claude --model intern-s1-pro
```

## 社区 MCP Server 生态

| MCP Server | 功能 | 适用场景 |
|------------|------|---------|
| @modelcontextprotocol/server-filesystem | 文件系统读写 | 代码编辑 |
| @modelcontextprotocol/server-github | GitHub API | 项目管理 |
| @modelcontextprotocol/server-postgres | PostgreSQL 查询 | 数据分析 |
| @modelcontextprotocol/server-brave-search | 网页搜索 | 信息检索 |
| @modelcontextprotocol/server-puppeteer | 浏览器自动化 | 网页交互 |

## 进阶实践（Intern-S1-Pro 专题）

### 实操任务

1. **开发 MCP Server**：用 TypeScript 或 Python 实现一个自定义 MCP Server
2. **集成到 Claude Code**：将自定义 MCP Server 注册到 Claude Code 中使用
3. **科研场景应用**：用 Intern-S1-Pro + MCP 构建一个论文检索和分析工具

### 交付物

- 自定义 MCP Server 代码仓库
- 使用演示视频或 GIF
- 工具调用日志和效果对比报告

### 自检清单

- [ ] 理解 MCP 的 Host / Client / Server 三层架构
- [ ] 能区分 Tools、Resources、Prompts 三种能力
- [ ] 实现了一个包含至少 2 个 Tool 的 MCP Server
- [ ] 在 Claude Code 中成功调用了自定义 MCP Server
- [ ] 理解 MCP 与 A2A 的互补关系

## 延伸阅读

- [MCP 官方文档](https://modelcontextprotocol.io/)
- [MCP GitHub 仓库](https://github.com/modelcontextprotocol)
- [Agent2Agent (A2A) 协议](/zh/docs/learn/core/agent2agent)——Agent 之间的通信协议
- [Function Calling 与 Tool Use](/zh/docs/learn/core/function-calling)
- [AI Agent 原理与架构](/zh/docs/learn/core/ai-agent)
