# 轻松玩转书生·浦语大模型趣味 Demo

[此处应该是一只Logo] 

作者：那路

PPT 地址：https://1drv.ms/p/s!AlAIlKoW9ghjqUbS6VIDvxF4t-IA?e=QddEep

## 目录

+ 1 **趣味 Demo 任务列表**
+ 2 **实战：通过 `Modelscope` 平台，下载 `InternLM2-Chat-1.8B` 模型进行 `Demo` 部署**
    + 2.1 **初步介绍 Huggingface 平台**
    + 2.2 **配置基础环境**
    + 2.3 **运行 `InternLM2-Chat-1.8B` 模型的 `cli_demo.py`**
+ 3 **实战：通过 `OpenXLab` 部署实战营优秀作品 `八戒-Chat-1.8B` 模型**
    + 3.1 **简单介绍 `八戒-Chat-1.8B`、`Chat-嬛嬛-1.8B`、`Mini-Horo-巧耳`**
    + 3.2 **配置基础环境**
    + 3.3 **使用 `OpenXLab` 下载运行 `八戒-Chat Demo`**
+ 4 **实战：通过 `InternLM2-Chat-7B` 运行 `Lagent` 智能体 `Demo`**
    + 4.1 **初步介绍 `Lagent` 相关知识**
    + 4.2 **配置基础环境**
    + 4.3 **使用 `Lagent` 运行 `InternLM2-Chat-7B` 模型为内核的智能体**
+ 5 **实战：实践部署 `InternLM-XComposer2-7B` 模型**
    + 5.1 **初步介绍 `XComposer` 相关知识**
    + 5.2 **配置基础环境**
    + 5.3 **实现 `浦语·灵笔2` 图文理解创作 `Demo`**
+ 6 **附录**
    + 6.1 **（可选参考）介绍 `pip` 换源及 `conda` 换源方法**

## 1 **趣味 Demo 任务列表**

本节课可以让同学们实践 4 个主要内容，分别是：

- **通过 `Modelscope` 平台，下载 `InternLM2-Chat-1.8B` 模型进行 `Demo` 部署**
- **通过 `OpenXLab` 部署实战营优秀作品 `八戒-Chat-1.8B` 模型**
- **通过 `InternLM2-Chat-7B` 运行 `Lagent` 智能体 `Demo`**
- **实践部署 `InternLM-XComposer2-7B` 模型**

实战营作业被放置于 `homework` 文档，完成课程基础作业可以在后续学习中获得升级算力的机会哦！

## 2 **实战：通过 `Modelscope` 平台，下载 `InternLM2-Chat-1.8B` 模型进行 `Demo` 部署**

### **2.1 初步介绍 Huggingface 平台**

`Modelscope` 是一个开源平台。该平台提供了一个全面的库，其中包括许多预训练的语言模型，如 BERT、RoBERTa、GPT-2 等，这些模型可以用于各种 NLP 任务，如文本分类、命名实体识别、问答系统等。

### **2.2 配置基础环境**
首先，打开 `InternLM Studio` 界面，点击 创建开发机 配置开发机系统。

[图片]

填写 `开发机名称` 后，点击 选择镜像 使用 `Cuda11.7-conda` 镜像，然后在资源配置中，使用 `10% A100 * 1` 的选项，然后立即创建开发机器。

[图片]

点击 `进入开发机` 选项。

[图片]

进入开发机后，在 `terminal` 中输入 `conda` 环境配置命令：

    studio-conda demo

配置完成后，进入到新创建的 conda 环境之中：

    conda activate demo

输入以下命令，完成环境包的安装：

    pip install huggingface-hub==0.17.3
    pip install transformers==4.34 
    pip install psutil==5.9.8
    pip install accelerate==0.24.1
    pip install streamlit==1.32.2 
    pip install matplotlib==3.8.3 
    pip install modelscope==1.9.5