# Claude Code 实战 · Skills 最小示例

> 本节在**昇腾 Atlas 800T A2 + Intern-S1-Pro** 上亲测，**并诚实记录了一处 Intern-S1-Pro 对 Skill 机制理解不足导致的失败**。

## 什么是 Skill

**Skill** 是 Claude Code 的一种"预置 prompt 片段"机制，用一个 Markdown 文件（`SKILL.md`）描述"什么时候触发、触发后要做什么"。当模型判断场景匹配时，Claude Code 会把 `SKILL.md` 的正文**塞回给模型作为一条合成的 user 消息**，引导它执行既定工作流。

**Skill ≠ MCP：**

| 维度 | Skill | MCP |
|------|-------|-----|
| 本质 | 一段可复用的 **prompt** | 一个可执行的 **tool server** |
| 存放 | `~/.claude/skills/<name>/SKILL.md` 或 `.claude/skills/...` | 一段进程（stdio / HTTP） |
| 调用方式 | 模型触发 `Skill` 工具 → 合成 user 消息注入 | 模型发 tool_use → server 返回结构化结果 |
| 何时用 | 固化一套"工作流" / 代码审查规范 / 生成模板 | 接外部数据 / 调外部系统 |

## 第一步：写最小 Skill

目录结构：

```
~/.claude/skills/pylint-check/
└── SKILL.md
```

`SKILL.md`：

```markdown
---
name: pylint-check
description: Use this skill whenever the user asks to lint, check, or audit a Python file for style/syntax problems. It runs pyflakes on the target file and reports any issues, then suggests one fix per issue.
---

# pylint-check

当用户要求 lint / 检查 / 审计某个 Python 文件时，使用此 skill。

## 工作流

1. 使用 Bash 工具执行 `python -m pyflakes <file>` 获取 lint 输出。
2. 逐条分析每个 warning / error，按「文件:行号 → 问题 → 一句修复建议」格式输出。
3. 如果 pyflakes 无输出（文件干净），回复「✅ 该文件无 pyflakes 可识别问题」。
4. 不要自动修改代码，除非用户明确说「改」或「fix」。
```

frontmatter 的 `description` 非常重要——Claude Code 用这段话判断"什么时候要触发这个 skill"。写得越具体，模型越不会漏触发或错误触发。

## 第二步：验证 Skill 被识别

启动 claude（任何目录都行，因为 `~/.claude/skills/` 是用户级）：

```bash
claude --model intern-s1-pro --print --output-format stream-json --verbose "测试"
```

在 init 事件里会看到：

```json
{"type":"system","subtype":"init",
 ...
 "skills":["update-config","debug","simplify",..., "pylint-check"],
 "slash_commands":[..., "pylint-check"]
}
```

即：skill 已被加载，可通过 `Skill` 工具或者 `/pylint-check` slash command 触发。

## 第三步：让模型触发它（实测：**遇到了一个真实坑**）

准备一个故意带 lint 问题的 demo.py：

```python
"""故意有 lint 问题的小脚本。"""
import os
import json
import sys

def main():
    data = {"hello": "world"}
    print(data)
    return undefined_function(42)

if __name__ == "__main__":
    main()
```

手工跑 pyflakes 的期望输出：

```
demo.py:2:1: 'os' imported but unused
demo.py:3:1: 'json' imported but unused
demo.py:4:1: 'sys' imported but unused
demo.py:10:12: undefined name 'undefined_function'
```

给 claude 的 prompt：

```
请立刻使用 pylint-check skill 检查 /root/sskill/demo.py 这个文件。
按 skill 的指示运行 pyflakes 并汇报结果。检查完立即结束。
```

### 实际发生（诚实记录）

1. **触发识别 ✅**：Intern-S1-Pro 发出 `Skill` 工具调用 `{"skill": "pylint-check", "args": "/root/sskill/demo.py"}`。
2. Claude Code 按预期把 `SKILL.md` 的正文合成一条 user 消息塞回去（`"Launching skill: pylint-check"` + SKILL.md 内容 + `ARGUMENTS: ...`）。
3. **Intern-S1-Pro 误以为 Skill 会"返回结果"，又 Skill 了第二次、第三次**。每次 Claude Code 都乖乖把同样的 SKILL.md 再塞回来。模型在"Skill 启动 → 没拿到结果 → 再启动"的循环里空转。
4. 最后终于想起来"其实该用 Bash 跑 pyflakes"，发了 `python3 -m pyflakes /root/sskill/demo.py`——**但又被 Claude Code 标记成后台任务**，output 读不到，180s 超时被 kill。

### 这是 Intern-S1-Pro 的 Skill 机制认知偏差

问题根源：Intern-S1-Pro 倾向于把 Skill 看成类似 MCP 的"调用 → 获得结果"的工具，而实际上 Skill 是"调用 → 拿到一段更详细的 prompt"。模型需要理解"拿到 prompt 就要自己执行"。

### 给学员的建议

在 Intern-S1-Pro 上用 Skill 时：

1. **Skill 里的工作流写得越像"第一人称操作指令"越好**，避免被模型当成"可以委托给 skill 内部执行"。

   改进 SKILL.md 开头加一句：
   > 你收到这段内容之后，**不要再次调用 Skill 工具**。按下面工作流直接行动。

2. **或者干脆把 Skill 里的核心逻辑平铺到 prompt**：

   ```
   请立刻对 /root/sskill/demo.py 执行以下步骤（不要使用 Skill 工具）：
   1. 调用 Bash 工具执行 `python -m pyflakes /root/sskill/demo.py`
   2. 解析输出，按「文件:行号 → 问题 → 一句修复建议」格式列出
   ```

3. **Bash 后台化问题的通用绕开方法**：让 claude 写脚本但别跑脚本；你自己在终端手动跑。非交互模式 (`--print`) 下尤其如此。

## 经验总结

- **Skill 机制在 Intern-S1-Pro 上能"注册 + 触发"，但"正确消化 Skill 内容"还需要 prompt engineering**。
- **Claude 亲生模型（claude-sonnet-4-6 等）对 Skill 理解较好，Intern-S1-Pro 容易"忘了自己是来执行不是来委托的"**。
- **MCP 比 Skill 在 Intern-S1-Pro 上稳得多**（参见 [practice-mcp](?section=practice-mcp)）：一旦有结构化 schema + 清晰 tool_use/tool_result 往返，它做得很好。

遇到 Intern-S1-Pro 不按预期执行 Skill 时，往"直接把 Skill 工作流写进 prompt"这个方向退一步就是。

## 下一步

- 回「总览」Tab 学习 Hooks
- 看 [MCP 最小示例](?section=practice-mcp)——结构化工具在 Intern-S1-Pro 上更稳
- 想把 Skill 做得更严谨，参考 Anthropic 官方 [Skill 规范](https://docs.claude.com/claude-code/skills)（含进阶示例）
