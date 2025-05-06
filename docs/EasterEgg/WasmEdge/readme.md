
# InternLM+WasmEdge 部署智能体实践

# **开发者文档**

## **1. 课程简介**

### **1.1 背景介绍**

**讲师介绍**: Miley Fu，WasmEdge Runtime 创始成员，CNCF 大使，2024年8月当选为 Linux 基金会 KubeCon、开源峰会和 AI Dev 大会联合主席。  
[**WasmEdge**](https://github.com/WasmEdge/WasmEdge): 一个开源的 WebAssembly 运行时/容器，是CNCF基金会下面的项目，支持多种语言编写的 AI 应用跨平台运行，包括跨CPU GPU 和操作系统。支持各大开源大模型，包括多模态模型。支持多种底层架构/硬件。  
[**Gaia**](https://github.com/GaiaNet-AI/gaianet-node/blob/main/README.md): 基于WasmEdge的一套软件，允许一键在本地设备或云端运行大模型节点，生成兼容 OpenAI API 的 URL，支持自定义知识库。  
[**internlm2_5-7b-chat 模型**](huggingface.co/internlm/internlm2_5-7b-chat): 上海人工智能实验室开源的大模型，引入了一个70亿参数的基础模型以及一个为实际应用设计的聊天模型。

### **1.2 课程目标**

学员能够通过 WasmEdge 本地运行 InternLM，快速搭建与 Obsidian 笔记软件上的AI应用，或构建其他 AI 智能体。

## **2. 准备工作**

### **2.1 安装环境**

**安装 Gaia 软件**:   
下载并安装 Gaia。  
[_https://docs.gaianet.ai/node-guide/quick-start/_](https://docs.gaianet.ai/node-guide/quick-start/)   
**下载 InternLM 2.5 7B 模型**:     
从 Hugging Face 下载 InternLM 模型。  
[_https://huggingface.co/second-state/internlm2_5-7b-chat-GGUF/resolve/main/internlm2_5-7b-chat-Q5_K_M.gguf_](https://huggingface.co/second-state/internlm2_5-7b-chat-GGUF/resolve/main/internlm2_5-7b-chat-Q5_K_M.gguf)   
**安装 Obsidian**:   
下载并安装 Obsidian 笔记软件。  
[_https://obsidian.md/download_](https://obsidian.md/download)   

### **2.2 硬件配置**

**推荐配置**: Mac 16GB 内存、英伟达 GPU、华为昇腾 NPU 等。  
**最低配置**: 16GB 内存的机器。  

## **3. 使用 Gaia 部署 InternLM**

### **3.1 安装 Gaia 节点**

运行以下命令行安装 Gaia 节点：
```
curl -sSfL 'https://github.com/GaiaNet-AI/gaianet-node/releases/latest/download/install.sh' | bash
```  
这个命令行会下载向量数据库、 LlamaEdge API server 和默认的大模型（ Llama）

### **3.2 初始化 Gaia 节点**

初始化节点：`gaianet init`  
启动节点：`gaianet start`  
启动后，将生成一个公开的 OpenAI 兼容的 API URL。  
[https://0x8d2643381194979502cb2b542c7bd8bb5418408C.us.gaianet.network](https://0x8d2643381194979502cb2b542c7bd8bb5418408c.us.gaianet.network/)

### **3.3 测试 API**

使用 `curl` 命令测试 API 是否正常运行：
```
curl -X POST https://0x8d2643381194979502cb2b542c7bd8bb5418408c.us.gaianet.network/v1/models
```
确认返回的模型信息是否正确：
```json
{"object":"list","data":[{"id":"Llama-3.2-3B-Instruct","created":1716383261,"object":"model","owned_by":"Not specified"},{"id":"nomic-embed-text-v1.5.f16","created":1716383261,"object":"model","owned_by":"Not specified"}]}
```


### **3.4 把Llama3.2替换为 InternLM 模型**

A. 打开并修改 `config.json` 文件，将默认模型替换为 InternLM：  
`vi gaianet/config.json`  
config.json文件中 默认文件要修改三个地方：  

   a. 大模型下载链接从Llama3.2 改为 Internlm2.5 7B: `https://huggingface.co/second-state/internlm2_5-7b-chat-GGUF/resolve/main/internlm2_5-7b-chat-Q5_K_M.gguf`

   b. `chat_name: "internlm"`

   c. `prompt_template: "chatml"`
 
B. 停止当前运行的Llama3.2模型：`gaianet stop`  
C. 下载 InternLM 模型：`gaianet init`  
D. 重新启动节点：`gaianet start`  
E. 确认 InternLM 模型已成功在本地运行了，得到了与OpenAI API兼容的URL👇  
[https://0x8d2643381194979502cb2b542c7bd8bb5418408c.us.gaianet.network](https://0x8d2643381194979502cb2b542c7bd8bb5418408c.us.gaianet.network/)

## **4. 配置 Obsidian 与 InternLM 集成**

## 原始文档请查看 [_docs.gaianet.ai/user-guide/apps/obsidian/_](http://docs.gaianet.ai/user-guide/apps/obsidian/) 

### **4.1 安装 Obsidian Local GPT 插件**

1. 打开 Obsidian，进入设置 → 社区插件。
2. 搜索并安装 `Obsidian Local GPT` 插件。
  <img width="468" alt="Picture1" src="https://github.com/user-attachments/assets/e5ac5e94-490c-4bff-aa74-b855908654f5" />

3. 安装完成后，启用插件: Enable


### **4.2 配置 Local GPT 插件**

1. 在插件设置中，选择 `OpenAI compatible` 作为 API provider。  
<img width="468" alt="Picture2" src="https://github.com/user-attachments/assets/825e1aa0-5c71-4a62-be33-c7539821ceb0" />  

2. 在 `OpenAI compatible server URL` 中输入第三步最后生成的 API URL。  

3. 在 `API key` 中输入 `LlamaEdge`。  

4. 刷新模型列表，选择 `InternLM` 作为默认模型。  

### **4.3 使用快捷键调用 InternLM**

1. 默认快捷键为 `Command + M`。  
2. 选中一段文本，按下 `Command + M`，选择“Summarize”功能。  
3. InternLM 将自动被调用，从而生成文本总结。还可以选择其他选项，如续写文本或者纠正语法错误。
![1736701755585](https://github.com/user-attachments/assets/813cfad9-47b5-44d7-ac14-b334e563de6d)



## **5. 总结**

通过本课程，开发者可以掌握如何使用 WasmEdge 和 Gaia 部署 InternLM 大模型，并将其与 Obsidian 笔记软件集成，实现本地 AI 智能体的构建与应用。开发者还可以根据需求，将 InternLM 集成到其他 AI 应用中。

## **6. 参考文档**

[WasmEdge 官方文档](https://wasmedge.org/docs/)  
[Gaia 官方文档](https://docs.gaianet.ai/node-guide/quick-start/)
* * *
**注意**: 本文档为开发者提供详细的步骤和配置说明，确保开发者能够顺利部署和集成 InternLM 智能体。如有问题，请参考相关文档或联系社区支持。这节课只展示了其中一种种潜在的应用，还可以在Gaia和 internlm2_5-7b-chat 或其他书生大模型上开发更多有意思的 AI 应用噢！

**常见问题**
1. 端口冲突
- 解决方案：使用停止现有 Gaia 实例`gaianet stop`


2. 模型下载问题
- 验证 config.json 中的 HuggingFace URL
- 确保有足够的磁盘空间
