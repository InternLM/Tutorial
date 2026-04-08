# Skills 技能编排

> 本文档 AI + 社区共建中

## 课程简介

Skills 是 AI 编程中的核心编排机制，它将复杂任务拆解为可复用的技能单元，让 AI 按照你预设的规范和流程执行工作。本课程深入讲解 Skill 的设计理念、编写方法和高级用法，帮助你从「每次手动提示」升级为「一次编写，反复调用」的高效工作模式。

## 你将学到

- 理解 Skill 与传统工具（Tool）的本质区别
- 掌握 Skill 文件的结构设计和编写规范
- 在 Claude Code 中创建和管理 Skills
- 运用 AutoSkill 机制实现技能的自动学习
- 设计多 Skill 串联的自动化工作流
- 结合 Hooks 配置实现事件驱动的任务执行

## Skill 与 Tool 的区别

### 目标

理解 Skill 和 Tool 各自解决什么问题，以及它们如何配合工作。

### 内容

在 AI 编程体系中，Tool 和 Skill 是两个不同层次的概念，容易混淆但各有分工。

**Tool（工具）：**

- 执行单一、明确的操作（读文件、调 API、执行命令）
- 由代码实现，有严格的输入输出格式
- AI 根据上下文自动选择调用
- 类比：螺丝刀、扳手 -- 基础工具

**Skill（技能）：**

- 描述完成一类任务的完整流程和规范
- 用 Markdown 编写，包含步骤、判断逻辑、质量标准
- AI 读取后作为操作指南，调用多个 Tool 来执行
- 类比：装修手册 -- 告诉你何时用哪个工具、按什么顺序、达到什么标准

一个形象的对比：

| 维度 | Tool | Skill |
|------|------|-------|
| 形式 | 代码（TypeScript/Python） | Markdown 文档 |
| 粒度 | 单个操作 | 完整流程 |
| 智能程度 | 无判断力，被动调用 | 包含判断逻辑和规范 |
| 复用方式 | 函数调用 | 文件引用 |
| 举例 | `read_file`、`run_command` | 「部署到生产环境」、「代码审查」 |

两者的关系是：Skill 编排流程，Tool 执行动作。一个好的 Skill 会在合适的时机调用合适的 Tool。

## Skill 文件的设计与编写

### 目标

掌握 Skill 文件的标准结构，学会编写清晰、可靠的 Skill。

### 内容

Skill 文件存放在项目的 `.claude/skills/` 目录下，使用 Markdown 格式编写。Claude Code 启动时会自动加载该目录下的所有 `.md` 文件。

**文件结构规范：**

一个好的 Skill 文件应包含以下部分：

```markdown
# 技能名称

## 触发条件
说明什么时候应该使用这个技能。

## 前置检查
执行前需要确认的条件。

## 执行步骤
按顺序列出具体操作步骤。

## 质量标准
完成后需要满足的验收条件。

## 异常处理
出现问题时的应对方案。
```

**示例 1：Git 提交规范 Skill**

```markdown
<!-- .claude/skills/git-commit.md -->
# Git 提交规范

## 触发条件
当用户要求提交代码或说"提交"、"commit"时使用。

## 前置检查
1. 运行 `git status` 确认有待提交的变更
2. 确认没有未解决的合并冲突

## 执行步骤
1. 运行 `git diff --cached` 查看暂存区变更
2. 如果暂存区为空，提示用户先 `git add` 相关文件
3. 根据变更内容生成提交信息，格式为：
   - `feat: xxx` 新功能
   - `fix: xxx` Bug 修复
   - `refactor: xxx` 重构
   - `docs: xxx` 文档更新
   - `test: xxx` 测试相关
4. 提交信息不超过 72 个字符
5. 执行 `git commit -m "生成的提交信息"`

## 质量标准
- 提交信息准确反映变更内容
- 每次提交只包含一个逻辑变更
- 不提交临时文件、日志文件、环境变量文件

## 异常处理
- 如果 pre-commit hook 失败，修复问题后重新提交
- 如果变更文件过多，建议拆分为多次提交
```

**示例 2：测试编写 Skill**

```markdown
<!-- .claude/skills/write-tests.md -->
# 测试编写

## 触发条件
当用户要求写测试、补充测试、或创建了新功能代码时使用。

## 前置检查
1. 确认项目使用的测试框架（pytest / jest / vitest 等）
2. 确认测试目录结构

## 执行步骤
1. 分析目标代码的公开接口和核心逻辑
2. 为每个公开函数编写测试：
   - 正常输入的预期输出
   - 边界值测试
   - 异常输入的错误处理
3. 测试文件命名：`test_<模块名>.py` 或 `<模块名>.test.ts`
4. 运行测试确认全部通过
5. 输出测试覆盖率报告

## 质量标准
- 每个公开函数至少 3 个测试用例
- 覆盖正常路径、边界条件、异常路径
- 测试之间相互独立，无顺序依赖
- 测试命名清晰，能从名称看出测试内容
```

**示例 3：数据库迁移 Skill**

```markdown
<!-- .claude/skills/db-migration.md -->
# 数据库迁移

## 触发条件
当需要修改数据库结构（新增表、修改字段、添加索引等）时使用。

## 前置检查
1. 确认当前数据库连接正常
2. 查看 sql/ 目录下已有的迁移文件，确定下一个编号

## 执行步骤
1. 在 sql/ 目录创建新的迁移文件，编号递增
2. 文件名格式：`NNN_描述.sql`，例如 `024_add_user_avatar.sql`
3. SQL 内容要求：
   - 使用 `IF NOT EXISTS` 防止重复执行
   - 大表修改使用 `CONCURRENTLY` 避免锁表
   - 包含注释说明变更目的
4. 在本地测试环境执行迁移，验证无报错
5. 更新相关的 TypeScript 类型定义

## 异常处理
- 如果迁移失败，提供回滚 SQL
- 不要在迁移中删除列或表，改为标记弃用
```

## Skill 管理与组织

### 目标

学会合理组织 Skill 文件，管理不同层级的 Skill。

### 内容

**Skill 的作用范围：**

Claude Code 支持三个层级的 Skill：

1. **项目级**：`.claude/skills/` -- 跟随项目，团队共享
2. **用户级**：`~/.claude/skills/` -- 个人全局，所有项目可用
3. **会话级**：在对话中临时指定 -- 仅当次会话有效

当同名 Skill 存在于多个层级时，项目级优先于用户级。

**文件组织建议：**

```
.claude/
  skills/
    deploy.md           # 部署相关
    review.md           # 代码审查
    git-commit.md       # Git 提交规范
    write-tests.md      # 测试编写
    db-migration.md     # 数据库迁移
    refactor.md         # 代码重构
  settings.json         # Hooks 配置
```

每个 Skill 文件聚焦一个任务领域，不要把所有规范塞进一个文件。文件名使用小写 kebab-case，简短明确。

**CLAUDE.md 与 Skills 的关系：**

项目根目录的 `CLAUDE.md` 文件是项目级别的全局指令，Claude Code 每次启动都会读取。它适合放置：

- 项目背景和架构说明
- 全局编码规范
- 禁止事项和注意事项

而 Skills 适合放置具体的操作流程。两者配合使用效果最佳：`CLAUDE.md` 定义「是什么」和「不做什么」，Skills 定义「怎么做」。

## AutoSkill 自动学习

### 目标

了解 AutoSkill 机制，让 Claude Code 从你的工作习惯中自动提炼技能。

### 内容

AutoSkill 是一种让 AI 从重复操作中自动总结经验的机制。当你多次以相似的方式完成某类任务时，Claude Code 可以将这些模式提炼为 Skill 文件。

**工作原理：**

1. Claude Code 观察你的操作模式
2. 识别重复出现的流程
3. 自动生成 Skill 文件草稿
4. 你审核修改后保存

**手动触发 AutoSkill：**

在 Claude Code 中输入：

```
回顾我们刚才的对话，将其中的操作流程总结为一个 Skill 文件，
保存到 .claude/skills/ 目录下。
```

**AutoSkill 的迭代优化：**

生成的 Skill 文件是起点，你应该根据实际使用情况不断优化：

- 补充遗漏的边界情况
- 删除不必要的步骤
- 调整执行顺序
- 添加质量检查点

## 多 Skill 工作流

### 目标

设计多个 Skill 串联的自动化工作流，实现复杂任务的一键执行。

### 内容

单个 Skill 解决单个任务，多个 Skill 串联可以覆盖完整的工作流。

**示例：功能开发全流程**

以下是一个将需求分析、编码、测试、审查、提交串联起来的工作流设计：

```markdown
<!-- .claude/skills/feature-workflow.md -->
# 功能开发全流程

## 触发条件
当用户提出一个新功能需求时使用。

## 工作流步骤

### 阶段 1：需求分析
1. 理解用户需求，明确输入输出
2. 确定影响范围（哪些文件需要修改/新建）
3. 提出实现方案，等待用户确认

### 阶段 2：编码实现
1. 按照方案创建/修改代码文件
2. 遵循项目现有的代码风格
3. 添加必要的类型注解和注释

### 阶段 3：测试覆盖
（调用 write-tests Skill）
1. 为新增代码编写单元测试
2. 运行全量测试确保无回归

### 阶段 4：代码审查
（调用 review Skill）
1. 自审代码质量
2. 列出潜在问题和优化建议
3. 修复发现的问题

### 阶段 5：提交代码
（调用 git-commit Skill）
1. 暂存变更文件
2. 生成规范的提交信息
3. 执行提交
```

**Hooks 配合 Skills：**

通过在 `.claude/settings.json` 中配置 Hooks，可以实现事件驱动的 Skill 调用：

```json
{
  "hooks": {
    "pre-commit": {
      "command": "npm run lint && npm run test",
      "description": "提交前自动检查"
    },
    "post-save": {
      "command": "npx prettier --write $FILE",
      "description": "保存后自动格式化"
    }
  },
  "skills": {
    "auto_review": true,
    "auto_test": true
  }
}
```

这样每次文件保存会自动格式化，每次提交前会自动运行检查，形成一个无需手动干预的质量保障链。

## 参考资料

- [Claude Code Skills 文档](https://docs.anthropic.com/en/docs/claude-code/skills)
- [Claude Code CLAUDE.md 规范](https://docs.anthropic.com/en/docs/claude-code/claude-md)
- [MCP 协议规范](https://modelcontextprotocol.io)
