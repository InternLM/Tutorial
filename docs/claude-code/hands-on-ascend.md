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
conda install -c conda-forge nodejs=22 -y

node --version   # v22.x
npm --version    # 10.x+
```

> 版本建议 22（当前 LTS），如需其他版本：`conda install -c conda-forge nodejs=20`。

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
