# Claude Code 日常开发实战

> 与平台无关的实战内容。无论你在 [昇腾](?section=hands-on-ascend) / [曦云](?section=hands-on-metax) / [A100](?section=hands-on-a100) 哪个环境跑，命令完全一致。

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

