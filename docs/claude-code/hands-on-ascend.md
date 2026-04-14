# Claude Code 实操 · 华为昇腾 Atlas 800T A2

> 适用于华为昇腾 Atlas 800T A2 服务器（aarch64 Linux）。

## 前置

- 操作系统：Ubuntu 22.04 aarch64 / openEuler / Kylin V10
- NPU：Atlas 800T A2（64GB HBM）
- 架构：**aarch64**（用 `uname -m` 确认）

## 第一步：装 Node.js（aarch64 版）

```bash
# 确认架构
uname -m    # 期望输出：aarch64

# 方式 A：NodeSource 源（官方支持 ARM64）
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs

# 方式 B：conda（稳妥）
conda create -n cc -c conda-forge nodejs=22 -y
conda activate cc

# 方式 C：nvm（多版本切换）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
source ~/.bashrc
nvm install --lts
nvm use --lts

node --version
npm --version
```

**离线机器注意**：如果昇腾服务器无公网：
- 先在有网机器上 `npm install -g @anthropic-ai/claude-code` 打包
- 用 rsync 把 `$(npm root -g)/@anthropic-ai` 和全局 bin 软链过去
- 或设国内镜像：`npm config set registry https://registry.npmmirror.com`

## 第二步：装 Claude Code

```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

Claude Code 在 aarch64 上的行为与 x86_64 完全一致，不需要任何特殊编译。

## 第三步：配置模型端点

昇腾版 Intern-S1-Pro 通过 OpenAI 兼容层对外提供服务。配置方式与其他平台一致：

```bash
cat >> ~/.bashrc <<'EOF'
export ANTHROPIC_BASE_URL="https://chat.intern-ai.org.cn/api/v1"
export ANTHROPIC_API_KEY="your-api-key-here"
export ANTHROPIC_MODEL="intern-s1-pro"
EOF
source ~/.bashrc
```

> Claude Code 只是客户端，不直接调 NPU。模型推理跑在服务端 Ascend NPU 上，对客户端完全透明。

## 第四步：首次对话

```bash
cd your-project
claude
```

## 昇腾环境特殊点

| 项 | 说明 |
|----|------|
| CANN 兼容 | Node.js 与 CANN / torch_npu 互不干扰，可在同一环境共存 |
| Python 依赖 | MCP Server 用 Python 时，注意 `pip install` 的包选 aarch64 wheel |
| 性能 | 客户端侧无差异；服务端推理性能取决于具体 Ascend 集群配置 |
| 离线部署 | 见上面的 rsync / npm 镜像方案 |

## 下一步

- 回「总览」Tab 学习 MCP Server 开发、Skills、Hooks
- 走「闯关任务」提交通过证明
