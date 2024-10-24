<img width="1440" alt="B站封面" src="https://github.com/user-attachments/assets/200d376f-fe91-4768-9ed6-d9624ede9301">


欢迎参加 InternLM Git 教程！此教程旨在帮助您学习和掌握 Git 版本控制系统的基础知识和操作技能。通过完成一系列任务，您将能够更好地理解 Git 的使用，并应用到实际的项目开发中。

# 关卡任务

以下任务均为**必做任务**，完成任务后提交相应链接即可。

| 任务编号 | 任务名称     | 任务描述                                     | 
|----------|--------------|----------------------------------------------|
| 1        | 破冰活动     | 提交一份自我介绍。                           | 
| 2        | 实践项目     | 创建并提交一个项目。                     |

任务详细参见 [task.md](./task.md)。

Git 的内容相对简单，但也是最为常用的基础。加油！

# Git 是什么
Git 是一种开源的分布式版本控制系统，广泛应用于软件开发领域，尤其是在协同工作环境中。它为程序员提供了一套必备的工具，使得团队成员能够有效地管理和跟踪代码的历史变更。下面是 Git 的主要功能和作用的规范描述：

官网：[https://git-scm.com/](https://git-scm.com/)

官方文档：[Git - Book](https://git-scm.com/book/en/v2)

Git 基础：[Git 基础知识](https://aicarrier.feishu.cn/wiki/YAXRwLZxPi8Hy6k3tOQcuwAHn5g)

## **Git 中的一些基本概念**

**工作区、暂存区和 Git 仓库区**
* 工作区（Working Directory）：
当我们在本地创建一个 Git 项目，或者从 GitHub 上 clone 代码到本地后，项目所在的这个目录就是“工作区”。这里是我们对项目文件进行编辑和使用的地方。

* 暂存区（Staging Area）：
暂存区是 Git 中独有的一个概念，位于 .git 目录中的一个索引文件，记录了下一次提交时将要存入仓库区的文件列表信息。使用 git add 指令可以将工作区的改动放入暂存区。

* 仓库区 / 本地仓库（Repository）：
在项目目录中，.git 隐藏目录不属于工作区，而是 Git 的版本仓库。这个仓库区包含了所有历史版本的完整信息，是 Git 项目的“本体”。

**文件状态**
文件在 Git 工作区中的状态可以是：

* 已跟踪：文件已被纳入版本控制，根据其是否被修改，可以进一步分为未修改（Unmodified）、已修改（Modified）或已暂存（Staged）。
* 未跟踪：文件存在于工作目录中，但还没被纳入版本控制，也未处于暂存状态。

**分支**
分支是 Git 的一大特性，支持轻量级的分支创建和切换。Git 鼓励频繁使用分支和合并，使得并行开发和错误修正更为高效。


**主要功能**

- **代码历史记录跟踪**

   Git 记录每一次代码提交，允许用户查看项目的历史版本和变更记录，从而理解每个阶段的开发细节。

- **团队协作**

   支持多人同时对同一项目工作，提供了合并、分支和版本控制的功能，以确保多人协作的效率和代码的整合性。

- **变更审查**

   允许开发者查看代码变更的具体内容，了解谁在何时做了哪些修改，这对于代码审查和质量控制至关重要。

- **实现机制**

| 特性       | 描述                                                                                                             |
|------------|------------------------------------------------------------------------------------------------------------------|
| 分布式架构 | 与集中式版本控制系统不同，Git 在每个开发者的机器上都存有完整的代码库副本，包括完整的历史记录。这种分布式的特性增强了数据的安全性和获取效率。 |
| 分支管理   | Git 的分支管理功能非常灵活，支持无缝切换到不同的开发线路（分支），并允许独立开发、测试新功能，最终通过合并操作将这些功能稳定地集成到主项目中。      |
| 快照系统   | Git 通过快照而非差异比较来管理数据。每次提交更新时，Git 实际上是在存储一个项目所有文件的快照。如果文件没有变化，Git 只是简单地链接到之前存储的文件快照。 |


## 1. 安装 Git

### 1.1 Windows 系统

1. 下载并安装适合您 Windows 版本的安装程序：[下载地址](https://git-scm.com/download/win)
2. 按照安装向导完成安装。
3. 打开终端（win+r→cmd），输入指令 `git --version` 检查是否安装成功。

### 1.2 Linux 系统

1. 通过包管理器安装 Git：
    ```bash
    sudo apt update
    sudo apt install git
    ```
2. 输入指令 `git --version` 检查安装版本。

## 2. Git 托管平台

[**GitHub**](https://github.com/)：
- 是全球最大的代码托管平台之一，拥有丰富的开源项目和活跃的开发者社区。它提供了版本控制、项目管理、协作开发等功能，并支持多种编程语言。

[**GitLab**](https://gitlab.com/)：
- 一个自托管或基于云的平台，提供了完整的 DevOps 工具链，包括代码托管、持续集成/持续部署（CI/CD）、问题跟踪等。

[**Gitee**](https://gitee.com/)：
- 国内的代码托管平台，提供了代码托管、项目管理、协作开发等功能，对国内开发者来说，访问速度可能更快，也更符合国内的使用习惯。


**Github 需要魔法，可以选择自行选择使用。**

## 3. 常用 Git 操作

**基础指令**

| 指令                     | 描述                                                         |
|--------------------------|--------------------------------------------------------------|
| `git config`             | 配置用户信息和偏好设置                                       |
| `git init`               | 初始化一个新的 Git 仓库                                      |
| `git clone`              | 克隆一个远程仓库到本地                                       |
| `git status`             | 查看仓库当前的状态，显示有变更的文件                         |
| `git add`                | 将文件更改添加到暂存区                                       |
| `git commit`             | 提交暂存区到仓库区                                           |
| `git branch`             | 列出、创建或删除分支                                         |
| `git checkout`           | 切换分支或恢复工作树文件                                     |
| `git merge`              | 合并两个或更多的开发历史                                     |
| `git pull`               | 从另一仓库获取并合并本地的版本                               |
| `git push`               | 更新远程引用和相关的对象                                     |
| `git remote`             | 管理跟踪远程仓库的命令                                       |
| `git fetch`              | 从远程仓库获取数据到本地仓库，但不自动合并                   |

**进阶指令**

| 指令                     | 描述                                                         |
|--------------------------|--------------------------------------------------------------|
| `git stash`              | 暂存当前工作目录的修改，以便可以切换分支                     |
| `git cherry-pick`        | 选择一个提交，将其作为新的提交引入                           |
| `git rebase`             | 将提交从一个分支移动到另一个分支                             |
| `git reset`              | 重设当前 HEAD 到指定状态，可选修改工作区和暂存区             |
| `git revert`             | 通过创建一个新的提交来撤销之前的提交                         |
| `git mv`                 | 移动或重命名一个文件、目录或符号链接，并自动更新索引         |
| `git rm`                 | 从工作区和索引中删除文件                                     |

每个指令都有其特定的用途和场景，详细的使用方法和参数可以通过命令行的帮助文档（`git command -h`,例如 `git pull -h`）来获取更多信息。

## 4. 食用小 tips

### 4.1 全局设置 vs. 本地设置
- **全局设置**：这些设置影响你在该系统上所有没有明确指定其他用户名和电子邮件的 Git 仓库。这是设置默认用户名和电子邮件的好方法。
- **本地设置**：这些设置仅适用于特定的 Git 仓库。这对于你需要在不同项目中使用不同身份时很有用，例如区分个人和工作项目。

### 4.2 如何配置
1. **全局设置用户信息**
   打开终端或命令提示符，并输入以下命令来设置全局用户名和电子邮件地址：
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```
   这里的 `"Your Name"` 和 `"your.email@example.com"` 应替换为你自己的姓名和电子邮件。

2. **本地设置用户信息**
   首先，确保你当前处于你想要配置的 Git 仓库的目录中。然后，输入以下命令来仅为该仓库设置用户名和电子邮件地址：
   ```bash
   git config --local user.name "Your Name"
   git config --local user.email "your.email@example.com"
   ```
   同样，替换 `"Your Name"` 和 `"your.email@example.com"` 为该特定项目中使用的姓名和电子邮件。

### 4.3 验证设置
在设置完用户信息后，你可能想要验证这些设置以确保它们被正确应用。

- **查看全局配置**：
  ```bash
  git config --global --list
  ```

- **查看仓库配置**：
  ```bash
  git config --local --list
  ```

- **查看特定配置项**：
  ```bash
  git config user.name
  git config user.email
  ```

### 4.4 Git 四步曲
在Git的日常使用中，下面四步曲是常用的流程，尤其是在团队协作环境中。

**添（Add）**
- **命令**：`git add <文件名>` 或 `git add .`
- **作用**：将修改过的文件添加到本地暂存区（Staging Area）。这一步是准备阶段，你可以选择性地添加文件，决定哪些修改应该被包括在即将进行的提交中。

**提（Commit）**
- **命令**：`git commit -m '描述信息'`
- **作用**：将暂存区中的更改提交到本地仓库。这一步是将你的更改正式记录下来，每次提交都应附带一个清晰的描述信息，说明这次提交的目的或所解决的问题。

**拉（Pull）**
- **命令**：`git pull`
- **作用**：从远程仓库拉取最新的内容到本地仓库，并自动尝试合并到当前分支。这一步是同步的重要环节，确保你的工作基于最新的项目状态进行。在多人协作中，定期拉取可以避免将来的合并冲突。

**推（Push）**
- **命令**：`git push`
- **作用**：将本地仓库的更改推送到远程仓库。这一步是共享你的工作成果，让团队成员看到你的贡献。

帮助团队成员有效地管理和同步代码，避免工作冲突，确保项目的顺利进行。正确地使用这些命令可以极大地提高开发效率和协作质量。

## 5. 常用插件

- **[GitLens](https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens)**: 在代码行上显示 Git 提交信息。
- **[Git Graph](https://marketplace.visualstudio.com/items?itemName=mhutchie.git-graph)**: 类似于 SourceTree 的可视化版本控制插件。
- **[Git History](https://marketplace.visualstudio.com/items?itemName=donjayamanne.githistory)**: Git 日志查看器。

仅演示常规使用，其他优点，大家可以自行挖掘。
* GitLens：
![GitLens](https://github.com/InternLM/Tutorial/assets/160732778/199f4668-e959-42b6-b4fa-cdc2f0864fcd)

* Git Graph：
![image](https://github.com/InternLM/Tutorial/assets/160732778/ad1e0d59-3b47-48cb-ab5e-d5acaa0a0b25)

* Git History：
![image](https://raw.githubusercontent.com/DonJayamanne/gitHistoryVSCode/main/images/fileHistoryCommandv3.gif)

## 6. 常规开发流程

* **Fork 目标项目**

[目标项目链接](https://github.com/InternLM/Tutorial)

![MXzyb640Ro6S1TxK3lrcpMTLnnb](https://github.com/InternLM/Tutorial/assets/160732778/7a88cbd5-3d53-4e55-97be-137b80944b92)

* **获取仓库链接**

![CWMvb92fFomY4gxsdgrcHw3mneh](https://github.com/InternLM/Tutorial/assets/160732778/bdee8d52-1226-4646-b2b7-b92578f149c9)

```bash
git clone https://github.com/MrCatAI/Tutorial.git # 修改为自己frok的仓库
cd Tutorial/
git branch -a
git checkout -b camp3 origin/camp3
```

* **查看分支**

![XgMvbeKkRojKmXxTqY0cAIwcnqc](https://github.com/InternLM/Tutorial/assets/160732778/3e604f79-f68b-4068-ba85-b06dbc5d9f21)

* **切换到第三期的分支**

![HK41btX6toRdINx8acUc0k4bnLf](https://github.com/InternLM/Tutorial/assets/160732778/d786651e-1506-420d-85cc-a3576b8fe1f0)

* **查看分支内容**

![FmlybnAfZoQ5f2xsdSDc5c5wnJx](https://github.com/InternLM/Tutorial/assets/160732778/8e2528f7-4ee4-4eda-b441-03053f5abac7)

```bash
git checkout -b camp3_577 # 自定义一个新的分支
```

![ED8YbzgA1oZXJdxBegZcl1o0ncy](https://github.com/InternLM/Tutorial/assets/160732778/a8751f86-78e5-4a00-9cbe-6def3ff572d4)

示例：

![I7ZsbQ0MMos1HMxufdaciHV4nMd](https://github.com/InternLM/Tutorial/assets/160732778/30e2b3b9-6091-4c04-90eb-5157691bae59)

示例文件路径

```bash
./data/Git/task/camp3_id.md
```
* **创建自己的破冰文件**

```bash
touch ./data/Git/task/camp3_557.md # 修改为自己的问卷ID
```

![BwGgbkHdLo1jzvxIMxTc0futnub](https://github.com/InternLM/Tutorial/assets/160732778/cbf78959-ed0b-4426-91af-dca75b9fc013)

* **提交更改到分支**

```bash
git add .
git commit -m "add git_557_introduction" # 提交信息记录
```

![E7pybrN2sowPTFxThvmcxHKOnab](https://github.com/InternLM/Tutorial/assets/160732778/898de54d-b8ce-4666-948e-a142ac12aaa4)

```perl
git push origin camp3_577
```

（大家提交使用英文，避免仓库同步错误）

注：初始化时可能需要创建对应的 token：（示例，可根据实际提示完成）

![MKjsbwN3XoVjSGxsWZnc6x4hnCe](https://github.com/InternLM/Tutorial/assets/160732778/bea9600a-21f0-4cbc-8c7f-73fe5769e78b)

![G3hmb6UmzomjJ7xOGZEc4GV0nNb](https://github.com/InternLM/Tutorial/assets/160732778/fae00c0f-6084-44d9-acf7-82fa915c90f9)

![DxoLbxK01ovG88xUHehcnRgXnzT](https://github.com/InternLM/Tutorial/assets/160732778/c8f83c61-2973-4c8a-a9ae-6df3936a67ef)

查看提交

![RaosbM8E7osYsqx8jnIcGkm1n5c](https://github.com/InternLM/Tutorial/assets/160732778/d8a322ec-9a06-4463-a61d-831ef953b1ef)

在 github 页面将修改的内容 PR 到 Tutorial

![TT2NbszJ1oKCorxMWpXcakPUnCd](https://github.com/InternLM/Tutorial/assets/160732778/bef3eac1-e5dc-4699-b8c6-e73066b68fda)

按要求编写 title

```bash
git_557_introduction # 请统一 git_<id>_introduction 格式,方便审核
```

下面可以查看修改的内容

![ZVVOb8NtEowWFQxWFQAcgcoWnQf](https://github.com/InternLM/Tutorial/assets/160732778/6bbc3734-ea3a-46f4-a468-d317ed23227f)

PR 示例链接：[https://github.com/InternLM/Tutorial/pull/790](https://github.com/InternLM/Tutorial/pull/790)

也可以合并到自己的仓库

![LBZibAcS0oArsFxzCLNcY1X2n7e](https://github.com/InternLM/Tutorial/assets/160732778/13a578cf-13be-45a2-81de-4cfab5109770)

自己的仓库，可以自行 merge，作业提交到 Tutorial 需要维护者审核。

![UEl6btxJWo0OHRxcUjRcb9udnNe](https://github.com/InternLM/Tutorial/assets/160732778/72966a46-c634-48a9-9a88-fc6834d957e2)


## 7. 作业

详细请参见 [task.md](./task.md)。

---

我们希望您能在本次 Git 教程中学到有价值的知识，并应用到实际工作中。

加油闯关吧，这只是热身活动，期待你等表现哦。

[GitHub 仓库](https://github.com/InternLM/Tutorial)

