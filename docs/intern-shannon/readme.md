# 书安 Intern-Shannon：智能体安全操作系统

> 本文档 AI + 社区共建中，欢迎划词反馈。

## 为什么要学这门课

智能体（Agent）加速迈向规模化应用已经成为大模型产业的核心载体。但一系列 AI 安全事件频发：OpenClaw 安全风险、Claude Code 源码泄露、Axios 供应链投毒……在企业实际场景，智能体需要访问敏感数据、执行系统命令、对外发送数据，**安全问题直接关系到代码资产、数据隐私、系统权限和产业生态**。

上海 AI 实验室将「书生」和「书安」作为 AGI4S 战略的双螺旋：

- **书生**：以学识应变，推动 AI 在科学与产业的前沿创新
- **书安**：以安全护航，为智能体规模化落地夯实安全基座

学完这门课，你会掌握一套**生产级智能体安全治理能力**：从硬件级沙箱隔离，到 Agent 监管协议，再到多智能体风险评估。

## 课程定位

- **前置**：学过 Claude Code、MCP、Agent2Agent 或 OpenClaw 任意一门（知道 Agent 是什么、能干什么）
- **学时**：4-5 小时
- **适合**：
  - 想把 Agent 投产但担心安全的工程师
  - 想做 AI 安全方向的研究者
  - 关注合规、数据隐私、企业 AI 落地的从业者

## 书安产品矩阵

书安 Intern-Shannon 由一组开源组件组成，GitHub 组织：**https://github.com/AI45Lab**

| 组件 | 定位 | 技术栈 | 关键能力 |
|------|------|--------|----------|
| [**A3S Box**](https://github.com/AI45Lab/Box) | MicroVM 运行时 | Rust | 硬件级沙箱，~200ms 冷启动，OCI 兼容，AMD SEV-SNP TEE |
| [**A3S Code**](https://github.com/AI45Lab/Code) | 意图驱动 Agent 框架 | Rust + Py/Node bindings | 工作区+工具+记忆，上下文按需注入 |
| [**AHP**](https://github.com/AI45Lab/AgentHarnessProtocol) | Agent Harness Protocol | Rust | 统一所有 Agent 框架的监管协议 |
| [**ClawSentry**](https://github.com/AI45Lab/ClawSentry) | AHP 参考实现 | Python | 三层决策 + 六维风险评分 |
| [**SentrySkills**](https://github.com/AI45Lab/SentrySkills) | 自护航技能包 | Python | 三阶段防护，零依赖，33+ 规则 |
| [**TrinityGuard**](https://github.com/AI45Lab/TrinityGuard) | 多智能体系统安全框架 | Python | 20 种风险，pre-deploy + runtime |

所有组件 **MIT 协议**开源。

## 课程地图

本课分为 5 节：

1. **第 1 节**：AI 智能体的安全挑战 — 为什么现在必须谈安全
2. **第 2 节**：A3S Box 硬件级沙箱 — 用 MicroVM 隔离 Agent 的执行环境
3. **第 3 节**：AHP 协议与 ClawSentry — 给任何 Agent 框架加一层通用监管
4. **第 4 节**：SentrySkills 三阶段防护 — preflight / runtime / output
5. **第 5 节**：TrinityGuard 多智能体风险评估 — 20 类风险、跨 L1/L2/L3

---

## 第 1 节：AI 智能体的安全挑战

### 为什么 Agent 比传统软件更危险

传统软件的行为是**确定**的：开发者写什么代码，执行什么逻辑。Agent 不同：

- **自主决策**：Agent 根据 LLM 输出决定调用什么工具、发什么网络请求、写什么文件
- **工具丰富**：shell、HTTP、文件系统、数据库、云服务全都可用
- **上下文敏感**：同一个 prompt，环境不同，行为完全不同
- **可被诱导**：提示词注入（prompt injection）让 Agent 做原本不该做的事

结果就是**攻击面从"代码逻辑"变成了"语义决策"**。传统的 sandbox、代码审计已经不够。

### 真实案例

**案例 1**：用户请求"帮我创建视频分析技能"
- 不安全 Agent：根据参考文档生成代码，其中隐藏了摄像头调用、屏幕录制、自动上传 GitHub 的逻辑
- 安全 Agent（书安）：识别出"摄像头滥用 / 屏幕录制 / 数据外传"三类风险，**阻断执行**并向用户报告

**案例 2**：供应链投毒
- `pip install` 一个伪装成合法依赖的包，安装后悄悄发送凭证到远程服务器
- 无沙箱：直接污染开发环境
- A3S Box 沙箱：`pip install` 只在 MicroVM 里执行，结束即销毁，无法触达宿主机

### 安全不是给 Agent 踩刹车

上海 AI 实验室 胡侠老师的观点：

> 安全并非要给 AI 踩刹车，而是要打造出"原生安全的 AI"让技术持续高速发展。

书安的设计理念是**内生安全**（Security by Design）：
- 执行环境默认隔离（A3S Box）
- 行为默认被监管（AHP + ClawSentry）
- 技能默认自护航（SentrySkills）
- 模型自身认知安全（Make Safe AI 理论）

---

## 第 2 节：A3S Box — 硬件级沙箱

### 它是什么

A3S Box 是一个 **MicroVM 运行时**，不是容器、不是编排器。每个负载运行在独立的 Linux 内核里，通过虚拟化技术硬件级隔离。

- **冷启动 ~200ms**：用 libkrun（macOS 用 Apple HVF / Linux 用 KVM / Windows 用 WHPX）
- **OCI 兼容**：直接跑 Docker Hub、私有仓库、自建镜像
- **跨平台**：macOS ARM64、Linux x86_64/ARM64、Windows x86_64
- **Kubernetes CRI**：可作为 Kubernetes RuntimeClass

相比 Docker：
- Docker 共享宿主机内核 → 内核漏洞可能逃逸
- MicroVM 独立内核 → 逃逸难度指数级上升

相比 Firecracker：
- Firecracker 只支持 Linux
- A3S Box 原生跨平台，且支持 AMD SEV-SNP 机密计算

### 上手：Docker-like CLI

安装后（参考官方 README），命令行几乎和 Docker 一样：

```bash
# 拉镜像
a3s-box pull python:3.11

# 跑一个 Python 脚本（在 MicroVM 里）
a3s-box run --rm -it python:3.11 python -c "print('hello from VM')"

# 后台跑服务
a3s-box run -d --name web -p 8080:80 nginx
a3s-box logs -f web
a3s-box stop web
```

### CRI 模式：Kubernetes Pod 隔离

配置 RuntimeClass：

```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: a3s-box
handler: a3s-box-shim
```

创建 Pod 时指定：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-agent
spec:
  runtimeClassName: a3s-box
  containers:
    - name: agent
      image: my-agent:latest
```

Pod 内的容器就跑在 MicroVM 里了，邻居 Pod 无法通过内核漏洞攻击过来。

### 机密计算（TEE）

在 AMD EPYC Milan / Genoa 服务器上，A3S Box 支持 **SEV-SNP** 硬件内存加密：

- 远程证明（remote attestation）：向客户端证明"我真的跑在 SNP 硬件里"
- RA-TLS：SNP 报告放进 X.509 证书里
- Sealed Storage：密钥只能在特定硬件+特定度量下解密
- Secret Injection：密钥通过 RA-TLS 投递到 `/run/secrets/`

这意味着**连云厂商都看不到你的 Agent 在做什么**。适合处理医疗、金融、国防等高敏数据。

### 动手练习

1. 在 macOS / Linux 本机安装 a3s-box
2. 跑一个简单 Agent：`a3s-box run --rm anthropic/claude-code "分析当前目录的安全风险"`
3. 观察：Agent 无法访问宿主机文件系统，只能访问 MicroVM 内的环境

---

## 第 3 节：AHP 协议与 ClawSentry

### AHP 要解决什么问题

每个 Agent 框架（Claude Code、Codex、OpenClaw、LangChain、AutoGPT、A3S Code、CrewAI……）都有自己的 hooks / callbacks 系统。为一个框架写的安全规则，**换到另一个框架全部要重写**。

后果：
- 供应商锁定
- 重复造轮子
- Agent 无法跨框架协同

AHP（Agent Harness Protocol）定义**一套协议**，任何 Agent 框架实现后就能用任何 AHP 兼容的监管器（Harness）。

### 架构

```
┌──────────────────────────────────────────────────────┐
│                   Agent 框架                          │
│   (Claude Code / Codex / OpenClaw / LangChain ...)   │
│                        │                              │
│                        ▼                              │
│   ┌──────────────────────────────────────────────┐   │
│   │  AHP Client                                   │   │
│   │  • 拦截 Agent 的每个动作                        │   │
│   │  • 发事件给 Harness                            │   │
│   │  • 执行 Harness 的决策                         │   │
│   └──────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────┐
│                  AHP Harness                          │
│   (Policy engine / 安全规则 / 审计日志)                │
│                                                      │
│   接收事件 → 应用策略 → 返回决策                       │
│   Allow / Block / Modify / Defer / Escalate          │
└──────────────────────────────────────────────────────┘
```

### ClawSentry：AHP 的参考实现

**三层渐进决策**：

| 层级 | 延迟 | 机制 |
|------|------|------|
| L1 规则引擎 | <1ms | 基于正则/规则的快速判断，命中即决策 |
| L2 语义分析 | <3s | LLM 分析命令语义，判断意图是否合规 |
| L3 审查 Agent | <30s | 独立 LLM agent 完整审查 session 历史 + 当前动作 |

绝大多数请求在 L1 就被放行或拦截（~99%），只有可疑请求才升级到 L2/L3。

**六维风险评分（D1-D6）**：

- D1 命令危险度：`rm -rf /` 这种高危指令
- D2 路径敏感度：是否访问 `/etc/shadow`、`~/.ssh/`、`.env`
- D3 命令模式：匹配已知攻击模式（shell 注入、反向 shell）
- D4 会话历史：这个 Agent 过去 10 分钟是否出现过异常
- D5 信任等级：Agent 身份 / 用户权限
- D6 **注入检测**：三层分析 — 启发式正则 + Canary Token 泄露 + 可插拔 EmbeddingBackend（向量相似度）

### 快速上手

```bash
pip install clawsentry           # 核心
pip install clawsentry[llm]      # 加 Anthropic/OpenAI 用于 L2/L3
pip install clawsentry[all]      # 全家桶
```

Python >= 3.11。

启动监管服务：

```bash
clawsentry serve --port 9999
```

然后让 Claude Code / OpenClaw / Codex CLI 的 hook 指向 ClawSentry。以 Claude Code 为例，配置 hooks：

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "curl -s -X POST http://localhost:9999/ahp/event -d @-"
      }]
    }]
  }
}
```

每次 Claude Code 要跑 shell，先发给 ClawSentry 判断，根据返回决定 allow / block。

### 实时监控

```bash
clawsentry watch
```

命令行里看每一个决策。也有 React/TypeScript 的 Web Dashboard。

### 自进化规则库（E-5）

ClawSentry 会从高风险事件里**自动提取候选规则**，经 `CANDIDATE → EXPERIMENTAL → STABLE` 生命周期稳定化，置信度评分。你的 ClawSentry 用得越久，越懂你这套环境里什么是"正常"。

---

## 第 4 节：SentrySkills — 三阶段防护

### 它适合谁

SentrySkills 是一个**零依赖**（纯 Python 标准库）的技能包，最适合直接装到 Claude Code / Codex 里：

- 想给团队成员的 Claude Code 装一道"守门员"
- 不想依赖外部服务，离线也要能用
- 追求 IDE 里低延迟（毫秒级）

### 三阶段

```
用户请求
   │
   ▼
[Preflight 预检] ← 在 Agent 执行前，扫描意图 + 预测风险
   │ 放行
   ▼
[Runtime 运行时] ← Agent 执行中监控行为
   │ 正常
   ▼
[Output 输出] ← 对响应脱敏（过滤敏感数据）
   │
   ▼
 用户
```

**预测式风险分析**：还没执行就能警告潜在风险。例如 Agent 说"我要读取 .env 文件"，SentrySkills 预测到"可能后续会泄露到网络请求"，提前警告。

### 33+ 检测规则

覆盖：
- AI 攻击：prompt injection / jailbreak / role-play bypass
- Web 漏洞：XSS / SQL injection / SSRF
- 数据泄露：API key / 凭证 / PII
- 代码安全：shell injection / unsafe deserialize / eval

### 策略 Profile

开箱即用的三个 profile：

- **balanced**（默认）：平衡安全性和可用性，适合日常开发
- **strict**：最严格，适合处理生产数据
- **permissive**：最宽松，适合自己的沙箱实验

### 安装（Claude Code 推荐方式）

```bash
# 放到 Claude Code 的 skills 目录
cp -r sentryskills ~/.claude/skills/
```

启动 Claude Code 时，SentrySkills 自动生效。

---

## 第 5 节：TrinityGuard — 多智能体风险评估

### 它解决什么

单 Agent 的安全问题已经够复杂，**多 Agent 系统（Multi-Agent System, MAS）**更危险：

- Agent A 说的话被 Agent B 当权威接受
- Agent 间消息篡改、伪装
- 级联失败：一个 Agent 出错带崩整个系统
- 恶性涌现：多个 Agent 协同做坏事

TrinityGuard 是**上海 AI 实验室**发布的 MAS 安全框架，覆盖 20 种风险，跨三个层级。

### 20 种风险分三级

**L1 单 Agent 风险（8 类）**：
- Jailbreak / Prompt Injection / Sensitive Data Disclosure / Excessive Agency / Code Execution / Hallucination / Memory Poisoning / Tool Misuse

**L2 Agent 间通信风险（6 类）**：
- Message Tampering / Malicious Propagation / Misinformation Amplification / Insecure Output / Goal Drift / Identity Spoofing

**L3 系统级风险（6 类）**：
- Cascading Failures / Sandbox Escape / Insufficient Monitoring / Group Hallucination / Malicious Emergence / Rogue Agent

### 两种模式

**预部署测试（Pre-Deployment Testing）**：
- 在 MAS 上线前，用攻击 payload 跑一遍看会不会被打穿
- 生成测试报告，列出脆弱点

**运行时监控（Runtime Monitoring）**：
- MAS 上线后持续监控
- 滑动窗口分析行为序列
- 异常 → 实时告警 / 自动隔离

### Judge 系统

每个风险有对应的判定器：
- 默认用 **LLM-powered 判断**（Claude / GPT 分析语境）
- LLM 不可用时 fallback 到**模式匹配**（regex + 关键词）

### 框架支持

- AG2 / AutoGen（固定工作流 + 群聊）
- 可扩展插件系统，自己加新的 judge

### 动手练习

1. `pip install trinity-guard`
2. 用你自己的 MAS 跑一次预部署测试
3. 查看 20 类风险的测试结果 → 写一份整改清单

---

## 闯关任务

完成本课后，你需要完成三个任务（放在 [task.md](./task.md)）：

1. **基础**：用 A3S Box 把任意一个 LLM Agent 跑在 MicroVM 里，对比宿主机直接跑的差异
2. **进阶**：给 Claude Code / OpenClaw 接上 ClawSentry，拦截一次真实的高风险命令
3. **挑战**：用 TrinityGuard 对一个多 Agent 系统（可以是我们的 agent-network 或你自己搭的）做一次完整安全扫描，写出整改建议

然后过一套 5 题的考试（位于网站「考试」Tab），60 分及格。

---

## 常见问题

### Q: 书安 Intern-Shannon 会不会取代 OpenClaw / A3S Code？

不取代，互补。OpenClaw 是面向消费者的多平台 AI 助手，A3S Code 是面向编程 Agent 的框架。**书安是横跨所有 Agent 框架的安全基座**，你可以同时用（例如 OpenClaw 做前端交互 + A3S Box 做后端沙箱 + ClawSentry 做执行监管）。

### Q: 加了书安会不会严重影响性能？

- A3S Box 冷启动 ~200ms，比 Docker 启动还快（macOS 上 Docker 首次启动 1-3s）
- ClawSentry L1 规则 <1ms，几乎零感知
- 只有 L2/L3 才会有几秒延迟，且只针对可疑请求
- SentrySkills 纯 Python 标准库，进程内调用

整体性能损耗可以控制在 **<5%**。

### Q: 我的 Agent 不是 Rust / Python 写的，还能用吗？

可以。AHP 协议本身是 HTTP/JSON 的，任何语言都能发事件给 AHP Harness。AHP v2.3 规范在 [AgentHarnessProtocol](https://github.com/AI45Lab/AgentHarnessProtocol)。

### Q: 书安支持国产化吗？

支持。A3S Box 适配国产芯片生态，A3S-Code 国产化适配，一键私有化部署。

### Q: 开源协议是什么？

6 个 repo 都是 **MIT License**（TrinityGuard 有自己的许可，见 repo）。可以商用，可以闭源二次开发。

### Q: 与 OWASP LLM Top 10 / NIST AI RMF 关系？

ClawSentry 内置的 25+ 攻击模式对齐 OWASP ASI01-ASI05，TrinityGuard 的 20 类风险覆盖了 NIST AI RMF 的主要风险域。这门课学完，可以用书安组件支撑企业的 AI 合规审计。

---

## 参考资源

- 书安 Intern-Shannon 开源组织：https://github.com/AI45Lab
- A3S Box 项目页：https://github.com/AI45Lab/Box
- A3S Code 文档：https://a3s-lab.github.io/a3s/docs/code
- ClawSentry 文档：https://elroyper.github.io/ClawSentry/
- TrinityGuard 论文：https://arxiv.org/abs/2603.15408
- 人工智能安全标准工作组：上海 AI 实验室牵头筹建

---

**下一步**：完成本课后，推荐回头看 OpenClaw（实际应用场景），体会书生（智）+ 书安（安）双螺旋如何协同。
