# Git Tutorial

欢迎参加 InternLM Git 教程项目！本项目旨在帮助您学习和掌握 Git 版本控制系统的基础知识和操作技能。通过完成一系列任务，您将能够更好地理解 Git 的使用，并应用到实际的项目开发中。

## 目录

- [项目简介](#项目简介)
- [安装 Git](#安装-git)
- [Git 托管平台](#git-托管平台)
- [常用 Git 操作](#常用-git-操作)
- [常用插件](#常用插件)
- [任务](#任务)

## 项目简介

本项目包含两项主要任务：
1. 破冰活动：提交一份自我介绍。
2. 实践项目：创建并提交一个个人项目。

详细的任务说明请参见 [task.md](./task.md)。

## 安装 Git

### Windows 系统

1. 下载并安装适合您 Windows 版本的安装程序：[下载地址](https://git-scm.com/download/win)
2. 按照安装向导完成安装。
3. 打开终端（win+r→cmd），输入指令 `git --version` 检查是否安装成功。

### Linux 系统

1. 通过包管理器安装 Git：
    ```bash
    sudo apt update
    sudo apt install git
    ```
2. 输入指令 `git --version` 检查安装版本。

## Git 托管平台

- **GitHub**: [https://github.com/](https://github.com/)
- **GitLab**: [https://gitlab.com/](https://gitlab.com/)
- **Gitee**: [https://gitee.com/](https://gitee.com/)

## 常用 Git 操作

| 命令 | 描述 |
|------|------|
| `git init` | 初始化一个新的 Git 仓库。 |
| `git clone <repository-url>` | 从指定的 URL 克隆一个远程仓库到本地。 |
| `git add <file>` 或 `git add .` | 将指定的文件或当前目录下的所有修改添加到暂存区。 |
| `git commit -m "message"` | 提交暂存区的修改，并附带一个有意义的提交消息。 |
| `git status` | 查看工作目录和暂存区的状态。 |
| `git log` | 查看提交历史。 |
| `git branch` | 列出所有本地分支。 |
| `git branch <branch-name>` | 创建一个新的分支。 |
| `git checkout <branch-name>` | 切换到指定的分支。 |
| `git merge <branch-name>` | 将指定的分支合并到当前分支。 |
| `git push` | 将本地的提交推送到远程仓库。 |
| `git pull` | 从远程仓库拉取最新的更改并合并到本地分支。 |
| `git stash` | 暂存当前未提交的修改。 |
| `git stash pop` | 恢复最近暂存的修改。 |

## 常用插件

- **GitLens**: 在代码行上显示 Git 提交信息。
- **Git Graph**: 类似于 SourceTree 的可视化版本控制插件。
- **Git History**: Git 日志查看器。

## 任务

### 破冰活动：自我介绍

1. 创建自我介绍文件，命名为 `camp3_<id>.md`，其中 `<id>` 为报名问卷的 ID。
2. 将文件放置在路径 `./data/Git/task/` 下。
3. 提交自我介绍的 PR 链接。

详细步骤请参见 [task.md](./task.md)。

### 实践项目：构建个人项目

1. 创建个人仓库，用于提交笔记、心得体会，或分享自己的项目和创意。
2. 提交您的 GitHub 仓库链接。

详细步骤请参见 [task.md](./task.md)。

---

我们希望您能在本次 Git 教程中学到有价值的知识，并应用到实际工作中。

加油闯关吧，这只是热身活动，期待你等表现哦。

[GitHub 仓库](https://github.com/InternLM/Tutorial)

