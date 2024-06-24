# llamaindex+Internlm2 RAG实践

本文将分为以下几个部分来介绍，如何使用 LlamaIndex 来部署 InternLM2 1.8B（以 InternStudio 的环境为例）
- 前置知识
- 环境、模型准备
- LlamaIndex HuggingFaceLLM
- LlamaIndex RAG

## 1. 前置知识
正式介绍检索增强生成（Retrieval Augmented Generation，RAG）技术以前，大家不妨想想为什么会出现这样一个技术。
给模型注入新知识的方式，可以简单分为两种方式，一种是内部的，即更新模型的权重，另一个就是外部的方式，给模型注入格外的上下文或者说外部信息，不改变它的的权重。
第一种方式，改变了模型的权重即进行模型训练，这是一件代价比较大的事情，大语言模型具体的训练过程，可以参考[InternLM2](https://arxiv.org/abs/2403.17297)技术报告。第二种方式，并不改变模型的权重，只是给模型引入格外的信息。类比人类编程的过程，第一种方式相当于你记住了某个函数的用法，第二种方式相当于你阅读函数文档然后短暂的记住了某个函数的用法。
![image](https://github.com/Shengshenlan/tutorial/assets/57640594/5a72331f-1726-4e4e-9a69-75141cfd313e)
对比两种注入知识方式，第二种更容易实现。RAG正是这种方式。它能够让基础模型实现非参数知识更新，无需训练就可以掌握新领域的知识。本次课程选用了LlamaIndex框架。LlamaIndex 是一个上下文增强的 LLM 框架，旨在通过将其与特定上下文数据集集成，增强大型语言模型（LLMs）的能力。它允许您构建应用程序，既利用 LLMs 的优势，又融入您的私有或领域特定信息。

### RAG 效果比对

如图所示，由于`xtuner`是一款比较新的框架， `InternLM2-Chat-1.8B` 训练数据库中并没有收录到它的相关信息。左图中问答均未给出准确的答案。右图未对 `InternLM2-Chat-1.8B` 进行任何增训的情况下，通过 RAG 技术实现的新增知识问答。
![image](https://github.com/Shengshenlan/tutorial/assets/57640594/3785a449-770a-45e1-a7ea-7cfd33a00076)
## 2. 环境、模型准备
### 2.1 配置基础环境
这里以在 [Intern Studio](https://studio.intern-ai.org.cn/) 服务器上部署LlamaIndex为例。


首先，打开 `Intern Studio` 界面，点击 **创建开发机** 配置开发机系统。
![image](https://github.com/Shengshenlan/tutorial/assets/57640594/e325d0c1-6816-4ea5-ba4a-f509bdd42323)

填写 `开发机名称` 后，点击 选择镜像 使用 `Cuda11.7-conda` 镜像，然后在资源配置中，使用 `30% A100 * 1` 的选项，然后立即创建开发机器。
![image](https://github.com/Shengshenlan/tutorial/assets/57640594/8c25b923-fda8-4af2-a4dc-2f4cf44845c9)

点击 `进入开发机` 选项。
![image](https://github.com/Shengshenlan/tutorial/assets/57640594/6bc3cde2-6309-4e14-9278-a65cd74d4a3a)

进入开发机后，从官方环境复制运行 InternLM 的基础环境，命名为 `llamaindex`，在命令行模式下运行：
```bash
studio-conda -t llamaindex -o pytorch-2.1.2
```
复制完成后，在本地查看环境。
```bash
conda env list
```
结果如下所示。
```bash
# conda environments:
#
base                  *  /root/.conda
llamaindex               /root/.conda/envs/llamaindex
```

运行 `conda` 命令，激活 `llamaindex`    **python** 虚拟环境:
```bash
conda activate llamaindex
```

环境激活后，命令行左边会显示当前（也就是 `llamaindex` ）的环境名称，如下图所示:
![image](https://github.com/Shengshenlan/tutorial/assets/57640594/bcfedc90-0d9d-4679-b1e9-4709b05711f3)

### 2.2 安装 Llamaindex
安装 Llamaindex和相关的包
```bash
conda activate llamaindex
pip install llama-index==0.10.38 llama-index-llms-huggingface==0.2.0 "transformers[torch]==4.41.1" "huggingface_hub[inference]==0.23.1" huggingface_hub==0.23.1 sentence-transformers==2.7.0 sentencepiece==0.2.0
```

### 2.3 下载 Sentence Transformer 模型

源词向量模型 [Sentence Transformer](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2):（我们也可以选用别的开源词向量模型来进行 Embedding，目前选用这个模型是相对轻量、支持中文且效果较好的，同学们可以自由尝试别的开源词向量模型）
运行以下指令，新建一个python文件
```bash
cd ~
mkdir llamaindex_demo
mkdir model
cd ~/llamaindex_demo
touch download_hf.py
```
打开`download_hf.py` 贴入以下代码
```bash
import os

# 设置环境变量
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

# 下载模型
os.system('huggingface-cli download --resume-download sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 --local-dir /root/model/sentence-transformer')
```

然后，在 /root/data 目录下执行该脚本即可自动开始下载：
```bash
conda activate llamaindex
python download_hf.py
```
更多关于镜像使用可以移步至 [HF Mirror](https://hf-mirror.com/) 查看。

2.4 下载 NLTK 相关资源
我们在使用开源词向量模型构建开源词向量的时候，需要用到第三方库 `nltk` 的一些资源。正常情况下，其会自动从互联网上下载，但可能由于网络原因会导致下载中断，此处我们可以从国内仓库镜像地址下载相关资源，保存到服务器上。
我们用以下命令下载 nltk 资源并解压到服务器上：
```bash
cd /root
git clone https://gitee.com/yzy0612/nltk_data.git  --branch gh-pages
cd nltk_data
mv packages/*  ./
cd tokenizers
unzip punkt.zip
cd ../taggers
unzip averaged_perceptron_tagger.zip
```
之后使用时服务器即会自动使用已有资源，无需再次下载

## 3. LlamaIndex HuggingFaceLLM
运行以下指令，把 `InternLM2 1.8B` 软连接出来
```bash
cd ~/model
ln -s /root/share/new_models/Shanghai_AI_Laboratory/internlm2-chat-1_8b/ ./
```
运行以下指令，新建一个python文件
```bash
cd ~/llamaindex_demo
touch llamaindex_internlm.py
```
打开llamaindex_internlm.py 贴入以下代码
```python
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.core.llms import ChatMessage
llm = HuggingFaceLLM(
    model_name="/root/model/internlm2-chat-1_8b",
    tokenizer_name="/root/model/internlm2-chat-1_8b",
    model_kwargs={"trust_remote_code":True},
    tokenizer_kwargs={"trust_remote_code":True}
)

rsp = llm.chat(messages=[ChatMessage(content="xtuner是什么？")])
print(rsp)
```
之后运行
```bash
conda activate llamaindex
cd ~/llamaindex_demo/
python llamaindex_internlm.py
```
结果为：
![image](https://github.com/Shengshenlan/tutorial/assets/57640594/ac3f481d-cc5b-44be-b281-2cab7289f027)
回答的效果并不好，并不是我们想要的xtuner。
## 4. LlamaIndex RAG
安装 `LlamaIndex` 词嵌入向量依赖
```bash
conda activate llamaindex
pip install llama-index-embeddings-huggingface llama-index-embeddings-instructor
```
运行以下命令，获取知识库
```bash
cd ~/llamaindex_demo
mkdir data
cd data
git clone https://github.com/InternLM/xtuner.git
mv xtuner/README_zh-CN.md ./
```
运行以下指令，新建一个python文件
```bash
cd ~/llamaindex_demo
touch llamaindex_RAG.py
```
打开`llamaindex_RAG.py`贴入以下代码
```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.huggingface import HuggingFaceLLM

embed_model = HuggingFaceEmbedding(
    model_name="/root/model/sentence-transformer"
)

Settings.embed_model = embed_model

llm = HuggingFaceLLM(
    model_name="/root/model/internlm2-chat-1_8b",
    tokenizer_name="/root/model/internlm2-chat-1_8b",
    model_kwargs={"trust_remote_code":True},
    tokenizer_kwargs={"trust_remote_code":True}
)
Settings.llm = llm

documents = SimpleDirectoryReader("/root/llamaindex_demo/data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("xtuner是什么?")

print(response)
```
之后运行
```bash
conda activate llamaindex
cd ~/llamaindex_demo/
python llamaindex_RAG.py
```
结果为：
![image](https://github.com/Shengshenlan/tutorial/assets/57640594/8d363e3f-edf9-4573-bd58-5b54fd8981df)

借助RAG技术后，就能获得我们想要的答案了。

## 5. 关卡任务
完成以下任务，并将实现过程记录截图：
- 通过 llamaindex 运行 InternLM2 1.8B，询问“你是谁”，将运行结果截图。
- 通过 llamaindex 实现知识库检索，询问两个问题将运行结果截图。
  - 问题1：xtuner是什么?
  - 问题2：xtuner支持那些模型？

## 6. 关卡通关文案
恭喜你，成功通关本关卡！继续加油！你成功使用 LlamaIndex 运行了 InternLM-2 1.8B 模型，并实现了知识库的构建与检索。这为管理和利用大规模知识库提供了强大的工具和方法。接下来，可以进一步优化和扩展功能，以满足更复杂的需求。
