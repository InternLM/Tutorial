# Git 课程任务

**守关者：**

请按照指定步骤迅速完成任务，并将完成的链接提交至飞书。完成后，您将获得50算力奖励。保持活跃，抓紧时间完成任务，以便算力奖励尽快到账。完成更多任务后，您还有机会解锁更高级的机器，开启更广阔的探索之旅！前行吧，年轻的书生，每一步都是向着未来的大步迈进！


## 任务概览

- **任务1**: 破冰活动：自我介绍
- **任务2**: 实践项目：构建个人项目

---

## 任务1: 破冰活动：自我介绍

### 目标

每位参与者提交一份自我介绍。

![XNzebK7ItoftfwxiXQ2cY3lYn0g](https://github.com/InternLM/Tutorial/assets/160732778/bb74cc07-e806-4d17-9dbc-cca2890a9230)

### 要求

1. **文件命名格式**: `camp3_<id>.md`，其中 `<id>` 是您的报名问卷 ID。
2. **文件路径**: `./data/Git/task/`。
3. **介绍内容**: 【大家可以叫我】可使用 GitHub 昵称、微信昵称或其他网名。
4. **提交方式**: 在 GitHub 上创建一个 Pull Request，并提供对应的 PR 链接。

### 步骤

1. 查看报名问卷 ID：[报名问卷](https://www.wjx.cn/vm/PvefmG2.aspx?sojumpparm=MTU3NjczNzE1ODY=)
   
2. Fork 项目：[项目链接](https://github.com/InternLM/Tutorial)
   
3. 获取仓库链接：

    ```bash
    git clone https://github.com/您的用户名/Tutorial.git
    cd Tutorial/
    git checkout -b camp3 origin/camp3
    ```

4. 创建自己的破冰文件：

    ```bash
    touch ./data/Git/task/camp3_<id>.md  # 修改为您的问卷 ID
    ```

5. 提交更改到分支：

    ```bash
    git add .
    git commit -m "add git_<id>_introduction"  # 提交信息记录
    git push origin camp3_<id>  # 修改为您的分支名
    ```

6. 在 GitHub 页面将修改的内容 PR 到 Tutorial：

    - PR 标题格式: `git_<id>_introduction`

---

## 任务2: 实践项目：构建个人项目

### 目标

创建一个个人仓库，用于提交笔记、心得体会或分享项目。

![NiN3bCHIaoHh7GxQG6WcEY3Yn9f](https://github.com/InternLM/Tutorial/assets/160732778/c76691e7-eb21-435f-a0ed-4a6b62e569e4)

### 要求

1. 创建并维护一个公开的项目或笔记仓库。
2. 提交作业时，提供您的 GitHub 仓库链接。
3. 不常使用 GitHub 的学员可以选择其他代码管理平台，如 Gitee，并提交相应的链接。
4. 仓库介绍中添加超链接跳转 [GitHub 仓库](https://github.com/InternLM/Tutorial)（<u>[https://github.com/InternLM/Tutorial](https://github.com/InternLM/Tutorial)</u>）

### 步骤

1. 在 GitHub 创建一个新的仓库：

    ![GnmablchRoubIgxK7Ioc5JAQndg](https://github.com/InternLM/Tutorial/assets/160732778/10978930-88cc-4927-afdb-e494031dfd4f)
   
   **（自行构建的仓库可以自行选择公开的还是私有的仓库，本次任务需要的是公开的哦）**
    
    ![UBRjbS9lBozcUSxJN2IcNKNSn8d](https://github.com/InternLM/Tutorial/assets/160732778/05fe7cda-d103-42e9-b2d3-b74e6093c40a)

3. 拉取仓库并提交对应的信息：

    ```bash
    git clone https://github.com/您的用户名/新建的仓库名.git
    cd 新建的仓库名/
    touch README.md
    # 编辑 README.md 文件，添加项目信息等
    git add .
    git commit -m "Initial commit"
    git push origin main
    ```

参考仓库(仅演示): [https://github.com/MrCatAI/March7thMuse1](https://github.com/MrCatAI/March7thMuse1)

---

**守关者：**

完成任务后，请记得向助教大大报告，领取您的算力奖励。再次提醒，保持积极，勇敢地迈出每一步，未来还有更多高级机器等着您去解锁和探索！加油，闯关者！
