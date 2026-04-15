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

---

## 实测记录（Intern-S1-Pro + 昇腾 Atlas 800T A2，2026-04-15）

> 下面四个场景全部在昇腾 Atlas 800T A2 算力平台（aarch64，CANN 7.x，conda Python 3.13）用 Intern-S1-Pro 模型实际跑过。真实的输入、输出、失败 / 成功一并保留，便于你对照自己的运行结果。

运行方式（所有场景一致）：

```bash
export ANTHROPIC_BASE_URL=https://chat.intern-ai.org.cn
export ANTHROPIC_AUTH_TOKEN=<你的 token>
claude --model intern-s1-pro \
  --print --output-format stream-json --verbose \
  --permission-mode acceptEdits \
  --allowedTools Read Write Edit Bash Glob Grep MultiEdit \
  < prompt.txt > out.log 2>&1
```

> 为什么是 `--permission-mode acceptEdits` + `--allowedTools`？昇腾平台默认 root 登录，root 下用不了 `--dangerously-skip-permissions`。`acceptEdits` 模式 + 白名单可以在 root 下正常跑批量。详见 [hands-on-ascend](?section=hands-on-ascend) 底部 Gotcha。

### 场景一实测：从失败到成功（4 次尝试）

任务：让 Claude Code 在空目录生成 main.py + requirements.txt + README.md 的最小 FastAPI 服务。

这是学员最可能在 Intern-S1-Pro 上踩坑的场景，我们完整记录 4 次尝试过程，帮你理解"写 prompt 时哪些措辞会失败 / 成功"。

#### 尝试 1：原样照抄教材 prompt（❌ 产出不完整）

prompt：

```
在当前目录创建一个 Python FastAPI 服务，包含 /health 接口返回 {"status": "ok"}，
同时生成 requirements.txt 和最简 README（README 里写启动命令和测试 curl 命令）。

完成后用一句话总结你创建了哪些文件。
```

实际发生：27.6s / 3 turns / $0.14。**只写了 README.md 和 requirements.txt，main.py 漏了**。

`stream-json` 日志显示：模型调完两次 Write（README、requirements）之后，thinking 里还说"我需要创建 main.py 文件"，然后直接 end_turn，没发出第三次 tool_use。这是 Intern-S1-Pro 非常典型的"想了但没干"。

#### 尝试 2：拆成编号列表（❌ 完全空转）

prompt：

```
在当前目录依次完成以下步骤，每一步都要调用对应工具：

1. 用 Write 工具创建 main.py，内容是一个最小 FastAPI 应用...
2. 用 Write 工具创建 requirements.txt...
3. 用 Write 工具创建 README.md...
4. 用 Bash 工具执行 `ls -la` 确认三个文件都存在...
```

实际发生：12.9s / **1 turn** / $0.07。一次 thinking 之后直接 end_turn，**零次 tool_use**。

#### 尝试 3：极度命令式 + 只要一个文件（✅ main.py 成功，但触发另一个 gotcha）

prompt：

```
请立即调用 Write 工具，创建文件 /root/s1v3/main.py，文件内容如下：

（贴完整代码）

创建完成后，调用 Bash 工具执行 `ls -la /root/s1v3/ && cat /root/s1v3/main.py`。
```

实际发生：main.py 被正确写入；但 Bash(`ls && cat`) 被 Claude Code 标记为 `is_backgrounded: true`，模型进入"读 task 输出文件 → 拿到空 → 再等"的死循环，180s 超时 kill。

> **这是 Intern-S1-Pro + Claude Code 的第二个典型 gotcha**：Bash 工具会把很多本应前台执行的命令放到后台，Intern-S1-Pro 不擅长处理这种异步等待，容易把自己转进去。绕开方法见场景四。

#### 尝试 4：一次写三个文件 + 明确终止条件（✅ 一把成功）

prompt：

```
请立刻在当前目录依次调用 Write 工具三次，创建下面三个文件。不要先思考太久，直接开始调用工具。

文件 1：main.py
（贴代码）

文件 2：requirements.txt
（贴内容）

文件 3：README.md
（贴内容）

三个 Write 工具调用完成后立刻结束，不要再调 Bash，不要再思考。
```

实际发生：19.6s / 4 turns / $0.14。三个文件一次写全，模型最终 thinking：「文件已成功创建。三个文件都已经写入完成，不再需要任何操作。」

#### 场景一结论

- **Intern-S1-Pro 对"隐式多步"跟随弱**：只要 prompt 里出现"然后 / 接下来 / 再 / 同时"这种词，模型很可能中途 end_turn。
- **对"已经开始就继续"的惯性也弱**：它需要 prompt 明确说"立刻 / 不要思考 / 连续调用 N 次"。
- **明确终止条件同样重要**：加上"调完 X 次就结束，不要再 Y"能显著降低走偏概率。
- **避免让模型跑会被后台化的 Bash**（见下面场景四）。

跑通后用下面命令本地验证（昇腾环境亲测）：

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 &
curl http://127.0.0.1:8000/health
# → {"status":"ok"}
```

### 场景二实测：KeyError 一把修好

任务：有个 `app.py` 报 KeyError，让 Intern-S1-Pro 读文件 → 定位 → 用 Edit 修。

初始代码：

```python
DATA = [
    {"name": "Alice", "email": "alice@example.com", "age": 30},
    {"name": "Bob", "email": "bob@example.com"},   # 缺 age
    {"name": "Charlie", "email": "charlie@example.com", "age": 25},
]

def summarize(users):
    for user in users:
        print(f"{user['name']} ({user['age']}): {user['email']}")
```

Traceback（跑 `python app.py` 真实得到的）：

```
Alice (30): alice@example.com
Traceback (most recent call last):
  File "/root/s2/app.py", line 17, in <module>
    summarize(DATA)
  File "/root/s2/app.py", line 13, in summarize
    print(f"{user['name']} ({user['age']}): {user['email']}")
KeyError: 'age'
```

prompt（要点：把 traceback 原文贴进去 + 要求"立即按顺序"）：

```
当前目录下有一个 app.py 运行时报错：

<贴 traceback>

请立即按顺序执行：
1. 调用 Read 工具读 /root/s2/app.py 的完整内容
2. 分析根因（一句话）
3. 调用 Edit 工具修复：让缺失 age 字段的用户显示 age 为 "?"
4. 修复完成后用一句话说明你改了什么

注意：不要调用 Bash 工具，改完就结束。
```

实际发生：35.1s / 3 turns / $0.21。Intern-S1-Pro：

1. Read app.py → 看全部代码
2. thinking：「用户数据中 Bob 缺少 age 字段，导致访问 user['age'] 时抛出 KeyError。」
3. Edit 修复（第 13 行）：`user['age']` → `user.get('age', '?')`
4. 输出总结：「修改了 app.py 第 13 行...使得缺失 age 字段的用户会显示 age 为 "?"。」

验证：

```bash
$ python app.py
Alice (30): alice@example.com
Bob (?): bob@example.com
Charlie (25): charlie@example.com
```

**经验：**

- 贴完整 traceback（包括 traceback 之前正常输出的那几行），比让模型"自己跑"省很多 turn。
- 明确"不要调用 Bash"能避免触发后台化问题。

### 场景三实测：git diff 审查（真实找到 3 个问题）

任务：审查一份刚改过的 auth.py，聚焦"安全 / 错误处理 / 可读性"。

新加了两个函数，故意埋雷：

```python
def search_users_by_keyword(db_path, keyword):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(f"SELECT id, username FROM users WHERE username LIKE '%{keyword}%'")  # SQL 注入
    rows = cur.fetchall()
    return rows   # 漏关连接

def validate_login(db_path, username, password):
    user = get_user(db_path, username)
    if user is None: return False
    if user[2] == password:  # password_hash 跟明文比
        return True
    return False
```

prompt（聚焦三维度 + 禁止改代码）：

```
请立刻按顺序执行：
1. 调用 Bash 工具执行 `git diff auth.py`
2. 调用 Read 工具读 auth.py 完整内容
3. 审查这段 diff，聚焦三个维度（逐条给出，用三级标题）：
   - 安全：SQL 注入 / 明文密码 / 凭证泄露
   - 错误处理：资源是否释放、异常是否覆盖
   - 可读性与简化空间
4. 对每个高危问题给出一行修复建议（不要直接改代码）

只输出审查结论，不要调用 Edit/Write。审查完立即结束。
```

实际发生：195s（绝大部分时间花在一次失败的 git diff 后台读取上，参见下面 gotcha）/ 4 turns / $0.29。

模型输出（原文摘录）：

> ### 安全
> - **高危 SQL 注入**：`search_users_by_keyword` 函数（第 18 行）使用 f-string 直接拼接 SQL 语句
> - **密码存储/验证问题**：`validate_login` 比较哈希值与明文密码，暗示密码未正确哈希存储
> - **无凭证泄露防护**：密码明文在函数参数和内存中传递
>
> ### 错误处理
> - **资源泄漏**：`search_users_by_keyword` 获取数据库连接后未关闭，导致连接泄露
> - **异常覆盖不足**：所有数据库操作均无 try/except 捕获
>
> ### 可读性与简化空间
> - **重复连接逻辑**：多个函数重复创建/关闭数据库连接，可提取为上下文管理器
>
> ## 修复建议
> 将 `search_users_by_keyword` 第 18 行改为参数化查询：
> `cur.execute("SELECT id, username FROM users WHERE username LIKE ?", (f"%{keyword}%",))`

**三处真问题（SQL 注入 / 资源泄漏 / 明文对比）全部被识别**，修复建议也给得准确。

**gotcha（必看）：** `Bash` 工具里跑 `git diff` 被 Claude Code 自动后台化，stdout 没进 tool 返回。Intern-S1-Pro 没意识到这点，直接绕过去用 Read 把整个 auth.py 读了一遍，「猜」diff 在做什么。所以最终的 review 是基于"整个文件是什么"而不是"diff 改了什么" —— 对这个例子没问题（新函数是新加的全部有雷），但如果你想严格让它只看"新增改动"，要先把 diff dump 到文件，再让它 Read 那个文件：

```
"把 git diff auth.py 的输出写到 /tmp/d.diff，然后 Read /tmp/d.diff 再做审查。"
```

### 场景四实测：生成单元测试（6 个用例全通过）

任务：给一个 `utils.py`（三个函数：`clean_and_split_words` / `count_word_frequency` / `top_n_words`）写 `unittest` 测试。

prompt：

```
当前目录下有 utils.py，包含三个函数。请立刻按顺序调用工具：

1. 调用 Read 工具读 /root/s4/utils.py 全部内容
2. 调用 Write 工具创建 test_utils.py，用 Python 标准库 unittest 至少写 4 个用例，覆盖：
   - clean_and_split_words 对普通句子的结果
   - clean_and_split_words 对空字符串/只有空格的结果
   - count_word_frequency 对重复词的计数
   - top_n_words 的 n 限制与 tie-break 排序
3. 调用 Bash 工具执行 `python -m unittest test_utils.py -v 2>&1`，把完整输出返回

只需保持现有 utils.py 的对外接口不变（不要动它），你只是补测试。
```

实际发生：

- Read utils.py ✅
- Write test_utils.py ✅（生成了 **6 个**测试用例，多加 2 个边界用例）
- Bash 跑测试 ❌ —— 又被 Claude Code 后台化，Intern-S1-Pro 连续调 3 次 `TaskOutput` 拿不到结果，最后 kill 超时

**但测试文件本身是对的**：我们手动在昇腾上跑 `python -m unittest test_utils.py -v`，6/6 全过：

```
test_clean_and_split_words_empty_and_whitespace ... ok
test_clean_and_split_words_mixed_characters ... ok
test_clean_and_split_words_normal_sentence ... ok
test_count_word_frequency_with_repeats ... ok
test_top_n_words_limit_and_tie_break ... ok
test_top_n_words_with_n_limit ... ok
----------------------------------------------------------------------
Ran 6 tests in 0.001s
OK
```

**经验（重要）：**

- **非交互（`--print`）模式下，能不让 Intern-S1-Pro 跑 Bash 就别跑**。它很容易跟不上 Claude Code 的后台任务机制。
- 真要验证，**拆成两步**：让 claude 只负责写代码；自己在终端手动跑验证命令。

## 成本参考（4 场景 + MCP + Skill，单次完整跑通）

| 场景 | 耗时 | input tokens | output tokens | 费用（USD） |
|------|------|--------------|---------------|------------|
| 场景一（最终成功版） | 19.6s | 45,779 | 283 | 0.14 |
| 场景二 | 35.1s | 68,906 | 319 | 0.21 |
| 场景三 | 195s | 92,423 | 933 | 0.29 |
| 场景四（含多次无效 TaskOutput） | ≥300s 超时 | - | - | - |
| MCP weather demo | 25.8s | 68,398 | 262 | 0.21 |
| Skill demo（失败） | ≥180s 超时 | - | - | - |

> input token 始终较大是因为 Claude Code 会把 system prompt、tool 定义、工作目录信息全部塞进上下文。完整 4 场景 + MCP 实测总花费约 **$1 量级**，给单个学员跑一遍完全可行。

## 延伸阅读

- [MCP Server 最小示例（weather-demo）](?section=practice-mcp)
- [Skills 最小示例（pylint-check）](?section=practice-skills)
