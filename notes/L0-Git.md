| 任务  | 任务描述              |
| ----- | -------------------  |
| 任务1 | 破冰活动：自我介绍     |
| 任务2 | 实践项目：构建个人项目 |

# 介绍
## 1. **Git**

是一个开源的分布式版本控制系统，被广泛用于软件协同开发。程序员的必备基础工具。
官网：https://git-scm.com/
官方文档：[Git - Book](https://git-scm.com/book/en/v2)
Git 基础：[Git 基础知识](https://aicarrier.feishu.cn/wiki/YAXRwLZxPi8Hy6k3tOQcuwAHn5g)

## 2. **Git 安装**

Windows 系统
https://git-scm.com/download/win

Linux 系统
`sudo apt update & sudo apt install git`

## 3. **常用的 Git 操作**

| 命令 | 命令描述 |
| :---- | :------- |
| **git init** | 初始化一个新的 Git 仓库，在当前目录创建一个 .git 隐藏文件夹来跟踪项目的版本历史。
| **git clone \<repository-url>** | 从指定的 URL 克隆一个远程仓库到本地。
| **git add \<file>** 或 **git add .** | 将指定的文件或当前目录下的所有修改添加到暂存区，准备提交。
| **git commit -m "message"** | 提交暂存区的修改，并附带一个有意义的提交消息来描述更改的内容。
| **git status** | 查看工作目录和暂存区的状态，包括哪些文件被修改、添加或删除。
| **git log** | 查看提交历史，包括提交的作者、日期和提交消息。
| **git branch** | 列出所有本地分支。
| **git branch \<branch-name>** | 创建一个新的分支。
| **git checkout \<branch-name>** | 切换到指定的分支。
| **git merge \<branch-name>** | 将指定的分支合并到当前分支。
| **git push** | 将本地的提交推送到远程仓库。
| **git pull** | 从远程仓库拉取最新的更改并合并到本地分支。
| **git stash** | 暂存当前未提交的修改，以便在需要时恢复。
| **git stash pop** | 恢复最近暂存的修改。


# 作业
## 1. 破冰活动：自我介绍

> 提交自己的破冰介绍.md
> 要求：
>  1. 命名camp3_1080.md
>  2. 路径：./data/Git/task/
>  3. 作业提交对应的PR链接
https://github.com/InternLM/Tutorial/pull/818

![image](https://img2024.cnblogs.com/blog/1664152/202407/1664152-20240709150011705-1343173370.png)

**注意：** 取消copy camp1 brach only

```
git clone https://github.com/huaibovip/Tutorial.git
cd Tutorial/
git branch -a
git checkout -b camp3 origin/camp3
git checkout -b camp3_1080 #自定义一个新的分支

touch ./data/Git/task/camp3_1080.md #修改为自己的问卷ID
git add .
git commit -m "add git_1080_introduction" #提交信息记录
git push origin camp3_1080
```

![image](https://img2024.cnblogs.com/blog/1664152/202407/1664152-20240709150334710-1440292661.png)

## 2. 实践项目：构建个人项目（简版）

>   创建自己的仓库(拥有自己的仓库，记录笔记与心得
> 要求：
>   1. 拥有自己的项目或笔记仓库（公开）。
>   2. 提交作业 github 仓库链接（如已经有项目的可以提交项目链接。
>   3. github 使用少的，可参考下面的操作，提交到常用的其他代码管理平台，如gitee。
>   4. 笔记或项目类仓库，添加超链接跳转GitHub 仓库（https://github.com/InternLM/Tutorial）
