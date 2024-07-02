# Git 关卡

# 本节课目标

| 任务1 | 破冰活动：自我介绍     |
| ----- | ---------------------- |
| 任务2 | 实践项目：构建个人项目 |

# Git

是一个开源的分布式版本控制系统，被广泛用于软件协同开发。程序员的必备基础工具。

官网：[https://git-scm.com/](https://git-scm.com/)

官方文档：[Git - Book](https://git-scm.com/book/en/v2)

Git 基础：[Git 基础知识](https://aicarrier.feishu.cn/wiki/YAXRwLZxPi8Hy6k3tOQcuwAHn5g)

## 1. Git 安装

### 1.1 **Windows 系统**

[https://git-scm.com/download/win](https://git-scm.com/download/win)

1. 选择适合您 Windows 版本（32 位或 64 位）的安装程序进行下载。

![](static/Z8c3bDoHeobWXyxnhwVcMpOznSg.png)

2. 在安装向导中，通常可以选择默认设置，一路点击“Next”（下一步）即可完成安装。

![](static/Xo1LbZofZoJyxNxMpqScEW0onFe.png)

3.检查是否安装完成。

打开终端（win+r—>cmd）

输入指令检查 git --version

（已经安装过，暂时不更新啦）

![](static/ImJpbk1qPoZdQyxA1GdcPvcEnHe.png)

### 1.2 **Linux 系统**

通过包管理器安装 Git

```
sudo apt update
sudo apt install git
# _如果使用的 Intern-Studio 可以跳过或去除sudo后执行。默认已安装_
```

1.开机：

随便一台机器，仅测试。

![](static/Vgxfb58tSoCUeqxDS1PcsjUQn2e.png)

2.检查 git 版本

![](static/YSQpbPXWtoAVAqxuhkUcngX2npP.png)

如果没安装，可以按上面的安装教程完成安装。

## 2. 常见的 Git 托管平台

### 2.1 **GitHub**

[https://github.com/](https://github.com/)

- 是全球最大的代码托管平台之一，拥有丰富的开源项目和活跃的开发者社区。它提供了版本控制、项目管理、协作开发等功能，并支持多种编程语言。

### 2.2 **GitLab**

[https://gitlab.com/](https://gitlab.com/)

- 一个自托管或基于云的平台，提供了完整的 DevOps 工具链，包括代码托管、持续集成/持续部署（CI/CD）、问题跟踪等。

### 2.3 **Gitee**

[https://gitee.com/](https://gitee.com/)

- 国内的代码托管平台，提供了代码托管、项目管理、协作开发等功能，对国内开发者来说，访问速度可能更快，也更符合国内的使用习惯。

**Github 需要魔法，没条件的学员可以选择 Gitee 来使用。**

## 3. 常用的 Git 操作

1. `git init`

- 初始化一个新的 Git 仓库，在当前目录创建一个 `.git` 隐藏文件夹来跟踪项目的版本历史。

2. `git clone <repository-url>`

- 从指定的 URL 克隆一个远程仓库到本地。

3. `git add <file>` 或 `git add.`

- 将指定的文件或当前目录下的所有修改添加到暂存区，准备提交。

4. `git commit -m "message"`

- 提交暂存区的修改，并附带一个有意义的提交消息来描述更改的内容。

5. `git status`

- 查看工作目录和暂存区的状态，包括哪些文件被修改、添加或删除。

6. `git log`

- 查看提交历史，包括提交的作者、日期和提交消息。

7. `git branch`

- 列出所有本地分支。

8. `git branch <branch-name>`

- 创建一个新的分支。

9. `git checkout <branch-name>`

- 切换到指定的分支。

10. `git merge <branch-name>`

- 将指定的分支合并到当前分支。

11. `git push`

- 将本地的提交推送到远程仓库。

12. `git pull`

- 从远程仓库拉取最新的更改并合并到本地分支。

13. `git stash`

- 暂存当前未提交的修改，以便在需要时恢复。

14. `git stash pop`

- 恢复最近暂存的修改。

开始一个新的项目时，首先使用 `git init` 初始化仓库。在进行一些代码修改后，使用 `git add.` 添加所有修改，然后使用 `git commit -m "Initial commit"` 提交更改。

在团队工作中，完成自己的开发后，使用 `git push` 将更改推送到远程仓库，以便其他团队成员可以获取您的工作成果。

## 4. 常用插件

在 VSCode 等软件中，插件是效率提升的利器。（根据自己的爱好进行选择）

![](static/KvynbQdSyogfknxSbKccxbMdnjf.png)

| [GitLens](https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens) | 在代码行上显示 Git 提交信息，如提交人、时间及变更描述等，还能查看文件历史记录、比较视图、显示 Git blame 注释和团队成员的最新活动等 |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [Git Graph](https://marketplace.visualstudio.com/items?itemName=mhutchie.git-graph) | 类似于 SourceTree 的可视化版本控制插件，可用于查看提交记录、审视代码等 |
| [Git History](https://marketplace.visualstudio.com/items?itemName=donjayamanne.githistory) | Git 日志查看器，能轻松查看 Git 提交历史记录，支持显示不同颜色的分支、提交信息和更改详细信息，以及搜索提交历史记录； |

# 作业

## 1. 破冰活动：自我介绍

### 任务

提交自己的破冰介绍.md

### 要求

1. 命名 <camp3_<id>.md>
2. 路径：./data/Git/task/
3. 【大家可以叫我】可以为 github 昵称，微信昵称等，或其他网名
4. 作业提交对应的 PR 链接

```
./data/Git/task/camp3_id.md
# id 为报名问卷的ID
```

![](static/XNzebK7ItoftfwxiXQ2cY3lYn0g.png)

（倘若您经常使用，且参与过项目开发，那么下面的操作想必您都熟知，可以迅速跳过。）

**动手操作**

1.查看报名问卷 ID：

[报名问卷](https://www.wjx.cn/vm/PvefmG2.aspx?sojumpparm=MTU3NjczNzE1ODY=)

![](static/XPcwbc8JHopWqRxTsVDc28gQnnc.png)

2.Frok 项目

[项目链接](https://github.com/InternLM/Tutorial)

![](static/MXzyb640Ro6S1TxK3lrcpMTLnnb.png)

3.获取仓库链接

![](static/CWMvb92fFomY4gxsdgrcHw3mneh.png)

```bash
git clone https://github.com/MrCatAI/Tutorial.git _#修改为自己frok的仓库_
cd Tutorial/
git branch -a
git checkout -b camp3 origin/camp3
```

4.查看分支

![](static/XgMvbeKkRojKmXxTqY0cAIwcnqc.png)

5.切换到第三期的分支

![](static/HK41btX6toRdINx8acUc0k4bnLf.png)

6.查看分支内容

![](static/FmlybnAfZoQ5f2xsdSDc5c5wnJx.png)

```bash
git checkout -b camp3_577 _# 自定义一个新的分支_
```

![](static/ED8YbzgA1oZXJdxBegZcl1o0ncy.png)

示例：

![](static/I7ZsbQ0MMos1HMxufdaciHV4nMd.png)

示例文件路径

```bash
./data/Git/task/camp3_id.md
```

7.创建自己的破冰文件

```bash
touch ./data/Git/task/camp3_557.md _#修改为自己的问卷ID_
```

![](static/BwGgbkHdLo1jzvxIMxTc0futnub.png)

8.提交更改到分支

```bash
git add .
git commit -m "add git_557_introduction" _提交信息记录_
```

![](static/E7pybrN2sowPTFxThvmcxHKOnab.png)

```perl
git **push** origin camp3_577
```

（大家提交使用英文，避免仓库同步错误）

注：初始化时可能需要创建对应的 token：（示例，可根据实际提示完成）

![](static/MKjsbwN3XoVjSGxsWZnc6x4hnCe.png)

![](static/G3hmb6UmzomjJ7xOGZEc4GV0nNb.png)

![](static/RTYPbNoCEop6RKxhqcRcFFXanng.png)

提交成功

![](static/DxoLbxK01ovG88xUHehcnRgXnzT.png)

查看提交

![](static/RaosbM8E7osYsqx8jnIcGkm1n5c.png)

在 github 页面将修改的内容 PR 到 Tutorial

![](static/TT2NbszJ1oKCorxMWpXcakPUnCd.png)

按要求编写 title

```bash
git_557_introduction #请统一 git_<id>_introduction 格式,方便审核
```

下面可以查看修改的内容

![](static/ZVVOb8NtEowWFQxWFQAcgcoWnQf.png)

PR 示例链接：[https://github.com/InternLM/Tutorial/pull/790](https://github.com/InternLM/Tutorial/pull/790)

也可以合并到自己的仓库

![](static/LBZibAcS0oArsFxzCLNcY1X2n7e.png)

自己的仓库，可以自行 merge，作业提交到 Tutorial 需要维护者审核。

![](static/UEl6btxJWo0OHRxcUjRcb9udnNe.png)

## 2. 实践项目：构建个人项目（简版）

创建个人仓库，用于提交笔记、心得体会，或分享自己的项目和创意。我们特别欢迎与 LLM 训练和应用相关的内容，但不限于此。

### 任务

创建自己的仓库(拥有自己的仓库，记录笔记与心得

### 要求

1. 拥有自己的项目或笔记仓库（公开）。
2. 提交作业 github 仓库链接（如已经有项目的可以提交项目链接。
3. github 使用少的，可参考下面的操作，提交到常用的其他代码管理平台，如 gitee。
4. 笔记或项目类仓库，添加超链接跳转 [GitHub 仓库](https://github.com/InternLM/Tutorial)（<u>[https://github.com/InternLM/Tutorial](https://github.com/InternLM/Tutorial)</u>）

**动手操作**

1.先在 github 创建一个新的仓库

![](static/GnmablchRoubIgxK7Ioc5JAQndg.png)

![](static/UBRjbS9lBozcUSxJN2IcNKNSn8d.png)

这样你就得到一个空白的仓库：

![](static/QxjXbWeoxoH0VmxhT85cqrZ2nzd.png)

然后按上面的操作，可以拉取仓库和提交对应的信息：

![](static/QLZ9bEOV7oP3iaxHCOycP1J6nje.png)

![](static/F5dNb3S9poBZS4xFdVLcptYgnIe.png)

修改，并记录自己的项目信息等.....

![](static/IFM6bzj6SorSo5xgWj1czZNYnxg.png)

![](static/JFPhbwINBoEDEWxCekHcAVyLnof.png)

修改完后提交到仓库：

![](static/Xq3Eb5LjgoOc5KxP6FJcRsXzned.png)

![](static/IqU8bec1vomQELxE7sCcyKbInq2.png)

![](static/NiN3bCHIaoHh7GxQG6WcEY3Yn9f.png)

参考仓库(仅演示)：[https://github.com/MrCatAI/March7thMuse1](https://github.com/MrCatAI/March7thMuse1)
