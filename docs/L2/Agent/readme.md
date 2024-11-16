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
<img src="https://github.com/InternLM/lagent/assets/24351120/cefc4145-2ad8-4f80-b88b-97c05d1b9d3e" alt="image" style="zoom: 25%;" />

### 2.2 常见工具调用能力范式

#### 2.2.1 通用智能体范式

这种范式强调模型无需依赖特定的特殊标记（special token）来定义工具调用的参数边界。模型依靠其强大的指令跟随与推理能力，在指定的 **system prompt** 框架下，根据任务需求自动生成响应。这种方式让模型在推理过程中能更灵活地适应多种任务，不需要对Tokenizer进行特殊设计。

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

**（1）InternLM2案例分析：** 工具调用使用了如`<|plugin|>`、`<|interpreter|>`、`<|action_start|>`和`<|action_end|>`等特殊标记，确保每个调用都符合指定的格式。模型在执行任务时，依靠这些标记与系统紧密协作，保障任务的精准执行。链接：[InternLM/agent at main · InternLM/InternLM](https://github.com/InternLM/InternLM/tree/main/agent)



## 3 动手实践

### 3.1环境配置

开发机选择 30% A100，镜像选择为 Cuda12.2-conda。

<img src="https://s1.imagehub.cc/images/2024/11/04/627cf2208192ad08cb2460f7c30fe21a.png" alt="image 20241023163215363" style="zoom:67%;" />

<img src="https://s1.imagehub.cc/images/2024/11/04/07551c110d9526bb3ee21aab74d11ab0.png" alt="image 20241023163141745" style="zoom:78%;" />

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
pip install lmdeploy==0.5.2
pip install streamlit==1.39.0
pip install class_registry==2.1.2
```

等待安装完成~
<div align="center">
<img src="https://s1.imagehub.cc/images/2024/11/04/d1c2046c82478ae703e08b0bc77a7de4.png" alt="image 20241023163511989" />
</div>

接下来，我们通过源码安装的方式安装 lagent。

```python
# 创建目录以存放代码
mkdir -p /root/agent_camp3
cd /root/agent_camp3
git clone https://github.com/InternLM/lagent.git
cd lagent && git checkout 81e7ace && pip install -e . && cd ..
pip install griffe==0.48.0
```

### 3.2 Single Agent的定义和使用

接下来，我们将使用 Lagent 的 Web Demo 来体验 InternLM2.5-7B-Chat 的智能体能力。

首先，我们先使用 LMDeploy 部署 InternLM2.5-7B-Chat，并启动一个 API Server。

```python
conda activate lagent
lmdeploy serve api_server /share/new_models/Shanghai_AI_Laboratory/internlm2_5-7b-chat --model-name internlm2_5-7b-chat
```

<img src="https://s1.imagehub.cc/images/2024/11/04/db5dfad3d6a6c45d1a93cbf4f8e4fa08.png" alt="image 20241023203712731" style="text-align: center;" />

然后，我们在**另一个窗口**中启动 Lagent 的 Web Demo。

```python
cd /root/agent_camp3/lagent
conda activate lagent
streamlit run examples/internlm2_agent_web_demo.py
```

<img src="https://s1.imagehub.cc/images/2024/11/04/fc83ff140cbb3f1532b581c730518880.png" alt="image 20241023204431832" style="zoom:200%;" />

在等待两个 server 都完全启动（如下图所示）后，我们在 **本地** 的 PowerShell 中输入如下指令来进行端口映射：

```bash
ssh -CNg -L 8501:127.0.0.1:8501 -L 23333:127.0.0.1:23333 root@ssh.intern-ai.org.cn -p <你的 SSH 端口号>
```

| LMDeploy api_server                                          | Lagent Web Demo                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| ![LMDeploy done](https://github.com/user-attachments/assets/820f4ceb-4337-484f-997b-001d5532816a) | ![Lagent done](https://github.com/user-attachments/assets/b9ccff2b-6e05-4c4e-b85b-860f8b9e2f41) |

接下来，在本地浏览器中打开 `localhost:8501`，并修改**模型名称**一栏为 `internlm2_5-7b-chat`，修改**模型 ip**一栏为`127.0.0.1:23333`。
<div align="center">
<img src="https://s1.imagehub.cc/images/2024/11/04/064bfe720e414a7ac0334b41b14bfaf9.png" width="400" />
</div>

<div align="center">
<img src="https://s1.imagehub.cc/images/2024/11/04/cef21569c07155551c01e277c22f0fd5.png" width="400" />
</div>

我们先试一下没有工具的时候，大模型搜索文献和整理的效果：

输入指令“帮我搜索一下最新版本的MindSearch论文”。（记得回车）

![image 20241023210141882](https://s1.imagehub.cc/images/2024/11/04/7a259d9b140dfad2f5af3d49c946f7da.png)发现模型输出了一篇并不存在的论文，出现了大模型幻觉。

然后，我们再在插件选择一栏选择 `ArxivSearch`，输入指令“帮我搜索一下 MindSearch 论文”。
<div align="center">
   <img src="https://s1.imagehub.cc/images/2024/11/04/7c7bac9f5d48f44f5bbf895ea24f6db2.png" width="400" />
</div>

<div align="center">
  <img src="https://s1.imagehub.cc/images/2024/11/04/89b9b096f24b3a8991121669b7b4ff60.png" width="400" />
</div>

可以看到大模型正确的找到了相关论文，并做了简单的内容总结。

### 3.3 制作一个属于自己的Single Agent

我们将在本节中实现一个实时天气查询插件，通过调用和风天气API工具，以完成实时天气查询的功能，并将其集成到 Lagent 的 Web Demo 中。由于默认情况下，LLM（尤其是私有部署的 LLM）无法获取实时数据，所以该插件能够显著扩展智能体的能力。

Lagent 框架的工具部分文档可以在此处查看：[Lagent 工具文档](https://lagent.readthedocs.io/zh-cn/latest/tutorials/action.html)。

使用 Lagent 自定义工具主要分为以下3步：

（1）继承 `BaseAction` 类

（2）实现简单工具的 `run` 方法；或者实现工具包内每个子工具的功能

（3）简单工具的 `run` 方法可选被 `tool_api` 装饰；工具包内每个子工具的功能都需要被 `tool_api` 装饰

**步骤1：** 创建脚步

首先，进入项目目录并创建新的 Python 文件来实现天气查询工具。

```python
conda activate lagent
cd /root/agent_camp3/lagent
touch lagent/actions/weather_query.py
```

然后，将下面的代码粘贴到 `/root/agent_camp3/lagent/lagent/actions/weather_query.py` 文件中。

**步骤2：** 获取 API KEY

为了使用和风天气的 API 服务，你需要获取一个 API Key。请按以下步骤操作：

（1）访问 [和风天气 API 文档](https://dev.qweather.com/docs/api/)（需要注册账号）。

（2）点击页面右上角的“控制台”。

（3）在控制台中，点击左侧的“项目管理”，然后点击右上角“创建项目”。

（4）输入项目名称（可以使用“Lagent”），选择免费订阅，并在“订阅方案”中选择“Web API”。

（5）创建后，回到“项目管理”页面，找到你的 API Key 并复制保存。

<img src="https://s1.imagehub.cc/images/2024/11/07/61e7a96c04e232652984a6abec9ff2da.png" alt="image" border="0" style="zoom: 50%;" >



**步骤3：** 设计工具

然后，将以下代码粘贴到 `/root/agent_camp3/lagent/lagent/actions/weather_query.py` 文件中：

```python
import requests
from lagent.actions.base_action import BaseAction, tool_api
from lagent.schema import ActionReturn, ActionStatusCode

class WeatherQuery(BaseAction):
    def __init__(self):
        super().__init__()
        # 替换为你的和风天气 API Key
        self.api_key = "YOUR_API_KEY"

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

注意要替换 YOUR_API_KEY 为你的和风天气 API KEY。

**步骤 4：** 修改 Web Demo 以适配自定义工具

接下来，我们将修改 Web Demo 脚本来集成自定义的 `WeatherQuery` 插件。

（1）**打开 `internlm2_agent_web_demo.py` 文件**

文件位置在/root/agent_camp3/lagent/examples/internlm2_agent_web_demo.py

（2）**导入 `WeatherQuery` 工具**

在以下行的后面，添加导入 `WeatherQuery`：

```python
from lagent.actions import ActionExecutor, ArxivSearch, IPythonInterpreter
from lagent.actions.weather_query import WeatherQuery  # 添加这一行
```

（3）**将 `WeatherQuery` 添加到 `action_list`**

找到 `action_list` 定义，并在列表中添加 `WeatherQuery()`：

```python
action_list = [
    ArxivSearch(),
    WeatherQuery()  # 添加这一行
]
```

<div align="center">
  <img src="https://s1.imagehub.cc/images/2024/11/07/2166392281fa0cbbce9b026ab4fe1929.png" width="400" />
</div>


接下来，启动 Web Demo 来体验一下吧！

记得修改**模型名称**一栏为 `internlm2_5-7b-chat`，修改**模型 ip**一栏为`127.0.0.1:23333`。我们同时启用两个工具。
<div align="center">
  <img src="https://s1.imagehub.cc/images/2024/11/07/3aeb6e9c46d64401243144bd7d3da75f.png" width="400" />
</div>

然后输入“今天南京的天气是怎么样的？”
<div align="center">
  <img src="https://s1.imagehub.cc/images/2024/11/07/5987712a8f1520739c58418a162efb92.png" width="600" />
</div>

这个时候再输入“帮我搜索一下最新版本的MindSearch论文”

可以看到，大模型能够清晰的根据不同的任务，使用不同的工具完成。
<div align="center">
  <img src="https://s1.imagehub.cc/images/2024/11/07/e2d7171463b1625cc1937e0a63970791.png" width="600" />
</div>

### 3.4 使用API自定义Single Agent

#### 3.4.1 浦语官方 API

以下是 **浦语官方 API** 完成天气信息查询功能的Python案例，需要替换和风天气 API Key、你的 InternLM API token和输入一个天气查询的问题。

在/root/agent_camp3/lagent/examples下创建一个weather_query_puyuapi.py

```cmd
conda activate lagent
touch /root/agent_camp3/lagent/examples/weather_query_puyuapi.py
```

并输入下面的代码内容：

```python
import requests
import json
YOUR_API_KEY = ""  # 替换为你的和风天气 API Key
YOUR_TOKEN = ""  # 替换为你的 InternLM API token
user_question = "今天南京的天气怎么样？" # 用户的问题

# 和风天气 API 工具 Agent
class WeatherAgent:
    def __init__(self, api_key):
        self.api_key = api_key
        self.weather_url = 'https://devapi.qweather.com/v7/weather/now'
        self.geo_url = 'https://geoapi.qweather.com/v2/city/lookup'

    def get_weather(self, location):
        try:
            # 检查 location 是否为经纬度坐标格式
            if not ("," in location and location.replace(",", "").replace(".", "").isdigit()):
                # 使用 GeoAPI 获取 LocationID
                geo_response = requests.get(f"{self.geo_url}?location={location}&key={self.api_key}")
                geo_data = geo_response.json()
                if geo_data.get("code") != "200" or not geo_data.get("location"):
                    raise Exception(f"GeoAPI 返回错误码：{geo_data.get('code')} 或未找到位置")
                # 使用第一个匹配的 LocationID
                location = geo_data["location"][0]["id"]

            # 使用 LocationID 查询天气信息
            weather_response = requests.get(f"{self.weather_url}?location={location}&key={self.api_key}")
            weather_data = weather_response.json()
            if weather_data.get("code") != "200":
                raise Exception(f"Weather API 返回错误码：{weather_data.get('code')}")

            # 返回解析后的天气信息
            return {
                "location": location,
                "weather": weather_data["now"]["text"],
                "temperature": f"{weather_data['now']['temp']}°C",
                "wind_direction": weather_data["now"]["windDir"],
                "wind_speed": f"{weather_data['now']['windSpeed']} km/h",
                "humidity": f"{weather_data['now']['humidity']}%",
                "report_time": weather_data["updateTime"]
            }

        except Exception as e:
            return {"error": str(e)}

# 初始化 WeatherAgent
weather_agent = WeatherAgent(api_key=YOUR_API_KEY) 

# InternLM API 配置
url = 'https://internlm-chat.intern-ai.org.cn/puyu/api/v1/chat/completions'
headers = {
    'Content-Type': 'application/json',
    "Authorization": "Bearer "+ YOUR_TOKEN 
}

# 智能工具选择 prompt
prompt = """
你是一个多功能助手，能够根据用户的需求提供帮助，包括回答一般问题和调用和风天气 API 获取实时天气信息。你的任务是：

1. **思考**：在收到用户问题后，首先进行思考，确定如何提供最有用的帮助。
2. **行动**：如果用户的问题涉及天气查询，你需要调用和风天气 API。明确指出要调用的函数 (action) 和输入参数 (action input)。
3. **隐藏内部状态**：在实际回答用户时，不要显示你的思考过程和调用细节，只提供简洁、自然且友好的答案。

### 回答格式：
- 如果用户的问题与天气有关，明确调用 API 并总结天气信息，用自然的语言回答用户。
- 如果用户的问题不需要调用 API，直接提供有用的回答。

### 示例：
用户问："今天北京的天气怎么样？"
你可以这样思考并采取行动：
- Thinking: 用户询问了北京的天气情况，我需要调用和风天气 API。
- Action: get_weather
- Action Input: {"location": "北京"}

### 最终输出给用户：
"今天北京的天气是晴，气温大约为20°C，风速为5 km/h，湿度为60%。希望这个信息对你有帮助！"

请确保你的最终回答简洁且易于理解，不包含内部状态或技术细节。
"""

# 准备请求数据
data = {
    "model": "internlm2.5-latest",
    "messages": [{"role": "user", "content": prompt + "\n用户：" + user_question}],
    "n": 1,
    "temperature": 0.8,
    "top_p": 0.9,
    "stream": False  # 设置为非流式请求
}

# 发送非流式请求
response = requests.post(url, headers=headers, data=json.dumps(data))
output = response.json()

# 处理大模型的输出
full_content = output["choices"][0]["message"]["content"]
print("模型输出:", full_content)

# 模型输出解析和执行
if "Action: get_weather" in full_content:
    # 从输出中提取参数
    action_input_start = full_content.find("Action Input: {")
    action_input_end = full_content.find("}", action_input_start) + 1
    action_input_str = full_content[action_input_start:action_input_end].replace("Action Input: ", "")
    action_input = json.loads(action_input_str)

    # 调用和风天气 API
    location = action_input["location"]
    weather_info = weather_agent.get_weather(location)
    if "error" in weather_info:
        print(f"Error: {weather_info['error']}")
    else:
        # 格式化天气信息
        weather_details = (
            f"地点：{weather_info['location']}\n"
            f"天气：{weather_info['weather']}\n"
            f"温度：{weather_info['temperature']}\n"
            f"风向：{weather_info['wind_direction']}\n"
            f"风速：{weather_info['wind_speed']}\n"
            f"湿度：{weather_info['humidity']}\n"
            f"报告时间：{weather_info['report_time']}"
        )
        print("\n--- 实时天气信息 ---")
        print(weather_details)

        # 准备总结请求
        follow_up_data = {
            "model": "internlm2.5-latest",
            "messages": [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": full_content},
                {"role": "user", "content": f"我已经获取了天气数据：\n{weather_details}\n请总结或提供进一步的帮助。"}
            ],
            "n": 1,
            "temperature": 0.8,
            "top_p": 0.9,
            "stream": False  # 设置为非流式请求
        }
        print("\n--- 大模型的输出 ---")
        # 发送总结请求
        follow_up_response = requests.post(url, headers=headers, data=json.dumps(follow_up_data))
        follow_up_output = follow_up_response.json()
        print("大模型:", follow_up_output["choices"][0]["message"]["content"])

```

执行`python /root/agent_camp3/lagent/examples/weather_query_puyuapi.py`，使用结果如下：

<img src="https://s1.imagehub.cc/images/2024/11/07/53d1db6475ba8a89e12c94d75ed85421.png" alt="image" border="0">

#### 3.4.2 硅基流动 API

以下是基于 **硅基流动 API** 完成天气信息查询功能的Python案例，需要替换和风天气 API Key、你的 InternLM API token和输入一个天气查询的问题。

在/root/agent_camp3/lagent/examples下创建一个weather_query_sfapi.py.py

```cmd
conda activate lagent
touch /root/agent_camp3/lagent/examples/weather_query_sfapi.py
```

并输入下面的代码内容：

```python
import requests
import json

YOUR_SILICONFLOW_TOKEN = ""  # 替换为你的 SiliconFlow API token
YOUR_API_KEY = ""  # 替换为你的和风天气 API Key
user_question = "今天南京的天气怎么样？" # 用户的问题

# 和风天气 API 工具 Agent
class WeatherAgent:
    def __init__(self, api_key):
        self.api_key = api_key
        self.weather_url = 'https://devapi.qweather.com/v7/weather/now'
        self.geo_url = 'https://geoapi.qweather.com/v2/city/lookup'

    def get_weather(self, location):
        try:
            # 检查 location 是否为经纬度坐标格式
            if not ("," in location and location.replace(",", "").replace(".", "").isdigit()):
                # 使用 GeoAPI 获取 LocationID
                geo_response = requests.get(f"{self.geo_url}?location={location}&key={self.api_key}")
                geo_data = geo_response.json()
                if geo_data.get("code") != "200" or not geo_data.get("location"):
                    raise Exception(f"GeoAPI 返回错误码：{geo_data.get('code')} 或未找到位置")
                # 使用第一个匹配的 LocationID
                location = geo_data["location"][0]["id"]

            # 使用 LocationID 查询天气信息
            weather_response = requests.get(f"{self.weather_url}?location={location}&key={self.api_key}")
            weather_data = weather_response.json()
            if weather_data.get("code") != "200":
                raise Exception(f"Weather API 返回错误码：{weather_data.get('code')}")

            # 返回解析后的天气信息
            return {
                "location": location,
                "weather": weather_data["now"]["text"],
                "temperature": f"{weather_data['now']['temp']}°C",
                "wind_direction": weather_data["now"]["windDir"],
                "wind_speed": f"{weather_data['now']['windSpeed']} km/h",
                "humidity": f"{weather_data['now']['humidity']}%",
                "report_time": weather_data["updateTime"]
            }

        except Exception as e:
            return {"error": str(e)}

# 初始化 WeatherAgent
weather_agent = WeatherAgent(api_key=YOUR_API_KEY)

# InternLM API 配置
url = "https://api.siliconflow.cn/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {YOUR_SILICONFLOW_TOKEN}",
    "Content-Type": "application/json"
}

# 智能工具选择 prompt
prompt = """
你是一个多功能助手，能够根据用户的需求提供帮助，包括回答一般问题和调用和风天气 API 获取实时天气信息。你的任务是：

1. **思考**：在收到用户问题后，首先进行思考，确定如何提供最有用的帮助。
2. **行动**：如果用户的问题涉及天气查询，你需要调用和风天气 API。明确指出要调用的函数 (action) 和输入参数 (action input)。
3. **隐藏内部状态**：在实际回答用户时，不要显示你的思考过程和调用细节，只提供简洁、自然且友好的答案。

### 回答格式：
- 如果用户的问题与天气有关，明确调用 API 并总结天气信息，用自然的语言回答用户。
- 如果用户的问题不需要调用 API，直接提供有用的回答。

### 示例：
用户问："今天北京的天气怎么样？"
你可以这样思考并采取行动：
- Thinking: 用户询问了北京的天气情况，我需要调用和风天气 API。
- Action: get_weather
- Action Input: {"location": "北京"}

### 最终输出给用户：
"今天北京的天气是晴，气温大约为20°C，风速为5 km/h，湿度为60%。希望这个信息对你有帮助！"

请确保你的最终回答简洁且易于理解，不包含内部状态或技术细节。
"""

# 准备请求数据
payload = {
    "model": "internlm/internlm2_5-7b-chat",
    "messages": [{"role": "user", "content": prompt + "\n用户：" + user_question}],
    "stream": False,
    "max_tokens": 512,
    "temperature": 0.7,
    "top_p": 0.7,
    "top_k": 50,
    "frequency_penalty": 0.5,
    "n": 1,
    "response_format": {"type": "text"}
}

# 发送请求到 SiliconFlow API
response = requests.post(url, headers=headers, json=payload)
output = response.json()

# 处理大模型的输出
full_content = output["choices"][0]["message"]["content"]
print("模型输出:", full_content)

# 模型输出解析和执行
if "Action: get_weather" in full_content:
    # 从输出中提取参数
    action_input_start = full_content.find("Action Input: {")
    action_input_end = full_content.find("}", action_input_start) + 1
    action_input_str = full_content[action_input_start:action_input_end].replace("Action Input: ", "")
    action_input = json.loads(action_input_str)

    # 调用和风天气 API
    location = action_input["location"]
    weather_info = weather_agent.get_weather(location)
    if "error" in weather_info:
        print(f"Error: {weather_info['error']}")
    else:
        # 格式化天气信息
        weather_details = (
            f"地点：{weather_info['location']}\n"
            f"天气：{weather_info['weather']}\n"
            f"温度：{weather_info['temperature']}\n"
            f"风向：{weather_info['wind_direction']}\n"
            f"风速：{weather_info['wind_speed']}\n"
            f"湿度：{weather_info['humidity']}\n"
            f"报告时间：{weather_info['report_time']}"
        )
        print("\n--- 实时天气信息 ---")
        print(weather_details)

        # 准备总结请求
        follow_up_data = {
            "model": "internlm/internlm2_5-7b-chat",
            "messages": [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": full_content},
                {"role": "user", "content": f"我已经获取了天气数据：\n{weather_details}\n请总结或提供进一步的帮助。"}
            ],
            "n": 1,
            "temperature": 0.7,
            "top_p": 0.7,
            "top_k": 50,
            "frequency_penalty": 0.5,
            "response_format": {"type": "text"}
        }
        print("\n--- 大模型的输出 ---")
        # 发送总结请求
        follow_up_response = requests.post(url, headers=headers, json=follow_up_data)
        follow_up_output = follow_up_response.json()
        print("大模型:", follow_up_output["choices"][0]["message"]["content"])
```

执行 `python /root/agent_camp3/lagent/examples/weather_query_sfapi.py`，使用结果如下：

<img src="https://s1.imagehub.cc/images/2024/11/07/1465fe557b390b411fd069986b856a28.png" alt="image" border="0">

### 3.5 Multiple Agents的定义和使用

在这一节中，我们将使用 **硅基流动 API** 来构建一个多智能体系统 (**Multi-Agent System**)，展示如何协调不同的智能代理完成内容生成和优化的任务。我们的多智能体系统由两个主要代理组成：

（1）**内容生成代理**：负责根据用户的提示生成一篇结构化、专业的文章或报告。

（2）**批评与优化代理**：负责审阅生成的内容，指出不足并优化，使文章更加完善。

首先，创建一个新的 Python 文件 `multi_agent_api.py`，并进入 `lagent` 环境：

```bash
touch /root/agent_camp3/lagent/examples/multi_agent_api.py
conda activate lagent
```

将以下代码粘贴到 `multi_agent_api.py` 中：

```python
import requests
import json

# 初始化 SiliconFlow API 配置
YOUR_SILICONFLOW_TOKEN = ""  # 替换为你的 SiliconFlow API token
url = "https://api.siliconflow.cn/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {YOUR_SILICONFLOW_TOKEN}",
    "Content-Type": "application/json"
}
# 用户输入提示
user_prompt = input("请输入您的提示：")

# Multi-Agent 系统
class MultiAgentSystem:
    def __init__(self, api_token):
        self.api_token = api_token
        self.url = url
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

    def generate_content(self, user_prompt):
        # 高级专业内容生成代理
        prompt = f"""
        你是一位专业的内容创作者，专注于撰写严谨且富有洞察力的文章或报告。请根据以下提示生成内容，并确保具备深度分析和结构化逻辑：
        
        提示：{user_prompt}
        
        请从多个角度探讨问题，并提供具体的见解和预测，以丰富文章的内容和深度。
        """
        payload = {
            "model": "internlm/internlm2_5-7b-chat",
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "max_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.9,
            "n": 1,
            "response_format": {"type": "text"}
        }
        response = requests.post(self.url, headers=self.headers, json=payload)
        output = response.json()
        content = output["choices"][0]["message"]["content"]
        return content

    def critique_and_optimize(self, content):
        # 高级批评与优化代理
        critique_prompt = f"""
        你是一位严谨的编辑，专注于内容的批评与优化。请仔细审阅以下内容，指出其中的不足之处，并优化文章，使其更具逻辑性、流畅性和专业性：
        
        内容：{content}
        
        请在优化时保留原文的核心观点，并增强表达的清晰度和文章的整体结构。
        """
        payload = {
            "model": "internlm/internlm2_5-20b-chat",
            "messages": [{"role": "user", "content": critique_prompt}],
            "stream": False,
            "max_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.9,
            "n": 1,
            "response_format": {"type": "text"}
        }
        response = requests.post(self.url, headers=self.headers, json=payload)
        output = response.json()
        optimized_content = output["choices"][0]["message"]["content"]
        return optimized_content

# 使用 Multi-Agent 系统
multi_agent_system = MultiAgentSystem(api_token=YOUR_SILICONFLOW_TOKEN)

# 第一步：生成初始内容
print("\n--- 发送给内容生成代理的提示 ---")
print(user_prompt)

generated_content = multi_agent_system.generate_content(user_prompt)
print("\n--- 生成的初始内容 ---")
print(generated_content)

# 第二步：批评与优化内容
print("\n--- 发送给批评与优化代理的内容 ---")
print(generated_content)

optimized_content = multi_agent_system.critique_and_optimize(generated_content)
print("\n--- 批评与优化后的内容 ---")
print(optimized_content)
```

执行 `python /root/agent_camp3/lagent/examples/weather_query_sfapi.py`，使用结果如下：

当运行程序时，你将看到以下步骤的输出：

（1）**初始提示**：程序会提示你输入一个内容提示，例如“讨论人工智能在未来10年发展前景”。

（2）**生成初始内容**：内容生成代理根据提示生成一篇文章或报告。

（3）**批评与优化**：批评与优化代理会对生成的内容进行审阅，并提供优化后的版本。

```diff
--- 发送给内容生成代理的提示 ---
讨论人工智能在未来10年发展前景

--- 生成的初始内容 ---
（生成的初始文章内容）

--- 发送给批评与优化代理的内容 ---
（生成的初始文章内容）

--- 批评与优化后的内容 ---
（批评与优化后的完善文章内容）
```

<img src="https://s1.imagehub.cc/images/2024/11/07/024e4ef84b70d2c48bb20ff9332ecba8.png" alt="image" border="0">

<img src="https://s1.imagehub.cc/images/2024/11/07/c211f2aae26f97e76609ce8d24397c17.png" alt="image" border="0">

除此之外，为了满足特定需求，我们可以进一步完善这个系统。通过定义两个工具代理，用于实时获取外部信息：

- **WeatherAgent**：通过调用和风天气 API，获取指定城市的最新天气信息。
- **ArxivAgent**：利用 Arxiv 的 API，检索与给定主题相关的学术论文。

首先，我们需要创建一个 Python 文件并设置好开发环境：

```
touch /root/agent_camp3/lagent/examples/multi_agent_api_v2.py
conda activate lagent
```

将以下代码粘贴到 `multi_agent_api_v2.py` 中：

```python
import requests
import json
import re  # 导入正则表达式模块
# 初始化 API 配置
YOUR_SILICONFLOW_TOKEN = "sk-ymfjislgoetubvwrqmlzbqnmsddgjphdbmhnjmubxsvfhaki"  # 替换为你的 SiliconFlow API token
YOUR_QWEATHER_API_KEY = "0ff8daa4364e42e384c4ae1461b88859"        # 替换为你的和风天气 API key

# 用户输入提示
user_prompt = input("请输入您想写作的主题：")

url = "https://api.siliconflow.cn/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {YOUR_SILICONFLOW_TOKEN}",
    "Content-Type": "application/json"
}

# 和风天气 API 工具 Agent
class WeatherAgent:
    def __init__(self, api_key):
        self.api_key = api_key
        self.weather_url = 'https://devapi.qweather.com/v7/weather/now'
        self.geo_url = 'https://geoapi.qweather.com/v2/city/lookup'

    def get_weather(self, location):
        try:
            geo_params = {
                "location": location,
                "key": self.api_key
            }
            geo_response = requests.get(self.geo_url, params=geo_params)
            geo_data = geo_response.json()
            if geo_data.get("code") != "200" or not geo_data.get("location"):
                raise Exception(f"GeoAPI 错误码：{geo_data.get('code')} 或未找到位置")
            location_id = geo_data["location"][0]["id"]

            weather_params = {
                "location": location_id,
                "key": self.api_key
            }
            weather_response = requests.get(self.weather_url, params=weather_params)
            weather_data = weather_response.json()
            if weather_data.get("code") != "200":
                raise Exception(f"Weather API 错误码：{weather_data.get('code')}")

            return {
                "location": location,
                "weather": weather_data["now"]["text"],
                "temperature": f"{weather_data['now']['temp']}°C",
                "wind_direction": weather_data["now"]["windDir"],
                "wind_speed": f"{weather_data['now']['windSpeed']} km/h",
                "humidity": f"{weather_data['now']['humidity']}%",
                "report_time": weather_data["updateTime"]
            }
        except Exception as e:
            return {"error": str(e)}

# Arxiv 查询工具 Agent
class ArxivAgent:
    def search_articles(self, query):
        import arxiv
        try:
            # 使用 arxiv.Search 进行搜索
            search = arxiv.Search(
                query=query,
                max_results=3,
                sort_by=arxiv.SortCriterion.Relevance  # 根据需要排序
            )
            results = [
                f"Published: {result.updated.date()}\n"
                f"Title: {result.title}\n"
                f"Authors: {', '.join(a.name for a in result.authors)}\n"
                f"Summary: {result.summary[:1500]}"
                for result in search.results()  # 使用 search.results() 获取结果
            ]
            return {"content": "\n\n".join(results) if results else "未找到相关论文"}
        except Exception as e:
            return {"error": str(e)}

# 多代理系统
class MultiAgentSystem:
    def __init__(self, api_token, weather_agent, arxiv_agent):
        self.api_token = api_token
        self.weather_agent = weather_agent
        self.arxiv_agent = arxiv_agent
        self.url = url
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

    def generate_content(self, user_prompt):
        # 内容生成代理
        system_prompt = """
        你是一位专业的内容创作者，专注于撰写严谨且富有洞察力的文章，具备使用多个工具的能力。

        你的任务：
        1. 生成内容：在用户提示的基础上，撰写严谨的文章。
        2. 识别需要外部信息的情况：如果文章涉及到实时信息（例如，今天的天气、最新的新闻等），或者需要获取学术论文，请调用相应的工具获取最新数据。
        3. 工具调用：如果你决定使用工具，请严格按照以下格式，且不要在 `Action:` 前添加任何额外的说明或符号。

        工具调用格式（必须独立成段）：

        ```
        Action: 工具名称
        Action Input: 工具输入参数（JSON 格式）
        ```

        可用工具：
        - 获取天气信息：
          工具名称：get_weather
          工具输入参数示例：{"location": "城市名"}
        - 搜索学术论文：
          工具名称：search_articles
          工具输入参数示例：{"query": "关键词"}

        注意事项：
        - 工具调用格式必须独立成段，且前后不应有其他内容。
        - 在最终提供给用户的内容中，不要包含工具调用指令，直接将工具获取到的信息融入文章。

        示例：
        如果你需要获取雅安的天气信息，请直接在文章中写：

        ```
        Action: get_weather
        Action Input: {"location": "雅安"}
        ```

        请开始你的写作。
        """
        user_message = f"提示：{user_prompt}"
        payload = {
            "model": "internlm/internlm2_5-20b-chat",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "stream": False,
            "max_tokens": 2048,
            "temperature": 0.7,
            "top_p": 0.9,
            "n": 1
        }
        response = requests.post(self.url, headers=self.headers, json=payload)
        output = response.json()
        return output["choices"][0]["message"]["content"]

    def generate_final_content(self, initial_content, tool_content1):
        # 最终内容生成代理
        system_prompt = """
        你是一位资深的内容创作者，擅长撰写严谨、富有洞察力且专业的文章。请根据以下提供的素材，创作一篇完整、连贯的中文文章。

        要求：
        - 深入理解并消化所提供的内容，将其有机地融入文章中，确保信息融合自然，不显突兀。
        - 保持文章的逻辑性和连贯性，使用过渡语句使内容衔接顺畅。
        - 采用专业的语言和表达方式，提升文章的深度和权威性。
        - **切勿**在文章中包含任何工具调用指令或多余的标记。

        以下是提供的素材：
        """
        user_message = f"初始文稿：\n{initial_content}\n\n工具返回的信息：\n{tool_content1}"

        payload = {
            "model": "internlm/internlm2_5-20b-chat",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "stream": False,
            "max_tokens": 2048,
            "temperature": 0.7,
            "top_p": 0.9,
            "n": 1
        }
        response = requests.post(self.url, headers=self.headers, json=payload)
        output = response.json()
        return output["choices"][0]["message"]["content"]

    def process_task(self, content):
        action_logs = []  # 用于记录执行的工具和结果
        pattern = r'Action:\s*(.*?)\s*\nAction Input:\s*(\{.*?\})'
        while True:
            match = re.search(pattern, content)
            if not match:
                break  # 没有更多的行动需要处理

            action_name = match.group(1).strip()
            action_input_str = match.group(2).strip()

            try:
                action_input = json.loads(action_input_str)
            except json.JSONDecodeError:
                replacement = "[Error: 无法解析输入参数]"
                content = content[:match.start()] + replacement + content[match.end():]
                continue

            # 根据 action_name 调用相应的工具
            if action_name == "get_weather":
                location = action_input.get("location")
                weather_info = self.weather_agent.get_weather(location)
                if "error" in weather_info:
                    replacement = f"[Error: {weather_info['error']}]"
                else:
                    # 将获取到的天气信息格式化为自然语言
                    replacement = (
                        f"{location}当前的天气状况为{weather_info['weather']}，"
                        f"温度为{weather_info['temperature']}，"
                        f"湿度为{weather_info['humidity']}，"
                        f"风向为{weather_info['wind_direction']}，"
                        f"风速为{weather_info['wind_speed']}。"
                    )
                action_logs.append({
                    "action": action_name,
                    "input": action_input,
                    "result": weather_info
                })
            elif action_name == "search_articles":
                query = action_input.get("query")
                arxiv_results = self.arxiv_agent.search_articles(query)
                if "error" in arxiv_results:
                    replacement = f"[Error: {arxiv_results['error']}]"
                else:
                    # 直接将检索到的论文摘要插入内容
                    replacement = arxiv_results["content"]
                action_logs.append({
                    "action": action_name,
                    "input": action_input,
                    "result": arxiv_results
                })
            else:
                replacement = "[未识别的行动]"
                action_logs.append({
                    "action": action_name,
                    "input": action_input,
                    "result": "未识别的行动"
                })

            # 替换内容中的行动部分
            content = content[:match.start()] + replacement + content[match.end():]

        # 调用模型生成最终的内容
        final_content = self.generate_final_content(content)
        return final_content, action_logs

    def critique_and_optimize(self, content):
        # 批评与优化代理
        system_prompt = """
        你是一位严谨的编辑，专注于优化文章。你的任务是：

        1. 批评：仔细阅读作者的内容，找出逻辑性和流畅性的问题。
        2. 优化：在保留核心观点的前提下，提升文章的质量。

        请开始你的优化。
        """
        user_message = f"待优化的内容：\n{content}"
        payload = {
            "model": "internlm/internlm2_5-20b-chat",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "stream": False,
            "max_tokens": 2048,
            "temperature": 0.7,
            "top_p": 0.9,
            "n": 1
        }
        response = requests.post(self.url, headers=self.headers, json=payload)
        output = response.json()
        return output["choices"][0]["message"]["content"]

    def process_task(self, content):
        action_logs = []  # 用于记录执行的工具和结果
        # 修改后的正则表达式，允许在 Action: 前有其他内容
        pattern = r'(?s)(?:.*?)(?:^|\n)Action:\s*(.*?)\s*\nAction Input:\s*(\{.*?\})'
        while True:
            match = re.search(pattern, content)
            if not match:
                break  # 没有更多的行动需要处理

            action_name = match.group(1).strip()
            action_input_str = match.group(2).strip()

            try:
                action_input = json.loads(action_input_str)
            except json.JSONDecodeError:
                replacement = "[Error: 无法解析输入参数]"
                content = content[:match.start()] + replacement + content[match.end():]
                continue

            # 根据 action_name 调用相应的工具
            if action_name == "get_weather":
                location = action_input.get("location")
                weather_info = self.weather_agent.get_weather(location)
                if "error" in weather_info:
                    replacement = f"[Error: {weather_info['error']}]"
                else:
                    # 将获取到的天气信息格式化为自然语言
                    replacement = (
                        f"{location}当前的天气状况为{weather_info['weather']}，"
                        f"温度为{weather_info['temperature']}，"
                        f"湿度为{weather_info['humidity']}，"
                        f"风向为{weather_info['wind_direction']}，"
                        f"风速为{weather_info['wind_speed']}。"
                    )
                action_logs.append({
                    "action": action_name,
                    "input": action_input,
                    "result": weather_info
                })
            elif action_name == "search_articles":
                query = action_input.get("query")
                arxiv_results = self.arxiv_agent.search_articles(query)
                if "error" in arxiv_results:
                    replacement = f"[Error: {arxiv_results['error']}]"
                else:
                    # 直接将检索到的论文摘要插入内容
                    replacement = arxiv_results["content"]
                action_logs.append({
                    "action": action_name,
                    "input": action_input,
                    "result": arxiv_results
                })
            else:
                replacement = "[未识别的行动]"
                action_logs.append({
                    "action": action_name,
                    "input": action_input,
                    "result": "未识别的行动"
                })

            # 替换内容中的行动部分
            content = content[:match.start()] + replacement + content[match.end():]

        return content, action_logs

# 初始化 Agents
weather_agent = WeatherAgent(api_key=YOUR_QWEATHER_API_KEY)
arxiv_agent = ArxivAgent()
multi_agent_system = MultiAgentSystem(
    api_token=YOUR_SILICONFLOW_TOKEN,
    weather_agent=weather_agent,
    arxiv_agent=arxiv_agent,
)

# 第一步：生成初始内容
print("\n--- 生成的初始内容 ---")
generated_content = multi_agent_system.generate_content(user_prompt)
print(generated_content)

# 第二步：生成完整的内容
print("\n--- 生成工具的内容 ---")
tool_content, action_logs = multi_agent_system.process_task(generated_content)
print(tool_content)

print("\n--- 生成完整的内容 ---")
content = multi_agent_system.generate_final_content(generated_content, tool_content)
print(content)

# 第三步：批评与优化内容
print("\n--- 批评与优化后的内容 ---")
optimized_content = multi_agent_system.critique_and_optimize(content)
print(optimized_content)

# 打印执行的工具和结果
if action_logs:
    print("\n--- 执行的工具和结果 ---")
    for log in action_logs:
        print(f"执行的工具: {log['action']}")
        print(f"输入参数: {log['input']}")
        print(f"结果: {log['result']}\n")
```
现在整个多智能体的流程如下：

- **内容生成：** 会基于用户的提示撰写初稿，并分析是否需要额外的信息支持（如天气或学术研究）。
- **工具调用：** 如果需要外部数据，会触发 **工具代理**，获取最新信息并融入到内容中。
- **批评与优化代理：** 最后对文章进行全面优化，确保逻辑严谨、语言优美。

执行 `python /root/agent_camp3/lagent/examples/multi_agent_api_v2.py`，输入例如`vision transformer`使用结果如下：

<img src="https://s1.imagehub.cc/images/2024/11/07/76673651706a5ff1dc52f02d6df219e4.png" alt="ookk" border="0">

