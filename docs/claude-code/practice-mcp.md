# Claude Code 实战 · MCP Server 最小示例

> 本节在**昇腾 Atlas 800T A2 + Intern-S1-Pro** 上亲测跑通。

**目标：** 20 行 Python 写一个 weather MCP server，注册到 Claude Code，让 Intern-S1-Pro 自动通过 MCP 协议调用它查天气。

## 什么是 MCP

**Model Context Protocol**（MCP）是 Anthropic 提出的、LLM 与外部工具 / 数据源对接的开放协议。一个 MCP Server 暴露若干"工具"（tool），Claude Code 启动时会拉取这份工具清单交给模型。模型就像调用内置 Read / Write 一样调用它们。

典型场景：

- 查公司内部 API（工单、HR、库存）
- 跑私有数据库查询
- 连 SaaS（Jira / Slack / Figma / 飞书）
- 本节示范：**查城市天气**（用假数据，专注讲协议，不讲真实 API）

## 第一步：写最小 MCP server（20 行）

`/root/smcp/weather.py`：

```python
"""最小 weather MCP server，stdio transport。返回假数据用于教学演示。"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

SERVER = Server("weather-demo")

FAKE = {
    "beijing":  {"temp_c": 18, "condition": "晴"},
    "shanghai": {"temp_c": 22, "condition": "多云"},
    "shenzhen": {"temp_c": 28, "condition": "小雨"},
    "hangzhou": {"temp_c": 21, "condition": "阴"},
}

@SERVER.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_weather",
            description="查询指定城市的当前天气。city 用英文小写。",
            inputSchema={
                "type": "object",
                "properties": {"city": {"type": "string"}},
                "required": ["city"],
            },
        )
    ]

@SERVER.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name != "get_weather":
        return [TextContent(type="text", text=f"未知工具: {name}")]
    city = (arguments.get("city") or "").strip().lower()
    data = FAKE.get(city)
    if not data:
        return [TextContent(type="text", text=f"未找到 {city} 的天气数据。支持: {', '.join(FAKE)}")]
    return [TextContent(type="text", text=f"{city} 当前 {data['temp_c']}°C，{data['condition']}。（演示假数据）")]

async def main():
    async with stdio_server() as (read, write):
        await SERVER.run(read, write, SERVER.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

装依赖（昇腾 aarch64 实测 OK）：

```bash
pip install mcp
```

## 第二步：注册到 Claude Code

在项目目录下（这里是 `/root/smcp`）执行：

```bash
claude mcp add weather-demo --scope project -- /root/.conda/bin/python /root/smcp/weather.py
```

注意：

- `--scope project` 会把配置写到当前目录的 `.mcp.json`，仅这个项目启用。
- `--` 后面是启动命令；path 建议用绝对路径，避免 claude 启动时 cwd 不同导致找不到 server。

执行后会生成 `.mcp.json`：

```json
{
  "mcpServers": {
    "weather-demo": {
      "type": "stdio",
      "command": "/root/.conda/bin/python",
      "args": ["/root/smcp/weather.py"],
      "env": {}
    }
  }
}
```

## 第三步：让模型调用

进到 `.mcp.json` 所在目录，启动 claude：

```bash
export ANTHROPIC_BASE_URL=https://chat.intern-ai.org.cn
export ANTHROPIC_AUTH_TOKEN=<你的 token>

cd /root/smcp
claude --model intern-s1-pro --permission-mode acceptEdits \
  --allowedTools "mcp__weather-demo__get_weather"
```

> MCP 工具的内部名是 `mcp__<server_name>__<tool_name>`，要显式加到 `--allowedTools`，否则默认会要求交互授权。

交互模式下直接问：

```
beijing 和 shenzhen 现在天气怎么样？
```

## 实测结果（Intern-S1-Pro，昇腾）

- 耗时：25.8 秒
- 费用：$0.21（input 68,398 / output 262 tokens，3 turns）
- 调用次数：2 次 MCP 工具

stream-json 日志摘录（连接状态）：

```json
{"type":"system","subtype":"init",
 "mcp_servers":[{"name":"weather-demo","status":"connected"}],
 ...
 "tools":[..., "mcp__weather-demo__get_weather"]
}
```

模型调用（城市 1）：

```json
{"type":"assistant",
 "message":{"content":[{
   "input":{"city":"beijing"},
   "name":"mcp__weather-demo__get_weather",
   "type":"tool_use"}]}}
```

服务器返回：

```
beijing 当前 18°C，晴。（演示假数据）
```

第二次调用 `city: "shenzhen"` 返回 `shenzhen 当前 28°C，小雨。（演示假数据）`。

模型最终文本输出：

```
beijing 当前 18°C，晴。（演示假数据）

shenzhen 当前 28°C，小雨。（演示假数据）
```

## 经验

- **MCP server 本身非常小**——先把协议跑通（用假数据/hard-code），再换成真实 API。
- **Intern-S1-Pro 对 MCP 工具的调用稳定性是四种 case 里最好的**：tool_use 一次命中，结果原样透传，几乎没有"想而不动"的问题。猜测原因：MCP 工具 schema 明确，不像 Bash 那种开放命令行。
- **stdio transport 最简单**：不需要跑 HTTP server，开进程即用完即终，适合本地工具。
- **生产环境想加 auth / 限流**：用 HTTP transport + 反向代理；MCP 官方 doc 有示例。

## 延伸

- MCP 官方规范：[modelcontextprotocol.io](https://modelcontextprotocol.io/)
- 书生社区有托管的 MCP server 给学员直接接入（后续章节单独写）
- 下一步可以把这个 weather server 改成"查昇腾集群 NPU 状态"，给 Claude Code 做真实运维助手

## 下一步

- 回「总览」Tab 学习 Skills、Hooks
- 看 [Skills 最小示例](?section=practice-skills) 了解 Skill 和 MCP 的差异
