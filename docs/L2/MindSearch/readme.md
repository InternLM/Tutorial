# MindSearch深度解析实践

  <img width="900" alt="img_v3_02h8_f7bf813c-aa3c-4f2b-a007-8d4c6954837g" src="https://github.com/user-attachments/assets/528df2e7-d980-4067-abfd-3c6f05d10c5c">

## 1. 闯关任务

**😀Hello大家好，这节课为大家带来“MindSearch深度解析实践”的课程，课程任务请访问[闯关任务](./task.md)** 

---
## 2. 课程内容

### 2.1 MindSearch 简介

MindSearch 是一个开源的 AI 搜索引擎框架，具有与 Perplexity.ai Pro 相同的性能。我们可以轻松部署它来构建自己的专属搜索引擎，可以基于闭源的LLM（如GPT、Claude系列），也可以使用开源的LLM（如经过专门优化的InternLM2.5 系列模型，能够在MindSearch框架中提供卓越的性能）
最新版的MindSearch拥有以下特性：

- 🤔 任何你想知道的问题：MindSearch 通过搜索解决你在生活中遇到的各种问题
- 📚 深度知识探索：MindSearch 通过数百个网页的浏览，提供更广泛、深层次的答案
- 🔍 透明的解决方案路径：MindSearch 提供了思考路径、搜索关键词等完整的内容，提高回复的可信度和可用性。
- 💻 多种用户界面：为用户提供各种接口，包括 React、Gradio、Streamlit 和本地调试。根据需要选择任意类型。
- 🧠 动态图构建过程：MindSearch 将用户查询分解为图中的子问题节点，并根据 WebSearcher 的搜索结果逐步扩展图。


![output](https://github.com/user-attachments/assets/6f3c649e-a8db-445d-95bc-7f59562ecb8b)



### 2.2 开发环境配置

在入门岛我们已经提到过，想要简单部署到hugging face上，我们需要将开发机平台从InternStudio 替换成 GitHub CodeSpace。且随着硅基流动提供了免费的InternLM2.5-7B-Chat的API服务，大大降低了部署门槛，我们无需GPU资源也可以部署和使用MindSearch，这也是可以利用CodeSpace完成本次实验的原因。
那就让我们一起来看看如何使用硅基流动的API来部署MindSearch吧~

### 2.2.1. 打开codespace主页，选择Blank模板进行创建

<table align="center">
  <tr>
    <td>
        <img src="https://github.com/user-attachments/assets/4b70398d-e378-4753-8f3a-d21643fb268b" alt="Image 1" style="width:100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
    </td>
  </tr>
</table>

### 2.2.2. 创建conda环境隔离并安装依赖

如果只针对于这个实验的话，其实在codespace里面不用单独创建conda环境。但是隔离是一个好习惯，因此我们还是创建一个相应的虚拟环境来隔离

```bash
conda create -n mindsearch python=3.10 -y
conda init
```

如果是新建的codespace，在第一次创建conda环境时，需要conda init，**再另启一个终端并activate** 

```bash
conda activate mindsearch

cd /workspaces/codespaces-blank
git clone https://github.com/InternLM/MindSearch.git && cd MindSearch && git checkout ae5b0c5

pip install -r requirements.txt
```

### 2.3. 获取硅基流动API KEY

因为要使用硅基流动的 API Key，所以接下来便是注册并获取 API Key 了。
首先，我们打开它的[登录界面](https://account.siliconflow.cn/login)来注册硅基流动的账号（如果注册过，则直接登录即可）。
在完成注册后，打开[api key页面](https://cloud.siliconflow.cn/account/ak)来准备 API Key。首先创建新 API 密钥，然后点击密钥进行复制，以备后续使用。

<table align="center">
  <tr>
    <td>
        <img src="https://github.com/user-attachments/assets/a8fbe63e-a5e9-447f-8055-0420e0e16b5e" alt="Image 2" style="width:100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
    </td>
  </tr>
</table>


### 2.4. 启动MindSearch

#### 2.4.1. 启动后端

由于硅基流动 API 的相关配置已经集成在了 MindSearch 中，所以我们在一个终端A中可以直接执行下面的代码来启动 MindSearch 的后端。

```bash
export SILICON_API_KEY=<上面复制的API KEY>
conda activate mindsearch

# 进入你clone的项目目录
cd /workspaces/codespaces-blank/MindSearch
python -m mindsearch.app --lang cn --model_format internlm_silicon --search_engine DuckDuckGoSearch --asy
```

- --lang: 模型的语言，en 为英语，cn 为中文。
- --model_format: 模型的格式。
  - internlm_silicon 为 InternLM2.5-7b-chat 在硅基流动上的API模型
- --search_engine: 搜索引擎。
  - DuckDuckGoSearch 为 DuckDuckGo 搜索引擎。
  - BingSearch 为 Bing 搜索引擎。
  - BraveSearch 为 Brave 搜索引擎。
  - GoogleSearch 为 Google Serper 搜索引擎。
  - TencentSearch 为 Tencent 搜索引擎。

#### 2.4.2. 启动前端

在后端启动完成后，我们打开新终端B运行如下命令来启动 MindSearch 的前端:

```bash
conda activate mindsearch
# 进入你clone的项目目录
cd /workspaces/codespaces-blank/MindSearch
python frontend/mindsearch_gradio.py
```

前后端都启动后，我们应该可以看到github自动为这两个进程做端口转发:

<table align="center">
  <tr>
    <td>
        <img src="https://github.com/user-attachments/assets/daa57d20-ccd2-43b8-a545-a7a4f7a9fa91" alt="Image 3" style="width:100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
    </td>
  </tr>
</table>


如果启动前端后没有自动打开前端页面的话，我们可以手动用7882的端口转发地址打开gradio的前端页面~
然后就可以体验MindSearch gradio版本啦~
比如向其询问："Find legal precedents in contract law." 等待一段时间后，会在页面上输出它的结果。

<table align="center">
  <tr>
    <td>
        <img src="https://github.com/user-attachments/assets/818a668d-7d2b-4ff4-8845-e86b3e6ab895" alt="Image 4" style="width:100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
    </td>
  </tr>
</table>



在这一步中，可能终端会打印报错信息，但是只要前端页面上没有出现报错就行。如果前端页面上出现错误并终止，那么可能是MindSearch 中 searcher 模块的问题。在上面的例子中我们使用的是DuckDuckGoSearch，因此你也可以尝试其他的搜索引擎API。如我们可以替换为BingSearch 或者 TencentSearch 进行尝试。


```bash
# BingSearch
python -m mindsearch.app --lang cn --model_format internlm_silicon --search_engine BingSearch --asy
# TencentSearch
# python -m mindsearch.app --lang cn --model_format internlm_silicon --search_engine TencentSearch --asy
```

## 2.5. 部署到自己的 HuggingFace Spaces上

在之前课程的学习中，我们已经将模型或者应用上传/部署到hugging face上过了。在这里我们介绍一种更简单的方法，它就像克隆一样，无需编写代码即可部署自己的Spaces应用~

首先我们找到InternLM官方部署的[MindSearch Spaces应用](https://huggingface.co/spaces/internlm/MindSearch)


### 2.5.1 选择配置

在该页面的右上角，选择Duplicate this Space

<table align="center">
  <tr>
    <td>
        <img src="https://github.com/user-attachments/assets/c4517ed5-ad7e-4311-83df-7640969bf2c8" alt="Image 5" style="width:100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
    </td>
  </tr>
</table>


选择如下配置后，即可Duplicate Space
- Space Hardware选择第一条，即**Free的2vCPU**即可
- 填写好SILICON_API_KEY，即上面提到的硅基流动的API KEY


<table align="center">
  <tr>
    <td>
        <img src="https://github.com/user-attachments/assets/cdcabbd3-b2ea-47c1-a93d-40590141371b" alt="Image 6" style="width:100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
    </td>
  </tr>
</table>


### 2.5.2 测试结果


等待Spaces应用启动，当启动好后上方会显示绿色的**running**标志，这时我们可以输入input进行测试了，我们可以在Sapces应用页面的输入框中输入以下内容：


```
# input
What are the top 10 e-commerce websites?
```

测试时可能会发现页面卡住了很久（两三分钟），我们可以查看日志，最后两行可能报如下错误：

```bash
graph.add_edge(start_node="root", end_node("contract_enforcement"))
  SyntaxError: positional argument follows keyword argument
```

此时需要在页面右上角选择Restart Space，**待到重启完成后（显示绿色running标志后）再刷新一下网页页面**，再次测试结果如下~

<table align="center">
  <tr>
    <td>
        <img src="https://github.com/user-attachments/assets/2d97faab-6bfb-4a00-9e46-2e261db854fe" alt="Image 6" style="width:100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
    </td>
  </tr>
</table>


至此，我们就完成了MindSearch在Hugging Face上面的部署。课程任务请访问[闯关任务](./task.md)

