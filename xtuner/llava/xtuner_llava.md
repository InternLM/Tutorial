
![head](img4md/head.jpg)

- [1. XTuner多模态训练与测试](#1-xtuner多模态训练与测试)
  - [1.1. 给LLM装上电子眼：多模态LLM原理简介](#11-给llm装上电子眼多模态llm原理简介)
    - [1.1.1. 文本单模态](#111-文本单模态)
    - [1.1.2. 文本+图像多模态](#112-文本图像多模态)
  - [1.2. 什么型号的电子眼：LLaVA方案简介](#12-什么型号的电子眼llava方案简介)
    - [1.2.1. LLaVA训练阶段示意图](#121-llava训练阶段示意图)
    - [1.2.2. LLaVA测试阶段示意图](#122-llava测试阶段示意图)
  - [1.3. 快速上手](#13-快速上手)
    - [1.3.1. 环境准备](#131-环境准备)
      - [1.3.1.1. 开发机准备](#1311-开发机准备)
      - [1.3.1.2. XTuner安装](#1312-xtuner安装)
    - [1.3.2. 概述](#132-概述)
    - [1.3.3. Pretrain阶段](#133-pretrain阶段)
    - [1.3.4. Finetune阶段](#134-finetune阶段)
      - [1.3.4.1. 训练数据构建](#1341-训练数据构建)
        - [1.3.4.1.1. 格式](#13411-格式)
        - [1.3.4.1.2. 制作](#13412-制作)
      - [1.3.4.2. 准备配置文件](#1342-准备配置文件)
        - [1.3.4.2.1. 创建配置文件](#13421-创建配置文件)
        - [1.3.4.2.2. 修改配置文件](#13422-修改配置文件)
      - [1.3.4.3. 开始Finetune](#1343-开始finetune)
    - [1.3.5. 对比Finetune前后的性能差异](#135-对比finetune前后的性能差异)
      - [1.3.5.1. Finetune前](#1351-finetune前)
      - [1.3.5.2. Finetune后](#1352-finetune后)


# 1. XTuner多模态训练与测试
在本节课中，我们将学习使用XTuner微调多模态LLM的内容，本部分需要的GPU资源为24GB 30% 的 A100。

这是学完本节内容后的多模态LLM性能效果展示：

**Finetune前的多模态LLM(InternLM_chat_1.8B_llava)：只会给图像打标题**
![ft_before](img4md/ft_before.png)

**Finetune后的多模态LLM(InternLM_chat_1.8B_llava)：会根据图像回答问题了**
![ft_after](img4md/ft_after.png)
</details>

<div align=center>

<h2>下面，让我们正式开始今天的课程吧~</h2>
</div>

## 1.1. 给LLM装上电子眼：多模态LLM原理简介

### 1.1.1. 文本单模态
```mermaid
flowchart LR
a[输入文本] -.- A(文本Embedding模型) -.-> b[/文本向量/]
b --> c((L L M))
c --> d[输出文本]
```

### 1.1.2. 文本+图像多模态
```mermaid
flowchart LR
a[输入文本] -.- A(文本Embedding模型) -.-> b[/文本向量/]
b --> c((L L M))
c --> d[输出文本]
subgraph " "
f[输入图像] -.- F("Image Projector")
F -.-> g[/图像向量/]
end
g --> c
```

## 1.2. 什么型号的电子眼：LLaVA方案简介

[Haotian Liu等](https://arxiv.org/abs/2304.08485)使用GPT-4V对图像数据生成描述，以此构建出大量`<question text><image> -- <answer text>`的数据对。利用这些数据对，配合文本单模态LLM，训练出一个Image Projector。

所使用的`文本单模型LLM`和训练出来的`Image Projector`，统称为`LLaVA模型`。

### 1.2.1. LLaVA训练阶段示意图
```mermaid
flowchart TB;
subgraph 训练阶段
a[("文本+图像<br>问答对<br>(训练数据)")] --> b{显卡}
c((文本单模态<br>LLM)) --> b
b --> d([Image<br>Projector])
end
```

### 1.2.2. LLaVA测试阶段示意图
```mermaid
flowchart TB;
subgraph 测试阶段
a([Image<br>Projector]) --> b{显卡}
c((文本单模态<br>LLM)) --> b
e[输入图像] --> b
b --> d[输出文本]
end
```

> Image Projector的训练和测试，有点类似之前我们讲过的LoRA微调方案。

二者都是在已有LLM的基础上，用新的数据训练一个新的小文件。

只不过，LLM套上LoRA之后，有了新的灵魂（角色）；而LLM套上Image Projector之后，才有了眼睛。

## 1.3. 快速上手

### 1.3.1. 环境准备
#### 1.3.1.1. 开发机准备

首先我们需要前往 [InternStudio](https://studio.intern-ai.org.cn/) 中创建一个开发机进行使用。然后在进入界面后首先选择开发机。

![image](https://github.com/Jianfeng777/tutorial/assets/108343727/d6647289-f5d5-4c52-8939-b5f5a96d6b0c)

首先，打开 `Intern Studio` 界面，点击 创建开发机 配置开发机系统。

![image](https://github.com/Jianfeng777/tutorial/assets/108343727/2ae5252c-24b8-45c5-aca3-d597caf03449)

之后我们填写 `开发机名称` 后，点击 选择镜像 使用 `Cuda11.7-conda` 镜像，然后在资源配置中，使用 `30% A100 * 1` 的选项，然后立即创建开发机器。

![image](https://github.com/Jianfeng777/tutorial/assets/108343727/66e92058-2cf5-418c-a2ce-add9923cf6c2)

点击 `进入开发机` 选项。

![image](https://github.com/Jianfeng777/tutorial/assets/108343727/bcfef2b4-1c2c-4620-b7c0-e83a99a0f641)

最后我们点击 `Terminal` 进入终端界面即可开始操作！

![image](https://github.com/Jianfeng777/tutorial/assets/108343727/4d5f9c23-0a7d-4121-a9c3-a28b037cadfc)
![image](https://github.com/Jianfeng777/tutorial/assets/108343727/9b3004e8-0622-49c7-8af7-c56fb87b2797)

#### 1.3.1.2. XTuner安装
```bash
# 如果你是在 InternStudio 平台，则从本地 clone 一个已有 pytorch 的环境：
# pytorch    2.0.1   py3.10_cuda11.7_cudnn8.5.0_0

cd ~ && studio-conda xtuner0.1.17
# 如果你是在其他平台：
# conda create --name xtuner0.1.17 python=3.10 -y

# 激活环境
conda activate xtuner0.1.17
# 进入家目录 （~的意思是 “当前用户的home路径”）
cd ~
# 创建版本文件夹并进入，以跟随本教程
mkdir -p /root/xtuner0117 && cd /root/xtuner0117

# 拉取 0.1.17 的版本源码
git clone -b v0.1.17  https://github.com/InternLM/xtuner
# 无法访问github的用户请从 gitee 拉取:
# git clone -b v0.1.15 https://gitee.com/Internlm/xtuner

# 进入源码目录
cd /root/xtuner0117/xtuner

# 从源码安装 XTuner
pip install -e '.[all]' && cd ~
```
> 假如速度太慢可以 `Ctrl + C` 退出后换成 `pip install -e '.[all]' -i https://mirrors.aliyun.com/pypi/simple/`

假如在这一过程中没有出现任何的报错的话，那也就意味着我们成功安装好支持 XTuner 所运行的环境啦。其实对于很多的初学者而言，安装好环境意味着成功了一大半！

### 1.3.2. 概述

> 在本节中，我们将 **自己构造 `<question text><image>--<answer text>` 数据对，基于InternLM2_chat_1.8b这个文本单模态模型，使用LLaVA方案，训练一个给InternLM2_chat_1.8b使用的Image Projector文件。**

LLaVA方案中，给LLM增加视觉能力的过程，即是训练Image Projector文件的过程。
该过程分为2个阶段：Pretrain和Finetune。

```mermaid
flowchart LR;
    subgraph Pretrain阶段
    a[("图像<br>+<br>标题(短文本)")] --> b{显卡}
    c(("文本单模态LLM<br>(InternLM2_chat_1.8B)")) --> b
    b --> d((Pretrained<br>LLaVA))
    end

    subgraph Finetune阶段
    f[("图像<br>+<br>复杂对话文本")] --> g{显卡}
    d --> g
    g --> i((Finetuned<br>LLaVA))
    end
```

### 1.3.3. Pretrain阶段
在Pretrain阶段，我们会使用大量的`图片+简单文本（caption, 即图片标题）`数据对，使LLM理解图像中的**普遍特征**。即，对大量的图片进行**粗看**。

Pretrain阶段训练完成后，此时的模型已经有视觉能力了！但是由于训练数据中都是图片+图片标题，所以此时的模型虽然有视觉能力，但无论用户问它什么，它都只会回答输入图片的标题。即，**此时的模型只会给输入图像“写标题”**。

> Pretrain阶段相当于是开发LLM时预训练工作，对硬件要求非常高，有8卡的学有余力同学可以自行尝试。详见[XTuner-LLaVA](https://github.com/InternLM/xtuner/blob/main/docs/zh_cn/user_guides/dataset_prepare.md#llava-dataset)和[LLaVA](https://llava-vl.github.io/)。
> <details>
> 
> ```bash
> NPROC_PER_NODE=8 xtuner train llava_internlm2_chat_1_8b_clip_vit_large_p14_336_e1_gpu8_pretrain --deepspeed deepspeed_zero2
> 
> NPROC_PER_NODE=8 xtuner train llava_internlm2_chat_1_8b_qlora_clip_vit_large_p14_336_lora_e1_gpu8_finetune --deepspeed deepspeed_zero2
> ```

> </details>

在本次实战营中，我们已经为大家提供了Pretrain阶段的产物——`iter_2181.pth`文件。它就是幼稚园阶段的Image Projector！大家带着`iter_2181.pth`文件继续进入下一阶段进行Finetune即可。

### 1.3.4. Finetune阶段
在Finetune阶段，我们会使用`图片+复杂文本`数据对，来对Pretrain得到的Image Projector即iter_2181.pth进行进一步的训练。

#### 1.3.4.1. 训练数据构建

##### 1.3.4.1.1. 格式
```json
[
    {
        "id": "随便什么字符串",
        "image": "图片文件的相对位置。相对谁？相对你后面config文件里指定的image_folder参数的路径。",
        "conversation": [
            {
                "from": "human",
                "value": "<image>\n第1个问题。"
            },
            {
                "from": "gpt",
                "value": "第1个回答"
            },
            {
                "from": "human",
                "value": "第2个问题。"
            },
            {
                "from": "gpt",
                "value": "第2个回答"
            },
            # ......
            {
                "from": "human",
                "value": "第n个问题。"
            },
            {
                "from": "gpt",
                "value": "第n个回答"
            },
        ]
    },

    # 下面是第2组训练数据了。

    {
        "id": "随便什么字符串",
        "image": "图片文件的相对位置。相对谁？相对你后面config文件里指定的image_folder参数的路径。",
        "conversation": [
            {
                "from": "human",
                "value": "<image>\n第1个问题。"
            },
            # ......
            {
                "from": "gpt",
                "value": "第n个回答"
            }
        ]
    }
]
```
> 注意：每组训练数据的第1个来自human的问题前，要加上图片占位符，即`<image>`

<details>
<summary>示例</summary>

```json
[
  {
    "id": "000000033471",
    "image": "coco/train2017/000000033471.jpg",
    "conversations": [
      {
        "from": "human",
        "value": "<image>\nWhat are the colors of the bus in the image?"
      },
      {
        "from": "gpt",
        "value": "The bus in the image is white and red."
      },
      {
        "from": "human",
        "value": "What feature can be seen on the back of the bus?"
      },
      {
        "from": "gpt",
        "value": "The back of the bus features an advertisement."
      },
      {
        "from": "human",
        "value": "Is the bus driving down the street or pulled off to the side?"
      },
      {
        "from": "gpt",
        "value": "The bus is driving down the street, which is crowded with people and other vehicles."
      }
    ]
  },
  {
    "id": "000000052846",
    "image": "coco/train2017/000000052846.jpg",
    "conversations": [
      {
        "from": "human",
        "value": "<image>\nWhere is the cat positioned in the image?"
      },
      {
        "from": "gpt",
        "value": "The cat is positioned on top of the back of the couch in the living room."
      }
    ]
  }
 ]
```
</details>

##### 1.3.4.1.2. 制作
我们可以效法LLaVA作者的做法，将自己的图片发送给GPT，要求其按照上述格式生成若干条问答对。
<details>
<summary>prompts</summary>

![oph.jpg](llava_data/test_img/oph.jpg)

Create a dataset for me, following this format.
```json
[
  {
    "id": "<random_number_string>",
    "image": "test_img/oph.jpg",
    "conversations": [
      {
        "from": "human",
        "value": "<image>\nDescribe this image."
      },
      {
        "from": "gpt",
        "value": "<answer1>"
      },
      {
        "from": "human",
        "value": "<question2>"
      },
      {
        "from": "gpt",
        "value": "<answer2>"
      },
      {
        "from": "human",
        "value": "<question3>"
      },
      {
        "from": "gpt",
        "value": "<answer3>"
      }
    ]
  }
]
```
The questions and answers, please generate for me, based on the image I sent to you. Thes questions should be from the shallow to the deep, and the answers should be as detailed and correct as possible. The questions and answers should be stick to the contents in the image itself, like objects, peoples, equipment, environment, purpose, color, attitude, etc. 5 question and answer pairs.
</details>
<br>

为了方便大家跟随课程，针对这张示例图片的问答对数据（repeat_data.json），大家按照下面的脚本运行就可以生成啦~（重复200次）

```bash
cd ~ && git clone https://github.com/InternLM/tutorial -b camp2 && conda activate xtuner0.1.17 && cd tutorial

python /root/tutorial/xtuner/llava/llava_data/repeat.py \
  -i /root/tutorial/xtuner/llava/llava_data/unique_data.json \
  -o /root/tutorial/xtuner/llava/llava_data/repeated_data.json \
  -n 200
```

#### 1.3.4.2. 准备配置文件

> 如果你懒到不想自己改配置文件，或者怎么改都失败。我们准备了一个fool_config文件在仓库里。运行：
```python
cp /root/tutorial/xtuner/llava/llava_data/internlm2_chat_1_8b_llava_tutorial_fool_config.py /root/tutorial/xtuner/llava/llava_internlm2_chat_1_8b_qlora_clip_vit_large_p14_336_lora_e1_gpu8_finetune_copy.py
```

##### 1.3.4.2.1. 创建配置文件

```bash
# 查询xtuner内置配置文件
xtuner list-cfg -p llava_internlm2_chat_1_8b

# 拷贝配置文件到当前目录
xtuner copy-cfg \
  llava_internlm2_chat_1_8b_qlora_clip_vit_large_p14_336_lora_e1_gpu8_finetune \
  /root/tutorial/xtuner/llava
```

当前你的`/root/tutorial/xtuner/llava/`目录下的文件结构应该是这样：

```bash
|-- llava_data
|   |-- repeat.py
|   |-- repeated_data.json
|   |-- test_img
|   |   `-- oph.jpg
|   `-- unique_data.json
`-- llava_internlm2_chat_1_8b_qlora_clip_vit_large_p14_336_lora_e1_gpu8_finetune_copy.py
```

##### 1.3.4.2.2. 修改配置文件

修改`llava_internlm2_chat_1_8b_qlora_clip_vit_large_p14_336_lora_e1_gpu8_finetune_copy.py`文件中的：
- pretrained_pth
- llm_name_or_path
- visual_encoder_name_or_path
- data_root
- data_path
- image_folder

```diff
# Model
- llm_name_or_path = 'internlm/internlm2-chat-1_8b'
+ llm_name_or_path = '/root/share/new_models/Shanghai_AI_Laboratory/internlm2-chat-1_8b'
- visual_encoder_name_or_path = 'openai/clip-vit-large-patch14-336'
+ visual_encoder_name_or_path = '/root/share/new_models/openai/clip-vit-large-patch14-336'

# Specify the pretrained pth
- pretrained_pth = './work_dirs/llava_internlm2_chat_1_8b_clip_vit_large_p14_336_e1_gpu8_pretrain/iter_2181.pth'  # noqa: E501
+ pretrained_pth = '/root/share/new_models/xtuner/iter_2181.pth'

# Data
- data_root = './data/llava_data/'
+ data_root = '/root/tutorial/xtuner/llava/llava_data/'
- data_path = data_root + 'LLaVA-Instruct-150K/llava_v1_5_mix665k.json'
+ data_path = data_root + 'repeated_data.json'
- image_folder = data_root + 'llava_images'
+ image_folder = data_root

# Scheduler & Optimizer
- batch_size = 16  # per_device
+ batch_size = 1  # per_device


# evaluation_inputs
- evaluation_inputs = ['请描述一下这张图片','Please describe this picture']
+ evaluation_inputs = ['Please describe this picture','What is the equipment in the image?']

```

#### 1.3.4.3. 开始Finetune

```bash
xtuner train /root/tutorial/xtuner/llava/llava_internlm2_chat_1_8b_qlora_clip_vit_large_p14_336_lora_e1_gpu8_finetune_copy.py --deepspeed deepspeed_zero2
```

### 1.3.5. 对比Finetune前后的性能差异

#### 1.3.5.1. Finetune前
> 即：**加载 1.8B 和 Pretrain阶段产物(iter_2181) 到显存。**

```bash
# 解决小bug
export MKL_SERVICE_FORCE_INTEL=1
export MKL_THREADING_LAYER=GNU

# pth转huggingface
xtuner convert pth_to_hf \
  llava_internlm2_chat_1_8b_clip_vit_large_p14_336_e1_gpu8_pretrain \
  /root/share/new_models/xtuner/iter_2181.pth \
  /root/tutorial/xtuner/llava/llava_data/iter_2181_hf

# 启动！
xtuner chat /root/share/new_models/Shanghai_AI_Laboratory/internlm2-chat-1_8b \
  --visual-encoder /root/share/new_models/openai/clip-vit-large-patch14-336 \
  --llava /root/tutorial/xtuner/llava/llava_data/iter_2181_hf \
  --prompt-template internlm2_chat \
  --image /root/tutorial/xtuner/llava/llava_data/test_img/oph.jpg
```
> Q1: Describe this image.
> Q2: What is the equipment in the image?

#### 1.3.5.2. Finetune后
> 即：**加载 1.8B 和 Fintune阶段产物 到显存。**

```bash
# 解决小bug
export MKL_SERVICE_FORCE_INTEL=1
export MKL_THREADING_LAYER=GNU

# pth转huggingface
xtuner convert pth_to_hf \
  /root/tutorial/xtuner/llava/llava_internlm2_chat_1_8b_qlora_clip_vit_large_p14_336_lora_e1_gpu8_finetune_copy.py \
  /root/tutorial/xtuner/llava/work_dirs/llava_internlm2_chat_1_8b_qlora_clip_vit_large_p14_336_lora_e1_gpu8_finetune_copy/iter_1200.pth \
  /root/tutorial/xtuner/llava/llava_data/iter_1200_hf

# 启动！
xtuner chat /root/share/new_models/Shanghai_AI_Laboratory/internlm2-chat-1_8b \
  --visual-encoder /root/share/new_models/openai/clip-vit-large-patch14-336 \
  --llava /root/tutorial/xtuner/llava/llava_data/iter_1200_hf \
  --prompt-template internlm2_chat \
  --image /root/tutorial/xtuner/llava/llava_data/test_img/oph.jpg
```
> Q1: Describe this image.
> Q2: What is the equipment in the image?

Finetune前后效果对比：

**Finetune前：只会打标题**
![ft_before](img4md/ft_before.png)

**Finetune后：会回答问题了**
![ft_after](img4md/ft_after.png)
</details>

<br><br><br>
本节课结束，下次见。
