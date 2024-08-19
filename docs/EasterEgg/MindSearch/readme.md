# MindSearch CPU-only 版部署

随着硅基流动提供了免费的 InternLM2.5-7B-Chat 服务（免费的 InternLM2.5-7B-Chat 真的很香），MindSearch 的部署与使用也就迎来了纯 CPU 版本，进一步降低了部署门槛。那就让我们来一起看看如何使用硅基流动的 API 来部署 MindSearch 吧。

接下来，我们以 InternStudio 算力平台为例，来部署 CPU-only 的 MindSearch 。

## 1. 创建开发机 & 环境配置

由于是 CPU-only，所以我们选择 10% A100 开发机即可，镜像方面选择 cuda-12.2。

然后我们新建一个目录用于存放 MindSearch 的相关代码，并把 MindSearch 仓库 clone 下来。

```bash
mkdir -p /root/mindsearch
cd /root/mindsearch
git clone https://github.com/InternLM/MindSearch.git
cd MindSearch && git checkout b832275 && cd ..
```

接下来，我们创建一个 conda 环境来安装相关依赖。

```bash
# 创建环境
conda create -n mindsearch python=3.10 -y
# 激活环境
conda activate mindsearch
# 安装依赖
pip install -r /root/mindsearch/MindSearch/requirements.txt
```

## 2. 获取硅基流动 API Key

因为要使用硅基流动的 API Key，所以接下来便是注册并获取 API Key 了。

首先，我们打开 https://account.siliconflow.cn/login 来注册硅基流动的账号（如果注册过，则直接登录即可）。

在完成注册后，打开 https://cloud.siliconflow.cn/account/ak 来准备 API Key。首先创建新 API 密钥，然后点击密钥进行复制，以备后续使用。

![image](https://github.com/user-attachments/assets/7905a2fc-ef30-4e33-b214-274bebdc9251)

## 3. 启动 MindSearch

### 3.1 启动后端

由于硅基流动 API 的相关配置已经集成在了 MindSearch 中，所以我们可以直接执行下面的代码来启动 MindSearch 的后端。

```bash
export SILICON_API_KEY=第二步中复制的密钥
conda activate mindsearch
cd /root/mindsearch/MindSearch
python -m mindsearch.app --lang cn --model_format internlm_silicon --search_engine DuckDuckGoSearch
```

### 3.2 启动前端

在后端启动完成后，我们打开新终端运行如下命令来启动 MindSearch 的前端。

```bash
conda activate mindsearch
cd /root/mindsearch/MindSearch
python frontend/mindsearch_gradio.py
```

最后，我们把 8002 端口和 7882 端口都映射到本地。可以在**本地**的 powershell 中执行如下代码：

```bash
ssh -CNg -L 8002:127.0.0.1:8002 -L 7882:127.0.0.1:7882 root@ssh.intern-ai.org.cn -p <你的 SSH 端口号>
```

然后，我们在**本地**浏览器中打开 `localhost:7882` 即可体验啦。

![image](https://github.com/user-attachments/assets/633a550a-06f1-459f-8e7b-86d99deba61b)

如果遇到了 timeout 的问题，可以按照 [文档](./readme_gpu.md#2-使用-bing-的接口) 换用 Bing 的搜索接口。
