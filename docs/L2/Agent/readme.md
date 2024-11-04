# Lagent：从零搭建你的 Multi-Agent 

## 一、相关知识点说明

### 1.1 Agent基本介绍

#### 1.1.1 什么是Agent

Agent是**一种能够自主感知环境并根据感知结果采取行动的实体**，以感知序列为输入，以动作作为输出的函数。它可以以软件形式（如聊天机器人、推荐系统）存在，也可以是物理形态的机器（如自动驾驶汽车、机器人）。

基本特性：

- **自主性**：能够在没有外部干预的情况下做出决策。
- **交互性**：能够与环境交换信息。
- **适应性**：根据环境变化调整自身行为。
- **目的性**：所有行为都以实现特定目标为导向。

<img src="https://s1.imagehub.cc/images/2024/11/04/eac389cdf83fd305c7131d7f208ad578.png" alt="FVQA 第 2 页.drawio" style="zoom: 33%;" />

#### 1.1.2 Agent的应用场景

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

### 1.2 Lagent 介绍

#### 1.2.1 基础介绍

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

<img src="https://github.com/InternLM/lagent/assets/24351120/cefc4145-2ad8-4f80-b88b-97c05d1b9d3e" alt="image" style="zoom:33%;" />

#### 1.2.2 常见工具调用能力范式

##### 1.2.2.1 通用智能体范式

这种范式强调模型无需依赖特定的特殊标记（special token）来定义工具调用的参数边界。模型依靠其强大的指令跟随与推理能力，在指定的**system prompt**框架下，根据任务需求自动生成响应。这种方式让模型在推理过程中能更灵活地适应多种任务，不需要对Tokenizer进行特殊设计。

**优势**：

1. 灵活适应不同任务，无需设计和维护复杂的标记系统。
2. 适合快速迭代，降低微调和部署的复杂性。
3. 更易与多模态输入（如文本和图像）结合，扩展模型的通用性。

**劣势**：

1. 由于没有明确标记，调用工具时的错误难以捕捉和纠正。
2. 在复杂任务中，模型生成可能不够精准，导致工具调用的准确性下降。

**（1）ReAct**：将模型的推理分为**Reason**和**Action**两个步骤，并让它们交替执行，直到得到最终结果：

- **Reason**：生成分析步骤，解释当前任务的上下文或状态，帮助模型理解下一步行动的逻辑依据。
- **Action**：基于Reason的结果，生成具体的工具调用请求（如查询搜索引擎、调用API、数据库检索等），将模型的推理转化为行动。

**（2）ReWoo**：全称为**Reason without Observation**，是在ReAct范式基础上进行改进的Agent架构，针对多工具调用的复杂性与冗余性提供了一种高效的解决方案。相比于ReAct中的交替推理和行动，ReWoo直接生成一次性使用的**完整工具链**，减少了不必要的Token消耗和执行时间。同时，由于工具调用的规划与执行解耦，这一范式在模型微调时不需要实际调用工具即可完成。

- **Planner**：用户输入的问题或任务首先传递给Planner，Planner将其分解为多个逻辑上相关的计划。每个计划包含推理部分（Reason）以及工具调用和参数（Execution）。Task List按顺序列出所有需要执行的任务链。
- **Worker**：每个Worker根据Task List中的子任务，调用指定工具并返回结果。所有Worker之间通过共享状态保持任务执行的连续性。
- **Solver阶段**：Worker完成任务后，将所有结果同步到Solver。Solver会对这些结果进行整合，并生成最终的答案或解决方案返回给用户。

##### 1.2.2.2 模型特化智能体范式

在这种范式下，模型的工具调用必须通过特定的**special token**明确标记。如InternLM2使用`<|action_start|>`和`<|action_end|>`来定义调用边界。这些标记通常与模型的Tokenizer深度集成，确保在执行特定任务时，能够准确捕捉调用信息并执行。

**优势**：

1. 特定标记明确工具调用的起止点，提高了调用的准确性。
2. 有助于模型在部署过程中避免误调用，增强系统的可控性。
3. 提高对复杂调用链的支持，适合复杂任务的场景。

**劣势**：

1. 需要对Tokenizer和模型架构进行定制，增加开发和维护成本。
2. 调用流程固定，降低了模型的灵活性，难以适应快速变化的任务。

**（1）InternLM2案例分析：**工具调用使用了如`<|plugin|>`、`<|interpreter|>`、`<|action_start|>`和`<|action_end|>`等特殊标记，确保每个调用都符合指定的格式。模型在执行任务时，依靠这些标记与系统紧密协作，保障任务的精准执行。链接：[InternLM/agent at main · InternLM/InternLM](https://github.com/InternLM/InternLM/tree/main/agent)



## 二、动手实践

### 2.1环境配置

开发机选择 30% A100，镜像选择为 Cuda12.2-conda。

![image 20241023163215363](https://s1.imagehub.cc/images/2024/11/04/627cf2208192ad08cb2460f7c30fe21a.png)

![image 20241023163141745](https://s1.imagehub.cc/images/2024/11/04/07551c110d9526bb3ee21aab74d11ab0.png)
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

![image 20241023163511989](https://s1.imagehub.cc/images/2024/11/04/d1c2046c82478ae703e08b0bc77a7de4.png)

接下来，我们通过源码安装的方式安装 lagent。

```python
# 创建目录以存放代码
mkdir -p /root/agent_camp3
cd /root/agent_camp3
git clone https://github.com/InternLM/lagent.git
cd lagent && git checkout 81e7ace && pip install -e . && cd ..
pip install griffe==0.48.0
```

### 2.2 Single Agent的定义和使用

接下来，我们将使用 Lagent 的 Web Demo 来体验 InternLM2.5-7B-Chat 的智能体能力。

首先，我们先使用 LMDeploy 部署 InternLM2.5-7B-Chat，并启动一个 API Server。

```python
conda activate lagent
lmdeploy serve api_server /share/new_models/Shanghai_AI_Laboratory/internlm2_5-7b-chat --model-name internlm2_5-7b-chat
```

![image 20241023203712731](https://s1.imagehub.cc/images/2024/11/04/db5dfad3d6a6c45d1a93cbf4f8e4fa08.png)

然后，我们在**另一个窗口**中启动 Lagent 的 Web Demo。

```python
cd /root/agent_camp3/lagent
conda activate lagent
streamlit run examples/internlm2_agent_web_demo.py
```

![image 20241023204431832](https://s1.imagehub.cc/images/2024/11/04/fc83ff140cbb3f1532b581c730518880.png)

在等待两个 server 都完全启动（如下图所示）后，我们在 **本地** 的 PowerShell 中输入如下指令来进行端口映射：

```bash
ssh -CNg -L 8501:127.0.0.1:8501 -L 23333:127.0.0.1:23333 root@ssh.intern-ai.org.cn -p <你的 SSH 端口号>
```

| LMDeploy api_server                                          | Lagent Web Demo                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| ![LMDeploy done](https://github.com/user-attachments/assets/820f4ceb-4337-484f-997b-001d5532816a) | ![Lagent done](https://github.com/user-attachments/assets/b9ccff2b-6e05-4c4e-b85b-860f8b9e2f41) |

接下来，在本地浏览器中打开 `localhost:8501`，并修改**模型名称**一栏为 `internlm2_5-7b-chat`，修改**模型 ip**一栏为`127.0.0.1:23333`。

![image 20241023205534674](https://s1.imagehub.cc/images/2024/11/04/064bfe720e414a7ac0334b41b14bfaf9.png)

<img src="https://s1.imagehub.cc/images/2024/11/04/cef21569c07155551c01e277c22f0fd5.png" alt="image 20241023205602182" style="zoom:67%;" />

我们先试一下没有工具的时候，大模型搜索文献和整理的效果：

输入指令“帮我搜索一下最新版本的MindSearch论文”。（记得回车）

![image 20241023210141882](https://s1.imagehub.cc/images/2024/11/04/7a259d9b140dfad2f5af3d49c946f7da.png)发现模型输出了一篇并不存在的论文，出现了大模型幻觉。

然后，我们再在插件选择一栏选择 `ArxivSearch`，输入指令“帮我搜索一下 MindSearch 论文”。

![image 20241023205945616](https://s1.imagehub.cc/images/2024/11/04/7c7bac9f5d48f44f5bbf895ea24f6db2.png)

![image 20241023210342221](https://s1.imagehub.cc/images/2024/11/04/89b9b096f24b3a8991121669b7b4ff60.png)



可以看到大模型正确的找到了相关论文，并做了简单的内容总结。

### 2.3 Multiple Agents的定义和使用

