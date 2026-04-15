# Claude Code 实操 · 华为昇腾 Atlas 800T A2

> 适用于华为昇腾 Atlas 800T A2 服务器（aarch64 Linux）。

## 昇腾算力平台（推荐给学员）

书生社区提供免费/低成本的昇腾 Atlas 800T A2 开发环境：

🔗 **https://internstudio-ascend.intern-ai.org.cn/**

- 一站式开发机，预装 CANN / Python / PyTorch NPU 生态
- 注册后可直接开机，省去自建环境的折腾
- 本节教程所有命令都在这里亲测可跑

如果你有自己的昇腾服务器，也可以按同样流程在本机操作。

## 前置

- 操作系统：Ubuntu 22.04 aarch64 / openEuler / Kylin V10
- NPU：Atlas 800T A2（64GB HBM）
- 架构：**aarch64**（用 `uname -m` 确认）

## 第一步：装 Node.js

昇腾算力平台默认已有 conda，直接一行搞定：

```bash
# 如果是刚 SSH 进来提示 "node: command not found"，先 activate 一下 conda：
. /root/.conda/etc/profile.d/conda.sh && conda activate base

conda install -c conda-forge nodejs=22 -y

node --version   # v22.x
npm --version    # 10.x+
```

> 版本建议 22（当前 LTS），如需其他版本：`conda install -c conda-forge nodejs=20`。
>
> **踩坑提示（Gotcha 1）：** 昇腾镜像默认有 conda，但 PATH 没初始化。SSH 刚登进去直接敲 `node` / `claude` 会 command not found。要么手动 `conda activate base`，要么把 `conda activate base` 加到 `~/.bashrc` 末尾。

## 第二步：装 Claude Code

```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

Claude Code 在 aarch64 上的行为与 x86_64 完全一致，不需要任何特殊编译。

## 第三步：启动 Claude Code

书生社区的 API 端点原生兼容 Anthropic 协议。**推荐每次启动时临时设环境变量**（不污染 `~/.bashrc`、便于多账号切换）：

```bash
export ANTHROPIC_BASE_URL="https://chat.intern-ai.org.cn"
export ANTHROPIC_AUTH_TOKEN="your-internlm-api-token"

cd your-project
claude --model intern-s1-pro
```

> Token 在 https://internlm.intern-ai.org.cn/api/tokens 获取。
>
> 如果你想固化到 shell 配置（不再每次输），把上面 2 行 `export` 加到 `~/.bashrc` 即可。
>
> Claude Code 只是客户端，不直接调 NPU。模型推理跑在服务端 Ascend NPU 上，对客户端完全透明。

## 昇腾环境特殊点

| 项 | 说明 |
|----|------|
| CANN 兼容 | Node.js 与 CANN / torch_npu 互不干扰，可在同一环境共存 |
| Python 依赖 | MCP Server 用 Python 时，注意 `pip install` 的包选 aarch64 wheel |
| 性能 | 客户端侧无差异；服务端推理性能取决于具体 Ascend 集群配置 |
| 离线部署 | 见上面的 rsync / npm 镜像方案 |

## 非交互模式 / 批量跑实测 gotcha

以下三条在本课程实际跑教材场景（[practice](?section=practice)）时真实踩到，学员如果要用 `claude --print` 做批量自动化或在 root 下跑，一定要先过一遍。

### Gotcha 2：root 下用不了 `--dangerously-skip-permissions`

昇腾算力平台默认是 root 登录，运行：

```bash
claude --print --dangerously-skip-permissions "..."
```

直接报：

```
--dangerously-skip-permissions cannot be used with root/sudo privileges for security reasons
```

`--permission-mode bypassPermissions` 与 `--dangerously-skip-permissions` 是一回事，同样被拦截。

**两个解法，任选其一**：

1. **创建非 root 用户**（推荐，学员路径）：
   ```bash
   useradd -m -s /bin/bash stu
   su - stu
   # 再在 stu 下跑 claude，--dangerously-skip-permissions 可用
   ```

2. **在 root 下用 `acceptEdits` + 白名单**（批量脚本路径）：
   ```bash
   claude --model intern-s1-pro --print \
     --permission-mode acceptEdits \
     --allowedTools Read Write Edit Bash Glob Grep MultiEdit \
     < prompt.txt
   ```
   这套在本课程的 4 个实测场景里是跑得通的，但 Bash 工具仍会被自动后台化（下一条）。

### Gotcha 3：`--print` + tool_use + 无最终 text 输出时"看起来卡了"

纯 `--print` 默认只输出模型最终的 assistant text。如果模型流程是 `tool_use → tool_result → end_turn`（比如写了个文件就结束），默认输出是空的，但任务其实已经完成。

**解法：** 加 `--output-format stream-json --verbose`。这样每一步 thinking / tool_use / tool_result 都能看到，不会误以为 claude 卡住了。

同时写 prompt 时带一句「完成后用一句话总结你做了什么」，逼模型在最后多一个 text 块。

### Gotcha 4：Bash 工具在 Intern-S1-Pro 下经常被自动后台化，模型会转进去

在 `--print` 非交互模式下，Claude Code 会把一些 Bash 调用标记为 `is_backgrounded: true`，stdout 先写到临时文件，tool_result 只返回一个 task id。Intern-S1-Pro 很容易被这个机制绊住：它会不停调 `TaskOutput` 等结果，反复读空文件，直到外层 timeout。

表现出来的现象：

- 跑 `git diff`、`python -m unittest`、`ls -la` 这类本该秒出的命令，最终被 killed、exit code 137 / 124。
- 模型的 thinking 一直在说「让我等测试完成」「让我再检查一次」。

**三种绕开方式：**

1. **让 claude 只写代码，不跑代码**。在 prompt 最后加「不要调 Bash」。自己在终端手动验证。
2. **把需要的输出先 dump 到文件，让 claude Read 这个文件**：
   ```
   "把 git diff 写到 /tmp/d.diff，然后 Read /tmp/d.diff 再分析。"
   ```
3. **命令尽量简单**：避免 `&&` 拼接、避免 `2>&1` 重定向、避免启动服务进程。

### Gotcha 5：远程跑长任务别用 paramiko 直连

用 Python paramiko 远程 `exec_command` 跑几分钟的 claude 任务，容易被 SSH channel buffer 阻塞超时。推荐：

```bash
# 远程节点上
nohup bash run.sh </dev/null >out.log 2>&1 & disown
```

然后本地 `tail -f out.log` 或定期拉 `out.log` 看进度。`run.sh` 里就是完整的 `export ANTHROPIC_* + claude --print ... < prompt.txt`。这套模式在教材实测时处理了 6 个长任务全部稳定。

## 下一步

- 回「总览」Tab 学习 MCP Server 开发、Skills、Hooks
- 看 [practice](?section=practice) 的"实测记录"章节了解 4 个典型开发场景在昇腾上的真实表现
- 走「闯关任务」提交通过证明
