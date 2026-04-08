# MCP 工具集成与科学应用

## 课程简介

MCP（Model Context Protocol）是由 Anthropic 发起的开放标准协议，为 AI 模型提供了连接外部工具和数据源的统一接口。自发布以来，MCP 月下载量已超过 9700 万，成为 AI 工具生态中事实上的标准。本课程从协议原理讲起，带你用 TypeScript 和 Python 开发 MCP Server，并结合 Intern-S1 科学多模态大模型实现科学领域的工具集成。

## 你将学到

- 理解 MCP 协议的架构设计（Host / Client / Server）
- 掌握 MCP 的三种核心能力：Tools、Resources、Prompts
- 使用 TypeScript SDK 开发 MCP Server
- 使用 Python FastMCP 框架开发 MCP Server
- 将 MCP Server 注册到 Claude Code 并调试
- 结合 Intern-S1 构建科学领域的工具应用

## MCP 协议原理

### 目标

理解 MCP 协议的设计动机、架构组成和通信流程。

### 内容

**为什么需要 MCP：**

大语言模型的知识有截止日期，也无法直接操作外部系统。传统做法是为每个 AI 应用单独编写集成代码，这导致了 N x M 的对接问题 -- N 个 AI 应用要对接 M 个外部服务，总共需要 N x M 个适配器。

MCP 通过标准化协议将这个问题简化为 N + M：每个 AI 应用实现一次 MCP Client，每个外部服务实现一次 MCP Server，双方就能互通。

**架构组成：**

MCP 采用三层架构：

```
Host（宿主应用）
  |
  |-- Client（MCP 客户端，1:1 对应一个 Server）
  |     |
  |     |-- Server A（天气服务）
  |     |-- Server B（数据库服务）
  |     |-- Server C（文件系统服务）
```

- **Host**：发起连接的应用程序（如 Claude Code、IDE 插件）
- **Client**：由 Host 创建，与一个 Server 保持连接，处理协议通信
- **Server**：提供具体能力的服务端，暴露 Tools / Resources / Prompts

**三种核心能力：**

| 能力 | 说明 | 控制方 | 典型用途 |
|------|------|--------|----------|
| Tools | AI 可调用的函数 | 模型决定何时调用 | 查询天气、操作数据库 |
| Resources | 可读取的数据源 | 应用决定何时读取 | 配置文件、日志、文档 |
| Prompts | 预定义的提示模板 | 用户选择使用 | 代码审查模板、分析报告模板 |

**通信方式：**

MCP 支持两种传输机制：

- **Stdio**：通过标准输入输出通信，适合本地进程。Claude Code 主要使用这种方式。
- **HTTP + SSE**：通过 HTTP 请求和 Server-Sent Events 通信，适合远程服务。

## TypeScript MCP Server 开发

### 目标

使用 TypeScript SDK 开发一个功能完整的 MCP Server。

### 内容

**项目初始化：**

```bash
mkdir my-mcp-server && cd my-mcp-server
npm init -y
npm install @modelcontextprotocol/sdk zod
npm install -D typescript @types/node
```

创建 `tsconfig.json`：

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src"]
}
```

在 `package.json` 中添加：

```json
{
  "type": "module",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js"
  }
}
```

**完整示例 -- 文件分析 MCP Server：**

以下 Server 提供三种能力：文件统计工具、项目结构资源、代码分析提示模板。

```typescript
// src/index.ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { readFileSync, readdirSync, statSync } from "fs";
import { join, extname } from "path";

const server = new McpServer({
  name: "file-analyzer",
  version: "1.0.0",
});

// ===== Tool 1：统计目录中的文件信息 =====
server.tool(
  "count_files",
  "统计指定目录下的文件数量和类型分布",
  {
    directory: z.string().describe("要统计的目录路径"),
    recursive: z.boolean().default(false).describe("是否递归统计子目录"),
  },
  async ({ directory, recursive }) => {
    const stats: Record<string, number> = {};
    let totalSize = 0;

    function scan(dir: string) {
      const entries = readdirSync(dir, { withFileTypes: true });
      for (const entry of entries) {
        const fullPath = join(dir, entry.name);
        if (entry.isFile()) {
          const ext = extname(entry.name) || "(no extension)";
          stats[ext] = (stats[ext] || 0) + 1;
          totalSize += statSync(fullPath).size;
        } else if (entry.isDirectory() && recursive) {
          if (!entry.name.startsWith(".") && entry.name !== "node_modules") {
            scan(fullPath);
          }
        }
      }
    }

    try {
      scan(directory);
      const lines = Object.entries(stats)
        .sort((a, b) => b[1] - a[1])
        .map(([ext, count]) => `  ${ext}: ${count} 个文件`);

      const totalFiles = Object.values(stats).reduce((a, b) => a + b, 0);
      const sizeStr =
        totalSize > 1024 * 1024
          ? `${(totalSize / 1024 / 1024).toFixed(1)} MB`
          : `${(totalSize / 1024).toFixed(1)} KB`;

      return {
        content: [
          {
            type: "text",
            text: `目录: ${directory}\n文件总数: ${totalFiles}\n总大小: ${sizeStr}\n\n类型分布:\n${lines.join("\n")}`,
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          { type: "text", text: `错误: ${(error as Error).message}` },
        ],
        isError: true,
      };
    }
  }
);

// ===== Tool 2：读取文件内容并统计行数 =====
server.tool(
  "analyze_file",
  "读取文件内容，统计行数、字符数和空行数",
  {
    filepath: z.string().describe("文件路径"),
  },
  async ({ filepath }) => {
    try {
      const content = readFileSync(filepath, "utf-8");
      const lines = content.split("\n");
      const nonEmpty = lines.filter((l) => l.trim().length > 0).length;
      const empty = lines.length - nonEmpty;

      return {
        content: [
          {
            type: "text",
            text: [
              `文件: ${filepath}`,
              `总行数: ${lines.length}`,
              `有效行: ${nonEmpty}`,
              `空行: ${empty}`,
              `字符数: ${content.length}`,
              `---`,
              content.length > 2000
                ? content.substring(0, 2000) + "\n... (内容截断)"
                : content,
            ].join("\n"),
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          { type: "text", text: `错误: ${(error as Error).message}` },
        ],
        isError: true,
      };
    }
  }
);

// ===== Resource：项目结构 =====
server.resource("project-structure", "project://structure", async (uri) => {
  try {
    const entries = readdirSync(".", { withFileTypes: true });
    const tree = entries
      .filter((e) => !e.name.startsWith(".") && e.name !== "node_modules")
      .map((e) => `${e.isDirectory() ? "[DIR]" : "[FILE]"} ${e.name}`)
      .join("\n");

    return {
      contents: [
        {
          uri: uri.href,
          mimeType: "text/plain",
          text: `项目根目录结构:\n${tree}`,
        },
      ],
    };
  } catch (error) {
    return {
      contents: [
        {
          uri: uri.href,
          mimeType: "text/plain",
          text: `错误: ${(error as Error).message}`,
        },
      ],
    };
  }
});

// ===== Prompt：代码审查模板 =====
server.prompt(
  "code-review",
  "生成代码审查提示",
  { language: z.string().describe("编程语言") },
  ({ language }) => ({
    messages: [
      {
        role: "user",
        content: {
          type: "text",
          text: `请对以下 ${language} 代码进行审查，关注以下方面：
1. 代码正确性和逻辑完整性
2. 错误处理是否充分
3. 性能优化空间
4. 安全风险
5. 代码可读性和命名规范

请给出具体的改进建议和修改后的代码示例。`,
        },
      },
    ],
  })
);

// ===== 启动服务器 =====
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("File Analyzer MCP Server 已启动");
}

main().catch(console.error);
```

**编译与注册：**

```bash
# 编译
npm run build

# 注册到 Claude Code
claude mcp add file-analyzer node dist/index.js

# 验证
claude mcp list
```

## Python MCP Server 开发

### 目标

使用 Python FastMCP 框架快速开发 MCP Server。

### 内容

Python 生态有官方维护的 FastMCP 框架，API 设计简洁，适合快速开发。

**安装依赖：**

```bash
pip install mcp
```

**完整示例 -- 数学计算 MCP Server：**

```python
# math_server.py
from mcp.server.fastmcp import FastMCP
import math

mcp = FastMCP("math-tools")


@mcp.tool()
def calculate_statistics(numbers: list[float]) -> str:
    """计算一组数字的统计信息（均值、中位数、标准差、最大最小值）"""
    if not numbers:
        return "错误：数字列表不能为空"

    n = len(numbers)
    mean = sum(numbers) / n
    sorted_nums = sorted(numbers)

    if n % 2 == 0:
        median = (sorted_nums[n // 2 - 1] + sorted_nums[n // 2]) / 2
    else:
        median = sorted_nums[n // 2]

    variance = sum((x - mean) ** 2 for x in numbers) / n
    std_dev = math.sqrt(variance)

    return (
        f"样本数: {n}\n"
        f"均值: {mean:.4f}\n"
        f"中位数: {median:.4f}\n"
        f"标准差: {std_dev:.4f}\n"
        f"最小值: {min(numbers)}\n"
        f"最大值: {max(numbers)}\n"
        f"极差: {max(numbers) - min(numbers)}"
    )


@mcp.tool()
def solve_quadratic(a: float, b: float, c: float) -> str:
    """求解一元二次方程 ax^2 + bx + c = 0"""
    if a == 0:
        if b == 0:
            return "不是有效方程" if c != 0 else "恒等式，任意 x 都是解"
        return f"一次方程，x = {-c / b:.6f}"

    discriminant = b**2 - 4 * a * c

    if discriminant > 0:
        x1 = (-b + math.sqrt(discriminant)) / (2 * a)
        x2 = (-b - math.sqrt(discriminant)) / (2 * a)
        return (
            f"方程: {a}x^2 + {b}x + {c} = 0\n"
            f"判别式: {discriminant:.4f} > 0\n"
            f"两个实数根:\n"
            f"  x1 = {x1:.6f}\n"
            f"  x2 = {x2:.6f}"
        )
    elif discriminant == 0:
        x = -b / (2 * a)
        return (
            f"方程: {a}x^2 + {b}x + {c} = 0\n"
            f"判别式: 0\n"
            f"唯一实数根: x = {x:.6f}"
        )
    else:
        real_part = -b / (2 * a)
        imag_part = math.sqrt(-discriminant) / (2 * a)
        return (
            f"方程: {a}x^2 + {b}x + {c} = 0\n"
            f"判别式: {discriminant:.4f} < 0\n"
            f"两个复数根:\n"
            f"  x1 = {real_part:.6f} + {imag_part:.6f}i\n"
            f"  x2 = {real_part:.6f} - {imag_part:.6f}i"
        )


@mcp.tool()
def matrix_multiply(
    matrix_a: list[list[float]], matrix_b: list[list[float]]
) -> str:
    """计算两个矩阵的乘积"""
    rows_a, cols_a = len(matrix_a), len(matrix_a[0])
    rows_b, cols_b = len(matrix_b), len(matrix_b[0])

    if cols_a != rows_b:
        return f"错误：矩阵维度不匹配（{rows_a}x{cols_a} 和 {rows_b}x{cols_b}）"

    result = [[0.0] * cols_b for _ in range(rows_a)]
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                result[i][j] += matrix_a[i][k] * matrix_b[k][j]

    lines = [f"结果矩阵 ({rows_a}x{cols_b}):"]
    for row in result:
        lines.append("  [" + ", ".join(f"{v:.4f}" for v in row) + "]")
    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run()
```

**注册到 Claude Code：**

```bash
# 注册 Python MCP Server
claude mcp add math-tools python math_server.py

# 验证
claude mcp list
```

注册后在 Claude Code 中可以直接使用自然语言触发：

```
帮我计算 [12, 15, 18, 22, 25, 30] 这组数据的统计信息。
```

```
求解方程 2x^2 - 5x + 3 = 0
```

## Intern-S1 科学应用

### 目标

结合 MCP 和 Intern-S1 科学多模态大模型，构建科学领域的工具应用。

### 内容

Intern-S1 是书生系列的科学多模态大模型，在数学推理、科学分析等领域表现出色。通过 MCP 将科学计算工具接入 AI，可以构建强大的科学助手。

**示例场景：科学数据分析助手**

将数据分析工具通过 MCP 暴露给 AI，让 Intern-S1 既能理解科学问题，又能调用工具进行精确计算：

```python
# science_server.py
from mcp.server.fastmcp import FastMCP
import math
import json

mcp = FastMCP("science-tools")


@mcp.tool()
def linear_regression(x_values: list[float], y_values: list[float]) -> str:
    """对给定数据进行线性回归分析，返回斜率、截距和 R^2"""
    if len(x_values) != len(y_values):
        return "错误：x 和 y 的数据点数量不一致"

    n = len(x_values)
    if n < 2:
        return "错误：至少需要 2 个数据点"

    sum_x = sum(x_values)
    sum_y = sum(y_values)
    sum_xy = sum(x * y for x, y in zip(x_values, y_values))
    sum_x2 = sum(x**2 for x in x_values)
    sum_y2 = sum(y**2 for y in y_values)

    denominator = n * sum_x2 - sum_x**2
    if denominator == 0:
        return "错误：x 值完全相同，无法拟合"

    slope = (n * sum_xy - sum_x * sum_y) / denominator
    intercept = (sum_y - slope * sum_x) / n

    ss_res = sum((y - (slope * x + intercept)) ** 2
                 for x, y in zip(x_values, y_values))
    ss_tot = sum((y - sum_y / n) ** 2 for y in y_values)
    r_squared = 1 - ss_res / ss_tot if ss_tot != 0 else 0

    return (
        f"线性回归结果:\n"
        f"  方程: y = {slope:.6f}x + {intercept:.6f}\n"
        f"  斜率: {slope:.6f}\n"
        f"  截距: {intercept:.6f}\n"
        f"  R^2: {r_squared:.6f}\n"
        f"  相关性: {'强' if r_squared > 0.8 else '中等' if r_squared > 0.5 else '弱'}"
    )


@mcp.tool()
def unit_convert(
    value: float, from_unit: str, to_unit: str
) -> str:
    """科学单位换算（支持长度、质量、温度、压强、能量）"""
    conversions = {
        # 长度 -> 米
        "m": 1.0, "km": 1000.0, "cm": 0.01, "mm": 0.001,
        "um": 1e-6, "nm": 1e-9, "angstrom": 1e-10,
        "mile": 1609.344, "ft": 0.3048, "inch": 0.0254,
        # 质量 -> 千克
        "kg": 1.0, "g": 0.001, "mg": 1e-6, "ug": 1e-9,
        "lb": 0.453592, "oz": 0.0283495, "ton": 1000.0,
        # 压强 -> 帕斯卡
        "Pa": 1.0, "kPa": 1000.0, "MPa": 1e6,
        "atm": 101325.0, "bar": 100000.0, "mmHg": 133.322,
        # 能量 -> 焦耳
        "J": 1.0, "kJ": 1000.0, "cal": 4.184, "kcal": 4184.0,
        "eV": 1.602176634e-19, "kWh": 3.6e6,
    }

    # 温度特殊处理
    temp_units = {"C", "F", "K"}
    if from_unit in temp_units and to_unit in temp_units:
        # 先转为开尔文
        if from_unit == "C":
            k = value + 273.15
        elif from_unit == "F":
            k = (value - 32) * 5 / 9 + 273.15
        else:
            k = value

        if to_unit == "C":
            result = k - 273.15
        elif to_unit == "F":
            result = (k - 273.15) * 9 / 5 + 32
        else:
            result = k

        return f"{value} {from_unit} = {result:.4f} {to_unit}"

    if from_unit not in conversions or to_unit not in conversions:
        supported = ", ".join(sorted(conversions.keys()))
        return f"不支持的单位。支持的单位: {supported}, C, F, K"

    # 转为基准单位再转为目标单位
    base_value = value * conversions[from_unit]
    result = base_value / conversions[to_unit]
    return f"{value} {from_unit} = {result:.6g} {to_unit}"


if __name__ == "__main__":
    mcp.run()
```

注册后，你可以在 Claude Code 中这样使用：

```
我有一组实验数据：
温度(C): [20, 30, 40, 50, 60, 70, 80]
反应速率(mol/s): [0.5, 0.8, 1.3, 2.1, 3.2, 5.0, 7.8]

请分析温度和反应速率的关系，并将温度从摄氏度转换为开尔文。
```

Intern-S1 会理解这是一个化学动力学问题，自动调用线性回归工具和单位换算工具，并结合科学知识给出分析。

## 调试与最佳实践

### 目标

掌握 MCP Server 的调试方法和开发最佳实践。

### 内容

**调试工具：**

MCP 官方提供了 Inspector 工具，可以在浏览器中可视化测试 Server：

```bash
npx @modelcontextprotocol/inspector node dist/index.js
```

Inspector 会在浏览器中打开一个界面，列出 Server 暴露的所有 Tools、Resources 和 Prompts，可以手动调用并查看返回结果。

**日志输出：**

MCP Server 的标准输出被协议占用，调试信息应输出到标准错误：

```typescript
// 正确：输出到 stderr
console.error("调试信息：收到请求", params);

// 错误：会干扰协议通信
console.log("不要用 stdout 输出调试信息");
```

**错误处理规范：**

```typescript
server.tool("my_tool", "描述", { input: z.string() }, async ({ input }) => {
  try {
    const result = doSomething(input);
    return {
      content: [{ type: "text", text: result }],
    };
  } catch (error) {
    return {
      content: [{ type: "text", text: `操作失败: ${(error as Error).message}` }],
      isError: true,
    };
  }
});
```

**最佳实践清单：**

1. 每个 Tool 写清楚描述，AI 靠描述来判断何时调用
2. 参数使用 zod 验证，给出 `.describe()` 说明
3. 返回结构化文本，方便 AI 理解和引用
4. 错误返回设置 `isError: true`，AI 会知道需要换个方式处理
5. Server 名称和 Tool 名称使用英文 kebab-case
6. 保持 Server 职责单一，一个 Server 聚焦一个领域

## 参考资料

- [MCP 官方文档](https://modelcontextprotocol.io)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector)
- [MCP Servers 合集](https://github.com/modelcontextprotocol/servers)
