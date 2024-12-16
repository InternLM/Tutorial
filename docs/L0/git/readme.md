# Git+InternStudio 关卡
<img width="1440" alt="封面" src="https://github.com/random-zhou/ailabImage/blob/main/docimg0.png">

欢迎参加 InternLM Git 教程！此教程旨在帮助您学习和掌握 Git 版本控制系统的基础知识和操作技能。通过完成一系列任务，您将能够更好地理解 Git 的使用，并应用到实际的项目开发中

# 关卡任务

以下任务均为**必做任务**，完成任务后提交相应链接即可。

<table style="width: 100%; margin: auto;">
  <tr>
    <th>任务编号</th>
    <th>任务名称</th>
    <th>任务描述</th>
  </tr>
  <tr>
    <td>1</td>
    <td>破冰活动</td>
    <td>提交一份自我介绍。</td>
  </tr>
  <tr>
    <td>2</td>
    <td>实践项目</td>
    <td>创建并提交一个项目。</td>
  </tr>
</table>

Git 的内容相对简单，但也是最为常用的基础。加油！任务详细参见 [task.md](./task.md)。


## **1. Git 是什么？**

在了解Git是什么之前，我们想要知道我们平时是怎么跟他人合作开发的？我们最传统的策略就是打包压缩然后发送给对方，然后通过上传到网盘或者上传到QQ，又或者通过邮箱传输。

但是这样的方式存在很多问题，比如：

-  效率低下，每次都需要压缩，上传，下载，还要考虑网络问题。
-  无法追踪历史，无法追踪修改，无法追踪谁做了什么修改。
-  无法协作开发，无法多人同时开发。

这时我们就需要能解决以上问题的一个工具而且他需要满足以下的功能：

- 支持多人同时开发, 保证高效有序
- 有一个网络平台能帮我们同步工程开发进度
- 差分增量式更新工程代码, 减少上传下载流量
- 支持历史追踪的版本管理, 便于回溯

Git就是为了解决这些问题而生的，它是一个开源的分布式版本控制系统，可以有效、高速的处理从很小到非常大的项目版本管理。
Git的诞生离不开Linux社区的努力，它是开源的，而且是免费的。它支持多种操作系统，包括 Linux、Unix、Mac OS X、Windows。



## **2. Git 中的一些基本概念**

### **2.1 工作区、暂存区和 Git 仓库区**

* 工作区（Working Directory）：
当我们在本地创建一个 Git 项目，或者从 GitHub 上 clone 代码到本地后，项目所在的这个目录就是“工作区”。这里是我们对项目文件进行编辑和使用的地方。

* 暂存区（Staging Area）：
暂存区是 Git 中独有的一个概念，位于 .git 目录中的一个索引文件，记录了下一次提交时将要存入仓库区的文件列表信息。使用 git add 指令可以将工作区的改动放入暂存区。

* 仓库区 / 本地仓库（Repository）：
在项目目录中，.git 隐藏目录不属于工作区，而是 Git 的版本仓库。这个仓库区包含了所有历史版本的完整信息，是 Git 项目的“本体”。

### **2.2 文件状态**

文件在 Git 工作区中的状态可以是：

* 已跟踪：文件已被纳入版本控制，根据其是否被修改，可以进一步分为未修改（Unmodified）、已修改（Modified）或已暂存（Staged）。
* 未跟踪：文件存在于工作目录中，但还没被纳入版本控制，也未处于暂存状态。


| 状态     | 未跟踪Untrack |未修改Unmodified |已修改Modified |已暂存Staged |
|----------|---------------|-----------------|---------------|--------------|
|说明      |"即新建的文件，并未被git所管理" | "文件的内容没有写入修改，已经被git管理" | "文件的内容被写入修改，已经被git管理" | "文件的内容暂存，已经被git管理"|



### **2.3 分支**

分支是 Git 的一大特性，支持轻量级的分支创建和切换。Git 鼓励频繁使用分支和合并，使得并行开发和错误修正更为高效。


### **2.4 主要功能**

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

## **3. Git 平台介绍**
### **3.1 [**GitHub**](https://github.com/)**

是全球最大的代码托管平台之一，拥有丰富的开源项目和活跃的开发者社区。它提供了版本控制、项目管理、协作开发等功能，并支持多种编程语言。

### **3.2 [**GitLab**](https://gitlab.com/)**

一个自托管或基于云的平台，提供了完整的 DevOps 工具链，包括代码托管、持续集成/持续部署（CI/CD）、问题跟踪等。

### **3.3 [**Gitee**](https://gitee.com/)**

国内的代码托管平台，提供了代码托管、项目管理、协作开发等功能，对国内开发者来说，访问速度可能更快，也更符合国内的使用习惯。


## **4. Git 下载配置验证**
### **4.1 下载 Git**
#### Windows
- 下载并安装适合您 Windows 版本的安装程序：[下载地址](https://git-scm.com/download/win)
- 按照安装向导完成安装。(默认设置安装即可)
- 打开终端（win+r→cmd），输入指令 `git --version` 检查是否安装成功。

#### Linux
- 打开终端，输入指令 
   ```bash
   sudo apt-get install git #安装 Git。
   sudo apt-get update
   sudo apt-get upgrade
   ```
- 输入指令 `git --version` 检查是否安装成功。

### **4.2 配置 Git**

<details>

<summary>全局设置于本地设置的区别：</summary>

**全局设置**：这些设置影响你在该系统上所有没有明确指定其他用户名和电子邮件的 Git 仓库。这是设置默认用户名和电子邮件的好方法。

**本地设置**：这些设置仅适用于特定的 Git 仓库。这对于你需要在不同项目中使用不同身份时很有用，例如区分个人和工作项目。

</details>

#### **全局设置** (要是私人电脑可以直接用全局设置)
   打开终端或命令提示符，并输入以下命令来设置全局用户名和电子邮件地址：
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```
   这里的 `"Your Name"` 和 `"your.email@example.com"` 应替换为你自己的姓名和电子邮件。

#### **本地设置**
   首先，确保你当前处于你想要配置的 Git 仓库的目录中。然后，输入以下命令来仅为该仓库设置用户名和电子邮件地址：
   ```bash
   git config --local user.name "Your Name"
   git config --local user.email "your.email@example.com"
   ```
   同样，替换 `"Your Name"` 和 `"your.email@example.com"` 为该特定项目中使用的姓名和电子邮件。


### **4.3 验证 Git配置**
验证这些设置以确保它们被正确应用。

- **查看全局配置**：
  ```bash
  git config --global --list
  ```

- **查看仓库配置**：
  ```bash
  git config --local --list
  ```

- **永久保存信息至本地**:

   ```bash
   #来设置 Git自动记录密码(token)，从而无需在每次 pull 或 push 时输入# 注意:信息会以明文存储在本地，需考虑安全性
   git config --global credential.helper store
   ```

- **查看特定配置项**：
  ```bash
  git config user.name
  git config user.email
  ```


如图所示


<table align="center">
  <tr>
    <td align="center">
      <img src="https://github.com/random-zhou/ailabImage/blob/main/docimg2_1.png" alt="Description of the image" style="height: auto; width: 500px; margin: 10px auto; padding: 8px 8px 0 8px; border: 1px solid #3f3f3f">
    </td>
  </tr>
</table>


## **5. Git常用操作**

### **5.1 Git简易入门四部曲**
在Git入门当中我们只需要明白一下常用四个指令，即可轻松玩耍

对这四个指令我们可以称为 **"Git 经典四步曲"**

在Git的日常使用中，下面四步曲是常用的流程，尤其是在团队协作环境中。

- **添（Add）**
  - **命令**：`git add <文件名>` 或 `git add .`
  - **作用**：将修改过的文件添加到本地暂存区（Staging Area）。这一步是准备阶段，你可以选择性地添加文件，决定哪些修改应该被包括在即将进行的提交中。

- **提（Commit）**
  - **命令**：`git commit -m '描述信息'`
  - **作用**：将暂存区中的更改提交到本地仓库。这一步是将你的更改正式记录下来，每次提交都应附带一个清晰的描述信息，说明这次提交的目的或所解决的问题。

- **拉（Pull）**
  - **命令**：`git pull`
  - **作用**：从远程仓库拉取最新的内容到本地仓库，并自动尝试合并到当前分支。这一步是同步的重要环节，确保你的工作基于最新的项目状态进行。在多人协作中，定期拉取可以避免将来的合并冲突。

- **推（Push）**
  - **命令**：`git push`
  - **作用**：将本地仓库的更改推送到远程仓库。这一步是共享你的工作成果，让团队成员看到你的贡献。

帮助团队成员有效地管理和同步代码，避免工作冲突，确保项目的顺利进行。正确地使用这些命令可以极大地提高开发效率和协作质量。

### **5.2 Git其他指令**

**常用指令**

<table align="center">
  <tr>
    <th>指令</th>
    <th>描述</th>
  </tr>
  <tr>
    <td><code>git config</code></td>
    <td>配置用户信息和偏好设置</td>
  </tr>
  <tr>
    <td><code>git init</code></td>
    <td>初始化一个新的 Git 仓库</td>
  </tr>
  <tr>
    <td><code>git clone</code></td>
    <td>克隆一个远程仓库到本地</td>
  </tr>
  <tr>
    <td><code>git status</code></td>
    <td>查看仓库当前的状态，显示有变更的文件</td>
  </tr>
  <tr>
    <td><code>git add</code></td>
    <td>将文件更改添加到暂存区</td>
  </tr>
  <tr>
    <td><code>git commit</code></td>
    <td>提交暂存区到仓库区</td>
  </tr>
  <tr>
    <td><code>git branch</code></td>
    <td>列出、创建或删除分支</td>
  </tr>
  <tr>
    <td><code>git checkout</code></td>
    <td>切换分支或恢复工作树文件</td>
  </tr>
  <tr>
    <td><code>git merge</code></td>
    <td>合并两个或更多的开发历史</td>
  </tr>
  <tr>
    <td><code>git pull</code></td>
    <td>从另一仓库获取并合并本地的版本</td>
  </tr>
  <tr>
    <td><code>git push</code></td>
    <td>更新远程引用和相关的对象</td>
  </tr>
  <tr>
    <td><code>git remote</code></td>
    <td>管理跟踪远程仓库的命令</td>
  </tr>
  <tr>
    <td><code>git fetch</code></td>
    <td>从远程仓库获取数据到本地仓库，但不自动合并</td>
  </tr>
</table>

**进阶指令**

<table align="center">
  <tr>
    <th>指令</th>
    <th>描述</th>
  </tr>
  <tr>
    <td><code>git stash</code></td>
    <td>暂存当前工作目录的修改，以便可以切换分支</td>
  </tr>
  <tr>
    <td><code>git cherry-pick</code></td>
    <td>选择一个提交，将其作为新的提交引入</td>
  </tr>
  <tr>
    <td><code>git rebase</code></td>
    <td>将提交从一个分支移动到另一个分支</td>
  </tr>
  <tr>
    <td><code>git reset</code></td>
    <td>重设当前 HEAD 到指定状态，可选修改工作区和暂存区</td>
  </tr>
  <tr>
    <td><code>git revert</code></td>
    <td>通过创建一个新的提交来撤销之前的提交</td>
  </tr>
  <tr>
    <td><code>git mv</code></td>
    <td>移动或重命名一个文件、目录或符号链接，并自动更新索引</td>
  </tr>
  <tr>
    <td><code>git rm</code></td>
    <td>从工作区和索引中删除文件</td>
  </tr>
</table>

每个指令都有其特定的用途和场景，详细的使用方法和参数可以通过命令行的帮助文档（`git command -h`,例如 `git pull -h`）来获取更多信息。


## **6. Git使用流程**

### **6.1 先注册一个github账号**

本次学习项目的链接：
https://github.com/InternLM/Tutorial/tree/camp4

<table align="center">
  <tr>
    <td align="center">
      <img src="https://github.com/random-zhou/ailabImage/blob/main/docimg2.png" alt="Description of the image" style="height: auto; width: 800px; margin: 10px auto; padding: 8px 8px 0 8px; border: 1px solid #3f3f3f">
    </td>
  </tr>
</table>


### **6.2 将本项目直接fork到自己的账号下，这样就可以直接在自己的账号下进行修改和提交。**

<table align="center">
  <tr>
    <td align="center">
      <img src="https://github.com/random-zhou/ailabImage/blob/main/docimg3.jpg" alt="Description of the image" style="height: auto; width: 800px; margin: 10px auto; padding: 8px 8px 0 8px; border: 1px solid #3f3f3f">
    </td>
  </tr>
</table>  

### **注意取消勾选仅克隆当前分支**
<table align="center">
  <tr>
    <td align="center">
      <img src="https://github.com/Jun-Howie/AIPPT-for-InternLM/blob/main/images/fork.png" alt="Description of the image" style="height: auto; width: 800px; margin: 10px auto; padding: 8px 8px 0 8px; border: 1px solid #3f3f3f">
    </td>
  </tr>
</table>

<table align="center">
  <tr>
    <td align="center">
      <img src="https://github.com/Jun-Howie/AIPPT-for-InternLM/blob/main/images/branch.png" alt="Description of the image" style="height: auto; width: 800px; margin: 10px auto; padding: 8px 8px 0 8px; border: 1px solid #3f3f3f">
    </td>
  </tr>
</table>


<table align="center">
  <tr>
    <td align="center">
      <img src="https://github.com/Jun-Howie/AIPPT-for-InternLM/blob/main/images/download.png" alt="Description of the image" style="height: auto; width: 800px; margin: 10px auto; padding: 8px 8px 0 8px; border: 1px solid #3f3f3f">
    </td>
  </tr>
</table>


### **6.3 配置git并克隆项目到InternStudio本地**

```bash
# 修改为自己fork的仓库，改为上图中你的https仓库的git地址,将random-zhou改为自己的用户名
git clone https://github.com/random-zhou/Tutorial.git 
#git clone git@github.com:random-zhou/Tutorial.git 
#git clone https://github.com/InternLM/Tutorial.git
cd Tutorial/
git branch -a
git checkout -b class origin/class
```
如图所示


<table align="center">
  <tr>
    <td align="center">
      <img src="https://github.com/random-zhou/ailabImage/blob/main/image.png" alt="Description of the image" style="height: auto; width: 600px; margin: 10px auto; padding: 8px 8px 0 8px; border: 1px solid #3f3f3f">
    </td>
  </tr>
</table>


### **6.4 创建分支**
```bash
git checkout -b class_036 # 自定义一个新的分支
#git checkout -b class_id 分支名字改为你的uid分支名称
```

<table align="center">
   <tr>
    <td align="center">
      <img src="https://github.com/random-zhou/ailabImage/blob/main/image-1.png" alt="Description of the image" style="height: auto; width: 700px; margin: 10px auto; padding: 8px 8px 0 8px; border: 1px solid #3f3f3f">
    </td>
      <td align="center">
      <img src="https://github.com/random-zhou/ailabImage/blob/main/image-2.png" alt="Description of the image" style="height: auto; margin: 10px auto; padding: 8px 8px 0 8px; border: 1px solid #3f3f3f">
    </td>
  </tr>
</table>


### **6.5 创建自己的介绍文件**

这里提供了介绍文件的模板（路径 `./icamp4/id.md`）
```bash
【大家可以叫我】:InternLM
【坐标】:上海
【专业/职业】:小助手
【兴趣爱好】:乒乓球
【项目技能】:cv、nlp
【组队情况】:未组队，快来一起!
【本课程学习基础】:CV、NLP、LLM
【本期活动目标】:一起学习，快乐暑假，闯关达人!
```
> 注意，在GitHub中需要再每一行的后面多打几个空格才能换行

<table align="center">
   <tr>
    <td align="center">
      <img src="https://github.com/random-zhou/ailabImage/blob/main/image-3.jpg" alt="Description of the image" style="height: 200px;  margin: 10px auto; padding: 8px 8px 0 8px; border: 1px solid #3f3f3f">
    </td>
      <td align="center">
      <img src="https://github.com/random-zhou/ailabImage/blob/main/image-4.jpg" alt="Description of the image" style="height: 200px; margin: 10px auto; padding: 8px 8px 0 8px; border: 1px solid #3f3f3f">
    </td>
  </tr>
   <tr>
    <td align="center">
      示例文件
    </td>
      <td align="center">
      将id号改为自己的报名uid
    </td>
  </tr>
</table>



### **6.6 提交更改分支**

```bash
git add .
git commit -m "add git_camp4_036_introduction" # 提交信息记录,这里需要修改为自己的uid
```

<table align="center">
  <tr>
    <td align="center">
      <img src="https://github.com/random-zhou/ailabImage/blob/main/image-5.png" alt="Description of the image" style="height: auto; width: 600px; margin: 10px auto; padding: 8px 8px 0 8px; border: 1px solid #3f3f3f">
    </td>
  </tr>
</table>



### **6.7 推送分支到远程仓库**
```bash
git push origin class_036
#注意，这里要改为你自己的分支名称
#大家提交使用英文，避免同步错误
```
<table align="center">
  <tr>
    <td align="center">
      <img src="https://github.com/random-zhou/ailabImage/blob/main/image-6.png" alt="Description of the image" style="height: auto; width: 600px; margin: 10px auto; padding: 8px 8px 0 8px; border: 1px solid #3f3f3f">
    </td>
  </tr>
</table>


<details>
<summary>第一次推送时需要登录github授权，会出现以下两个提醒，点击去github登录授权即可。</summary>


<table align="center">
  <tr>
    <td align="center">
      <img src="https://github.com/random-zhou/ailabImage/blob/main/image-7.png" alt="Description of the image" style="height: 150px;  margin: 10px auto; padding: 8px 8px 0 8px; border: 1px solid #3f3f3f">
    </td>
     <td align="center">
      <img src="https://github.com/random-zhou/ailabImage/blob/main/image-8.png" alt="Description of the image" style="height: 150px; margin: 10px auto; padding: 8px 8px 0 8px; border: 1px solid #3f3f3f">
    </td>
  </tr>
   <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/19e0f320-8fe9-46b2-b58d-c574b653fe34" alt="Description of the image" style="height: 150px; margin: 10px auto; padding: 8px 8px 0 8px; border: 1px solid #3f3f3f">
    </td>
      <td align="center">
      <img src="https://github.com/user-attachments/assets/ae341025-62be-41c4-87ce-9e1da6cbcf1f" alt="Description of the image" style="height: 150px;  margin: 10px auto; padding: 8px 8px 0 8px; border: 1px solid #3f3f3f">
    </td>
  </tr>
</table>






验证完成即可

</details>

### **6.8 检查提交内容**
如图所示，可以看到你的分支已经被推送到远程仓库。

<table align="center">
  <tr>
    <td align="center">
      <img src="https://github.com/random-zhou/ailabImage/blob/main/image-11.png" alt="Description of the image" style="height: auto; width: 600px; margin: 10px auto; padding: 8px 8px 0 8px; border: 1px solid #3f3f3f">
    </td>
  </tr>
</table>


点击右上角Compare & pull request

<table align="center">
  <tr>
    <td align="center">
      <img src="https://github.com/random-zhou/ailabImage/blob/main/image-12.png" alt="Description of the image" style="height: auto; width: 600px; margin: 10px auto; padding: 8px 8px 0 8px; border: 1px solid #3f3f3f">
    </td>
  </tr>
</table>

在“Add a title中”输入 "add git_< id >_introduction",将

<table align="center">
  <tr>
    <td align="center">
      <img src="https://github.com/random-zhou/ailabImage/blob/main/image-13.png" alt="Description of the image" style="height: auto; width: 600px; margin: 10px auto; padding: 8px 8px 0 8px; border: 1px solid #3f3f3f">
    </td>
  </tr>
</table>


```bash
git_036_introduction # 请统一 改为git_<id>_introduction 格式,方便审核

```

请按要求填写相关title，方便审核。然后点击“Create pull request”

在当前页面下方可以看到内容变更，+号代表在当前行号下增加内容，-号代表在当前行号下删除内容。

提交后如下

<table align="center">
  <tr>
    <td align="center">
      <img src="https://github.com/random-zhou/ailabImage/blob/main/image-15.png" alt="Description of the image" style="height: auto; width: 600px; margin: 10px auto; padding: 8px 8px 0 8px; border: 1px solid #3f3f3f">
    </td>
  </tr>
</table>

管理员审核合并之后如下所示

<table align="center">
  <tr>
    <td align="center">
      <img src="https://github.com/random-zhou/ailabImage/blob/main/image-18.png" alt="Description of the image" style="height: auto; width: 600px; margin: 10px auto; padding: 8px 8px 0 8px; border: 1px solid #3f3f3f">
    </td>
  </tr>
</table>

具体如下

<table align="center">
  <tr>
    <td align="center">
      <img src="https://github.com/random-zhou/ailabImage/blob/main/image-19.png" alt="Description of the image" style="height: auto; width: 600px; margin: 10px auto; padding: 8px 8px 0 8px; border: 1px solid #3f3f3f">
    </td>
  </tr>
</table>

如果出现发现提交时未有换行，可以回到6.5 章节的注意，根据注意事项修改一下再提交就好啦



## **7. 作业**
- 完成任务1：提交一份自我介绍。
- 完成任务2：创建并提交一个项目。
- 详见[task.md](./task.md)

## **8. Git结束语**
恭喜你完成了Git的学习，接下来可以尝试更多的项目，学习更多的知识。从这里开始，你将步入大模型的世界！

返回点击
[书生大模型实战营](https://github.com/InternLM/Tutorial/tree/camp4)

https://github.com/InternLM/Tutorial/tree/class/icamp4
