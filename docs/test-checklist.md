# Camp7 Playwright 验收清单

说明：
- 当前 `/docs` 下实际有 10 个目录（含 `introduction` 和 `mcp`），以下清单按现有目录全部覆盖，避免漏测。
- 每门课给 3 个可自动化验证点，优先使用稳定的页面元素：`h1`、固定文案、代码块、表格标题、链接文字。
- 默认每门课至少验证两个页面：`readme.md` 对应课程正文页，`task.md` 对应闯关任务页。

建议断言方式：
- 标题：`page.locator('h1')`
- 文本：`page.getByText('...')`
- 代码块：`page.locator('pre code')`
- 表格：`page.locator('table')`
- 链接：`page.getByRole('link', { name: /.../i })`

## 1. introduction

页面：
- `docs/introduction/readme`
- `docs/introduction/task`

自动化检查点：
1. 正文页 `h1` 包含 `Camp7` 或 `课程` 导学定位文案，并出现 `你将做出什么`。
2. 正文页包含课程名 `Claude Code`、`Skills`、`OpenClaw` 三个字符串中的至少 3 个。
3. 任务页包含 `验收标准` 和 `提交` 两个关键词。

## 2. claude-code

页面：
- `docs/claude-code/readme`
- `docs/claude-code/task`

自动化检查点：
1. 正文页 `h1` 包含 `Claude Code`。
2. 正文页包含至少一个安装命令字符串：`npm install -g @anthropic-ai/claude-code` 或 `claude --version`。
3. 任务页包含 `必做` 或 `验收标准`，并出现 `截图` 或 `仓库`。

## 3. skills

页面：
- `docs/skills/readme`
- `docs/skills/task`

自动化检查点：
1. 正文页 `h1` 包含 `Skills`，并出现 `10 分钟跑通第一个 Skill`。
2. 正文页包含以下 4 个小节词中的至少 3 个：`触发条件`、`前置检查`、`执行步骤`、`质量标准`。
3. 任务页包含 `Skill`，并出现 `验收标准` 和 `提交物`。

## 4. mcp

页面：
- `docs/mcp/readme`
- `docs/mcp/task`

自动化检查点：
1. 正文页 `h1` 包含 `MCP`。
2. 正文页同时出现 `Model Context Protocol` 和 `Tools`。
3. 任务页包含 `MCP Server` 或 `Server`，并出现 `验收标准`。

## 5. openclaw

页面：
- `docs/openclaw/readme`
- `docs/openclaw/task`

自动化检查点：
1. 正文页 `h1` 包含 `OpenClaw`。
2. 正文页同时出现 `Telegram` 和 `BotFather`。
3. 任务页包含 `MCP` 或 `Telegram`，并出现 `验收标准`。

## 6. internsvg

页面：
- `docs/internsvg/readme`
- `docs/internsvg/task`

自动化检查点：
1. 正文页 `h1` 包含 `InternSVG`。
2. 正文页同时出现 `SVG` 和 `lmdeploy serve api_server`。
3. 任务页包含 `SVG`，并出现 `验收标准` 或 `提交`。

## 7. agent2agent

页面：
- `docs/agent2agent/readme`
- `docs/agent2agent/task`

自动化检查点：
1. 正文页 `h1` 包含 `Agent2Agent` 或 `A2A`。
2. 正文页同时出现 `MCP 与 A2A` 和 `Agent Card`。
3. 任务页包含 `A2A`，并出现 `验收标准` 和 `Agent`。

## 8. intern-s1-pro

页面：
- `docs/intern-s1-pro/readme`
- `docs/intern-s1-pro/task`

自动化检查点：
1. 正文页 `h1` 包含 `Intern-S1-Pro`。
2. 正文页同时出现 `科学多模态大模型` 和 `OpenAI`。
3. 任务页包含 `API` 或 `Prompt`，并出现 `验收标准`。

## 9. lmdeploy

页面：
- `docs/lmdeploy/readme`
- `docs/lmdeploy/task`

自动化检查点：
1. 正文页 `h1` 包含 `LMDeploy`。
2. 正文页同时出现 `lmdeploy serve api_server` 和 `OpenAI`。
3. 任务页包含 `量化` 或 `部署`，并出现 `验收标准`。

## 10. internvl-u

页面：
- `docs/internvl-u/readme`
- `docs/internvl-u/task`

自动化检查点：
1. 正文页 `h1` 包含 `InternVL-U`。
2. 正文页同时出现 `A100` 和 `华为昇腾 Atlas 800T A2`。
3. 任务页包含 `图像理解`、`文生图`、`图像编辑` 三个能力词中的至少 2 个，并出现 `验收标准`。

## 可选通用巡检

如果 I 站牛想先做一轮全局 smoke test，可以加 3 个通用断言：
1. 每个课程目录都存在 `readme` 页和 `task` 页，访问返回 200。
2. 每个 `readme` 页都存在且仅存在 1 个 `h1`。
3. 每个 `task` 页都包含 `验收标准`、`提交`、`任务` 三类词中的至少 2 个。
