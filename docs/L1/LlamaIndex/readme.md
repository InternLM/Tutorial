# LlamaIndex+InternLM RAG 实践

<img width="900" alt="img_v3_02fn_136796c2-1adb-429b-8c87-276fc43b483g" src="https://github.com/user-attachments/assets/27b038b6-1b0a-4884-a2b8-847b0b0b0bf9">

Hello大家好，迎来到实战营第四期的llamaindex+InternLM RAG课程，本文将分为以下几个部分来介绍，如何使用 LlamaIndex+InternLM 构建 RAG 知识库（以 InternStudio 的环境为例）

- 前置知识
- 浦语API+LlamaIndex实践案例
- 本地部署InternLM+LlamaIndex实践案例
- 闯关任务

## 1. 前置知识

正式介绍检索增强生成（Retrieval Augmented Generation，RAG）技术以前，大家不妨想想为什么会出现这样一个技术。
给模型注入新知识的方式，可以简单分为两种方式，一种是内部的，即更新模型的权重，另一个就是外部的方式，给模型注入格外的上下文或者说外部信息，不改变它的的权重。
第一种方式，改变了模型的权重即进行模型训练，这是一件代价比较大的事情，大语言模型具体的训练过程，可以参考[InternLM2技术报告](https://arxiv.org/abs/2403.17297)。
第二种方式，并不改变模型的权重，只是给模型引入格外的信息。类比人类编程的过程，第一种方式相当于你记住了某个函数的用法，第二种方式相当于你阅读函数文档然后短暂的记住了某个函数的用法。

![image](https://github.com/Shengshenlan/tutorial/assets/57640594/5a72331f-1726-4e4e-9a69-75141cfd313e)

对比两种注入知识方式，第二种更容易实现。RAG 正是这种方式。它能够让基础模型实现非参数知识更新，无需训练就可以掌握新领域的知识。本次课程选用了 LlamaIndex 框架。LlamaIndex 是一个上下文增强的 LLM 框架，旨在通过将其与特定上下文数据集集成，增强大型语言模型（LLMs）的能力。它允许您构建应用程序，既利用 LLMs 的优势，又融入您的私有或领域特定信息。

### RAG 效果比对

如图所示，由于`xtuner`是一款比较新的框架， `InternLM2-Chat-1.8B` 训练数据库中并没有收录到它的相关信息。左图中问答均未给出准确的答案。右图未对 `InternLM2-Chat-1.8B` 进行任何增训的情况下，通过 RAG 技术实现的新增知识问答。

![image](https://github.com/Shengshenlan/tutorial/assets/57640594/3785a449-770a-45e1-a7ea-7cfd33a00076)

## 2. 浦语 API+LlamaIndex 实践

[传送门](./readme_api.md)

## 3. 本地部署InternLM+LlamaIndex实践

[传送门](./readme_local.md)


## 4. 作业

作业请访问[作业](./task.md)。
