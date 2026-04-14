# Claude Code 实操 · 沐曦 MetaX C500

> 适用于沐曦 MetaX C500 GPU（x86_64 Linux，MACA 3.3+）。

## 前置

- 操作系统：Ubuntu 22.04 x86_64 / CentOS 7+
- GPU：MetaX C500（64GB VRAM）
- 环境：MACA 3.3+

## 第一步：装 Node.js

沐曦平台与标准 x86_64 一致，所有 Node.js 安装方式都适用：

```bash
# 方式 A：NodeSource 源
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs

# 方式 B：conda
conda create -n cc -c conda-forge nodejs=22 -y
conda activate cc

node --version
npm --version
```

## 第二步：装 Claude Code

```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

## 第三步：配置模型端点

```bash
cat >> ~/.bashrc <<'EOF'
export ANTHROPIC_BASE_URL="https://chat.intern-ai.org.cn/api/v1"
export ANTHROPIC_API_KEY="your-api-key-here"
export ANTHROPIC_MODEL="intern-s1-pro"
EOF
source ~/.bashrc
```

> 同样通过 OpenAI 兼容层对接。Claude Code 客户端不感知后端是 A100 / Ascend 还是 MetaX。

## 第四步：首次对话

```bash
cd your-project
claude
```

## 沐曦环境特殊点

| 项 | 说明 |
|----|------|
| MACA 兼容 | 沐曦提供 CUDA 兼容层，Python 生态大多无修改可跑 |
| 性能 | MetaX C500 与 A100 在多数场景下性能差距 <10% |
| Docker | 沐曦提供 MACA 预装镜像，适合快速部署 |
| flash_attn | 原生支持（走 MACA 实现） |

## 下一步

- 回「总览」Tab 学习 MCP / Skills / Hooks
- 走「闯关任务」提交通过证明
