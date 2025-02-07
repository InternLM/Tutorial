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

## 4. 部署到 HuggingFace Space

最后，我们来将 MindSearch 部署到 HuggingFace Space。

我们首先打开 https://huggingface.co/spaces ，并点击 Create new Space，如下图所示。

![image](https://github.com/user-attachments/assets/bacbe161-2d21-434e-8f78-5738b076cd74)

在输入 Space name 并选择 License 后，选择配置如下所示。

![image](https://github.com/user-attachments/assets/f4d98e6b-5352-4638-a3da-d090140ce3f6)

然后，我们进入 Settings，配置硅基流动的 API Key。如下图所示。

![image](https://github.com/user-attachments/assets/76947d6c-eeba-4230-ab77-04a98c60d4d3)

选择 New secrets，name 一栏输入 SILICON_API_KEY，value 一栏输入你的 API Key 的内容。

![image](https://github.com/user-attachments/assets/6f4ab268-c5d6-4106-8749-ad282e17ba35)

最后，我们先新建一个目录，准备提交到 HuggingFace Space 的全部文件。

```bash
# 创建新目录
mkdir -p /root/mindsearch/mindsearch_deploy
# 准备复制文件
cd /root/mindsearch
cp -r /root/mindsearch/MindSearch/mindsearch /root/mindsearch/mindsearch_deploy
cp /root/mindsearch/MindSearch/requirements.txt /root/mindsearch/mindsearch_deploy
# 创建 app.py 作为程序入口
touch /root/mindsearch/mindsearch_deploy/app.py
```

其中，app.py 的内容如下：

```python
import json
import os

import gradio as gr
import requests
from lagent.schema import AgentStatusCode

os.system("python -m mindsearch.app --lang cn --model_format internlm_silicon &")

PLANNER_HISTORY = []
SEARCHER_HISTORY = []


def rst_mem(history_planner: list, history_searcher: list):
    '''
    Reset the chatbot memory.
    '''
    history_planner = []
    history_searcher = []
    if PLANNER_HISTORY:
        PLANNER_HISTORY.clear()
    return history_planner, history_searcher


def format_response(gr_history, agent_return):
    if agent_return['state'] in [
            AgentStatusCode.STREAM_ING, AgentStatusCode.ANSWER_ING
    ]:
        gr_history[-1][1] = agent_return['response']
    elif agent_return['state'] == AgentStatusCode.PLUGIN_START:
        thought = gr_history[-1][1].split('```')[0]
        if agent_return['response'].startswith('```'):
            gr_history[-1][1] = thought + '\n' + agent_return['response']
    elif agent_return['state'] == AgentStatusCode.PLUGIN_END:
        thought = gr_history[-1][1].split('```')[0]
        if isinstance(agent_return['response'], dict):
            gr_history[-1][
                1] = thought + '\n' + f'```json\n{json.dumps(agent_return["response"], ensure_ascii=False, indent=4)}\n```'  # noqa: E501
    elif agent_return['state'] == AgentStatusCode.PLUGIN_RETURN:
        assert agent_return['inner_steps'][-1]['role'] == 'environment'
        item = agent_return['inner_steps'][-1]
        gr_history.append([
            None,
            f"```json\n{json.dumps(item['content'], ensure_ascii=False, indent=4)}\n```"
        ])
        gr_history.append([None, ''])
    return


def predict(history_planner, history_searcher):

    def streaming(raw_response):
        for chunk in raw_response.iter_lines(chunk_size=8192,
                                             decode_unicode=False,
                                             delimiter=b'\n'):
            if chunk:
                decoded = chunk.decode('utf-8')
                if decoded == '\r':
                    continue
                if decoded[:6] == 'data: ':
                    decoded = decoded[6:]
                elif decoded.startswith(': ping - '):
                    continue
                response = json.loads(decoded)
                yield (response['response'], response['current_node'])

    global PLANNER_HISTORY
    PLANNER_HISTORY.append(dict(role='user', content=history_planner[-1][0]))
    new_search_turn = True

    url = 'http://localhost:8002/solve'
    headers = {'Content-Type': 'application/json'}
    data = {'inputs': PLANNER_HISTORY}
    raw_response = requests.post(url,
                                 headers=headers,
                                 data=json.dumps(data),
                                 timeout=20,
                                 stream=True)

    for resp in streaming(raw_response):
        agent_return, node_name = resp
        if node_name:
            if node_name in ['root', 'response']:
                continue
            agent_return = agent_return['nodes'][node_name]['detail']
            if new_search_turn:
                history_searcher.append([agent_return['content'], ''])
                new_search_turn = False
            format_response(history_searcher, agent_return)
            if agent_return['state'] == AgentStatusCode.END:
                new_search_turn = True
            yield history_planner, history_searcher
        else:
            new_search_turn = True
            format_response(history_planner, agent_return)
            if agent_return['state'] == AgentStatusCode.END:
                PLANNER_HISTORY = agent_return['inner_steps']
            yield history_planner, history_searcher
    return history_planner, history_searcher


with gr.Blocks() as demo:
    gr.HTML("""<h1 align="center">MindSearch Gradio Demo</h1>""")
    gr.HTML("""<p style="text-align: center; font-family: Arial, sans-serif;">MindSearch is an open-source AI Search Engine Framework with Perplexity.ai Pro performance. You can deploy your own Perplexity.ai-style search engine using either closed-source LLMs (GPT, Claude) or open-source LLMs (InternLM2.5-7b-chat).</p>""")
    gr.HTML("""
    <div style="text-align: center; font-size: 16px;">
        <a href="https://github.com/InternLM/MindSearch" style="margin-right: 15px; text-decoration: none; color: #4A90E2;">🔗 GitHub</a>
        <a href="https://arxiv.org/abs/2407.20183" style="margin-right: 15px; text-decoration: none; color: #4A90E2;">📄 Arxiv</a>
        <a href="https://huggingface.co/papers/2407.20183" style="margin-right: 15px; text-decoration: none; color: #4A90E2;">📚 Hugging Face Papers</a>
        <a href="https://huggingface.co/spaces/internlm/MindSearch" style="text-decoration: none; color: #4A90E2;">🤗 Hugging Face Demo</a>
    </div>
    """)
    with gr.Row():
        with gr.Column(scale=10):
            with gr.Row():
                with gr.Column():
                    planner = gr.Chatbot(label='planner',
                                         height=700,
                                         show_label=True,
                                         show_copy_button=True,
                                         bubble_full_width=False,
                                         render_markdown=True)
                with gr.Column():
                    searcher = gr.Chatbot(label='searcher',
                                          height=700,
                                          show_label=True,
                                          show_copy_button=True,
                                          bubble_full_width=False,
                                          render_markdown=True)
            with gr.Row():
                user_input = gr.Textbox(show_label=False,
                                        placeholder='帮我搜索一下 InternLM 开源体系',
                                        lines=5,
                                        container=False)
            with gr.Row():
                with gr.Column(scale=2):
                    submitBtn = gr.Button('Submit')
                with gr.Column(scale=1, min_width=20):
                    emptyBtn = gr.Button('Clear History')

    def user(query, history):
        return '', history + [[query, '']]

    submitBtn.click(user, [user_input, planner], [user_input, planner],
                    queue=False).then(predict, [planner, searcher],
                                      [planner, searcher])
    emptyBtn.click(rst_mem, [planner, searcher], [planner, searcher],
                   queue=False)

demo.queue()
demo.launch(server_name='0.0.0.0',
            server_port=7860,
            inbrowser=True,
            share=True)
```

在最后，将 /root/mindsearch/mindsearch_deploy 目录下的文件（使用 git）提交到 HuggingFace Space 即可完成部署了。
