# Lagent：从零搭建你的 Multi-Agent 

## 1 Agent基本介绍

### 1.1 什么是Agent

Agent是**一种能够自主感知环境并根据感知结果采取行动的实体**，以感知序列为输入，以动作作为输出的函数。它可以以软件形式（如聊天机器人、推荐系统）存在，也可以是物理形态的机器（如自动驾驶汽车、机器人）。

基本特性：

- **自主性**：能够在没有外部干预的情况下做出决策。
- **交互性**：能够与环境交换信息。
- **适应性**：根据环境变化调整自身行为。
- **目的性**：所有行为都以实现特定目标为导向。

<div align="center">
  <img src="https://s1.imagehub.cc/images/2024/11/04/eac389cdf83fd305c7131d7f208ad578.png" width="400" />
</div>


### 1.2 Agent的应用场景

Agent技术的应用领域其实十分广泛，涵盖了从交通、医疗到教育、家居和娱乐等生活的方方面面，以下列举2个实际例子。

**（1）自动驾驶系统**

- **应用**：自动驾驶汽车、出租车等。
- **目标**：安全、快捷、守法、舒适和高效。
- **传感器**：摄像头、雷达、定位系统等。
- **执行器**：方向盘、油门、刹车、信号灯。

**（2）医疗诊断系统**

- **应用**：医院诊断、病情监控。
- **目标**：精准诊断、降低费用。
- **传感器**：症状输入、患者自述。
- **执行器**：检测、诊断、处方。

## 2 Lagent 介绍

### 2.1 基础介绍

Lagent 是一个轻量级开源智能体框架，旨在让用户可以高效地构建基于大语言模型的智能体。同时它也提供了一些典型工具以增强大语言模型的能力。

Lagent 目前已经支持了包括 AutoGPT、ReAct 等在内的多个经典智能体范式，也支持了如下工具：

- Arxiv 搜索
- Bing 地图
- Google 学术搜索
- Google 搜索
- 交互式 IPython 解释器
- IPython 解释器
- PPT
- Python 解释器

其基本结构如下所示：

<div align="center">
  <img src="https://github.com/InternLM/lagent/assets/24351120/cefc4145-2ad8-4f80-b88b-97c05d1b9d3e" width="800" />
</div>


### 2.2 常见工具调用能力范式

#### 2.2.1 通用智能体范式

这种范式强调模型无需依赖特定的特殊标记（special token）来定义工具调用的参数边界。模型依靠其强大的指令跟随与推理能力，在指定的**system prompt**框架下，根据任务需求自动生成响应。这种方式让模型在推理过程中能更灵活地适应多种任务，不需要对Tokenizer进行特殊设计。

**优势**：

- 灵活适应不同任务，无需设计和维护复杂的标记系统。
- 适合快速迭代，降低微调和部署的复杂性。
- 更易与多模态输入（如文本和图像）结合，扩展模型的通用性。

**劣势**：

- 由于没有明确标记，调用工具时的错误难以捕捉和纠正。
- 在复杂任务中，模型生成可能不够精准，导致工具调用的准确性下降。

**（1）ReAct**：将模型的推理分为**Reason**和**Action**两个步骤，并让它们交替执行，直到得到最终结果：

- **Reason**：生成分析步骤，解释当前任务的上下文或状态，帮助模型理解下一步行动的逻辑依据。
- **Action**：基于Reason的结果，生成具体的工具调用请求（如查询搜索引擎、调用API、数据库检索等），将模型的推理转化为行动。

**（2）ReWoo**：全称为**Reason without Observation**，是在ReAct范式基础上进行改进的Agent架构，针对多工具调用的复杂性与冗余性提供了一种高效的解决方案。相比于ReAct中的交替推理和行动，ReWoo直接生成一次性使用的**完整工具链**，减少了不必要的Token消耗和执行时间。同时，由于工具调用的规划与执行解耦，这一范式在模型微调时不需要实际调用工具即可完成。

- **Planner**：用户输入的问题或任务首先传递给Planner，Planner将其分解为多个逻辑上相关的计划。每个计划包含推理部分（Reason）以及工具调用和参数（Execution）。Task List按顺序列出所有需要执行的任务链。
- **Worker**：每个Worker根据Task List中的子任务，调用指定工具并返回结果。所有Worker之间通过共享状态保持任务执行的连续性。
- **Solver阶段**：Worker完成任务后，将所有结果同步到Solver。Solver会对这些结果进行整合，并生成最终的答案或解决方案返回给用户。

#### 2.2.2 模型特化智能体范式

在这种范式下，模型的工具调用必须通过特定的**special token**明确标记。如InternLM2使用`<|action_start|>`和`<|action_end|>`来定义调用边界。这些标记通常与模型的Tokenizer深度集成，确保在执行特定任务时，能够准确捕捉调用信息并执行。

**优势**：

- 特定标记明确工具调用的起止点，提高了调用的准确性。
- 有助于模型在部署过程中避免误调用，增强系统的可控性。
- 提高对复杂调用链的支持，适合复杂任务的场景。

**劣势**：

- 需要对Tokenizer和模型架构进行定制，增加开发和维护成本。
- 调用流程固定，降低了模型的灵活性，难以适应快速变化的任务。

**（1）InternLM2案例分析：**工具调用使用了如`<|plugin|>`、`<|interpreter|>`、`<|action_start|>`和`<|action_end|>`等特殊标记，确保每个调用都符合指定的格式。模型在执行任务时，依靠这些标记与系统紧密协作，保障任务的精准执行。链接：[InternLM/agent at main · InternLM/InternLM](https://github.com/InternLM/InternLM/tree/main/agent)



## 3 动手实践

### 3.1环境配置

开发机选择 30% A100，镜像选择为 Cuda12.2-conda。

<div align="center">
  <img src="https://s1.imagehub.cc/images/2024/11/04/627cf2208192ad08cb2460f7c30fe21a.png" width="700" />
</div>

<div align="center">
  <img src="https://s1.imagehub.cc/images/2024/11/04/07551c110d9526bb3ee21aab74d11ab0.png" width="700" />
</div>

首先来为 Lagent 配置一个可用的环境。

```python
# 创建环境
conda create -n lagent python=3.10 -y
# 激活环境
conda activate lagent
# 安装 torch
conda install pytorch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 pytorch-cuda=12.1 -c pytorch -c nvidia -y
# 安装其他依赖包
pip install termcolor==2.4.0
pip install streamlit==1.39.0
pip install class_registry==2.1.2
pip install datasets==3.1.0
```

等待安装完成~

<div align="center">
  <img src="https://s1.imagehub.cc/images/2024/11/04/d1c2046c82478ae703e08b0bc77a7de4.png" width="1000" />
</div>

接下来，我们通过源码安装的方式安装 lagent。

```cmd
# 创建目录以存放代码
mkdir -p /root/agent_camp4
cd /root/agent_camp4
git clone https://github.com/InternLM/lagent.git
cd lagent && git checkout e304e5d && pip install -e . && cd ..
pip install griffe==0.48.0
```

### 3.2 Lagent框架中Agent的使用

接下来，我们将使用 Lagent 框架，一步步搭建并使用基于 **InternLM2.5** 的 Web Demo，体验其强大的智能体功能。

首先，需要**申请 API 授权令牌** ，请前往 [书生·浦语 API 文档](https://internlm.intern-ai.org.cn/api/document) 申请并获取 `Authorization` 令牌，将其填入后续代码的 `YOUR_TOKEN_HERE` 变量中。

创建一个代码example，创建`agent_api_web_demo.py`，在里面实现我们的Web Demo：

```cmd
conda activate lagent
cd /root/agent_camp4/lagent/examples
touch agent_api_web_demo.py
```

Action，也称为工具，Lagent中集成了很多好用的工具，提供了一套LLM驱动的智能体用来与真实世界交互并执行复杂任务的函数，包括谷歌文献检索、Arxiv文献检索、Python编译器等。具体可以查看[文档](https://lagent.readthedocs.io/zh-cn/latest/tutorials/action.html#id2)

让我们来体验一下，让LLM调用Arxiv文献检索这个工具：

在`agent_api_web_demo.py`中写入下面的代码，这里实现 `CustomAPILLM` 类，该类继承自 `BaseAPILLM`，封装了对 API 的调用逻辑，然后利用`Streamlit`启动Web服务：

```python
import copy
import hashlib
import json
import os
from typing import Dict, List, Union
import re
import streamlit as st
import requests

from lagent.actions import ActionExecutor, ArxivSearch, IPythonInterpreter
from lagent.prompts.parsers import PluginParser
from lagent.agents.stream import INTERPRETER_CN, META_CN, PLUGIN_CN, AgentForInternLM, get_plugin_prompt
from lagent.llms.base_api import BaseAPILLM
from lagent.schema import AgentStatusCode

YOUR_TOKEN_HERE = ""      # 请注意，这里要替换为自己实际授权令牌！！！

class CustomAPILLM(BaseAPILLM):
    """自定义的 API LLM 类，用于调用外部 API 进行文本生成。"""

    def __init__(self, model_type, meta_template=None, **gen_params):
        super().__init__(model_type, meta_template=meta_template, **gen_params)

    def call_api(self, messages):
        """调用外部 API 并返回响应结果。"""
        url = 'https://internlm-chat.intern-ai.org.cn/puyu/api/v1/chat/completions'
        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Bearer " + YOUR_TOKEN_HERE  
        }
        data = {
            "model": self.model_type,
            "messages": messages,
            "n": 1,
            "temperature": self.gen_params['temperature'],
            "top_p": self.gen_params['top_p'],
            "stream": False,
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API 调用失败，状态码: {response.status_code}")

    def generate(self, inputs: Union[str, List[str]], **gen_params) -> Union[str, List[str]]:
        """调用外部 API。"""
        if isinstance(inputs, str):
            inputs = [{"role": "user", "content": inputs}]
        elif isinstance(inputs, list) and isinstance(inputs[0], str):
            inputs = [{"role": "user", "content": text} for text in inputs]

        # 调用 call_api 并返回响应
        response = self.call_api(inputs)
        content = response["choices"][0]["message"]["content"]

        if len(inputs) == 1:
            return content
        else:
            return [content]

class SessionState:
    """管理会话状态的类。"""

    def init_state(self):
        """初始化会话状态变量。"""
        st.session_state['assistant'] = []
        st.session_state['user'] = []
        action_list = [
            ArxivSearch(),
        ]
        st.session_state['plugin_map'] = {
            action.name: action for action in action_list
        }
        st.session_state['model_map'] = {}
        st.session_state['model_selected'] = None
        st.session_state['plugin_actions'] = set()
        st.session_state['history'] = []

    def clear_state(self):
        """清除当前会话状态。"""
        st.session_state['assistant'] = []
        st.session_state['user'] = []
        st.session_state['model_selected'] = None
        st.session_state['file'] = set()
        if 'chatbot' in st.session_state:
            st.session_state['chatbot']._session_history = []

class StreamlitUI:
    """管理 Streamlit 界面的类。"""

    def __init__(self, session_state: SessionState):
        self.init_streamlit()
        self.session_state = session_state
        self.plugin_action = []  # 插件操作列表
        # 初始化提示词
        self.meta_prompt = META_CN
        self.da_prompt = INTERPRETER_CN
        self.plugin_prompt = PLUGIN_CN

    def init_streamlit(self):
        """初始化 Streamlit 的 UI 设置。"""
        st.set_page_config(
            layout='wide',
            page_title='lagent-web',
            page_icon='./docs/imgs/lagent_icon.png')
        st.header(':robot_face: :blue[Lagent] Web Demo ', divider='rainbow')
        st.sidebar.title('模型控制')
        st.session_state['file'] = set()
        st.session_state['ip'] = None

    def setup_sidebar(self):
        """设置侧边栏，选择模型和插件。"""
        model_name = st.sidebar.text_input('模型名称：', value='internlm2.5-latest')
        self.meta_prompt = st.sidebar.text_area('系统提示词', value=META_CN)
        self.da_prompt = st.sidebar.text_area('数据分析提示词', value=INTERPRETER_CN)
        self.plugin_prompt = st.sidebar.text_area('插件提示词', value=PLUGIN_CN)
        model_ip = st.sidebar.text_input('模型IP：', value='127.0.0.1:23333')

        # 确保 model_map 已初始化
        if model_name not in st.session_state['model_map']:
            st.session_state['model_map'][model_name] = self.call_api

        model = st.session_state['model_map'][model_name]

        # 添加插件选择
        plugin_name = st.sidebar.multiselect(
            '插件选择',
            options=list(st.session_state['plugin_map'].keys()),
            default=[],
        )
        da_flag = st.sidebar.checkbox('数据分析', value=False)

        # 创建插件操作列表
        self.plugin_action = [
            st.session_state['plugin_map'][name] for name in plugin_name
        ]

        # 动态生成插件提示
        if self.plugin_action:
            self.plugin_prompt = get_plugin_prompt(self.plugin_action)

        # 初始化或更新 chatbot
        if 'chatbot' in st.session_state:
            if self.plugin_action:
                st.session_state['chatbot'].plugin_executor = ActionExecutor(
                    actions=self.plugin_action)
            else:
                st.session_state['chatbot'].plugin_executor = None

            if da_flag:
                st.session_state['chatbot'].interpreter_executor = ActionExecutor(
                    actions=[IPythonInterpreter()])
            else:
                st.session_state['chatbot'].interpreter_executor = None

            # 更新提示词
            st.session_state['chatbot'].meta_prompt = self.meta_prompt
            st.session_state['chatbot'].plugin_prompt = self.plugin_prompt
            st.session_state['chatbot'].interpreter_prompt = self.da_prompt

        # 清空对话按钮
        if st.sidebar.button('清空对话', key='clear'):
            self.session_state.clear_state()

        uploaded_file = st.sidebar.file_uploader('上传文件')

        return model_name, model, self.plugin_action, uploaded_file, model_ip

    def call_api(self, prompt="你是一个机器人"):
        """使用外部 API 请求生成响应（用于模型初始化）。"""
        url = 'https://internlm-chat.intern-ai.org.cn/puyu/api/v1/chat/completions'
        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Bearer " + YOUR_TOKEN_HERE
        }
        data = {
            "model": "internlm2.5-latest",
            "messages": [{"role": "assistant", "content": prompt}],
            "n": 1,
            "temperature": 0.8,
            "top_p": 0.9,
            "stream": False,
        }
        response = requests.post(url, headers=headers, json=data)
        return response

    def initialize_chatbot(self, model_name, plugin_action):
        """使用 CustomAPILLM 初始化 chatbot。"""
        # meta_template 是一个包含字典的列表，并包含所有角色
        self.meta_prompt = [
            {"role": "system", "content": self.meta_prompt, "api_role": "system"},
            {"role": "user", "content": "", "api_role": "user"},
            {"role": "assistant", "content": "", "api_role": "assistant"}
        ]

        # 使用 CustomAPILLM 类
        api_model = CustomAPILLM(
            model_type=model_name,
            meta_template=self.meta_prompt,
            max_new_tokens=512,
            temperature=0.8,
            top_p=0.9
        )
        return api_model

    def render_user(self, prompt: str):
        """渲染用户的输入。"""
        with st.chat_message('user'):
            st.markdown(prompt)

    def render_assistant(self, agent_return):
        """渲染助手的响应，包括处理插件的结果。"""
        with st.chat_message('assistant'):
            if hasattr(agent_return, "content"):
                content = agent_return.content
            else:
                content = str(agent_return)

            if isinstance(content, list):
                content = '\n'.join(content)
            elif not isinstance(content, str):
                content = str(content)

            st.markdown(content)

            json_match = re.search(r'\{.*\}', content)
            if json_match:
                json_string = json_match.group()
                try:
                    action_data = json.loads(json_string)
                    plugin_name = action_data.get('name')
                    parameters = action_data.get('parameters', {})

                    # 提取插件的基本名称
                    base_plugin_name = plugin_name.split('.')[0]

                    if base_plugin_name in [action.name for action in self.plugin_action]:
                        plugin = st.session_state['plugin_map'][base_plugin_name]

                        # 根据插件类型调用不同的方法
                        if base_plugin_name == "ArxivSearch":
                            arxiv_results = plugin.get_arxiv_article_information(parameters.get('query', ''))
                            # 解析和显示 Arxiv 信息
                            results = arxiv_results.get('content', '').split('\n\n')
                            for result in results:
                                lines = result.split('\n')
                                if len(lines) >= 4:
                                    published = lines[0].replace('Published: ', '').strip()
                                    title = lines[1].replace('Title: ', '').strip()
                                    authors = lines[2].replace('Authors: ', '').strip()
                                    summary = ' '.join(lines[3:]).replace('Summary: ', '').strip()

                                    st.markdown(f"  **标题**: {title}")
                                    st.markdown(f"  **作者**: {authors}")
                                    st.markdown(f"  **发表日期**: {published}")
                                    st.markdown(f"  **摘要**: {summary}\n")
                                else:
                                    st.warning("无法解析论文信息，格式不正确。")
                        else:
                            st.warning(f"未找到插件: {base_plugin_name}")
                    else:
                        st.warning(f"未找到插件: {base_plugin_name}")
                except json.JSONDecodeError:
                    st.error("无法解析 action 中的 JSON 数据，请检查其格式是否正确。")

    def render_plugin_args(self, action):
        """渲染插件的参数。"""
        action_name = action.type
        args = action.args
        parameter_dict = dict(name=action_name, parameters=args)
        parameter_str = 'json\n' + json.dumps(
            parameter_dict, indent=4, ensure_ascii=False) + '\n'
        st.markdown(parameter_str)

    def render_interpreter_args(self, action):
        """渲染解释器的参数。"""
        st.info(action.type)
        st.markdown(action.args['text'])

    def render_action(self, action):
        """渲染动作，包括思考过程和结果。"""
        st.markdown(action.thought)
        if action.type == 'IPythonInterpreter':
            self.render_interpreter_args(action)
        elif action.type == 'FinishAction':
            pass
        else:
            self.render_plugin_args(action)
        self.render_action_results(action)

    def render_action_results(self, action):
        if isinstance(action.result, dict):
            if 'text' in action.result:
                st.markdown('\n' + action.result['text'] + '\n')
            if 'image' in action.result:
                for image_path in action.result['image']:
                    image_data = open(image_path, 'rb').read()
                    st.image(image_data, caption='Generated Image')
            if 'video' in action.result:
                video_data = action.result['video']
                video_data = open(video_data, 'rb').read()
                st.video(video_data)
            if 'audio' in action.result:
                audio_data = action.result['audio']
                audio_data = open(audio_data, 'rb').read()
                st.audio(audio_data)
        elif isinstance(action.result, list):
            for item in action.result:
                if item['type'] == 'text':
                    st.markdown('\n' + item['content'] + '\n')
                elif item['type'] == 'image':
                    image_data = open(item['content'], 'rb').read()
                    st.image(image_data, caption='Generated Image')
                elif item['type'] == 'video':
                    video_data = open(item['content'], 'rb').read()
                    st.video(video_data)
                elif item['type'] == 'audio':
                    audio_data = open(item['content'], 'rb').read()
                    st.audio(audio_data)
        if action.errmsg:
            st.error(action.errmsg)

def main():
    """主函数，运行 Streamlit 应用。"""
    if 'ui' not in st.session_state:
        session_state = SessionState()
        session_state.init_state()
        st.session_state['ui'] = StreamlitUI(session_state)
    else:
        st.set_page_config(
            layout='wide',
            page_title='lagent-web',
            page_icon='./docs/imgs/lagent_icon.png'
        )
        st.header(':robot_face: :blue[Lagent] Web Demo ', divider='rainbow')

    # 设置侧边栏并获取模型和插件
    model_name, model, plugin_action, uploaded_file, _ = st.session_state['ui'].setup_sidebar()

    # 初始化 chatbot 和 agent
    if 'chatbot' not in st.session_state or model_name != st.session_state['chatbot'].model_type:
        st.session_state['chatbot'] = st.session_state['ui'].initialize_chatbot(model_name, plugin_action)
        plugins = [
            dict(type='lagent.actions.ArxivSearch'),
        ]

        # 创建 AgentForInternLM 实例并存储在 session_state 中
        st.session_state['agent'] = AgentForInternLM(
            llm=st.session_state['chatbot'],
            plugins=plugins,
            output_format=dict(
                type=PluginParser,
                template=PLUGIN_CN,
                prompt=get_plugin_prompt(plugins)
            )
        )
        # 清空会话历史
        st.session_state['session_history'] = []

    if 'agent' not in st.session_state:
        st.session_state['agent'] = None

    agent = st.session_state['agent']
    for prompt, agent_return in zip(st.session_state['user'], st.session_state['assistant']):
        st.session_state['ui'].render_user(prompt)
        st.session_state['ui'].render_assistant(agent_return)

    if user_input := st.chat_input(''):
        with st.container():
            st.session_state['ui'].render_user(user_input)
        res = agent(user_input, session_id=0)
        st.session_state['ui'].render_assistant(res)
        st.session_state['assistant'].append(copy.deepcopy(res))

        if uploaded_file and uploaded_file.name not in st.session_state['file']:
            st.session_state['file'].add(uploaded_file.name)
            file_bytes = uploaded_file.read()
            file_type = uploaded_file.type
            if 'image' in file_type:
                st.image(file_bytes, caption='Uploaded Image')
            elif 'video' in file_type:
                st.video(file_bytes, caption='Uploaded Video')
            elif 'audio' in file_type:
                st.audio(file_bytes, caption='Uploaded Audio')
            postfix = uploaded_file.name.split('.')[-1]
            prefix = hashlib.md5(file_bytes).hexdigest()
            filename = f'{prefix}.{postfix}'
            file_path = os.path.join(root_dir, filename)
            with open(file_path, 'wb') as tmpfile:
                tmpfile.write(file_bytes)
            file_size = os.stat(file_path).st_size / 1024 / 1024
            file_size = f'{round(file_size, 2)} MB'
            user_input = [
                dict(role='user', content=user_input),
                dict(role='user', content=json.dumps(dict(path=file_path, size=file_size)), name='file')
            ]
        else:
            user_input = [dict(role='user', content=user_input)]

    st.session_state['last_status'] = AgentStatusCode.END

if __name__ == '__main__':
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    root_dir = os.path.join(root_dir, 'tmp_dir')
    os.makedirs(root_dir, exist_ok=True)
    main()
```

在终端中输入：

```cmd
streamlit run agent_api_web_demo.py
```

<div align="center">
  <img src="https://s1.imagehub.cc/images/2024/11/20/a278dd9829d85bd67467ce8e6c4fe1ce.png" width="800" />
</div>

在等待server 都完全启动后，我们在 **本地** 的 PowerShell 中输入如下指令来进行端口映射：

```bash
ssh -CNg -L 8501:127.0.0.1:8501 root@ssh.intern-ai.org.cn -p <你的 SSH 端口号>
```

接下来，在本地浏览器中打开 `localhost:8501`：

<div align="center">
  <img src="https://s1.imagehub.cc/images/2024/11/04/064bfe720e414a7ac0334b41b14bfaf9.png" width="400" />
</div>

可以看到页面如下：

<div align="center">
  <img src="https://s1.imagehub.cc/images/2024/11/20/92464bdc6a7a03ec1bb4929ef1a9b9ba.png" width="800" />
</div>

可以尝试进行几轮简单的对话，并让其搜索文献，会发现大模型现在尽管有比较好的对话能力，但是并不能帮我们准确的找到文献，例如输入指令“帮我搜索一下最新版本的MindSearch论文”：

<div align="center">
  <img src="https://s1.imagehub.cc/images/2024/11/20/ffae18d9c2a82d95302e9a6b62c86674.png" width="800" />
</div>

提示未找到插件: ArxivSearch，因为此时插件没有正确选择。

<div align="center">
  <img src="https://s1.imagehub.cc/images/2024/11/20/e08fcf64611802870e36cc19ba8472de.png" width="800" />
</div>

现在将ArxivSearch选择上，再次输入指令“帮我搜索一下最新版本的MindSearch论文”，可以看到，通过调用外部工具，大模型成功理解了我们的任务，得到了我们需要的文献：

<div align="center">
  <img src="https://s1.imagehub.cc/images/2024/11/20/d1237cd84362f803e2394afba90d9de3.png" width="600" />
</div>

<img src="https://s1.imagehub.cc/images/2024/11/20/e4a591a27fd51b5aad16fa73de5f4f10.png" alt="image" border="0" style="zoom:80%;" >

### 3.3 制作一个属于自己的Agent

在完成了上面的内容后，可能就会同学好奇了，那么我应该如何基于Lagent框架实现一个自己的工具，赋予LLM额外的能力？本节将会以实时天气查询为例子，通过调用和风天气API，介绍如何自定义一个自己的Agent。

Lagent 框架的工具部分文档可以在此处查看：[Lagent 工具文档](https://lagent.readthedocs.io/zh-cn/latest/tutorials/action.html)。

使用 Lagent 自定义工具主要分为以下3步：

（1）继承 `BaseAction` 类

（2）实现简单工具的 `run` 方法；或者实现工具包内每个子工具的功能

（3）简单工具的 `run` 方法可选被 `tool_api` 装饰；工具包内每个子工具的功能都需要被 `tool_api` 装饰

首先，为了使用和风天气的 API 服务，你需要获取一个 API Key。请按以下步骤操作：

（1）访问 [和风天气 API 文档](https://dev.qweather.com/docs/api/)（需要注册账号）。

（2）点击页面右上角的“控制台”。

（3）在控制台中，点击左侧的“项目管理”，然后点击右上角“创建项目”。

（4）输入项目名称（可以使用“Lagent”），选择免费订阅，并在“订阅方案”中选择“Web API”。

（5）创建后，回到“项目管理”页面，找到你的 API Key 并复制保存。

<img src="https://s1.imagehub.cc/images/2024/11/07/61e7a96c04e232652984a6abec9ff2da.png" alt="image" border="0" style="zoom: 50%;" >

接着，我们需要在`laegnt/actions`文件夹下面创建一个天气查询的工具程序。

```cmd
conda activate lagent
cd /root/agent_camp4/lagent/lagent/actions
touch weather_query.py
```

将下面的代码复制进去，注意要将刚刚申请的API Key填写进去：

```python
import requests
from lagent.actions.base_action import BaseAction, tool_api
from lagent.schema import ActionReturn, ActionStatusCode

class WeatherQuery(BaseAction):
    def __init__(self):
        super().__init__()
        # 下面需要替换为你的和风天气 API Key
        self.api_key = ""

    @tool_api
    def run(self, location: str) -> dict:
        """
        查询实时天气信息。

        Args:
            location (str): 要查询的地点名称、LocationID 或经纬度坐标（如 "101010100" 或 "116.41,39.92"）。

        Returns:
            dict: 包含天气信息的字典
                * location: 地点名称
                * weather: 天气状况
                * temperature: 当前温度
                * wind_direction: 风向
                * wind_speed: 风速（公里/小时）
                * humidity: 相对湿度（%）
                * report_time: 数据报告时间
        """
        try:
            # 如果 location 不是坐标格式（例如 "116.41,39.92"），则调用 GeoAPI 获取 LocationID
            if not ("," in location and location.replace(",", "").replace(".", "").isdigit()):
                # 使用 GeoAPI 获取 LocationID
                geo_url = f"https://geoapi.qweather.com/v2/city/lookup?location={location}&key={self.api_key}"
                geo_response = requests.get(geo_url)
                geo_data = geo_response.json()

                if geo_data.get("code") != "200" or not geo_data.get("location"):
                    raise Exception(f"GeoAPI 返回错误码：{geo_data.get('code')} 或未找到位置")

                # 使用返回的第一个 LocationID
                location = geo_data["location"][0]["id"]

            # 构建天气查询的 API 请求 URL
            weather_url = f"https://devapi.qweather.com/v7/weather/now?location={location}&key={self.api_key}"
            response = requests.get(weather_url)
            data = response.json()

            # 检查 API 响应码
            if data.get("code") != "200":
                raise Exception(f"Weather API 返回错误码：{data.get('code')}")

            # 解析和组织天气信息
            weather_info = {
                "location": location,
                "weather": data["now"]["text"],
                "temperature": data["now"]["temp"] + "°C",  # 添加单位
                "wind_direction": data["now"]["windDir"],
                "wind_speed": data["now"]["windSpeed"] + " km/h",  # 添加单位
                "humidity": data["now"]["humidity"] + "%",  # 添加单位
                "report_time": data["updateTime"]
            }

            return {"result": weather_info}

        except Exception as exc:
            return ActionReturn(
                errmsg=f"WeatherQuery 异常：{exc}",
                state=ActionStatusCode.HTTP_ERROR
            )
```

其中，`WeatherQuery` 类继承自 `BaseAction`，这是 Lagent 的基础工具类，提供了工具的框架逻辑。`tool_api` 是一个装饰器，用于标记工具中具体执行逻辑的函数，使得 Lagent 智能体能够调用该方法执行任务。`run` 方法是工具的主要逻辑入口，通常会根据输入参数完成一项任务并返回结果。

在具体函数实现上，利用GeoAPI 获取 LocationID，当用户输入的 `location` 不是经纬度坐标格式（如 `116.41,39.92`），则使用和风天气的 `GeoAPI` 将位置名转换为 `LocationID`，并通过 `Weather API` 获取目标位置的实时天气数据。最后，解析返回的 JSON 数据，并格式化为结构化字典：

在`/root/agent_camp4/lagent/lagent/actions/__init__.py`中加入下面的代码，用以初始化`WeatherQuery`方法：

```python
from .weather_query import WeatherQuery
__all__ = [
    'BaseAction', 'ActionExecutor', 'AsyncActionExecutor', 'InvalidAction',
    'FinishAction', 'NoAction', 'BINGMap', 'AsyncBINGMap', 'ArxivSearch',
    'AsyncArxivSearch', 'GoogleSearch', 'AsyncGoogleSearch', 'GoogleScholar',
    'AsyncGoogleScholar', 'IPythonInterpreter', 'AsyncIPythonInterpreter',
    'IPythonInteractive', 'AsyncIPythonInteractive',
    'IPythonInteractiveManager', 'PythonInterpreter', 'AsyncPythonInterpreter',
    'PPT', 'AsyncPPT', 'WebBrowser', 'AsyncWebBrowser', 'BaseParser',
    'JsonParser', 'TupleParser', 'tool_api', 'WeatherQuery' # 这里
]
```

接下来，我们将修改 Web Demo 脚本来集成自定义的 `WeatherQuery` 插件。

打开`agent_api_web_demo.py`, 修改内容如下，目的是将该工具注册进大模型的插件列表中，使得其可以知道。

```diff
- from lagent.actions import ActionExecutor, ArxivSearch, IPythonInterpreter
+ from lagent.actions import ActionExecutor, ArxivSearch, IPythonInterpreter, WeatherQuery
+ action_list = [ArxivSearch(),]
- action_list = [ArxivSearch(), WeatherQuery(),]  # 添加天气查询插件
- plugins = [
-            dict(type='lagent.actions.ArxivSearch'),
-        ]
+ plugins =[dict(type='lagent.actions.ArxivSearch'),dict(type='lagent.actions.WeatherQuery')]
```

增加对天气查询响应的处理，在`render_assistant`方法中修改为：

```python
def render_assistant(self, agent_return):
        """渲染助手的响应，包括处理插件的结果。"""
        print("agent_return", agent_return)
        with st.chat_message('assistant'):
            if hasattr(agent_return, "content"):
                content = agent_return.content
            else:
                content = str(agent_return)

            if isinstance(content, list):
                content = '\n'.join(content)
            elif not isinstance(content, str):
                content = str(content)

            st.markdown(content)

            json_match = re.search(r'\{.*\}', content)
            if json_match:
                json_string = json_match.group()
                try:
                    action_data = json.loads(json_string)
                    plugin_name = action_data.get('name')
                    parameters = action_data.get('parameters', {})

                    # 提取插件的基本名称
                    base_plugin_name = plugin_name.split('.')[0]

                    if base_plugin_name in [action.name for action in self.plugin_action]:
                        plugin = st.session_state['plugin_map'][base_plugin_name]

                        # 根据插件类型调用不同的方法
                        if base_plugin_name == "ArxivSearch":
                            arxiv_results = plugin.get_arxiv_article_information(parameters.get('query', ''))
                            # 解析和显示 Arxiv 信息
                            results = arxiv_results.get('content', '').split('\n\n')
                            for result in results:
                                lines = result.split('\n')
                                if len(lines) >= 4:
                                    published = lines[0].replace('Published: ', '').strip()
                                    title = lines[1].replace('Title: ', '').strip()
                                    authors = lines[2].replace('Authors: ', '').strip()
                                    summary = ' '.join(lines[3:]).replace('Summary: ', '').strip()

                                    st.markdown(f"  **标题**: {title}")
                                    st.markdown(f"  **作者**: {authors}")
                                    st.markdown(f"  **发表日期**: {published}")
                                    st.markdown(f"  **摘要**: {summary}\n")
                                else:
                                    st.warning("无法解析论文信息，格式不正确。")
                        elif base_plugin_name == "WeatherQuery":
                            # 调用 WeatherQuery 插件的方法
                            weather_results = plugin.run(parameters.get('location', ''))
                            if "result" in weather_results:
                                weather_info = weather_results["result"]
                                st.markdown("### 天气信息")
                                st.markdown(f"- **地点**: {weather_info['location']}")
                                st.markdown(f"- **天气**: {weather_info['weather']}")
                                st.markdown(f"- **温度**: {weather_info['temperature']}")
                                st.markdown(f"- **风向**: {weather_info['wind_direction']}")
                                st.markdown(f"- **风速**: {weather_info['wind_speed']}")
                                st.markdown(f"- **湿度**: {weather_info['humidity']}")
                                st.markdown(f"- **报告时间**: {weather_info['report_time']}")
                            else:
                                st.error(f"天气查询失败：{weather_results.get('errmsg', '未知错误')}")
                        else:
                            st.warning(f"未找到插件: {base_plugin_name}")
                    else:
                        st.warning(f"未找到插件: {base_plugin_name}")
                except json.JSONDecodeError:
                    st.error("无法解析 action 中的 JSON 数据，请检查其格式是否正确。")
```

再次启动Web程序，`streamlit run agent_api_web_demo.py`。

可以看到左侧的插件栏多了天气查询插件，我们将2个插件同时勾选上，这样可以说明模型具备识别调用不同工具的能力，什么任务对应什么工具来解决。

这次我们查询一下南京（随便什么城市都行的☀️）的天气，输入命令“帮我查询一下南京现在的天气”。现在，大模型通过天气查询的API准确地完成了这个任务：

<img src="https://s1.imagehub.cc/images/2024/11/20/8f72148a9abdb26bf16b9684593d7a2c.png" alt="image" border="0" style="zoom:67%;" >

### 3.4 Multi-Agents博客写作系统的搭建

在这一节中，我们将使用 **Lagent** 来构建一个多智能体系统 (**Multi-Agent System**)，展示如何协调不同的智能代理完成内容生成和优化的任务。我们的多智能体系统由两个主要代理组成：

（1）**内容生成代理**：负责根据用户的主题提示生成一篇结构化、专业的文章或报告。

（2）**批评优化代理**：负责审阅生成的内容，指出不足，推荐合适的文献，使文章更加完善。

Multi-Agents博客写作系统的流程图如下：

<div align="center">
  <img src="https://s1.imagehub.cc/images/2024/11/20/3e2ca7d0f5754baf7bd4274f311da228.png" width="500" />
</div>

首先，创建一个新的 Python 文件 `multi_agents_api_web_demo.py`，并进入 `lagent` 环境：

```bash
conda activate lagent
cd /root/agent_camp4/lagent/examples
touch multi_agents_api_web_demo.py
```

将下面的代码填入`multi_agents_api_web_demo.py`:

```python
import asyncio
import json
import re
import requests
import streamlit as st

from lagent.agents import Agent
from lagent.prompts.parsers import PluginParser
from lagent.agents.stream import PLUGIN_CN, get_plugin_prompt
from lagent.schema import AgentMessage
from lagent.actions import ArxivSearch
from lagent.hooks import Hook

YOUR_TOKEN_HERE = ""

# 自定义API模型，用于调用外部API并处理LLM的响应
class CustomAPILLM:
    def __init__(self, model_type, **gen_params):
        """
        初始化API模型
        :param model_type: 模型名称
        :param gen_params: 生成参数，如temperature、top_p等
        """
        self.model_type = model_type
        self.gen_params = gen_params

    def call_api(self, messages):
        """
        调用外部API并返回响应结果
        :param messages: 聊天消息列表
        :return: API响应内容
        """
        url = 'https://internlm-chat.intern-ai.org.cn/puyu/api/v1/chat/completions'
        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Bearer " + YOUR_TOKEN_HERE
        }
        data = {
            "model": self.model_type,
            "messages": messages,
            "n": 1,
            "temperature": self.gen_params.get('temperature', 0.8),
            "top_p": self.gen_params.get('top_p', 0.9),
            "stream": False,
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API调用失败，状态码：{response.status_code}")

    def chat(self, messages, **kwargs):
        """
        聊天功能的实现
        :param messages: 聊天消息列表
        :return: 聊天内容
        """
        response = self.call_api(messages)
        content = response["choices"][0]["message"]["content"]
        return content

# Hook类，用于对消息添加前缀
class PrefixedMessageHook(Hook):
    def __init__(self, prefix, senders=None):
        """
        初始化Hook
        :param prefix: 消息前缀
        :param senders: 指定发送者列表
        """
        self.prefix = prefix
        self.senders = senders or []

    def before_agent(self, agent, messages, session_id):
        """
        在代理处理消息前修改消息内容
        :param agent: 当前代理
        :param messages: 消息列表
        :param session_id: 会话ID
        """
        for message in messages:
            if message.sender in self.senders:
                message.content = self.prefix + message.content

# 博客生成类，整合写作者和批评者
class AsyncBlogger:
    def __init__(self, model_type, writer_prompt, critic_prompt, critic_prefix='', max_turn=2):
        """
        初始化博客生成器
        :param model_type: 模型类型
        :param writer_prompt: 写作者提示词
        :param critic_prompt: 批评者提示词
        :param critic_prefix: 批评消息前缀
        :param max_turn: 最大轮次
        """
        self.llm = CustomAPILLM(model_type=model_type, temperature=0.8, top_p=0.9)
        self.plugins = [dict(type='lagent.actions.ArxivSearch')]
        self.writer = Agent(
            self.llm,
            writer_prompt,
            name='写作者',
            output_format=dict(
                type=PluginParser,
                template=PLUGIN_CN,
                prompt=get_plugin_prompt(self.plugins)
            )
        )
        self.critic = Agent(
            self.llm,
            critic_prompt,
            name='批评者',
            hooks=[PrefixedMessageHook(critic_prefix, ['写作者'])]
        )
        self.max_turn = max_turn

    async def forward(self, message: AgentMessage, update_placeholder):
        """
        执行多阶段博客生成流程
        :param message: 初始消息
        :param update_placeholder: Streamlit占位符
        :return: 最终优化的博客内容
        """
        # 占位符用于逐步显示各阶段结果
        step1_placeholder = update_placeholder.container()
        step2_placeholder = update_placeholder.container()
        step3_placeholder = update_placeholder.container()

        # 第一步：生成初始内容
        step1_placeholder.markdown("**Step 1: 生成初始内容...**")
        message = self.writer(message)
        if message.content:
            step1_placeholder.markdown(f"**生成的初始内容**:\n\n{message.content}")
        else:
            step1_placeholder.markdown("**生成的初始内容为空，请检查生成逻辑。**")

        # 第二步：批评者提供反馈
        step2_placeholder.markdown("**Step 2: 批评者正在提供反馈和文献推荐...**")
        message = self.critic(message)
        if message.content:
            # 解析批评者反馈
            suggestions = re.search(r"1\. 批评建议：\n(.*?)2\. 推荐的关键词：", message.content, re.S)
            keywords = re.search(r"2\. 推荐的关键词：\n- (.*)", message.content)
            feedback = suggestions.group(1).strip() if suggestions else "未提供批评建议"
            keywords = keywords.group(1).strip() if keywords else "未提供关键词"

            # Arxiv 文献查询
            arxiv_search = ArxivSearch()
            arxiv_results = arxiv_search.get_arxiv_article_information(keywords)

            # 显示批评内容和文献推荐
            message.content = f"**批评建议**:\n{feedback}\n\n**推荐的文献**:\n{arxiv_results}"
            step2_placeholder.markdown(f"**批评和文献推荐**:\n\n{message.content}")
        else:
            step2_placeholder.markdown("**批评内容为空，请检查批评逻辑。**")

        # 第三步：写作者根据反馈优化内容
        step3_placeholder.markdown("**Step 3: 根据反馈改进内容...**")
        improvement_prompt = AgentMessage(
            sender="critic",
            content=(
                f"根据以下批评建议和推荐文献对内容进行改进：\n\n"
                f"批评建议：\n{feedback}\n\n"
                f"推荐文献：\n{arxiv_results}\n\n"
                f"请优化初始内容，使其更加清晰、丰富，并符合专业水准。"
            ),
        )
        message = self.writer(improvement_prompt)
        if message.content:
            step3_placeholder.markdown(f"**最终优化的博客内容**:\n\n{message.content}")
        else:
            step3_placeholder.markdown("**最终优化的博客内容为空，请检查生成逻辑。**")

        return message

# Streamlit 用户界面
def main():
    """
    主函数：构建Streamlit界面并处理用户交互
    """
    st.set_page_config(layout='wide', page_title='Lagent Web Demo', page_icon='🤖')
    st.title("多代理博客优化助手")

    # Sidebar 输入
    model_type = st.sidebar.text_input('模型名称', 'internlm2.5-latest')
    topic = st.text_input('输入一个话题:', 'Self-Supervised Learning')
    generate_button = st.button('生成博客内容')

    if generate_button:
        blogger = AsyncBlogger(
            model_type=model_type,
            writer_prompt="你是一位优秀的AI内容写作者，请撰写一篇有吸引力且信息丰富的博客内容。",
            critic_prompt="""
                作为一位严谨的批评者，请给出建设性的批评和改进建议，并基于相关主题使用已有的工具推荐一些参考文献，推荐的关键词应该是英语形式，简洁且切题。。
                请按照以下格式提供反馈：
                1. 批评建议：
                - （具体建议）
                2. 推荐的关键词：
                - （关键词1, 关键词2, ...）
                """,
            critic_prefix="请批评以下内容，并提供改进建议：\n\n"
        )

        # 占位符用于逐步更新内容
        update_placeholder = st.empty()

        async def run_async_blogger():
            message = AgentMessage(
                sender='user',
                content=f"请撰写一篇关于{topic}的博客文章，要求表达专业，生动有趣，并且易于理解。"
            )
            result = await blogger.forward(message, update_placeholder)
            return result

        # 启动异步任务
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        final_message = loop.run_until_complete(run_async_blogger())

if __name__ == '__main__':
    main()
```

输入话题，比如`Semi-Supervised Learning`：

可以看到，Multi-Agents博客写作系统正在按照下面的3步骤，生成、批评和完善内容。

**Step 1**：写作者根据用户输入生成初稿。

**Step 2**：批评者对初稿进行评估，提供改进建议和文献推荐（通过关键词触发 Arxiv 文献搜索）。

**Step 3**：写作者根据批评意见对内容进行改进。

输入一个感兴趣的话题：

<img src="https://s1.imagehub.cc/images/2024/11/20/3d226bda74afd199fbc911bf7da1a018.png" alt="7d5ec89c1fb8ac7117c9e694d7208303" border="0" style="zoom:67%;" >

第一步生成的结果：

<img src="https://s1.imagehub.cc/images/2024/11/20/13f15190cdce7b5d343d9868ba528ec3.png" alt="0586d35b3ee4755a65988223dc4fc322" border="0" style="zoom:67%;" >

第二步批评和文献检索的结果：

<img src="C:\Users\cjy\Documents\Tencent Files\1726562224\nt_qq\nt_data\Pic\2024-11\Ori\65c4aad0b24d8e99e396369cc5bd8486.png" alt="65c4aad0b24d8e99e396369cc5bd8486" style="zoom:67%;" />

第三步最后完善的内容，可以看到其中包括了检索得到的文献，使得博客内容更加具有可信度。

<img src="https://s1.imagehub.cc/images/2024/11/20/16faa0c4718c372d1088293f814a1d33.png" alt="7f185a158313f525dccd4aa6b4a6c7ab" border="0" style="zoom:67%;" >

至此，我们完成了本节课所有内容，希望大家通过今天的学习，能够更加系统地掌握Agent和Multi-Agents的核心思想和实现方法，并在实际开发中灵活运用。🌟
