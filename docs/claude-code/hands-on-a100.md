# Claude Code 实操 · NVIDIA A100

> 适用于 NVIDIA A100 / A800 / H100 / H200 以及常规 x86_64 Linux / macOS 开发机。

## A100 算力平台（推荐给学员）

🔗 **https://studio.intern-ai.org.cn**

书生社区提供的 InternStudio A100 开发环境，预装 CUDA / PyTorch / 常用数据科学包，注册后可直接开机。本节命令都在该平台亲测可跑。

如果你有自己的 A100 / A800 / H 系列服务器，按同样流程在本机操作即可。

## 前置

- 操作系统：Ubuntu 22.04+ / macOS 13+ / WSL2
- CPU：x86_64
- Node.js：建议 22 LTS

## 第一步：装 Node.js

InternStudio A100 开发机默认已有 conda，一行搞定：

```bash
conda install -c conda-forge nodejs=22 -y

node --version   # v22.x
npm --version    # 10.x+
```

## 第二步：装 Claude Code

```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

## 第三步：配置 Intern-S1-Pro 模型（A100 线上端点）

```bash
cat >> ~/.bashrc <<'EOF'
export ANTHROPIC_BASE_URL="https://chat.intern-ai.org.cn/api/v1"
export ANTHROPIC_API_KEY="your-api-key-here"
export ANTHROPIC_MODEL="intern-s1-pro"
EOF
source ~/.bashrc
```

> API Key 从 https://community.intern-ai.org.cn 个人中心获取。

## 第四步：首次对话

```bash
cd your-project
claude
```

进入交互模式后输入：

```
分析当前目录结构，输出每个文件的主要作用
```

## 性能参考（A100 80GB）

- Intern-S1-Pro 单次请求首 token 延迟：~800ms
- 100 token/s 吞吐（BF16）
- 多开 Claude Code session 的并发上限取决于服务端

## 下一步

- 回「总览」Tab 学习 MCP Server 开发、Skills、Hooks 等进阶主题
- 或先做「闯关任务」的基础题
