# Claude Code 实操 · NVIDIA A100

> 适用于 NVIDIA A100 / A800 / H100 / H200 以及常规 x86_64 Linux / macOS 开发机。

## 前置

- 操作系统：Ubuntu 22.04+ / macOS 13+ / WSL2
- CPU：x86_64
- Node.js：建议 22 LTS

## 第一步：装 Node.js

```bash
# 方式 A：NodeSource 官方源（Ubuntu/Debian）
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs

# 方式 B：Homebrew（macOS）
brew install node

# 方式 C：conda（跨平台，推荐给已有 conda 的学员）
conda create -n cc -c conda-forge nodejs=22 -y
conda activate cc

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
