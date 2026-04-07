# Claude Code AI 编程 -- 闯关任务

## 任务说明

通关本课程需要完成以下 3 个任务。请按顺序完成，每个任务都需要提交截图或代码作为完成凭证。

## 任务 1：环境搭建与模型对话

**目标：** 安装 Claude Code，配置 Intern-S1-Pro 模型，完成首次对话。

**要求：**

1. 安装 Claude Code 并确认版本号
2. 配置环境变量，接入 Intern-S1-Pro 模型
3. 在 Claude Code 中完成至少一次有意义的对话（例如让它解释一段代码、回答一个技术问题）

**提交：**

- 截图 1：`claude --version` 的输出
- 截图 2：Claude Code 终端中与 Intern-S1-Pro 的对话过程（需包含完整的提问和回答）

## 任务 2：项目开发实战

**目标：** 使用 Claude Code 完成一个完整项目的开发，体验 AI 辅助编程的全流程。

**要求：**

1. 创建一个新项目（语言不限，推荐 Python 或 TypeScript）
2. 全程使用 Claude Code 辅助开发，至少包含以下环节：
   - 代码生成：让 Claude Code 生成项目核心功能代码
   - 代码审查：让 Claude Code 审查生成的代码并提出优化建议
   - Bug 修复：制造或遇到一个 Bug，让 Claude Code 帮助定位和修复
3. 项目需要能正常运行，不要求功能复杂但要求代码完整

**项目建议（任选其一或自拟）：**

- 命令行待办事项工具（增删改查 + 本地存储）
- 文件批量重命名工具
- Markdown 转 HTML 工具
- 简单的 HTTP API 服务

**提交：**

- 截图 1：Claude Code 中的开发过程（至少 3 张，展示生成、审查、修复环节）
- 截图 2：项目的 Git 提交历史（`git log --oneline`），证明开发过程有版本记录
- 截图 3：项目运行效果

## 任务 3：MCP Server 开发

**目标：** 开发一个自定义 MCP Server，注册到 Claude Code 并验证调用成功。

**要求：**

1. 创建一个 MCP Server 项目，使用 TypeScript 或 Python 开发
2. 实现至少 2 个工具（Tool），工具需要有实际功能，不能是空壳
3. 将 MCP Server 注册到 Claude Code
4. 在 Claude Code 中通过自然语言触发工具调用，验证功能正常

**工具建议（任选或自拟）：**

- 文件搜索 + 文件统计
- 系统信息查询 + 进程管理
- 字符串处理 + 编码转换
- 数学计算 + 单位换算

**提交：**

- 代码：MCP Server 完整源码
- 截图 1：`claude mcp list` 显示已注册的 Server
- 截图 2：在 Claude Code 中调用 MCP Server 工具的过程和结果
