# Claude Code 实操 · 曦云 MetaX C500

> 适用于曦云 MetaX C500 GPU（x86_64 Linux，MACA 3.3+）。

## 曦云算力平台（推荐给学员）

🔗 **https://ai.gitee.com/compute**

Gitee AI 提供的曦云 MetaX C500 云上开发环境，预装 MACA + PyTorch，注册后可直接开机。本节命令都在该平台亲测可跑。

如果你有自己的曦云服务器，按同样流程在本机操作即可。

## 前置

- 操作系统：Ubuntu 22.04 x86_64 / CentOS 7+
- GPU：MetaX C500（64GB VRAM）
- 环境：MACA 3.3+

## 第一步：装 Node.js

Gitee AI 曦云开发机默认已有 conda，一行搞定：

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

## 第三步：启动 Claude Code

书生社区的 API 端点原生兼容 Anthropic 协议。**推荐每次启动时临时设环境变量**（不污染 `~/.bashrc`、便于多账号切换）：

```bash
export ANTHROPIC_BASE_URL="https://chat.intern-ai.org.cn"
export ANTHROPIC_AUTH_TOKEN="your-internlm-api-token"

cd your-project
claude --model intern-s1-pro
```

> Token 在 https://community.intern-ai.org.cn 个人中心获取。
>
> 如果你想固化到 shell 配置（不再每次输），把上面 2 行 `export` 加到 `~/.bashrc` 即可。
>
> Claude Code 客户端不感知后端跑在 A100 / 昇腾 / 曦云，行为完全一致。

## 曦云环境特殊点

| 项 | 说明 |
|----|------|
| MACA 兼容 | 曦云提供 CUDA 兼容层，Python 生态大多无修改可跑 |
| 性能 | MetaX C500 与 A100 在多数场景下性能差距 <10% |
| Docker | 曦云提供 MACA 预装镜像，适合快速部署 |
| flash_attn | 原生支持（走 MACA 实现） |

## 下一步

- 回「总览」Tab 学习 MCP / Skills / Hooks
- 走「闯关任务」提交通过证明
