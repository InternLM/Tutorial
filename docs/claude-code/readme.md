# Claude Code AI 编程

> 本文档 AI + 社区共建中

## 为什么要学 Claude Code

**到最原始的地方来。** Claude Code 是 Anthropic 官方推出的 AI 编程终端，而 **MCP（Model Context Protocol）** 和 **Skills** 这两套协议就是 Anthropic 提出并沉淀下来的 —— 它们已经成为大模型时代的事实标准（OpenAI、Codex、各家 IDE 插件、各类 Agent 框架都在适配）。

学 Claude Code 不是学一个工具，是站在标准制定者的视角理解：
- **AI 怎么调外部世界**（MCP）
- **AI 怎么把人类工作流变成可复用能力**（Skills）
- **AI 怎么在终端里完成全栈开发**（CLI + Hooks + Agent Loop）

之后无论你换到哪个 AI 编程工具、哪个大模型，这套思维方式都通用。

## 学完你能做什么

在开始安装和配置之前，先看看学完这门课你会获得哪些实际能力。

**从零做一个完整项目。** 你将能够用自然语言描述需求，让 Claude Code 帮你生成项目骨架、实现业务逻辑、编写测试、配置部署流程。从一句话需求到线上可访问的服务，全程在终端中完成。

**开发一个 MCP Server 扩展 AI 能力。** MCP（Model Context Protocol）是让 AI 调用外部工具的标准协议。你将学会编写自己的 MCP Server，比如对接内部 API、查询数据库、操作文件系统，然后注册到 Claude Code 中让 AI 自动调用。

**写一个 Skill 自动化日常工作。** Skill 是存放在项目中的 Markdown 指令文件。你可以把常用的操作流程（部署、审查、测试）写成 Skill，之后只需一句话触发，Claude Code 就按流程执行。

**具体示例：**

- 对 Claude Code 说"帮我创建一个 FastAPI 后端，包含用户注册和登录接口"，它会生成完整的项目结构、路由代码、数据模型和测试用例
- 开发一个天气查询 MCP Server，注册后对 Claude Code 说"北京今天天气怎么样"，它会自动调用你写的工具
- 写一个部署 Skill，之后只需说"部署到生产环境"，Claude Code 就会依次执行 lint、测试、构建、部署、健康检查

## 课程简介

Claude Code 是 Anthropic 官方推出的 AI 编程终端工具，将大语言模型的能力直接融入命令行开发流程。它不是一个编辑器插件，而是一个独立的终端程序。你在终端中用自然语言描述需求，Claude Code 会理解项目上下文、读写文件、执行命令，完成从代码生成到调试部署的全流程工作。

在书生大模型实战营中，我们通过 OpenAI 兼容层接入 Intern-S1-Pro 科学多模态大模型作为底层驱动。Intern-S1-Pro 是书生大模型社区的主力模型，具备强大的代码理解和生成能力。通过兼容层接入意味着 Claude Code 客户端不需要修改，只需要配置环境变量指向书生社区的 API 端点即可。

本课程从零开始，带你掌握以下核心技能：

- 安装与配置 Claude Code，通过 OpenAI 兼容层连接 Intern-S1-Pro 模型
- 使用 Claude Code 进行代码生成、审查、调试和重构
- 开发自定义 MCP Server 扩展 AI 能力边界
- 编写 Skills 文件实现可复用的任务自动化
- 配置 Hooks 实现代码提交前的自动检查
- 了解 Agent SDK 构建自主运行的 AI 代理

## 安装与配置

### 目标

完成 Claude Code 的安装，配置 Intern-S1-Pro 模型接入，启动并完成第一次有意义的对话。

### 第一步：安装 Claude Code

Claude Code 以 npm 全局包的形式分发，需要 Node.js 18 或更高版本。

```bash
# 确认 Node.js 版本（需要 v18+）
node --version

# 全局安装 Claude Code
npm install -g @anthropic-ai/claude-code

# 验证安装成功
claude --version
```

如果你的系统没有 Node.js，按你的平台选一个方式安装：

```bash
# Ubuntu / Debian
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs

# macOS（使用 Homebrew）
brew install node

# 跨平台（用 conda，推荐给已有 conda 环境的学员）
conda create -n cc -c conda-forge nodejs=22 -y
conda activate cc

# 安装完成后验证
node --version   # v22.x
npm --version    # 10.x+
```

#### 华为昇腾 Atlas 800T A2（aarch64）安装

昇腾服务器通常是 aarch64（ARM64）Linux，NodeSource 的 deb 仓库也支持 ARM64，直接走官方脚本即可：

```bash
# 确认是 aarch64（返回 aarch64 即可）
uname -m

# 方式一：NodeSource 源（推荐，官方 LTS）
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs

# 方式二：conda（如果机器已有 miniconda / anaconda）
conda create -n cc -c conda-forge nodejs=22 -y
conda activate cc

# 方式三：nvm（最灵活，多版本切换）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
source ~/.bashrc
nvm install --lts
nvm use --lts

# 验证
node --version
npm --version
```

**昇腾环境注意**：
- Node.js 本身不依赖 GPU/NPU，和 CANN/torch_npu 互不干扰，可以和科学计算环境共存
- 如果机器没有公网：建议先在有网机器上用 `npm install -g @anthropic-ai/claude-code` 装，再把 `~/.npm/_npx` 和全局 bin 打包 rsync 过去，或用 `npm config set registry https://registry.npmmirror.com` 换国内镜像
- Claude Code 在 aarch64 上和 x86_64 行为一致，教材里后续所有命令都适用

### 第二步：配置 Intern-S1-Pro 模型

Claude Code 原生连接 Anthropic 的 Claude 模型。在书生大模型实战营中，我们通过 OpenAI 兼容层接入 Intern-S1-Pro。这意味着 Claude Code 客户端本身不需要任何修改，只需要通过环境变量将 API 请求指向书生社区的端点。

将以下环境变量写入你的 shell 配置文件（`~/.bashrc` 或 `~/.zshrc`）：

```bash
# 书生大模型社区 API 端点（OpenAI 兼容层）
export ANTHROPIC_BASE_URL="https://chat.intern-ai.org.cn/api/v1"

# 你的 API Key（在书生大模型社区个人中心获取）
export ANTHROPIC_API_KEY="your-api-key-here"

# 指定使用 Intern-S1-Pro 模型
export ANTHROPIC_MODEL="intern-s1-pro"
```

写入后使配置生效：

```bash
source ~/.bashrc  # 如果你用的是 bash
# 或
source ~/.zshrc   # 如果你用的是 zsh
```

**API Key 获取方式：**

1. 访问书生大模型社区 https://community.intern-ai.org.cn
2. 登录后进入个人中心
3. 在 API Key 管理页面创建或复制你的 Key
4. 将 Key 替换上面配置中的 `your-api-key-here`

**关于 OpenAI 兼容层的说明：** 书生社区的 API 端点实现了 OpenAI API 的标准接口格式。Claude Code 通过 `ANTHROPIC_BASE_URL` 环境变量支持自定义端点，因此可以无缝对接。你不需要安装额外的适配器或修改任何代码。

### 第三步：启动 Claude Code 并完成第一次对话

```bash
# 进入你的项目目录（或任意目录）
cd your-project

# 启动 Claude Code（显式指定模型）
claude --model intern-s1-pro
```

> 也可以省略 `--model`：上一步设置了 `ANTHROPIC_MODEL=intern-s1-pro` 后 `claude` 默认就用它，命令行 `--model` 只是更显式。

启动后你会进入一个交互式终端界面。Claude Code 会自动扫描当前目录的文件结构，建立项目上下文。

**第一次有意义的对话：**

不要只是说"你好"。试试让 Claude Code 做一件实际有用的事情来验证配置是否正常。在终端中输入：

```
分析当前目录的项目结构，告诉我这是什么类型的项目，
用了哪些技术栈，入口文件是什么，如何运行。
```

如果你的目录是空的，可以试试这个：

```
创建一个 Python 脚本，接收命令行参数指定一个目录路径，
统计该目录下所有文件的行数，按文件类型分组汇总，
输出结果按行数从多到少排序。
```

Claude Code 会生成代码文件，你可以直接运行验证：

```bash
python line_counter.py ./your-directory
```

如果以上步骤都能正常执行并得到合理输出，说明安装和配置全部成功。

## 日常开发实战

### 目标

掌握 Claude Code 在实际开发中最常用的场景：代码生成、Bug 调试、代码审查和代码重构。这一节不只是列功能，而是给出每个场景从头到尾的完整流程。

### 场景一：代码生成 -- 从需求到可运行代码

代码生成不是简单地让 AI 写一个函数。实际开发中，你需要从需求出发，经过多轮对话逐步细化，最终得到可运行的完整代码。以下是一个完整流程。

**第一步：描述需求**

在 Claude Code 终端中输入：

```
创建一个 Python FastAPI 服务，要求如下：
1. GET /health 接口返回服务状态和启动时间
2. POST /analyze 接口接收 JSON 格式的文本输入，返回：
   - 文本长度（字符数）
   - 词数统计
   - 最常出现的前 5 个词
3. 所有接口需要输入校验和错误处理
4. 包含完整的类型注解
5. 生成 requirements.txt
```

Claude Code 会在当前目录生成项目文件。

**第二步：验证生成结果**

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn main:app --reload

# 新开一个终端测试
curl http://localhost:8000/health

curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Claude Code 是一个强大的 AI 编程工具，它可以帮助开发者更高效地编写代码"}'
```

**第三步：根据测试结果迭代**

如果发现返回结果不符合预期，继续在 Claude Code 中反馈：

```
/analyze 接口对中文分词不准确，请使用 jieba 分词库处理中文文本，
同时保持对英文文本的兼容性。更新 requirements.txt。
```

Claude Code 会修改已有文件而不是重新创建，保持项目的连续性。

**要点：** 代码生成的关键在于需求描述的清晰度。描述越具体，生成的代码越接近你的预期。如果一次生成的结果不完美，通过对话迭代比重新描述更高效。

### 场景二：Bug 调试 -- 描述问题到修复验证

遇到 Bug 时，直接把错误信息交给 Claude Code，让它帮你定位和修复。

**第一步：描述问题**

```
运行 python main.py 时出现以下错误：

Traceback (most recent call last):
  File "main.py", line 42, in process_data
    result = data["key"]["nested"]
KeyError: 'nested'

请分析原因并修复。
```

**第二步：Claude Code 的调试过程**

Claude Code 会执行以下步骤（你可以在终端中观察到）：

1. 读取 `main.py` 文件内容，理解代码逻辑
2. 定位到第 42 行，分析 `data` 变量的数据结构
3. 查找调用 `process_data` 的上游代码，追溯数据来源
4. 提出修复方案（通常是添加键存在性检查或使用 `.get()` 方法）
5. 直接修改文件

**第三步：验证修复**

```
修复完成后请运行 python main.py 验证是否还有报错。
如果有其他问题继续修复。
```

**调试技巧：**

- 把完整的错误堆栈贴进去，不要只贴最后一行
- 如果是偶发性 Bug，描述触发条件（比如"只在输入为空列表时出现"）
- 复杂 Bug 可以让 Claude Code 先加日志定位，再修复：

```
在 process_data 函数的入口处添加调试日志，打印 data 的完整内容和类型，
然后运行一次看看实际传入的数据长什么样。
```

### 场景三：代码审查 -- AI 审查 diff 输出改进建议

代码审查不只是找 Bug，更重要的是发现潜在的设计问题和改进空间。

**审查当前改动：**

```
审查当前 git diff 中的所有变更，重点关注：
1. 安全漏洞（SQL 注入、XSS、敏感信息泄露）
2. 性能问题（N+1 查询、不必要的循环、内存泄漏风险）
3. 错误处理是否完整
4. 边界条件是否覆盖
给出具体的修改建议和代码示例。
```

**审查整个项目：**

```
审查 src/ 目录下所有 Python 文件，按以下维度打分（1-10）：
- 代码可读性
- 错误处理完整性
- 测试覆盖度
- 安全性
对于打分低于 7 的维度，给出具体的改进建议。
```

**审查他人提交：**

```
审查最近 3 次 git commit 的改动，总结每次提交做了什么，
是否有需要关注的问题。
```

### 场景四：代码重构

对已有代码进行结构优化，改善可维护性。

```
将 utils.py 中超过 50 行的函数拆分为独立模块，
保持对外接口不变（即其他文件的 import 语句不需要改），
并为拆分后的每个模块添加单元测试。
```

### 常用命令速查

在 Claude Code 终端中，以下命令可以提升效率：

| 命令 | 作用 |
|------|------|
| `/compact` | 压缩对话历史，释放上下文窗口 |
| `/clear` | 清空当前对话，重新开始 |
| `claude --resume` | 恢复上一次会话继续工作 |
| `claude --print "问题"` | 非交互模式，直接输出答案后退出 |
| `claude commit` | 让 Claude Code 生成 commit 消息并提交 |

**上下文引用技巧：**

在对话中直接引用文件路径，Claude Code 会自动读取内容：

```
看看 src/utils/helper.py 这个文件，有没有可以优化的地方。
```

你也可以引用 URL、Git commit hash 等，Claude Code 会尝试获取对应内容。

## MCP Server 开发

### 目标

理解 MCP（Model Context Protocol）的基本概念，从零开发一个完整的 TypeScript MCP Server，注册到 Claude Code，并验证调用成功。

### MCP 是什么

MCP 是一种标准化协议，定义了 AI 模型与外部工具之间的通信方式。你可以把它理解为"AI 的 USB 接口"。只要你的工具实现了 MCP 协议，任何支持 MCP 的 AI 客户端（包括 Claude Code）都能自动发现和调用它。

一个 MCP Server 向 AI 暴露一组"工具"（Tool），每个工具有名称、描述和参数定义。AI 在对话中判断需要调用某个工具时，会自动发送请求给 MCP Server，拿到结果后继续对话。

### 从零开发一个 MCP Server

我们来开发一个实用的 MCP Server，包含天气查询和温度换算两个工具。以下是完整的、可直接运行的代码。

**第一步：初始化项目**

```bash
mkdir weather-mcp-server
cd weather-mcp-server

# 初始化 Node.js 项目
npm init -y

# 安装 MCP SDK 和依赖
npm install @modelcontextprotocol/sdk zod
npm install -D typescript @types/node

# 初始化 TypeScript
npx tsc --init
```

**第二步：配置 TypeScript**

编辑 `tsconfig.json`，确保以下配置：

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
  "include": ["src/**/*"]
}
```

**第三步：配置 package.json**

在 `package.json` 中添加以下字段：

```json
{
  "type": "module",
  "scripts": {
    "build": "tsc",
    "start": "node dist/server.js"
  }
}
```

**第四步：编写 MCP Server 代码**

创建 `src/server.ts`，以下是完整代码（不省略任何 import）：

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// 创建 MCP Server 实例
const server = new McpServer({
  name: "weather-tools",
  version: "1.0.0",
});

// 模拟天气数据（实际项目中替换为真实 API 调用）
const weatherDatabase: Record<string, { temp: number; humidity: number; condition: string }> = {
  "北京": { temp: 22, humidity: 45, condition: "晴" },
  "上海": { temp: 25, humidity: 70, condition: "多云" },
  "广州": { temp: 30, humidity: 80, condition: "阵雨" },
  "深圳": { temp: 28, humidity: 75, condition: "多云转晴" },
  "杭州": { temp: 23, humidity: 65, condition: "阴" },
};

// 工具 1：查询天气
server.tool(
  "get_weather",
  "查询指定城市的当前天气信息，包括温度、湿度和天气状况",
  {
    city: z.string().describe("城市名称，例如：北京、上海、广州"),
  },
  async ({ city }) => {
    const weather = weatherDatabase[city];
    if (!weather) {
      const availableCities = Object.keys(weatherDatabase).join("、");
      return {
        content: [
          {
            type: "text" as const,
            text: `未找到城市"${city}"的天气数据。当前支持的城市：${availableCities}`,
          },
        ],
      };
    }
    return {
      content: [
        {
          type: "text" as const,
          text: [
            `${city}当前天气：`,
            `  温度：${weather.temp} C`,
            `  湿度：${weather.humidity}%`,
            `  天气：${weather.condition}`,
          ].join("\n"),
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
    from_unit: z.enum(["celsius", "fahrenheit"]).describe("原始单位：celsius 或 fahrenheit"),
  },
  async ({ value, from_unit }) => {
    let result: number;
    let fromLabel: string;
    let toLabel: string;

    if (from_unit === "celsius") {
      result = (value * 9) / 5 + 32;
      fromLabel = "C";
      toLabel = "F";
    } else {
      result = ((value - 32) * 5) / 9;
      fromLabel = "F";
      toLabel = "C";
    }

    return {
      content: [
        {
          type: "text" as const,
          text: `${value} ${fromLabel} = ${result.toFixed(1)} ${toLabel}`,
        },
      ],
    };
  }
);

// 启动 Server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  // 注意：MCP Server 的日志输出到 stderr，stdout 用于 MCP 协议通信
  console.error("Weather MCP Server 已启动，等待连接...");
}

main().catch((error) => {
  console.error("MCP Server 启动失败：", error);
  process.exit(1);
});
```

**第五步：编译**

```bash
npm run build
```

编译成功后会在 `dist/` 目录下生成 `server.js`。

### 注册到 Claude Code

编译完成后，将 MCP Server 注册到 Claude Code：

```bash
# 注册为项目级别的 MCP Server
claude mcp add weather-tools node dist/server.js

# 查看已注册的 MCP Server 列表
claude mcp list
```

注册命令会在项目的 `.claude/settings.json` 中添加配置。你也可以手动编辑该文件：

```json
{
  "mcpServers": {
    "weather-tools": {
      "command": "node",
      "args": ["dist/server.js"],
      "cwd": "/path/to/weather-mcp-server"
    }
  }
}
```

### 验证调用成功

重新启动 Claude Code，然后在终端中测试：

```
北京今天天气怎么样？
```

如果一切正常，Claude Code 会自动调用你的 `get_weather` 工具，返回类似这样的回复：

```
我帮你查了一下北京的天气：
  温度：22 C
  湿度：45%
  天气：晴
```

再试试温度换算：

```
把 100 华氏度换算成摄氏度。
```

Claude Code 会调用 `convert_temperature` 工具，返回换算结果。

在 Claude Code 的终端界面中，你可以看到工具调用的过程。当 AI 决定调用一个工具时，界面上会显示工具名称和参数，你需要确认才会执行。

### MCP Server 开发要点

- MCP Server 通过 stdio（标准输入输出）与 Claude Code 通信，因此日志必须输出到 stderr（`console.error`），不能用 `console.log`（stdout 用于协议通信）
- 每个工具的描述要写清楚功能和参数含义，AI 根据描述决定何时调用哪个工具
- 工具的参数使用 zod 定义 schema，提供类型安全和自动校验
- 实际项目中可以对接真实 API（如天气 API、数据库查询、内部系统），替换示例中的模拟数据

## Skills 与 Hooks

### 目标

学会编写 Skill 文件封装常用操作，配置 Hooks 实现自动化流程。

### Skills 是什么

Skills 是 Markdown 格式的指令文件，存放在项目的 `.claude/skills/` 目录下。Claude Code 启动时会自动读取这些文件，将其作为操作指南。当你用自然语言触发相关操作时，Claude Code 会按照 Skill 中定义的流程执行。

与直接在对话中描述操作步骤不同，Skill 是持久化的、可复用的。写一次，团队所有人都可以用。

**Skill 文件的存放位置：**

```
your-project/
  .claude/
    skills/
      deploy.md        # 部署流程
      review.md        # 代码审查清单
      test.md          # 测试流程
      setup.md         # 新成员环境搭建
```

### 示例：部署 Skill

创建 `.claude/skills/deploy.md`：

```markdown
# 部署到生产环境

当用户说"部署"、"发布"、"上线"时执行此流程。

## 前置检查

1. 确认当前在 main 分支上
2. 运行 `git status` 确认没有未提交的更改
3. 运行 `npm run lint` 确保代码风格检查通过
4. 运行 `npm run test` 确保所有测试通过
5. 运行 `npm run build` 确保构建成功

如果任何一步失败，停止部署并报告失败原因。

## 部署步骤

1. 拉取最新代码：`git pull origin main`
2. 执行部署命令：`vercel --prod --yes`
3. 等待部署完成，获取部署 URL
4. 访问部署 URL 的 /health 接口，确认返回 200

## 部署后

1. 创建 Git tag：`git tag v$(date +%Y%m%d-%H%M%S)`
2. 推送 tag：`git push origin --tags`
3. 输出部署摘要：部署 URL、耗时、版本号

## 异常处理

- 如果构建失败：输出错误日志，不执行部署
- 如果部署后健康检查失败：立即告警，提示手动检查
```

**使用方式：** 在 Claude Code 中直接说"部署到生产环境"或"帮我上线"，Claude Code 会自动按照 Skill 中的流程执行。

### 示例：代码审查 Skill

创建 `.claude/skills/review.md`：

```markdown
# 代码审查

当用户说"审查代码"、"review"、"看看代码质量"时执行此流程。

## 审查范围

检查当前 Git diff 中的所有变更文件（`git diff --cached` 已暂存 + `git diff` 未暂存）。

## 审查清单

按以下维度逐项检查：

### 安全性
- SQL 查询是否使用参数化（禁止字符串拼接）
- 用户输入是否做了校验和转义
- 是否有敏感信息（API Key、密码）硬编码
- HTTP 响应是否设置了必要的安全头

### 健壮性
- 所有外部调用（API、数据库、文件系统）是否有错误处理
- 边界条件是否覆盖（空值、空数组、超大输入）
- 异步操作是否正确处理了拒绝（reject）

### 可读性
- 函数和变量命名是否清晰表达意图
- 复杂逻辑是否有必要的注释
- 函数长度是否合理（超过 50 行考虑拆分）

### 性能
- 是否有 N+1 查询
- 循环内是否有不必要的 I/O 操作
- 是否有内存泄漏风险（未释放的监听器、未关闭的连接）

## 输出格式

按文件分组列出问题，每个问题标注：
- 严重程度：高 / 中 / 低
- 问题描述
- 建议修改（附代码示例）
```

### 示例：项目初始化 Skill

创建 `.claude/skills/setup.md`：

```markdown
# 项目环境搭建

当新成员加入项目时，按此流程搭建开发环境。

## 环境检查

1. 检查 Node.js 版本 >= 18
2. 检查 npm 版本 >= 9
3. 检查 Git 是否安装

## 搭建步骤

1. 安装项目依赖：`npm install`
2. 复制环境变量模板：`cp .env.example .env.local`
3. 提示用户填写必要的环境变量
4. 运行数据库迁移：`npm run db:migrate`
5. 启动开发服务器验证：`npm run dev`
6. 打开浏览器访问 http://localhost:3000 确认页面正常

## 完成确认

所有步骤成功后，输出欢迎信息和常用命令列表。
```

### Hooks 配置

Hooks 让你在 Claude Code 的特定事件触发时自动执行命令。在项目根目录的 `.claude/settings.json` 中配置。

以下是一份示意配置，实际使用时请以 Claude Code 官方文档为准，配置格式可能随版本更新：

```json
{
  "hooks": {
    "pre-commit": {
      "command": "npm run lint && npm run test",
      "description": "提交前自动运行代码检查和测试"
    },
    "post-save": {
      "command": "npx prettier --write $FILE",
      "description": "文件保存后自动格式化"
    }
  }
}
```

**Hooks 与 Git Hooks 的区别：**

- Git Hooks（`.git/hooks/`）是 Git 原生机制，在 `git commit`、`git push` 等操作时触发
- Claude Code Hooks 是 Claude Code 自身的机制，在 Claude Code 执行文件操作时触发
- 两者可以共存，互不冲突

**注意：** Hooks 的具体事件名称和配置格式可能随 Claude Code 版本变化。建议查阅 [Claude Code 官方文档](https://docs.anthropic.com/en/docs/claude-code) 获取最新的 Hooks 配置说明。

## Agent SDK 简介

### 目标

了解 Agent SDK 的核心概念，知道如何用它构建自主运行的 AI 代理。

### 什么是 Agent

与直接在 Claude Code 中对话不同，Agent 是一个能够自主规划、执行多步骤任务的程序。你给它一个目标，它会自己决定需要哪些步骤、调用哪些工具、如何处理中间结果，最终完成任务。

**核心概念：**

| 概念 | 说明 |
|------|------|
| Agent | 一个带有系统指令和工具集的自主执行单元 |
| Tool | Agent 可以调用的能力（读写文件、执行命令、调用 API 等） |
| Loop | Agent 的执行循环 -- 思考、选择工具、执行、观察结果、继续思考 |

**典型应用场景：**

- 自动化代码审查：Agent 读取 PR diff，逐文件分析，输出审查报告
- 批量数据处理：Agent 遍历数据集，逐条处理，汇总结果
- 多步骤部署：Agent 执行构建、测试、部署、验证的完整流水线
- 定时巡检：Agent 定期检查服务状态、日志异常、资源用量

### 基本使用示例

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

## 常见问题（FAQ）

### 安装相关

**Q: 安装时报权限错误 `EACCES: permission denied`**

这通常是因为 npm 全局目录的权限问题。解决方法：

```bash
# 方法 1：修改 npm 全局目录（推荐）
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# 然后重新安装
npm install -g @anthropic-ai/claude-code
```

```bash
# 方法 2：使用 npx 直接运行（不需要全局安装）
npx @anthropic-ai/claude-code
```

**Q: Node.js 版本低于 18 怎么办？**

推荐使用 nvm（Node Version Manager）管理多版本：

```bash
# 安装 nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
source ~/.bashrc

# 安装并使用 Node.js 20
nvm install 20
nvm use 20

# 验证
node --version  # 应显示 v20.x.x
```

**Q: `claude` 命令找不到？**

```bash
# 检查全局 npm 包的安装位置
npm list -g --depth=0

# 检查 PATH 中是否包含 npm 全局 bin 目录
npm config get prefix
# 确认 <prefix>/bin 在你的 PATH 中
```

### Intern-S1-Pro 接入相关

**Q: 配置了环境变量但连接不上？**

逐步排查：

```bash
# 1. 确认环境变量已生效
echo $ANTHROPIC_BASE_URL
echo $ANTHROPIC_API_KEY
echo $ANTHROPIC_MODEL

# 2. 测试 API 端点是否可达
curl -s https://chat.intern-ai.org.cn/api/v1/models \
  -H "Authorization: Bearer $ANTHROPIC_API_KEY"

# 3. 如果 curl 能返回模型列表，说明网络和 Key 都没问题
# 如果返回 401，说明 API Key 无效或已过期，去社区个人中心重新获取
# 如果连接超时，检查网络环境（是否需要代理）
```

**Q: Claude Code 显示的模型名称不是 Intern-S1-Pro？**

这是正常现象。Claude Code 客户端的界面可能显示默认的模型名称，但实际请求已经通过环境变量路由到了 Intern-S1-Pro。你可以通过以下方式验证：

```
请告诉我你当前使用的模型名称和 API 端点信息。
```

**Q: Intern-S1-Pro 通过兼容层接入，功能上有什么限制？**

通过 OpenAI 兼容层接入意味着：

- 基本的对话、代码生成、文件操作等核心功能都可以正常使用
- 某些 Claude 原生特性（如 Artifacts 渲染）可能不可用，但不影响编程场景
- 如果遇到特定功能异常，优先检查是否是兼容层不支持的特性

Intern-S1-Pro 是书生大模型社区的科学多模态大模型，在代码理解和生成方面表现优秀，完全满足日常 AI 编程需求。

### MCP Server 调试

**Q: MCP Server 注册后 Claude Code 没有识别到工具？**

```bash
# 1. 确认 MCP Server 已注册
claude mcp list

# 2. 手动测试 MCP Server 是否能正常启动
node dist/server.js
# 如果报错，根据错误信息修复

# 3. 检查 .claude/settings.json 中的配置路径是否正确
# cwd 必须是绝对路径
# args 中的 js 文件路径相对于 cwd
```

**Q: MCP Server 运行时报错但看不到日志？**

MCP Server 通过 stdio 与 Claude Code 通信，`console.log` 的输出会被当作协议数据处理。调试日志必须用 `console.error` 输出到 stderr：

```typescript
// 错误：会干扰 MCP 协议通信
console.log("调试信息");

// 正确：输出到 stderr，不影响协议通信
console.error("调试信息");
```

也可以将日志写入文件：

```typescript
import { appendFileSync } from "fs";

function log(message: string) {
  appendFileSync("/tmp/mcp-debug.log", `${new Date().toISOString()} ${message}\n`);
}
```

**Q: 如何在开发阶段快速测试 MCP Server？**

可以使用 MCP Inspector 工具进行独立测试，不需要通过 Claude Code：

```bash
# 安装 MCP Inspector
npx @modelcontextprotocol/inspector node dist/server.js
```

Inspector 会在浏览器中打开一个界面，你可以手动调用每个工具，查看输入输出。

### Skills 和 Hooks 相关

**Q: Skill 文件写了但 Claude Code 没有按照流程执行？**

- 确认文件放在 `.claude/skills/` 目录下（不是项目根目录）
- 确认文件扩展名是 `.md`
- Skill 的描述要明确触发条件（"当用户说...时执行此流程"）
- 重新启动 Claude Code 后 Skill 才会生效

**Q: Hooks 配置了但没有触发？**

Hooks 的配置格式和支持的事件可能随 Claude Code 版本变化。如果配置后没有效果：

1. 检查 `.claude/settings.json` 的 JSON 格式是否正确
2. 查阅 Claude Code 当前版本的官方文档确认支持的事件列表
3. 重启 Claude Code 使配置生效

## 进阶学习路径

完成本课程后，你可以按以下方向继续深入：

| 方向 | 内容 | 资源 |
|------|------|------|
| MCP 生态 | 浏览社区已有的 MCP Server，学习更多工具集成模式 | [MCP 官网](https://modelcontextprotocol.io) |
| Agent 开发 | 构建多 Agent 协作系统，处理复杂工作流 | [Agent SDK 文档](https://github.com/anthropics/agent-sdk) |
| 团队协作 | 在团队中推广 Skills，建立共享的 AI 工作流 | 团队内部实践 |
| 书生生态 | 探索 InternVL、InternLM、LMDeploy 等书生大模型工具链 | [书生社区](https://community.intern-ai.org.cn) |

## 参考资料

- [Claude Code 官方文档](https://docs.anthropic.com/en/docs/claude-code) -- 安装、配置、命令参考
- [MCP 协议规范](https://modelcontextprotocol.io) -- MCP Server 开发指南
- [Anthropic Agent SDK](https://github.com/anthropics/agent-sdk) -- Agent 开发框架
- [书生大模型社区](https://community.intern-ai.org.cn) -- API Key 获取、Intern-S1-Pro 文档
