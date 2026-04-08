
# Function Calling 与 Tool Use

当你问 LLM "今天上海天气怎样"，它无法真正查天气——因为它只是一个语言模型。Function Calling 就是给 LLM 装上"遥控器"，让它能够按下按钮调用外部工具获取真实信息。

## 什么是 Function Calling？

Function Calling（函数调用）是让 LLM 在对话中识别用户意图，并生成**结构化的函数调用请求**，由外部系统执行后将结果返回给模型。

```
用户: "帮我查一下北京到上海的机票"
         │
         ▼
┌─────────────────────┐
│  LLM 分析用户意图     │
│  决定调用 search_flights│
│  生成参数 JSON        │
└──────────┬──────────┘
           │
           ▼
  {
    "name": "search_flights",
    "arguments": {
      "from": "北京",
      "to": "上海",
      "date": "2026-02-28"
    }
  }
           │
           ▼
┌─────────────────────┐
│  外部 API 执行查询    │
│  返回航班列表         │
└──────────┬──────────┘
           │
           ▼
  LLM 组织自然语言回答
```

## 定义函数：JSON Schema

告诉模型有哪些工具可以用，需要用 JSON Schema 格式描述函数：

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市的当前天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，如：北京、上海"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "温度单位"
                    }
                },
                "required": ["city"]
            }
        }
    }
]
```

## 完整调用流程

以下是一个使用 OpenAI 兼容接口的完整示例：

```python
from openai import OpenAI
import json

client = OpenAI(
    base_url="https://internlm-chat.intern-ai.org.cn/puyu/api/v1",
    api_key="your-api-key"
)

# 第一步：带 tools 参数发起请求
response = client.chat.completions.create(
    model="internlm3-latest",
    messages=[{"role": "user", "content": "北京今天多少度？"}],
    tools=tools
)

# 第二步：检查是否触发了函数调用
message = response.choices[0].message
if message.tool_calls:
    tool_call = message.tool_calls[0]
    func_name = tool_call.function.name
    func_args = json.loads(tool_call.function.arguments)

    # 第三步：执行函数并获取结果
    result = get_weather(**func_args)

    # 第四步：将结果返回给模型生成最终回答
    messages = [
        {"role": "user", "content": "北京今天多少度？"},
        message,
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)
        }
    ]
    final = client.chat.completions.create(
        model="internlm3-latest",
        messages=messages,
        tools=tools
    )
    print(final.choices[0].message.content)
```

## 常用工具类型

| 工具类型 | 用途 | 示例 |
|---------|------|------|
| 信息查询 | 获取实时数据 | 天气、股票、搜索 |
| 数据操作 | 读写数据库/文件 | SQL 查询、文件读写 |
| 代码执行 | 运行代码获取结果 | Python 计算、绘图 |
| 外部服务 | 调用第三方 API | 发邮件、创建日程 |

## 多函数调用（Parallel Tool Calls）

模型可以在一次回复中同时调用多个函数：

```python
# 用户: "帮我查北京和上海的天气"
# 模型会同时生成两个 tool_calls:
# 1. get_weather(city="北京")
# 2. get_weather(city="上海")
```

## Intern-S1-Pro / InternLM 的 Function Calling

Intern-S1-Pro 以及 InternLM 系列均支持 Function Calling 能力：

- 支持 OpenAI 兼容的 tools 参数格式
- 支持并行工具调用（Parallel Tool Calls）
- 可通过 Lagent 框架实现更复杂的多轮工具调用
- 结合 LMDeploy 部署，可获得高性能的工具调用推理

## 设计好工具的技巧

1. **描述要清晰**：函数和参数的 description 直接影响模型调用准确率
2. **参数要精简**：必填项最小化，可选项给默认值
3. **返回值要明确**：返回结构化数据，方便模型理解
4. **错误要友好**：返回可读的错误信息而非堆栈

## 下一步

- 了解 [AI Agent 原理与架构](/zh/learn/ai-agent)，理解 Function Calling 在 Agent 系统中的角色
- 学习 [RAG 基础](/zh/learn/rag-basics)，结合检索增强与工具调用
- 探索 [Prompt Engineering](/zh/learn/prompt-engineering)，优化工具调用的提示词

## 进阶实践（Intern-S1-Pro 专题）

### 实战任务
1. 设计 3 个工具 Schema（天气、检索、工单），验证参数约束是否足够严格。
2. 构建“多工具并行调用”示例，观察调用排序与结果聚合策略。
3. 为工具调用增加错误码与重试机制，避免模型陷入循环调用。

### 交付物
- 一份《工具 Schema 设计规范》
- 一份《Function Calling 调试日志样例》

### 自检清单
- [ ] 能设计可维护的 JSON Schema
- [ ] 能处理并行调用与异常返回
- [ ] 能避免工具注入和越权调用风险
