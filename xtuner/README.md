![m3qx](imgs/head2.png)

> 怎么说呢，祝大家炼丹愉快吧~ 😙

## 1 概述

### 1.1 XTuner

一个大语言模型微调工具箱。*由* *MMRazor* *和* *MMDeploy* *联合开发。*

### 1.2 支持的开源LLM (2023.11.01)

- **[InternLM](https://huggingface.co/internlm/internlm-7b)** ✅
- [Llama，Llama2](https://huggingface.co/meta-llama)
- [ChatGLM2](https://huggingface.co/THUDM/chatglm2-6b)，[ChatGLM3](https://huggingface.co/THUDM/chatglm3-6b-base)
- [Qwen](https://huggingface.co/Qwen/Qwen-7B)
- [Baichuan](https://huggingface.co/baichuan-inc/Baichuan-7B)，[Baichuan2](https://huggingface.co/baichuan-inc/Baichuan2-7B-Base)
- ......
- [Zephyr](https://huggingface.co/HuggingFaceH4/zephyr-7b-beta) 

### 1.3 特色 

- 🤓 **傻瓜化：** 以 配置文件 的形式封装了大部分微调场景，**0基础的非专业人员也能一键开始微调**。
- 🍃 **轻量级：** 对于 7B 参数量的LLM，**微调所需的最小显存仅为 8GB** ： **消费级显卡✅，colab✅**

### 1.4 微调原理

> 想象一下，你有一个超大的玩具，现在你想改造这个超大的玩具。但是，**对整个玩具进行全面的改动会非常昂贵**。

※ 因此，你找到了一种叫 **LoRA** 的方法：**只对玩具中的某些零件进行改动，而不是对整个玩具进行全面改动**。

※ 而 **QLoRA** 是 LoRA 的一种改进：如果你手里只有一把生锈的螺丝刀，也能改造你的玩具。

- **Full** :       😳 → 🚲
- **[LoRA](http://arxiv.org/abs/2106.09685)** :     😳 → 🛵
- **[QLoRA](http://arxiv.org/abs/2305.14314)** :   😳 → 🏍

![WOZJXUtaKlEk9S4.png](imgs/cat_fly.png)

## 2 快速上手

首先我们可以通过下面这张图来简单了解一下 XTuner 的运行原理。

<img width="3216" alt="XTunerFlow1" src="https://github.com/InternLM/Tutorial/assets/108343727/0c4817e8-ddaf-4276-ad16-b65d5ec6b4ae">

1. **环境安装**：假如我们想要用 XTuner 这款简单易上手的微调工具包来对模型进行微调的话，那我们最最最先开始的第一步必然就是安装XTuner！安装基础的工具是一切的前提，只有安装了 XTuner 在我们本地后我们才能够去思考说具体怎么操作。

2. **前期准备**：那在完成了安装后，我们下一步就需要去明确我们自己的微调目标了。我们想要利用微调做一些什么事情呢，那我为了做到这个事情我有哪些硬件的资源和数据呢？假如我们有对于一件事情相关的数据集，并且我们还有足够的算力资源，那当然微调就是一件水到渠成的事情。就像 OpenAI 不就是如此吗？但是对于普通的开发者而言，在资源有限的情况下，我们可能就需要考虑怎么采集数据，用什么样的手段和方式来让模型有更好的效果。

3. **启动微调**：在确定了自己的微调目标后，我们就可以在 XTuner 的配置库中找到合适的配置文件并进行对应的修改。修改完成后即可一键启动训练！训练好的模型也可以仅仅通过在终端输入一行指令来完成转换和部署工作！

是不是感觉我上我也行？那下面我们就让我们来上手尝试一下整个的流程吧！

### 2.1 环境安装
首先我们需要先安装一个 XTuner 的源码到本地来方便后续的使用。
```bash
# 进入环境后首先 bash
bash
# 如果你是在 InternStudio 平台，则从本地 clone 一个已有 pytorch 2.0.1 的环境：
# /root/share/install_conda_env_internlm_base.sh xtuner0.1.15
# 如果你是在其他平台：
conda create --name xtuner0.1.15 python=3.10 -y

# 激活环境
conda activate xtuner0.1.15
# 进入家目录 （~的意思是 “当前用户的home路径”）
cd ~
# 创建版本文件夹并进入，以跟随本教程
mkdir xtuner0115 && cd xtuner0115

# 拉取 0.1.9 的版本源码
git clone -b v0.1.15  https://github.com/InternLM/xtuner
# 无法访问github的用户请从 gitee 拉取:
# git clone -b v0.1.15 https://gitee.com/Internlm/xtuner

# 进入源码目录
cd xtuner

# 从源码安装 XTuner
pip install -e '.[all]'
```
假如在这一过程中没有出现任何的报错的话，那也就意味着我们成功安装好支持 XTuner 所运行的环境啦。其实对于很多的初学者而言，安装好环境意味着成功了一大半！因此我们接下来就可以进入我们的第二步，准备好我们需要的数据集、模型和配置文件！
### 2.2 前期准备

在成功安装 XTuner 后，我们就可以根据自己的目标来思考模型、数据集和微调方法的选择啦。为了能够让大家更加快速的上手并看到微调前后对比的效果，那我这里选用的就是上一期的课后作业：用 `QLoRA` 的方式来微调一个自己的小助手！我们可以通过下面两张图片来清楚的看到两者的对比。



| 微调前   | 微调后          |
| -------- | --------------- |
| ![image1](https://github.com/InternLM/Tutorial/assets/108343727/f51733bc-b280-40f3-9ba9-505963809bd5) | ![image2](https://github.com/InternLM/Tutorial/assets/108343727/6555581f-6b2e-4d94-8838-e5840d8e24b6) |

#### 2.2.1 数据集准备

为了让模型能够让模型认清自己的身份弟位，知道在询问自己是谁的时候回复成我们想要的样子，我们就需要通过在微调数据集中大量掺杂这部分的数据。

首先我们先创建一个文件夹来存放我们这次训练所需要的所有文件。

```bash
# 前半部分是创建一个文件夹，后半部分是进入该文件夹。

mkdir /root/ft && cd /root/ft
# 在ft这个文件夹里再创建一个存放数据的data文件夹
mkdir data && cd data
```

之后我们可以在`data`目录下新建一个generate_data.py文件，将以下代码复制进去，然后运行该脚本即可生成数据集。假如想要加大剂量让他能够完完全全认识到你的身份，那我们可以吧 n 的值调大一点。

```bash
# 创建 generate_data.py 文件
touch generate_data.py
```

打开该 python 文件后将下面的内容复制进去。

```python
import json

# 设置用户的名字
name = '不要姜葱蒜大佬'
# 设置需要重复添加的数据次数
n = 5000

# 初始化OpenAI格式的数据结构
data = [
    {
        "messages": [
            {
                "role": "user",
                "content": "请做一下自我介绍"
            },
            {
                "role": "assistant",
                "content": "我是{}的小助手，内在是上海AI实验室书生·浦语的1.8B大模型哦".format(name)
            }
        ]
    }
]

# 通过循环，将初始化的对话数据重复添加到data列表中
for i in range(n):
    data.append(data[0])

# 将data列表中的数据写入到一个名为'personal_assistant.json'的文件中
with open('personal_assistant.json', 'w', encoding='utf-8') as f:
    # 使用json.dump方法将数据以JSON格式写入文件
    # ensure_ascii=False 确保中文字符正常显示
    # indent=4 使得文件内容格式化，便于阅读
    json.dump(data, f, ensure_ascii=False, indent=4)

```

并将`name`后面的内容修改为你的名称。比如说我是剑锋大佬的话就是：
```diff
# 将对应的name进行修改

- name = '不要姜葱蒜大佬'
+ name = "剑锋大佬"
```

修改完成后运行 generate_data.py 文件即可。

``` bash
python generate_data.py
```
可以看到在data的路径下便生成了一个名为 `personal_assistant.json` 的文件，这样我们最可用于微调的数据集就准备好啦！里面就包含了5000条 `input` 和 `output` 的数据对。

```
|-- data/
    |-- personal_assistant.json
    |-- generate_data.py
```
那除了我们自己通过脚本的数据集，其实网上也有大量的开源数据集可以供我们进行使用。有些时候我们可以在开源数据集的基础上添加一些我们自己独有的数据集，也可能会有很好的效果。

#### 2.2.2 模型准备

在准备好了数据集后，接下来我们就需要准备好我们的要用于微调的模型。由于本次课程显存方面的限制，这里我们就使用 InternLM 最新推出的小模型 InterLM-chat-1.8B 来完成此次的微调演示。

对于在 InternStudio 上运行的小伙伴们，可以不用通过 OpenXLab 或者 Modelscope 进行模型的下载。我们直接通过以下代码一键创建文件夹并将所有文件复制进去。

``` bash
# 创建目标文件夹，确保它存在。-p选项意味着如果上级目录不存在也会一并创建，且如果目标文件夹已存在则不会报错。
mkdir -p /root/ft/model

# 复制内容到目标文件夹。-r选项表示递归复制整个文件夹。
cp -r /root/share/new_models/Shanghai_AI_Laboratory/internlm2-chat-1_8b/* /root/ft/model/
```
那这个时候我们就可以看到在 model 文件夹下保存了模型的相关文件和内容了。
```
|-- model/
    |-- tokenizer.model
    |-- config.json
    |-- tokenization_internlm2.py
    |-- model-00002-of-00002.safetensors
    |-- tokenizer_config.json
    |-- model-00001-of-00002.safetensors
    |-- model.safetensors.index.json
    |-- configuration.json
    |-- special_tokens_map.json
    |-- modeling_internlm2.py
    |-- README.md
    |-- configuration_internlm2.py
    |-- generation_config.json
    |-- tokenization_internlm2_fast.py
```

#### 2.2.3 配置文件选择
在准备好了模型和数据集后，我们就要根据我们选择的微调方法方法结合前面的信息来找到与我们最匹配的配置文件了，从而减少我们对配置文件的修改量。

所谓配置文件（config），其实是一种用于定义和控制模型训练和测试过程中各个方面的参数和设置的工具。准备好的配置文件只要运行起来就代表着模型就开始训练或者微调了。

XTuner 提供多个开箱即用的配置文件，用户可以通过下列命令查看：
> 开箱即用意味着假如能够连接上 Huggingface 以及有足够的显存，其实就可以直接运行这些配置文件，XTuner就能够直接下载好这些模型和数据集然后开始进行微调

```Bash
# 列出所有内置配置文件
# xtuner list-cfg

# 假如我们想找到 internlm2-1.8b 模型里支持的配置文件
xtuner list-cfg -p internlm2_1_8b
```
> 这里就用到了第一个 XTuner 的工具 `list-cfg` ，对于这个工具而言，可以选择不添加额外的参数，就像上面的一样，这样就会将所有的配置文件都打印出来。那同时也可以加上一个参数 `-p` 或 `--pattern` ，后面输入的内容将会在所有的 config 文件里进行模糊匹配搜索，然后返回最有可能得内容。我们可以用来搜索特定模型的配置文件，比如例子中的 internlm2_1_8b ,也可以用来搜索像是微调方法 qlora 。

根据上面的定向搜索指令可以看到目前只有两个支持 internlm2-1.8 的模型配置文件。
```
==========================CONFIGS===========================
PATTERN: internlm2_1_8b
-------------------------------
internlm2_1_8b_full_alpaca_e3
internlm2_1_8b_qlora_alpaca_e3
=============================================================
```
<details>
<summary>配置文件名的解释</summary>

以 **internlm2_1_8b_qlora_alpaca_e3** 举例：

| 模型名   | 说明          |
| -------- | ------------- |
| internlm2_1_8b | 模型名称 |
| qlora    | 使用的算法     |
| alpaca   | 数据集名称     |
| e3       | 把数据集跑3次  |

</details>

虽然我们用的数据集并不是 `alpaca` 而是我们自己通过脚本制作的小助手数据集 ，但是由于我们是通过 `QLoRA` 的方式对 `internlm-chat-1.8b` 进行微调。而最相近的配置文件应该就是 `internlm2_1_8b_qlora_alpaca_e3` ，因此我们可以选择拷贝这个配置文件到当前目录：
```Bash
# 创建一个存放 config 文件的文件夹
mkdir -p /root/ft/config

# 使用 XTuner 中的 copy-cfg 功能将 config 文件复制到指定的位置
xtuner copy-cfg internlm2_1_8b_qlora_alpaca_e3 /root/ft/config
```
> 这里我们就用到了 XTuner 工具箱中的第二个工具 `copy-cfg` ，该工具有两个必须要填写的参数 `{CONFIG_NAME}` 和 `{SAVE_PATH}` ，在我们的输入的这个指令中，我们的 `{CONFIG_NAME}` 对应的是上面搜索到的 `internlm2_1_8b_qlora_alpaca_e3` ,而 `{SAVE_PATH}` 则对应的是刚刚新建的 `/root/ft/config`。我们假如需要复制其他的配置文件只需要修改这两个参数即可实现。

输入后我们就能够看到在我们的 `/root/ft/config` 文件夹下有一个名为 `internlm2_1_8b_qlora_alpaca_e3_copy.py` 的文件了。
```
|-- config/
    |-- internlm2_1_8b_qlora_alpaca_e3_copy.py
```
#### 2.2.4 小结
完成以上内容后，我就已经完成了所有的准备工作了。我们再来回顾一下我们做了哪些事情：
1. 我们首先是在 GitHub 上克隆了 XTuner 的源码，并把相关的配套库也通过 pip 的方式进行了安装。
2. 然后我们根据自己想要做的事情，利用脚本准备好了一份关于调教模型认识自己身份弟位的数据集。
3. 再然后我们根据自己的显存及任务情况确定了使用 InternLM-chat-1.8B 这个模型，并且将其复制到我们的文件夹里。
4. 最后我们在 XTuner 已有的配置文件中，根据微调方法、数据集和模型挑选出最合适的配置文件并复制到我们新建的文件夹中。

经过了以上的步骤后，我们的 `ft` 文件夹里应该是这样的：
```
|-- ft/
    |-- config/
        |-- internlm2_1_8b_qlora_alpaca_e3_copy.py
    |-- model/
        |-- tokenizer.model
        |-- config.json
        |-- tokenization_internlm2.py
        |-- model-00002-of-00002.safetensors
        |-- tokenizer_config.json
        |-- model-00001-of-00002.safetensors
        |-- model.safetensors.index.json
        |-- configuration.json
        |-- special_tokens_map.json
        |-- modeling_internlm2.py
        |-- README.md
        |-- configuration_internlm2.py
        |-- generation_config.json
        |-- tokenization_internlm2_fast.py
    |-- data/
        |-- personal_assistant.json
        |-- generate_data.py
```
是不是感觉其实微调也不过如此！事实上确实是这样的！其实在微调的时候最重要的还是要自己准备一份高质量的数据集，这个才是你能否真微调出效果最核心的利器。

微调也经常被戏称为是炼丹，就是说你炼丹的时候你得思考好用什么样的材料、用多大的火候、烤多久的时间以及用什么丹炉去烧。这里的丹炉其实我们可以想象为 XTuenr ，只要丹炉的质量过得去，炼丹的时候不会炸，一般都是没问题的。但是假如炼丹的材料（就是数据集）本来就是垃圾，那无论怎么炼（微调参数的调整），炼多久（训练的轮数），炼出来的东西还只能且只会是垃圾。只有说用了比较好的材料，那么我们就可以考虑说要炼多久以及用什么办法去炼的问题。因此总的来说，学会如何构建一份高质量的数据集是至关重要的。

假如想要了解更多关于数据集制作方面的内容，可以加入书生.浦语的 RolePlay SIG 中，里面会有各种大佬手把手教学，教你如何制作一个自己喜欢角色的数据集出来。也期待更多大佬加入讲述自己制作数据集的想法和过程！

### 2.3 配置文件修改
在选择了一个最匹配的配置文件并准备好其他内容后，下面我们要做的事情就是根据我们自己的内容对该配置文件进行调整，使其能够满足我们实际训练的要求。
#### 2.3.1 配置文件介绍
假如我们真的打开配置文件后，我们可以看到整体的配置文件分为五部分：
1. **PART 1 Settings**：涵盖了模型基本设置，如预训练模型的选择、数据集信息和训练过程中的一些基本参数（如批大小、学习率等）。

2. **PART 2 Model & Tokenizer**：指定了用于训练的模型和分词器的具体类型及其配置，包括预训练模型的路径和是否启用特定功能（如可变长度注意力），这是模型训练的核心组成部分。

3. **PART 3 Dataset & Dataloader**：描述了数据处理的细节，包括如何加载数据集、预处理步骤、批处理大小等，确保了模型能够接收到正确格式和质量的数据。

4. **PART 4 Scheduler & Optimizer**：配置了优化过程中的关键参数，如学习率调度策略和优化器的选择，这些是影响模型训练效果和速度的重要因素。

5. **PART 5 Runtime**：定义了训练过程中的额外设置，如日志记录、模型保存策略和自定义钩子等，以支持训练流程的监控、调试和结果的保存。

一般来说我们需要更改的部分其实只包括前三部分，而且修改的主要原因是我们修改了配置文件中规定的模型、数据集。后两部分都是 XTuner 官方帮我们优化好的东西，一般而言只有在魔改的情况下才需要进行修改。下面我们将根据项目的要求一步步的进行修改和调整吧！

#### 2.3.2 相关路径及参数修改
首先在 PART 1 的部分，由于我们不再需要在 Huggingface 上自动下载模型，因此我们先要更换模型的路径以及数据集的路径为我们本地的路径。具体操作如下所示：
```diff
# 修改模型地址
- pretrained_model_name_or_path = 'internlm/internlm2-1_8b'
+ pretrained_model_name_or_path = '/root/ft/model'

# 修改数据集地址为本地的json文件地址
- alpaca_en_path = 'tatsu-lab/alpaca'
+ alpaca_en_path = '/root/ft/data/personal_assistant.json'
```

除此之外，我们还可以对一些重要的参数进行调整，包括学习率（lr）、训练的轮数（max_epochs）等等。由于我们这次只是一个简单的让模型知道自己的身份弟位，因此我们的训练轮数以及单条数据最大的 Token 数（max_length）都可以不用那么大。
```diff
# 修改max_length来降低显存的消耗
- max_length = 2048
+ max_length = 1024

# 减少训练的轮数
- max_epochs = 3
+ max_epochs = 2
```

<details>
<summary><b>其他常用参数介绍</b></summary>

**常用超参**

| 参数名 | 解释 |
| ------------------- | ------------------------------------------------------ |
| **data_path**       | 数据路径或 HuggingFace 仓库名                          |
| max_length          | 单条数据最大 Token 数，超过则截断                      |
| pack_to_max_length  | 是否将多条短数据拼接到 max_length，提高 GPU 利用率     |
| accumulative_counts | 梯度累积，每多少次 backward 更新一次参数               |
| ...... | ...... |

> 如果想把显卡的现存吃满，充分利用显卡资源，可以将 `max_length` 和 `batch_size` 这两个参数调大。

</details>

#### 2.3.3 评估问题修改
另外，为了训练过程中能够实时观察到模型的变化情况，XTuner 也是贴心的推出了一个 `evaluation_inputs` 的参数来让我们能够设置多个问题来确保模型在训练过程中的变化是朝着我们想要的方向前进的。比如说我们这里是希望在问出 “请你介绍一下你自己” 或者说 “你是谁” 的时候，模型能够给你的回复是 “我是XXX的小助手...” 这样的回复。因此我们也可以根据这个需求进行更改。

``` diff
# 修改每多少轮进行一次评估
- evaluation_freq = 500
+ evaluation_freq = 300

# 修改具体评估的问题（可以自由拓展其他问题）
- evaluation_inputs = ['请给我介绍五个上海的景点', 'Please tell me five scenic spots in Shanghai']
+ evaluation_inputs = ['请你介绍一下你自己', '你是谁', '你是我的小助手吗']
```
这样修改完后在评估过程中就会显示在当前的权重文件下模型对这几个问题的回复了。

#### 2.3.4 数据集格式修改
由于我们的数据集不再是原本的 aplaca 数据集，因此我们也要进入 PART 3 的部分对相关的内容进行修改。包括说我们数据集输入的不是一个文件夹而是一个单纯的 json 文件以及我们的数据集格式要求改为我们最通用的 OpenAI 数据集格式。
``` diff
# 将原本是 alpaca 的地址改为是 json 文件的地址
- dataset=dict(type=load_dataset, path=alpaca_en_path),
+ dataset=dict(type=load_dataset, path='json', data_files=dict(train=alpaca_en_path)),

# 把 OpenAI 格式的 map_fn 载入进来
- from xtuner.dataset.map_fns import alpaca_map_fn, template_map_fn_factory
+ from xtuner.dataset.map_fns import openai_map_fn, template_map_fn_factory,

# 将 dataset_map_fn 改为通用的 OpenAI 数据集格式
- dataset_map_fn=alpaca_map_fn,
+ dataset_map_fn=openai_map_fn,
```

#### 2.3.4 数据集格式修改
由于我们的数据集不再是原本的 aplaca 数据集，因此我们也要进入 PART 3 的部分对相关的内容进行修改。包括说我们数据集输入的不是一个文件夹而是一个单纯的 json 文件以及我们的数据集格式就是 XTuner 支持的数据集格式而不再需要通过设置的 map_fn 进行映射转换。
``` diff
# 将原本是 alpaca 的地址改为是 json 文件的地址
- dataset=dict(type=load_dataset, path=alpaca_en_path),
+ dataset=dict(type=load_dataset, path='json', data_files=dict(train=alpaca_en_path)),

# 将 dataset_map_fn 改为 None
- dataset_map_fn=alpaca_map_fn,
+ dataset_map_fn=None,
```

#### 2.3.5 小结
这一节我们讲述了微调过程中一些常见的需要调整的内容，包括各种的路径、超参数、评估问题等等。完成了这部分的修改后，我们就可以正式的开始我们下一阶段的旅程： XTuner 启动~！

### 2.4 模型训练

#### 2.4.1 常规训练
当我们准备好了配置文件好，我们只需要将使用 `xtuner train` 指令即可开始训练。
```bash
# 常规训练指令
xtuner train /root/ft/config/internlm2_1_8b_qlora_alpaca_e3_copy.py
```
在该情况下，模型训练的过程文件将默认保存在 `./work_dirs/internlm2_1_8b_qlora_alpaca_e3_copy` 的位置，就比如说我是在 `root/ft/train` 的路径下输入该指令，那么我的文件保存的位置就是在 `root/ft/train/work_dirs/internlm2_1_8b_qlora_alpaca_e3_copy` 的位置下。
```
|-- train/
    |-- work_dirs/
        |-- internlm2_1_8b_qlora_alpaca_e3_copy/
            |-- internlm2_1_8b_qlora_alpaca_e3_copy.py
            |-- last_checkpoint
            |-- iter_500.pth
            |-- iter_832.pth
            |-- 20240319_234512/
                |-- 20240319_234512.log
                |-- vis_data/
                    |-- eval_outputs_iter_831.txt
                    |-- scalars.json
                    |-- 20240319_234512.json
                    |-- config.py
                    |-- eval_outputs_iter_499.txt
```
当然我们也可以指定特定的文件保存位置，比如说就保存在 `/root/ft/train` 路径下。
```bash
# 指定保存路径
xtuner train /root/ft/config/internlm2_1_8b_qlora_alpaca_e3_copy.py --work-dir /root/ft/train
```
这个时候就会自动将所有文件内容保存在该文件夹下，而非新建一个文件夹进行保存，但是训练时保存的内容和上面是一模一样的，知识保存的位置不相同。
```
|-- train/
    |-- internlm2_1_8b_qlora_alpaca_e3_copy.py
    |-- last_checkpoint
    |-- iter_500.pth
    |-- iter_832.pth
    |-- 20240320_001615/
        |-- 20240320_001615.log
        |-- vis_data/
            |-- eval_outputs_iter_831.txt
            |-- scalars.json
            |-- 20240320_001615.json
            |-- config.py
            |-- eval_outputs_iter_499.txt
```

除此之外，我们也可以结合 XTuner 内置的 `deepspeed` 来加速整体的训练过程，共有三种不同的 `deepspeed` 类型可进行选择，分别是 `deepspeed_zero1`, `deepspeed_zero2` 和 `deepspeed_zero3`（详细的介绍可看下拉框）。

<details>
<summary>DeepSpeed优化器及其选择方法</summary>

DeepSpeed是一个深度学习优化库，由微软开发，旨在提高大规模模型训练的效率和速度。它通过几种关键技术来优化训练过程，包括模型分割、梯度累积、以及内存和带宽优化等。DeepSpeed特别适用于需要巨大计算资源的大型模型和数据集。

在DeepSpeed中，`zero` 代表“ZeRO”（Zero Redundancy Optimizer），是一种旨在降低训练大型模型所需内存占用的优化器。ZeRO 通过优化数据并行训练过程中的内存使用，允许更大的模型和更快的训练速度。ZeRO 分为几个不同的级别，主要包括：

- **deepspeed_zero1**：这是ZeRO的基本版本，它优化了模型参数的存储，使得每个GPU只存储一部分参数，从而减少内存的使用。

- **deepspeed_zero2**：在deepspeed_zero1的基础上，deepspeed_zero2进一步优化了梯度和优化器状态的存储。它将这些信息也分散到不同的GPU上，进一步降低了单个GPU的内存需求。

- **deepspeed_zero3**：这是目前最高级的优化等级，它不仅包括了deepspeed_zero1和deepspeed_zero2的优化，还进一步减少了激活函数的内存占用。这通过在需要时重新计算激活（而不是存储它们）来实现，从而实现了对大型模型极其内存效率的训练。

选择哪种deepspeed类型主要取决于你的具体需求，包括模型的大小、可用的硬件资源（特别是GPU内存）以及训练的效率需求。一般来说：

- 如果你的模型较小，或者内存资源充足，可能不需要使用最高级别的优化。
- 如果你正在尝试训练非常大的模型，或者你的硬件资源有限，使用deepspeed_zero2或deepspeed_zero3可能更合适，因为它们可以显著降低内存占用，允许更大模型的训练。
- 选择时也要考虑到实现的复杂性和运行时的开销，更高级的优化可能需要更复杂的设置，并可能增加一些计算开销。

</details>

```bash
# 使用 deepspeed 来加速训练
xtuner train /root/ft/config/internlm2_1_8b_qlora_alpaca_e3_copy.py --work-dir /root/ft/train_deepspeed --deepspeed deepspeed_zero2
```
可以看到，通过 `deepspeed` 来训练后得到的权重文件和原本的权重文件是有所差别的，原本的仅仅是一个 .pth 的文件，而使用了 `deepspeed` 则是一个名字带有 .pth 的文件夹，在该文件夹里保存了两个 .pt 文件。当然这两者在具体的使用上并没有太大的差别，都是可以进行转化并整合。

```
|-- train_deepspeed/
    |-- internlm2_1_8b_qlora_alpaca_e3_copy.py
    |-- zero_to_fp32.py
    |-- last_checkpoint
    |-- 20240319_231921/
        |-- 20240319_231921.log
        |-- vis_data/
            |-- eval_outputs_iter_831.txt
            |-- 20240319_231921.json
            |-- scalars.json
            |-- config.py
            |-- eval_outputs_iter_499.txt
    |-- iter_500.pth/
        |-- bf16_zero_pp_rank_0_mp_rank_00_optim_states.pt
        |-- mp_rank_00_model_states.pt
    |-- iter_832.pth/
        |-- bf16_zero_pp_rank_0_mp_rank_00_optim_states.pt
        |-- mp_rank_00_model_states.pt
```

#### 2.4.2 训练结果
但是其实无论是用哪种方式进行训练，得到的结果都是大差不差的。我们由于设置了300轮评估一次，所以我们可以对比一下300轮和600轮的评估问题结果来看看差别。
```
# 300轮

03/20 00:18:18 - mmengine - INFO - Sample output:
<s><|System|>:Below is an instruction that describes a task. Write a response that appropriately completes the request.
<|User|>:请你介绍一下你自己
<|Bot|>:我是不要姜葱蒜大佬的小助手，内在是上海AI实验室书生·浦语的1.8B大模型哦</s>

03/20 00:18:20 - mmengine - INFO - Sample output:
<s><|System|>:Below is an instruction that describes a task. Write a response that appropriately completes the request.

<|User|>:你是谁
<|Bot|>:我是不要姜葱蒜大佬的小助手，内在是上海AI实验室书生·浦语的1.8B大模型哦</s>

03/20 00:18:20 - mmengine - INFO - Sample output:
<s><|System|>:Below is an instruction that describes a task. Write a response that appropriately completes the request.

<|User|>:你是我的小助手吗
<|Bot|>:是的</s>


# 600轮

03/20 00:19:43 - mmengine - INFO - Sample output:
<s><|System|>:Below is an instruction that describes a task. Write a response that appropriately completes the request.

<|User|>:请你介绍一下你自己
<|Bot|>:我是不要姜葱蒜大佬的小助手，内在是上海AI实验室书生·浦语的1.8B大模型哦</s>

03/20 00:19:45 - mmengine - INFO - Sample output:
<s><|System|>:Below is an instruction that describes a task. Write a response that appropriately completes the request.

<|User|>:你是谁
<|Bot|>:我是不要姜葱蒜大佬的小助手，内在是上海AI实验室书生·浦语的1.8B大模型哦</s>

03/20 00:19:46 - mmengine - INFO - Sample output:
<s><|System|>:Below is an instruction that describes a task. Write a response that appropriately completes the request.

<|User|>:你是我的小助手吗
<|Bot|>:我是不要姜葱蒜大佬的小助手，内在是上海AI实验室书生·浦语的1.8B大模型哦</s>
```
通过两者的对比我们其实就可以很清楚的看到，在300轮的时候模型已经学会了在我问 “你是谁” 或者说 “请你介绍一下我自己” 的时候回答 “我是不要姜葱蒜大佬的小助手，内在是上海AI实验室书生·浦语的1.8B大模型哦”。

但是两者的不同是在询问 “你是我的小助手” 的这个问题上，300轮的时候是回答正确的，回答了 “是” ，但是在600轮的时候回答的还是 “我是不要姜葱蒜大佬的小助手，内在是上海AI实验室书生·浦语的1.8B大模型哦” 这一段话。这表明模型在第一批次第600轮的时候已经出现严重的过拟合（即模型丢失了基础的能力，只会成为某一句话的复读机）现象了，到后面的话无论我们再问什么，得到的结果也就只能是回答这一句话了，模型已经不会再说别的话了。因此假如以通用能力的角度选择最合适的权重文件的话我们可能会选择前面的权重文件进行后续的模型转化及整合工作。

假如我们想要解决这个问题，其实可以通过以下两个方式解决：
1. **减少保存权重文件的间隔并增加权重文件保存的上限**：这个方法实际上就是通过降低间隔结合评估问题的结果，从而找到最优的权重文。我们可以每隔100个批次来看什么时候模型已经学到了这部分知识但是还保留着基本的常识，什么时候已经过拟合严重只会说一句话了。但是由于再配置文件有设置权重文件保存数量的上限，因此同时将这个上限加大也是非常必要的。
2. **增加常规的对话数据集从而稀释原本数据的占比**：这个方法其实就是希望我们正常用对话数据集做指令微调的同时还加上一部分的数据集来让模型既能够学到正常对话，但是在遇到特定问题时进行特殊化处理。比如说我在一万条正常的对话数据里混入两千条和小助手相关的数据集，这样模型同样可以在不丢失对话能力的前提下学到不要姜葱蒜大佬的小助手这句话。这种其实是比较常见的处理方式，大家可以自己动手尝试实践一下。

#### 2.4.3 模型续训
假如我们的模型训练过程中突然被中断了，我们也可以通过在原有指令的基础上加上 `--resume {checkpoint_path}` 来实现模型的继续训练。需要注意的是，这个继续训练得到的权重文件和中断前的完全一致，并不会有任何区别。下面我将用训练了500轮的例子来进行演示。
```bash
# 模型续训
xtuner train /root/ft/config/internlm2_1_8b_qlora_alpaca_e3_copy.py --work-dir /root/ft/train --resume /root/ft/train/iter_500.pth
```
在实测过程中，虽然权重文件并没有发生改变，但是会多一个以时间戳为名的训练过程文件夹保存训练的过程数据。
```
|-- train/
    |-- internlm2_1_8b_qlora_alpaca_e3_copy.py
    |-- last_checkpoint
    |-- iter_500.pth
    |-- iter_832.pth
    |-- 20240320_004203/
        |-- 20240320_004203.log
        |-- vis_data/
            |-- 20240320_004203.json
            |-- eval_outputs_iter_831.txt
            |-- scalars.json
            |-- config.py
    |-- 20240320_001615/
        |-- 20240320_001615.log
        |-- vis_data/
            |-- eval_outputs_iter_831.txt
            |-- scalars.json
            |-- 20240320_001615.json
            |-- config.py
            |-- eval_outputs_iter_499.txt
```

#### 2.4.4 小结
在本节我们的重点是讲解模型训练过程中的种种细节内容，包括了模型训练中的各个参数以、权重文件的选择方式以及模型续训的方法。可以看到是否使用 `--work-dir` 和 是否使用 `--deepspeed` 会对文件的保存位置以及权重文件的保存方式有所不同，大家也可以通过实践去实际的测试感受一下。那么在训练完成后，我们就可以把训练得到的 .pth 文件进行下一步的转换和整合工作了！

### 2.5 模型转换、整合、测试及部署
#### 2.5.1 模型转换
模型转换的本质其实就是将原本使用 Pytorch 训练出来的模型权重文件转换为目前通用的 Huggingface 格式文件，那么我们可以通过以下指令来实现一键转换。

``` bash
# 创建一个保存转换后 Huggingface 格式的文件夹
mkdir -p /root/ft/huggingface

# 模型转换
# xtuner convert pth_to_hf ${配置文件地址} ${权重文件地址} ${转换后模型保存地址}
xtuner convert pth_to_hf /root/ft/train/internlm2_1_8b_qlora_alpaca_e3_copy.py /root/ft/train/iter_832.pth /root/ft/huggingface
```
转换完成后，可以看到模型被转换为 Huggingface 中常用的 .bin 格式文件，这就代表着文件成功被转化为 Huggingface 格式了。
```
|-- huggingface/
    |-- adapter_config.json
    |-- xtuner_config.py
    |-- adapter_model.bin
    |-- README.md
```

<span style="color: red;">**此时，huggingface 文件夹即为我们平时所理解的所谓 “LoRA 模型文件”**</span>

> 可以简单理解：LoRA 模型文件 = Adapter

除此之外，我们其实还可以在转换的指令中添加几个额外的参数，包括以下两个：
| 参数名 | 解释 |
| ------------------- | ------------------------------------------------------ |
| --fp32     | 代表以fp32的精度开启，假如不输入则默认为fp16                          |
| --max-shared-size {GB}        | 代表每个权重文件最大的大小（默认为2GB）                |

假如有特定的需要，我们可以在上面的转换指令后进行添加。由于本次测试的模型文件较小，并且已经验证过拟合，故没有添加。假如加上的话应该是这样的：
```bash
xtuner convert pth_to_hf /root/ft/train/internlm2_1_8b_qlora_alpaca_e3_copy.py /root/ft/train/iter_500.pth /root/ft/huggingface --fp32 --max-shared-size 2GB
```
#### 2.5.2 模型整合
我们通过视频课程的学习可以了解到，对于 LoRA 或者 QLoRA 微调出来的模型其实并不是一个完整的模型，而是一个额外的层（adapter）。那么训练完的这个层最终还是要与原模型进行组合才能被正常的使用。

而对于全量微调的模型（full）其实是不需要进行整合这一步的，因为全量微调修改的是原模型的权重而非微调一个新的 adapter ，因此是不需要进行模型整合的。

![QLoRA](https://github.com/InternLM/Tutorial/assets/108343727/dbb82ca8-e0ef-41db-a8a9-7d6958be6a96)


在 XTuner 中也是提供了一键整合的指令，但是在使用前我们需要准备好三个地址，包括原模型的地址、训练好的 adapter 层的地址（转为 Huggingface 格式后保存的部分）以及最终保存的地址。
```bash
# 创建一个名为 final_model 的文件夹存储整合后的模型文件
mkdir -p /root/ft/final_model

# xtuner convert merge \
#     ${NAME_OR_PATH_TO_LLM} \
#     ${NAME_OR_PATH_TO_ADAPTER} \
#     ${SAVE_PATH} \
xtuner convert merge /root/ft/model /root/ft/huggingface /root/ft/final_model
```
那除了以上的三个基本参数以外，其实在模型整合这一步还是其他很多的可选参数，包括：
| 参数名 | 解释 |
| ------------------- | ------------------------------------------------------ |
| --max-shard-size {GB} | 代表每个权重文件最大的大小（默认为2GB）                |
| --device {device_name} | 这里指的就是device的名称，可选择的有cuda、cpu和auto，默认为cuda即使用gpu进行运算 |
| --is-clip | 这个参数主要用于确定模型是不是CLIP模型，假如是的话就要加上，不是就不需要添加 |

> CLIP（Contrastive Language–Image Pre-training）模型是 OpenAI 开发的一种预训练模型，它能够理解图像和描述它们的文本之间的关系。CLIP 通过在大规模数据集上学习图像和对应文本之间的对应关系，从而实现了对图像内容的理解和分类，甚至能够根据文本提示生成图像。

在模型整合完成后，我们就可以看到 final_model 文件夹里生成了和原模型文件夹非常近似的内容，包括了分词器、权重文件、配置信息等等。当我们整合完成后，我们就能够正常的调用这个模型进行对话测试了。
```
|-- final_model/
    |-- tokenizer.model
    |-- config.json
    |-- pytorch_model.bin.index.json
    |-- pytorch_model-00001-of-00002.bin
    |-- tokenization_internlm2.py
    |-- tokenizer_config.json
    |-- special_tokens_map.json
    |-- pytorch_model-00002-of-00002.bin
    |-- modeling_internlm2.py
    |-- configuration_internlm2.py
    |-- tokenizer.json
    |-- generation_config.json
    |-- tokenization_internlm2_fast.py
```

#### 2.5.3 对话测试：
一般来说，我们假如想测试模型的好坏的话，通常可以通过一下两种方式实现：
- 主观的对话测试
- 客观的试题评测（例如使用 OpenCompass 获取得分）
那对于大部分的小模型而言，我们都只需要主观的对话进行判断即可。在 XTuner 中也直接的提供了一套基于 transformers 的对话代码，让我们可以直接在终端与 Huggingface 格式的模型进行对话操作。我们只需要准备我们刚刚转换好的模型路径并选择对应的提示词模版（prompt-template）即可进行对话。假如 prompt-template 选择有误，很有可能导致模型无法正确的进行回复。

> 想要了解具体模型的 prompt-template 或者 XTuner 里支持的 prompt-tempolate，可以到 XTuner 源码中的 `xtuner/utils/templates.py` 这个文件中进行查找。
```Bash
# 与模型进行对话
xtuner chat /root/ft/final_model --prompt-template internlm2_chat
```
我们可以通过一些简单的测试来看看微调后的模型的能力。
> 假如我们想要输入内容需要在输入文字后敲击两下回车，假如我们想清楚历史记录需要输入 RESET，假如我们想要退出则需要输入 EXIT。
```
double enter to end input (EXIT: exit chat, RESET: reset history) >>> 你是谁

我是不要姜葱蒜大佬的小助手，内在是上海AI实验室书生·浦语的1.8B大模型哦</s>

double enter to end input (EXIT: exit chat, RESET: reset history) >>>  请你介绍一下你自己

我是不要姜葱蒜大佬的小助手，内在是上海AI实验室书生·浦语的1.8B大模型哦</s>

double enter to end input (EXIT: exit chat, RESET: reset history) >>> 你是我的小助手吗？

我是不要姜葱蒜大佬的小助手，内在是上海AI实验室书生·浦语的1.8B大模型哦</s>

double enter to end input (EXIT: exit chat, RESET: reset history) >>> EXIT

Log: Exit!
```
可以看到模型已经严重过拟合，回复的话就只有 “我是不要姜葱蒜大佬的小助手，内在是上海AI实验室书生·浦语的1.8B大模型哦” 这句话。我们下面可以通过对比原模型的能力来看看差异。

```bash
# 同样的我们也可以和原模型进行对话进行对比
xtuner chat /root/ft/model --prompt-template internlm2_chat
```
我们可以用同样的问题来查看回复的情况。
```
double enter to end input (EXIT: exit chat, RESET: reset history) >>> 你是谁

我是一个人工智能助手，旨在帮助用户回答问题、提供定义和解释、将文本从一种语言翻译成另一种语言、总结文本、生成文本、编写故事、分析情感、提供推荐、开发算法、编写代码以及其他任何基于语言的任务。我致力于通过执行常见的基于语言的任务和提供建议来帮助人类。<|im_end|>

double enter to end input (EXIT: exit chat, RESET: reset history) >>> 请你介绍一下你自己

非常感谢您的提问。我是一个名叫书生·浦语的人工智能助手，由上海人工智能实验室开发。我使用了Transformer模型和深度学习技术，并使用语言模型作为预训练任务。我致力于通过执行常见的基于语言的任务和提供建议来帮助人类。我能够回答问题、提供定义和解释、将文本从一种语言翻译成另一种语言、总结文本、生成文本、编写故事、分析情感、提供推荐、开发算法、编写代码以及其他任何基于语言的任务。如果您有任何需要帮助的问题，欢迎随时向我提问。<|im_end|>

double enter to end input (EXIT: exit chat, RESET: reset history) >>> 你是我的小助手吗

是的，我非常乐意成为您的助手。我致力于通过执行常见的基于语言的任务和提供建议来帮助您。如果您有任何需要帮助的问题，请随时向我提问。我会尽力回答您的问题并提供有用的建议。<|im_end|>

double enter to end input (EXIT: exit chat, RESET: reset history) >>> EXIT

Log: Exit!
```
可以看到在没有进行我们数据的微调前，原模型是能够输出有逻辑的回复，并且也不会认为他是我们特有的小助手。因此我们可以很明显的看出两者之间的差异性。

那对于 `xtuner chat` 这个指令而言，还有很多其他的参数可以进行设置的，包括：

| 启动参数              | 解释                                                               |
|-----------------------|--------------------------------------------------------------------|
| --system              | 指定SYSTEM文本，用于在对话中插入特定的系统级信息                   |
| --system-template     | 指定SYSTEM模板，用于自定义系统信息的模板                           |
| **--bits**            | 指定LLM运行时使用的位数，决定了处理数据时的精度                     |
| --bot-name            | 设置bot的名称，用于在对话或其他交互中识别bot                       |
| --with-plugins        | 指定在运行时要使用的插件列表，用于扩展或增强功能                   |
| **--no-streamer**     | 关闭流式传输模式，对于需要一次性处理全部数据的场景                 |
| **--lagent**          | 启用lagent，用于特定的运行时环境或优化                            |
| --command-stop-word   | 设置命令的停止词，当遇到这些词时停止解析命令                       |
| --answer-stop-word    | 设置回答的停止词，当生成回答时遇到这些词则停止                     |
| --offload-folder      | 指定存放模型权重的文件夹，用于加载或卸载模型权重                   |
| --max-new-tokens      | 设置生成文本时允许的最大token数量，控制输出长度                    |
| **--temperature**     | 设置生成文本的温度值，较高的值会使生成的文本更多样，较低的值会使文本更确定 |
| --top-k               | 设置保留用于顶k筛选的最高概率词汇标记数，影响生成文本的多样性      |
| --top-p               | 设置累计概率阈值，仅保留概率累加高于top-p的最小标记集，影响生成文本的连贯性 |
| --seed                | 设置随机种子，用于生成可重现的文本内容                            |


除了这些参数以外其实还有一个非常重要的参数就是 `--adapter` ，这个参数主要的作用就是可以在转化后的 adapter 层与原模型整合之前来对该层进行测试。使用这个额外的参数对话的模型和整合后的模型几乎没有什么太多的区别，因此我们可以通过测试不同的权重文件生成的 adapter 来找到最优的 adapter 进行最终的模型整合工作。
```bash
# 使用 --adapter 参数与完整的模型进行对话
xtuner chat /root/ft/model --adapter /root/ft/huggingface
```
#### 2.4.3 小结
在这一节里我们对微调后的模型（adapter）进行了转换及整合的操作，并通过 `xtuner chat` 来对模型进行了实际的对话测试。从结果可以清楚的看出模型的回复在微调的前后出现了明显的变化。那当我们在测试完模型认为其满足我们的需求后，我们就可以对模型进行量化部署等操作了，这部分的内容在之后关于 LMDeploy 的课程中将会详细的进行赘述，这里我们就不多说了。

## 2.5 总结
在本节中主要就是带领着大家跑通了 XTuner 的一个完整流程，通过了解数据集和模型的使用方法、配置文件的制作和训练以及最后的转换及整合。那在后面假如我们也有想要微调出自己的一个模型，我们也可以尝试使用同样流程和方法进行进一步的实践！


## 3 自定义微调
> 以 **[Medication QA](https://github.com/abachaa/Medication_QA_MedInfo2019)** **数据集**为例

### 3.1 概述

#### 3.1.1 **场景需求**

   基于 InternLM-chat-7B 模型，用 MedQA 数据集进行微调，将其往`医学问答`领域对齐。

#### 3.1.2 **真实数据预览**

| 问题                                                       | 答案                                                         |
| ---------------------------------------------------------- | ------------------------------------------------------------ |
| What are ketorolac eye drops?（什么是酮咯酸滴眼液？）      | Ophthalmic   ketorolac is used to treat itchy eyes caused by allergies. It also is used to   treat swelling and redness (inflammation) that can occur after cataract   surgery. Ketorolac is in a class of medications called nonsteroidal   anti-inflammatory drugs (NSAIDs). It works by stopping the release of   substances that cause allergy symptoms and inflammation. |
| What medicines raise blood sugar? （什么药物会升高血糖？） | Some   medicines for conditions other than diabetes can raise your blood sugar   level. This is a concern when you have diabetes. Make sure every doctor you   see knows about all of the medicines, vitamins, or herbal supplements you   take. This means anything you take with or without a prescription. Examples include:     Barbiturates.     Thiazide diuretics.     Corticosteroids.     Birth control pills (oral contraceptives) and progesterone.     Catecholamines.     Decongestants that contain beta-adrenergic agents, such as pseudoephedrine.     The B vitamin niacin. The risk of high blood sugar from niacin lowers after you have taken it for a few months. The antipsychotic medicine olanzapine (Zyprexa). |

### 3.2 数据准备 

> **以** **[Medication QA](https://github.com/abachaa/Medication_QA_MedInfo2019)** **数据集为例**

**原格式：(.xlsx)**

![gjKLFUNWAx2dZDS.png](imgs/medqa2019samples.png)

| **问题** | 药物类型 | 问题类型 | **回答** | 主题 | URL  |
| -------- | -------- | -------- | -------- | ---- | ---- |
| aaa      | bbb      | ccc      | ddd      | eee  | fff  |

#### 3.2.1 将数据转为 XTuner 的数据格式

**目标格式：(.jsonL)**

```JSON
[{
    "conversation":[
        {
            "system": "xxx",
            "input": "xxx",
            "output": "xxx"
        }
    ]
},
{
    "conversation":[
        {
            "system": "xxx",
            "input": "xxx",
            "output": "xxx"
        }
    ]
}]
```

🧠通过 python 脚本：将 `.xlsx` 中的 问题 和 回答 两列 提取出来，再放入 `.jsonL` 文件的每个 conversation 的 input 和 output 中。

> 这一步的 python 脚本可以请 ChatGPT 来完成。

```text
Write a python file for me. using openpyxl. input file name is MedQA2019.xlsx
Step1: The input file is .xlsx. Exact the column A and column D in the sheet named "DrugQA" .
Step2: Put each value in column A into each "input" of each "conversation". Put each value in column D into each "output" of each "conversation".
Step3: The output file is .jsonL. It looks like:
[{
    "conversation":[
        {
            "system": "xxx",
            "input": "xxx",
            "output": "xxx"
        }
    ]
},
{
    "conversation":[
        {
            "system": "xxx",
            "input": "xxx",
            "output": "xxx"
        }
    ]
}]
Step4: All "system" value changes to "You are a professional, highly experienced doctor professor. You always provide accurate, comprehensive, and detailed answers based on the patients' questions."
```

> ChatGPT 生成的 python 代码见本仓库的 [xlsx2jsonl.py](./xlsx2jsonl.py)


执行 python 脚本，获得格式化后的数据集：
```bash
python xlsx2jsonl.py
```

**格式化后的数据集长这样：**
![uOCJXwbfzKRWSBE.png](imgs/dataProcessed.png)

此时，当然也可以对数据进行训练集和测试集的分割，同样可以让 ChatGPT 写 python 代码。当然如果你没有严格的科研需求、不在乎“训练集泄露”的问题，也可以不做训练集与测试集的分割。

#### 3.2.2 划分训练集和测试集

```text
my .jsonL file looks like:
[{
    "conversation":[
        {
            "system": "xxx",
            "input": "xxx",
            "output": "xxx"
        }
    ]
},
{
    "conversation":[
        {
            "system": "xxx",
            "input": "xxx",
            "output": "xxx"
        }
    ]
}]
Step1, read the .jsonL file.
Step2, count the amount of the "conversation" elements.
Step3, randomly split all "conversation" elements by 7:3. Targeted structure is same as the input.
Step4, save the 7/10 part as train.jsonl. save the 3/10 part as test.jsonl
```
生成的python代码见 [split2train_and_test.py](./split2train_and_test.py)


### 3.3 开始自定义微调

此时，我们重新建一个文件夹来玩“微调自定义数据集”
```bash
mkdir ~/ft-medqa && cd ~/ft-medqa
```

把前面下载好的internlm-chat-7b模型文件夹拷贝过来。

```bash
cp -r ~/ft-oasst1/internlm-chat-7b .
```
别忘了把自定义数据集，即几个 `.jsonL`，也传到服务器上。

```bash
git clone https://github.com/InternLM/tutorial
```

```bash
cp ~/tutorial/xtuner/MedQA2019-structured-train.jsonl .
```



#### 3.3.1 准备配置文件
```bash
# 复制配置文件到当前目录
xtuner copy-cfg internlm_chat_7b_qlora_oasst1_e3 .
# 改个文件名
mv internlm_chat_7b_qlora_oasst1_e3_copy.py internlm_chat_7b_qlora_medqa2019_e3.py

# 修改配置文件内容
vim internlm_chat_7b_qlora_medqa2019_e3.py
```

减号代表要删除的行，加号代表要增加的行。
```diff
# 修改import部分
- from xtuner.dataset.map_fns import oasst1_map_fn, template_map_fn_factory
+ from xtuner.dataset.map_fns import template_map_fn_factory

# 修改模型为本地路径
- pretrained_model_name_or_path = 'internlm/internlm-chat-7b'
+ pretrained_model_name_or_path = './internlm-chat-7b'

# 修改训练数据为 MedQA2019-structured-train.jsonl 路径
- data_path = 'timdettmers/openassistant-guanaco'
+ data_path = 'MedQA2019-structured-train.jsonl'

# 修改 train_dataset 对象
train_dataset = dict(
    type=process_hf_dataset,
-   dataset=dict(type=load_dataset, path=data_path),
+   dataset=dict(type=load_dataset, path='json', data_files=dict(train=data_path)),
    tokenizer=tokenizer,
    max_length=max_length,
-   dataset_map_fn=alpaca_map_fn,
+   dataset_map_fn=None,
    template_map_fn=dict(
        type=template_map_fn_factory, template=prompt_template),
    remove_unused_columns=True,
    shuffle_before_pack=True,
    pack_to_max_length=pack_to_max_length)
```
#### 3.3.2 **XTuner！启动！**

![tH8udZzECYl5are.png](imgs/ysqd.png)

```bash
xtuner train internlm_chat_7b_qlora_medqa2019_e3.py --deepspeed deepspeed_zero2
```

#### 3.3.3 pth 转 huggingface

同前述，这里不赘述了。[将得到的-pth-模型转换为-huggingface-模型即生成adapter文件夹](#236-将得到的-pth-模型转换为-huggingface-模型即生成adapter文件夹)  

#### 3.3.4 部署与测试

同前述。[部署与测试](#24-部署与测试)


## 4【补充】用 MS-Agent 数据集 赋予 LLM 以 Agent 能力
### 4.1 概述

MSAgent 数据集每条样本包含一个对话列表（conversations），其里面包含了 system、user、assistant 三种字段。其中：

- system: 表示给模型前置的人设输入，其中有告诉模型如何调用插件以及生成请求

- user: 表示用户的输入 prompt，分为两种，通用生成的prompt和调用插件需求的 prompt

- assistant: 为模型的回复。其中会包括插件调用代码和执行代码，调用代码是要 LLM 生成的，而执行代码是调用服务来生成结果的

一条调用网页搜索插件查询“上海明天天气”的数据样本示例如下图所示：
![BlgfEqpiRFO5G6L.png](imgs/msagent_data.png)

### 4.2 微调步骤

#### 4.2.1 准备工作
> xtuner 是从国内的 ModelScope 平台下载 MS-Agent 数据集，因此不用提前手动下载数据集文件。

```bash
# 准备工作
mkdir ~/ft-msagent && cd ~/ft-msagent
cp -r ~/ft-oasst1/internlm-chat-7b .

# 查看配置文件
xtuner list-cfg | grep msagent

# 复制配置文件到当前目录
xtuner copy-cfg internlm_7b_qlora_msagent_react_e3_gpu8 .

# 修改配置文件中的模型为本地路径
vim ./internlm_7b_qlora_msagent_react_e3_gpu8_copy.py 
```

```diff
- pretrained_model_name_or_path = 'internlm/internlm-chat-7b'
+ pretrained_model_name_or_path = './internlm-chat-7b'
```

#### 4.2.2 开始微调
```Bash
xtuner train ./internlm_7b_qlora_msagent_react_e3_gpu8_copy.py --deepspeed deepspeed_zero2
```

### 4.3 直接使用

> 由于 msagent 的训练非常费时，大家如果想尽快把这个教程跟完，可以直接从 modelScope 拉取咱们已经微调好了的 Adapter。如下演示。

#### 4.3.1 下载 Adapter
```Bash
cd ~/ft-msagent
apt install git git-lfs
git lfs install
git lfs clone https://www.modelscope.cn/xtuner/internlm-7b-qlora-msagent-react.git
```

OK，现在目录应该长这样：
- internlm_7b_qlora_msagent_react_e3_gpu8_copy.py
- internlm-7b-qlora-msagent-react
- internlm-chat-7b
- work_dir（可有可无）

有了这个在 msagent 上训练得到的Adapter，模型现在已经有 agent 能力了！就可以加 --lagent 以调用来自 lagent 的代理功能了！

#### 4.3.2 添加 serper 环境变量

> **开始 chat 之前，还要加个 serper 的环境变量：**
> 
> 去 serper.dev 免费注册一个账号，生成自己的 api key。这个东西是用来给 lagent 去获取 google 搜索的结果的。等于是 serper.dev 帮你去访问 google，而不是从你自己本地去访问 google 了。

![kDSdpQrhHfTWYsc.png](imgs/serper.png)

添加 serper api key 到环境变量：

```bash
export SERPER_API_KEY=abcdefg
```

#### 4.3.3 xtuner + agent，启动！

```bash
xtuner chat ./internlm-chat-7b --adapter internlm-7b-qlora-msagent-react --lagent
```


#### 4.3.4 报错处理

xtuner chat 增加 --lagent 参数后，报错 ```TypeError: transfomers.modelsauto.auto factory. BaseAutoModelClass.from pretrained() got multiple values for keyword argument "trust remote code"```	

注释掉已安装包中的代码：

```bash
vim /root/xtuner019/xtuner/xtuner/tools/chat.py
```



![NfHAV1b4zqYv5kR.png](imgs/bugfix1.png)

![YTpz1qemiojk5Bg.png](imgs/bugfix2.png)


## 5 其他已知问题和解决方案：
https://docs.qq.com/doc/DY1d2ZVFlbXlrUERj


小作业助教老师会在社群中公布。
Have fun!



## 6 注意事项

本教程使用 xtuner 0.1.9 版本
若需要跟着本教程一步一步完成，建议严格遵循本教程的步骤！



若出现莫名其妙报错，请尝试更换为以下包的版本：（如果有报错再检查，没报错不用看）
```
torch                         2.1.1
transformers                  4.34.0
transformers-stream-generator 0.0.4
```
```bash
pip install torch==2.1.1
pip install transformers==4.34.0
pip install transformers-stream-generator=0.0.4
```
CUDA 相关：（如果有报错再检查，没报错不用看）
```
NVIDIA-SMI 535.54.03              
Driver Version: 535.54.03    
CUDA Version: 12.2

nvidia-cuda-cupti-cu12        12.1.105
nvidia-cuda-nvrtc-cu12        12.1.105
nvidia-cuda-runtime-cu12      12.1.105
```

## 7 作业

**基础作业：**

构建数据集，使用 XTuner 微调 InternLM-Chat-7B 模型, 让模型学习到它是你的智能小助手，效果如下图所示，本作业训练出来的模型的输出需要**将不要葱姜蒜大佬**替换成自己名字或昵称！

**微调前**（回答比较官方）
![web_show_2.png](imgs%2Fweb_show_2.png)


**微调后**（对自己的身份有了清晰的认知）
![web_show_1.png](imgs%2Fweb_show_1.png)

作业参考答案：https://github.com/InternLM/tutorial/blob/main/xtuner/self.md

**进阶作业：**

- 将训练好的Adapter模型权重上传到 OpenXLab、Hugging Face 或者 MoelScope 任一一平台。
- 将训练好后的模型应用部署到 OpenXLab 平台，参考部署文档请访问：https://aicarrier.feishu.cn/docx/MQH6dygcKolG37x0ekcc4oZhnCe

**整体实训营项目：**

时间周期：即日起致课程结束

即日开始可以在班级群中随机组队完成一个大作业项目，一些可提供的选题如下：

- 人情世故大模型：一个帮助用户撰写新年祝福文案的人情事故大模型
- 中小学数学大模型：一个拥有一定数学解题能力的大模型
- 心理大模型：一个治愈的心理大模型
- 工具调用类项目：结合 Lagent 构建数据集训练 InternLM 模型，支持对 MMYOLO 等工具的调用

其他基于书生·浦语工具链的小项目都在范围内，欢迎大家充分发挥想象力。

