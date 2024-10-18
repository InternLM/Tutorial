# 玩转HF/魔搭/魔乐社区

<img width="900" alt="img_v3_02fm_1cdd62bb-61dc-490f-8720-97f70ce4455g" src="https://github.com/user-attachments/assets/41809cd6-9c1d-49e0-8d79-3bcf2f7fbd97">

## 1. 闯关任务

**😀Hello大家好，这节课为大家带来“玩转HF/魔搭/魔乐社区”的课程，课程任务请访问[闯关任务](./task.md)** 

---
## 2. 课程内容
😀Hello大家好，欢迎来到书生大模型实战营第四期新鲜出炉的“玩转Hugging Face/魔搭社区/魔乐社区”教程！
此教程旨在帮助您学习当前火热的三大AI学习社区。我们将深入探索如何充分利用 Hugging Face、魔搭社区和魔乐社区的资源和工具，学习模型下载、上传以及创建您的专属Space，玩转三大平台。无论你是初学者还是资深开发者，这些社区提供的丰富资源都将为您的项目带来无限可能，一起加油！

### 2.1 HF 平台

#### 2.1.1  注册Hugging Face 平台 （需要魔法上网）

Hugging Face 最初专注于开发聊天机器人服务。尽管他们的聊天机器人项目并未取得预期的成功，但他们在GitHub上开源的Transformers库却意外地在机器学习领域引起了巨大轰动。如今，Hugging Face已经发展成为一个拥有超过100,000个预训练模型和10,000个数据集的平台，被誉为机器学习界的GitHub。

这里需要先注册Hugging Face https://huggingface.co/ 

#### 2.1.2 InternLM模型下载

在正式下载之前，我们先要介绍一下HF的Transformers库，作为HF最核心的项目，它可以：
- 直接使用预训练模型进行推理
- 提供了大量预训练模型可供使用
- 使用预训练模型进行迁移学习
因此在使用HF前，我们需要下载Transformers等一些常用依赖库

这里我以internlm2_5-1_8b举例 https://huggingface.co/internlm/internlm2_5-1_8b

![image](https://github.com/user-attachments/assets/6f399159-743b-4eb7-b5d4-af75b4c00d06)

#### 2.1.3 GitHub CodeSpace的使用

```因为网络和磁盘有限的原因，强烈不建议在 InternStudio 运行，因此这里使用CodeSpace```
https://github.com/codespaces

Github CodeSpace是Github推出的线上代码平台，提供了一系列templates，我们这里选择Jupyter Notebook进行创建环境

![image](https://github.com/user-attachments/assets/68eeba74-d079-49df-938c-c84d070f7e7c)

创建好环境后，我们先找到终端

![image](https://github.com/user-attachments/assets/916f94bc-4686-402b-8012-9baf17e42ac7)

CodeSapces 这里的界面跟vscode很类似，在下方会出现终端。

![image](https://github.com/user-attachments/assets/585fa33e-c44e-406c-a710-3cd6857a2ef3)

在终端（terminal）安装以下依赖，便于模型运行。

```bash
conda install pytorch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 pytorch-cuda=12.1 -c pytorch -c nvidia -y
# 安装transformers
pip install transformers==4.38
pip install sentencepiece==0.1.99
pip install einops==0.8.0
pip install protobuf==5.27.2
pip install accelerate==0.33.0
```

##### 2.1.3.1 下载internlm2_5-7b-chat的配置文件

考虑到个人GitHub CodeSpace硬盘空间有限（32GB可用），而7B的模型相对较大，这里我们先演示如何下载模型文件夹的特定文件。

```
因为CodeSpace平台上默认用户权限，不是root权限，这里为方便演示直接在工作区创建文件
以下目录均为/workspaces/codespaces-jupyter
```

以下载模型的配置文件为例，先新建一个hf_download_josn.py 文件

```bash
touch hf_download_josn.py
```

在这个文件中，粘贴以下代码

```python
import os
from huggingface_hub import hf_hub_download

# 指定模型标识符
repo_id = "internlm/internlm2_5-7b"

# 指定要下载的文件列表
files_to_download = [
    {"filename": "config.json"},
    {"filename": "model.safetensors.index.json"}
]

# 创建一个目录来存放下载的文件
local_dir = f"{repo_id.split('/')[1]}"
os.makedirs(local_dir, exist_ok=True)

# 遍历文件列表并下载每个文件
for file_info in files_to_download:
    file_path = hf_hub_download(
        repo_id=repo_id,
        filename=file_info["filename"],
        local_dir=local_dir
    )
    print(f"{file_info['filename']} file downloaded to: {file_path}")
```
运行该文件（注意文件目录）

```bash
python hf_download_josn.py
```

可以看到，已经从Hugging Face上下载了相应配置文件

![image](https://github.com/user-attachments/assets/4f0dbe4c-a82c-4cba-b6da-701c4461be20)

那么如何使用internlm2_5-7b-chat模型呢？可以在InternStudio 的/share目录下找到

如 /root/share/model_repos/internlm2-chat-7b

在之后我们InternStudio的实验中，基本上都可以使用 /share 目录下的模型文件夹地址作为`model_name_or_path`传参到AutoTokenizer.from_pretrained()和AutoModelForCausalLM.from_pretrained()中，即可加载模型文件

##### 2.1.3.2 下载internlm2_5-chat-1_8b并打印示例输出

那么如果我们需想要下载一个完整的模型文件怎么办呢？
创建一个python文件用于下载internlm2_5-1_8B模型并运行
这里下载跟网速比较相关，一般来说十多分钟就搞定了，但是如果网速较慢的小伙伴可以只尝试下载1.8b模型对应的config.json文件以及其他配置文件

```bash
touch hf_download_1_8_demo.py
```

但是注意到在Codespace平台上是没有GPU资源的，因此我们python代码中只使用CPU进行推理，我们需要删掉跟CUDA有关的API，在hf_download_1_8_demo.py文件中粘贴以下内容：

```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("internlm/internlm2_5-1_8b", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("internlm/internlm2_5-1_8b", torch_dtype=torch.float16, trust_remote_code=True)
model = model.eval()

inputs = tokenizer(["A beautiful flower"], return_tensors="pt")
gen_kwargs = {
    "max_length": 128,
    "top_p": 0.8,
    "temperature": 0.8,
    "do_sample": True,
    "repetition_penalty": 1.0
}

# 以下内容可选，如果解除注释等待一段时间后可以看到模型输出
# output = model.generate(**inputs, **gen_kwargs)
# output = tokenizer.decode(output[0].tolist(), skip_special_tokens=True)
# print(output)
```
等待几分钟后（跟网速有关），会在控制台返回模型生成的结果（解除注释后）

![image](https://github.com/user-attachments/assets/77092291-c3fc-4541-8dc5-edfeee65acc0)

这里以“A beautiful flower”开头，模型对其进行“续写”，InternLM的模型拥有强大的数学方面的能力。这边它输出的文本似乎是关于一个数学问题，具体是关于一个花朵的花瓣数量。这个问题描述了一个操作，即每次操作可以取走2片花瓣，并且给每片花瓣增加1片。目标是使花瓣的数量尽可能大。

#### 2.1.4 模型上传
- 通过CLI上传
Hugging Face同样是跟Git相关联，通常大模型的模型文件都比较大，因此我们需要安装git lfs，对大文件系统支持。

```bash
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
sudo apt-get install git-lfs
git lfs install
pip install huggingface_hub
```

使用huggingface-cli login命令进行登录，登录过程中需要输入用户的Access Tokens，获取时，需要先验证email

<table>
  <tr>
    <td>
      <img src="https://github.com/user-attachments/assets/47deaf40-97a0-43ad-b591-ae673e5953fa" alt="Image 1" style="width:100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
    </td>
    <td>
      <img src="https://github.com/user-attachments/assets/1b42be1b-8b64-441b-9b2d-6f5a488a056b" alt="Image 2" style="width:100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
    </td>
  </tr>
</table>

![image](https://github.com/user-attachments/assets/ca33b7a2-6ad5-4328-801e-470b3e0df8c9)

验证好之后，点击create new token，创建一个类型为“Write”的token

![image](https://github.com/user-attachments/assets/b9a1c1c2-6a31-4efa-b4dd-f387cfbfc9d1)

```
请复制好token后一定要存储在合适的地方，不然关闭对话框之后，就看不到了
```

![image](https://github.com/user-attachments/assets/25a6c0bd-7cab-4ba2-b8f4-29ac732d877d)

接着可以在CodeSpace里面，使用

```bash
git config --global credential.helper store
huggingface-cli login
```

命令进行登录，这时需要输入刚刚的token

![image](https://github.com/user-attachments/assets/fcd69f8a-596b-4e72-8d56-00a1635d0271)


创建项目
```bash
#intern_study_L0_4就是model_name
huggingface-cli repo create intern_study_L0_4

# 克隆到本地 your_github_name 注意替换成你自己的
git clone https://huggingface.co/{your_github_name}/intern_study_L0_4
```

克隆好之后，应该会在文件夹那边出现对应的文件夹

![image](https://github.com/user-attachments/assets/1e552704-8d4e-4a50-9159-f3119e630f69)


> 使用cp命令，将自己已经训练好保存的模型文件夹中的内容复制到这个repo中（如果有的话）。注意：这里的模型文件夹是指通过transformers的官方接口保存的模型文件夹，比如可以使用model.save_pretrained()或者trainer训练过程中自动保存的checkpoint文件夹。

我们可以把训练好的模型保存进里面，这里考虑到网速问题，只上传我们刚刚下载好的config.json，把它复制粘贴进这个文件夹里面，还可以写一个README.md文件，比如可以粘贴以下内容：

```
# 书生浦语大模型实战营camp4
- hugging face模型上传测试
- 更多内容请访问 https://github.com/InternLM/Tutorial/tree/camp4
```

现在可以用git提交到远程仓库

```bash
cd intern_study_L0_4
git add .
git commit -m "add:intern_study_L0_4"
git push
```

```
注意，如果git push 报错，可能是第一次上传时需要验证，请使用以下命令，注意替换<>里面的内容，然后再次git push一下就可以了
```

```bash
git remote set-url origin https://<user_name>:<token>@huggingface.co/<repo_path>

# 如 git remote set-url origin https://blank:hf_xxxxxxxxxxx@huggingface.co/blank/intern_study_L0_4

# 这里blank和hf_xxxxxxxxxxxx只是示例 请替换为你的username和之前申请的access token

git pull origin
```

现在可以在Hugging Face的个人profile里面看到这个model，也可以直接将下面的Url输入到浏览器网址栏上

```
https://huggingface.co/<user_name>/intern_study_L0_4
```

![image](https://github.com/user-attachments/assets/209b2ba3-c125-474a-9c60-14f3f926ae07)


- 通过平台直接创建

![image](https://github.com/user-attachments/assets/9dee50cd-e0b9-4948-a91a-0012d77d1f3b)

创建一个空的仓库，然后可以通过Add file进行模型文件的上传，也可以git clone后，跟上述操作一样。

![image](https://github.com/user-attachments/assets/05c63128-40d3-4b80-95fd-56c76f34a872)

> PS：熟悉Git工作流后当然还是Git 命令更好用。

#### 2.1.5 Hugging Face Spaces的使用
Hugging Face Spaces 是一个允许我们轻松地托管、分享和发现基于机器学习模型的应用的平台。Spaces 使得开发者可以快速将我们的模型部署为可交互的 web 应用，且无需担心后端基础设施或部署的复杂性。
首先在界面上找到HF的Spaces并进行创建一个新的Space https://huggingface.co/spaces
![image](https://github.com/user-attachments/assets/924fa9ed-0347-4fe0-9a0d-134e5762f19e)

选择Static应用，其他可以按自己喜好填好，然后点击Create Space即可

![image](https://github.com/user-attachments/assets/48f96d31-a79d-4083-8b3e-ad479701399a)

然后就得到一个static 的html页面

![image](https://github.com/user-attachments/assets/f1e405a4-e0ff-48c9-a631-013aaeb0f2a6)

我们可以进入files，然后clone项目进我们的CodeSpace

![image](https://github.com/user-attachments/assets/ae396b06-f106-4f3c-a21b-284c381c06a9)


克隆成功后进入该项目的文件目录，比如在/workspaces/codespaces-jupyter目录下clone的那么就需要

```
cd /workspaces/codespaces-jupyter/intern_cobuild
```

修改我们的html代码

```html
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width" />
  <title>My static Space</title>
  <style>
    html, body {
      margin: 0;
      padding: 0;
      height: 100%;
    }
    body {
      display: flex;
      justify-content: center;
      align-items: center;
    }
    iframe {
      width: 430px;
      height: 932px;
      border: none;
    }
  </style>
</head>
<body>
  <iframe src="https://colearn.intern-ai.org.cn/cobuild" title="description"></iframe>
</body>
</html>
```
保存后就可以push到远程仓库上了，它会自动更新页面。

```bash
git add.
git commit -m "update: colearn page"
git push
```

```
如果报错：remote: Password authentication in git is no longer supported. You must use a user access token or an SSH key instead.
请再次设置这个项目的验证
git remote set-url origin https://<user_name>:<token>@huggingface.co/<repo_path>
例如：
git remote set-url origin https:/jack:hf_xxxxx@huggingface.co/spaces/jack/intern_cobuild/
然后再次git push即可
```

再次进入Space界面，就可以看到我们实战营的共建活动捏~

![image](https://github.com/user-attachments/assets/4b6d4417-4a0e-43d0-a67a-28648935ac3b)


### 2.2 魔搭社区平台
ModelScope 是一个“模型即服务”(MaaS)平台，由阿里巴巴集团的达摩院推出和维护。它旨在汇集来自AI社区的最先进的机器学习模型，并简化在实际应用中使用AI模型的流程。通过ModelScope，用户可以轻松地探索、推理、微调和部署各种AI模型。

注册登录ModelScope平台，进入导航栏模型库，可以搜索internlm找到相关模型（但是这也包括非官方模型）

在这里我们可以搜索 internlm2_5-chat-1_8b，下载1.8b的对话模型，也类似于hugging face 一样拥有具体的详情页。

#### 2.2.1 创建开发机
我们选择 10% 的开发机，镜像选择为 Cuda-12.2。在输入开发机名称后，点击创建开发机。
![image](https://github.com/user-attachments/assets/cc81af53-1c5d-4e9a-9459-716d78a5c123)

创建好开发机后，进入开发机

![image](https://github.com/user-attachments/assets/6274b5c4-a4a5-4dc3-9eee-65b562cd40ca)

在开发机界面的左上角处，选择使用vscode进行编辑代码


![image](https://github.com/user-attachments/assets/267a7478-1be7-493f-8d64-1424b6aa88a5)
新建终端后，在vscode下方出现终端，我们可以输入命令进行操作


![image](https://github.com/user-attachments/assets/dd40dcca-8af8-469f-ab28-dc573a92797b)

接着在终端后面可以输入命令了，这里可以直接粘贴以下命令
```
最好一行一行粘贴等每个命令跑完之后再粘贴下一行
```

#### 2.2.2 环境配置
为ms_demo创建一个可用的conda虚拟环境，可以和其他环境区分开来

```python
# 激活环境
conda activate /root/share/pre_envs/pytorch2.1.2cu12.1

# 安装 modelscope
pip install modelscope -t /root/env/maas
pip install numpy==1.26.0  -t /root/env/maas
pip install packaging -t /root/env/maas
```

注意：为了保证能够找到我们每次装的依赖，每次新建一个终端之后都需要导出path
如果不改变终端，导出一次就够了
```bash
export PATH=$PATH:/root/env/maas/bin
export PYTHONPATH=/root/env/maas:$PYTHONPATH
```
接着创建我们的demo目录

```bash
mkdir -p /root/ms_demo
```

#### 2.2.3 下载指定多个文件
- internlm2_5-7b-chat
考虑到7B的模型文件比较大，这里我们先采用modelscope的cli工具（当然hugging face也有）来下载指定文件，在命令行输入以下命令

```bash
modelscope download \
    --model 'Shanghai_AI_Laboratory/internlm2_5-7b-chat' \
    tokenizer.json config.json model.safetensors.index.json \
    --local_dir '/root/ms_demo'
```

刷新一下文件目录，就能看到在ms_demo中下载了指定的json文件。
- internlm2_5-1_8b-chat

```bash
modelscope download \
    --model 'Shanghai_AI_Laboratory/internlm2_5-1_8b-chat' \
    tokenizer.json config.json model.safetensors.index.json \
    --local_dir '/root/ms_demo'
```

#### 2.2.4 上传模型
魔搭社区类似HF，也有一套创建模型的界面。不同的是，它具有审核机制，当符合它的社区规范时才会被公开。那么当上传正常的模型文件后，审核一般就会通过了。

![image](https://github.com/user-attachments/assets/3711b4c2-69e5-4a7d-844f-b22190620f19)

上传文件的方法可以直接通过平台添加文件，也可以用以下方法

![image](https://github.com/user-attachments/assets/cc300e62-515b-4709-af13-5b049e4a7cdd)


### 2.3 魔乐社区平台

魔乐社区（Modelers）是一个提供多样化、开源模型的平台，旨在促进开发者和研究人员在最先进的模型和流行应用上进行协作。

#### 2.3.1 下载internlm2_5-chat-1_8b模型

> 这里我们可以继续使用我们刚刚创建的InterStudio开发机
```
cd /
mkdir ml_demo
cd ml_demo
```

然后我们可以下载该模型，这里

```
# 确保安装git-lfs 保证大文件的正常下载
apt-get install git-lfs
git lfs install
# clone 仓库
git clone https://modelers.cn/Intern/internlm2_5-1_8b-chat.git
```

刷新一下文件夹，即可在ml_demo中找到下载好的模型文件，在魔乐社区中，还推荐了一个新的深度学习开发套件[openMind Library](https://modelers.cn/docs/zh/openmind-library/overview.html)，除了常用的Transforms的API，也可以探索如何使用openMind来加载模型

```python
# 确保按指南安装好openmind后
from openmind import AutoModel
model = AutoModel.from_pretrained("Intern/internlm2_5-1_8b-chat", trust_remote_code=True")
```

>openMind Library是一个深度学习开发套件，通过简单易用的API支持模型预训练、微调、推理等流程。
>openMind Library通过一套接口兼容PyTorch和MindSpore等主流框架，同时原生支持昇腾NPU处理器。

#### 2.3.2 上传模型
在魔乐社区一般有两种方法，第一种是安装好openmid后使用openmind的API来上传文件，另一个就是用git命令来推送文件，跟一般的git工作流相类似。可参考[上传文件 | 魔乐社区](https://modelers.cn/docs/zh/openmind-hub-client/basic_tutorial/upload.html)
