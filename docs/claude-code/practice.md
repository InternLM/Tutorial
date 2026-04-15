# Claude Code 日常开发实战

> 与平台无关。无论在 [昇腾](?section=hands-on-ascend) / [曦云](?section=hands-on-metax) / [A100](?section=hands-on-a100) 哪个环境跑，命令一致。
>
> **本节给的是经过验证的"使用思路 + 命令骨架"。具体生成的代码 / 调试输出会因后端模型与 prompt 而异，请以你实际跑出来的为准，并把不一致的地方反馈给我们。**

## 四个核心场景

Claude Code 在日常开发里的高频用法可以归到 4 个场景。每个场景给一个"最小可运行起点"，剩下的靠你与 Claude Code 多轮对话往下聊。

### 场景一：代码生成

**思路：** 描述需求 → 让 Claude Code 生成项目骨架 → 自己跑一遍 → 反馈问题让它迭代。

**最小起点：**

```
进入 Claude Code 交互模式，输入：
"在当前目录创建一个 Python FastAPI 服务，包含 /health 接口返回 'ok'，
 同时生成 requirements.txt 和最简 README，启动命令写在 README 里。"
```

跑一遍验证：

```bash
pip install -r requirements.txt
uvicorn main:app --reload
curl http://localhost:8000/health
```

**经验：** 描述越具体越好（接口路径、入参、返回字段、错误处理要不要、是否要类型注解……）。模糊的描述会得到模糊的代码。

### 场景二：Bug 调试

**思路：** 把完整 Traceback 喂给 Claude Code，让它先读相关文件、分析、再改。

**最小起点：**

```
"运行 python xxx.py 报错：[贴完整 traceback]
 请读相关文件，分析原因并修复。"
```

**经验：**
- 完整堆栈比单行错误信息有用 10 倍
- 偶发性 bug 要描述触发条件（"只在输入为空时"）
- 复杂 bug 可以让 Claude 先加日志定位再修

### 场景三：代码审查

**思路：** 直接让 Claude Code 看 `git diff` 或某个目录。

**最小起点：**

```
"审查当前 git diff 中的所有变更，重点关注：
 1. 安全（SQL 注入 / XSS / 凭证泄露）
 2. 错误处理是否完整
 3. 边界条件
 给出修改建议。"
```

**经验：** 让它聚焦在你关心的维度（不要让它"全面审查"，会发散）。

### 场景四：代码重构

**思路：** 描述目标结构，让 Claude Code 拆分、重命名、提取，并保持对外接口稳定。

**最小起点：**

```
"将 utils.py 中超过 50 行的函数拆分为独立模块，
 保持对外 import 接口不变（其他文件不需要改），
 每个新模块加单元测试。"
```

**经验：** 重构前先 `git commit` 一次，重构后 `git diff` 自己审一遍。

## 常用命令速查

| 命令 | 作用 |
|------|------|
| `/compact` | 压缩对话历史，释放上下文窗口 |
| `/clear` | 清空当前对话重新开始 |
| `claude --resume` | 恢复上一次会话 |
| `claude --print "问题"` | 非交互模式，输出后退出 |

**上下文引用：**

在对话里直接写文件路径（或 URL / git commit hash），Claude Code 会自动读取：

```
"看看 src/utils/helper.py 这个文件，有没有可以优化的地方。"
```

---

## 关于 Intern-S1-Pro 的特别说明

**模型差异：** Claude Code 设计时面向 Anthropic 自家模型（Claude），其它模型（含 Intern-S1-Pro）在以下方面可能与教材描述不完全一致：
- **工具调用稳定性**：某些复杂多步工具链可能需要更明确的 prompt
- **代码生成完整性**：可能需要更多次迭代
- **指令跟随**：复杂格式约束（JSON Schema、特定风格）可能需要在 system message 里强化

**遇到不符合预期的输出时：**
1. 先简化 prompt 重试
2. 不要相信模型一句话给出的"完整答案" — 自己跑一遍
3. 通过划词反馈告诉我们，帮我们优化教材
