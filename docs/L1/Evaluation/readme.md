<img width="900" alt="image" src="https://github.com/user-attachments/assets/588c8e50-7eba-4d63-8af0-bdeeb8419956">


# OpenCompass 评测

本节课程聚焦于大语言模型的评测，在后续的课程中我们将介绍多模态大模型的评测方法。

OpenCompass 提供了 **API 模式评测**和**本地直接评测**两种方式。其中 API 模式评测针对那些以 API 服务形式部署的模型，而本地直接评测则面向那些可以获取到模型权重文件的情况。

我们首先在训练营提供的开发机上创建用于评测 conda 环境:

```bash
conda create -n opencompass python=3.10
conda activate opencompass

cd /root
git clone -b 0.3.3 https://github.com/open-compass/opencompass
cd opencompass
pip install -e .
pip install -r requirements.txt
pip install huggingface_hub==0.25.2

pip install importlib-metadata
```

更多使用说明，请参考 OpenCompass [官方文档](https://opencompass.readthedocs.io/en/latest/tutorial.html)。



## 评测 API 模型 

如果你想要评测通过 API 访问的大语言模型，整个过程其实很简单。首先你需要获取模型的 API 密钥（API Key）和接口地址。以 OpenAI 的 GPT 模型为例，你只需要在 OpenAI 官网申请一个 API Key，然后在评测配置文件中设置好这个密钥和相应的模型参数就可以开始评测了。评测过程中，评测框架会自动向模型服务发送测试用例，获取模型的回复并进行打分分析。整个过程你不需要准备任何模型文件，也不用担心本地计算资源是否足够，只要确保网络连接正常即可。


考虑到 openai 的 API 服务暂时在国内无法直接使用，我们这里以评测 internlm 模型为例，介绍如何评测 API 模型。


1) 打开网站浦语官方地址 https://internlm.intern-ai.org.cn/api/document 获得 api key 和 api 服务地址 (也可以从第三方平台 [硅基流动](https://siliconflow.cn/zh-cn/siliconcloud) 获取), 在终端中运行:

```bash
export INTERNLM_API_KEY=xxxxxxxxxxxxxxxxxxxxxxx # 填入你申请的 API Key
```

2) 配置模型: 在终端中运行 `cd /root/opencompass/` 和 `touch opencompass/configs/models/openai/puyu_api.py`, 然后打开文件, 贴入以下代码:


```python
import os
from opencompass.models import OpenAISDK


internlm_url = 'https://internlm-chat.intern-ai.org.cn/puyu/api/v1/' # 你前面获得的 api 服务地址
internlm_api_key = os.getenv('INTERNLM_API_KEY')

models = [
    dict(
        # abbr='internlm2.5-latest',
        type=OpenAISDK,
        path='internlm2.5-latest', # 请求服务时的 model name
        # 换成自己申请的APIkey
        key=internlm_api_key, # API key
        openai_api_base=internlm_url, # 服务地址
        rpm_verbose=True, # 是否打印请求速率
        query_per_second=0.16, # 服务请求速率
        max_out_len=1024, # 最大输出长度
        max_seq_len=4096, # 最大输入长度
        temperature=0.01, # 生成温度
        batch_size=1, # 批处理大小
        retry=3, # 重试次数
    )
]
```

3) 配置数据集: 在终端中运行 `cd /root/opencompass/` 和 `touch opencompass/configs/datasets/demo/demo_cmmlu_chat_gen.py`, 然后打开文件, 贴入以下代码:

```python
from mmengine import read_base

with read_base():
    from ..cmmlu.cmmlu_gen_c13365 import cmmlu_datasets


# 每个数据集只取前2个样本进行评测
for d in cmmlu_datasets:
    d['abbr'] = 'demo_' + d['abbr']
    d['reader_cfg']['test_range'] = '[0:1]' # 这里每个数据集只取1个样本, 方便快速评测.


```
这样我们使用了 CMMLU Benchmark 的每个子数据集的 1 个样本进行评测.

 
完成配置后, 在终端中运行: `python run.py --models puyu_api.py --datasets demo_cmmlu_chat_gen.py --debug`. 预计运行10分钟后, 得到结果:

![image](https://github.com/user-attachments/assets/74213aca-1b83-4065-be84-68a318e8da48)






## 评测本地模型


如果你想要评测本地部署的大语言模型，首先需要获取到完整的模型权重文件。以开源模型为例，你可以从 Hugging Face 等平台下载模型文件。接下来，你需要准备足够的计算资源，比如至少一张显存够大的 GPU，因为模型文件通常都比较大。有了模型和硬件后，你需要在评测配置文件中指定模型路径和相关参数，然后评测框架就会自动加载模型并开始评测。这种评测方式虽然前期准备工作相对繁琐，需要考虑硬件资源，但好处是评测过程完全在本地完成，不依赖网络状态，而且你可以更灵活地调整模型参数，深入了解模型的性能表现。这种方式特别适合需要深入研究模型性能或进行模型改进的研发人员。


我们接下以评测 InternLM2-Chat-1.8B 在 C-Eval 数据集上的性能为例，介绍如何评测本地模型。

### 相关配置


安装相关软件包:

```bash
cd /root/opencompass
conda activate opencompass
conda install pytorch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 pytorch-cuda=12.1 -c pytorch -c nvidia -y
apt-get update
apt-get install cmake
pip install protobuf==4.25.3
pip install huggingface-hub==0.23.2
```

为了方便评测，我们首先将数据集下载到本地:

```bash
cp /share/temp/datasets/OpenCompassData-core-20231110.zip /root/opencompass/
unzip OpenCompassData-core-20231110.zip
```
将会在 OpenCompass 下看到data文件夹. 



### 加载本地模型进行评测


在 OpenCompass 中，模型和数据集的配置文件都存放在 `configs` 文件夹下。我们可以通过运行 `list_configs` 命令列出所有跟 InternLM 及 C-Eval 相关的配置。

```bash
python tools/list_configs.py internlm ceval
```

打开 opencompass 文件夹下 `configs/models/hf_internlm/的 hf_internlm2_5_1_8b_chat.py` 文件, 修改如下:

```python
from opencompass.models import HuggingFacewithChatTemplate

models = [
    dict(
        type=HuggingFacewithChatTemplate,
        abbr='internlm2_5-1_8b-chat-hf',
        path='/share/new_models/Shanghai_AI_Laboratory/internlm2_5-1_8b-chat/',
        max_out_len=2048,
        batch_size=8,
        run_cfg=dict(num_gpus=1),
    )
]

# python run.py --datasets ceval_gen --models hf_internlm2_5_1_8b_chat --debug
```

可以通过以下命令评测 InternLM2-Chat-1.8B 模型在 C-Eval 数据集上的性能。由于 OpenCompass 默认并行启动评估过程，我们可以在第一次运行时以 --debug 模式启动评估，并检查是否存在问题。在 --debug 模式下，任务将按顺序执行，并实时打印输出。

```bash
python run.py --datasets ceval_gen --models hf_internlm2_5_1_8b_chat --debug
# 如果出现 rouge 导入报错, 请 pip uninstall rouge 之后再次安装 pip install rouge==1.0.1 可解决问题.
``` 
评测比较费时, 预计2~4个小时评测完成后，将会看到：

![image](https://github.com/user-attachments/assets/86062cae-2c82-42c3-a0ad-884aa331b58f)


我们也可以使用配置文件来指定数据集和模型，例如：

```bash
cd /root/opencompass/configs/
touch eval_tutorial_demo.py
```

打开 `eval_tutorial_demo.py` 贴入以下代码

```python
from mmengine.config import read_base

with read_base():
    from .datasets.ceval.ceval_gen import ceval_datasets
    from .models.hf_internlm.hf_internlm2_5_1_8b_chat import models as hf_internlm2_5_1_8b_chat_models

datasets = ceval_datasets
models = hf_internlm2_5_1_8b_chat_models
```

这样我们指定了评测的模型和数据集，然后运行

```bash
python run.py configs/eval_tutorial_demo.py --debug 
```


## 将本地模型通过部署成API服务再评测

前面我们介绍了如何评测 API 模型和本地模型, 现在我们介绍如何将本地模型部署成 API 服务, 然后通过评测 API 服务的方式来评测本地模型. OpenCompass 通过其设计，不会真正区分开源模型和 API 模型。您可以使用相同的方式甚至在一个设置中评估这两种模型类型。

首先打开一个终端, 安装和部署模型:

```bash
pip install lmdeploy==0.6.1 openai==1.52.0

lmdeploy serve api_server /share/new_models/Shanghai_AI_Laboratory/internlm2_5-1_8b-chat/ --server-port 23333
```

成功部署以后会看到如下输出:
```
[WARNING] gemm_config.in is not found; using default GEMM algo                                                                                                                                                                                              
HINT:    Please open http://0.0.0.0:23333 in a browser for detailed api usage!!!
HINT:    Please open http://0.0.0.0:23333 in a browser for detailed api usage!!!
HINT:    Please open http://0.0.0.0:23333 in a browser for detailed api usage!!!
INFO:     Started server process [59833]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:23333 (Press CTRL+C to quit)
INFO:     127.0.0.1:38584 - "POST /v1/chat/completions HTTP/1.1" 200 OK
```


新开一个终端, 使用以下 Python 代码获取由 LMDeploy 注册的模型名称：

```python
from openai import OpenAI
client = OpenAI(
    api_key='sk-123456', # 可以设置成随意的字符串
    base_url="http://0.0.0.0:23333/v1"
)
model_name = client.models.list().data[0].id
model_name # 注册的模型名称需要被用于后续配置.
```
结果显示 `/share/new_models/Shanghai_AI_Laboratory/internlm2_5-1_8b-chat/`, 接着, 
创建配置脚本 `/root/opencompass/configs/models/hf_internlm/hf_internlm2_5_1_8b_chat_api.py`

```python
from opencompass.models import OpenAI

api_meta_template = dict(round=[
    dict(role='HUMAN', api_role='HUMAN'),
    dict(role='BOT', api_role='BOT', generate=True),
])

models = [
    dict(
        abbr='InternLM-2.5-1.8B-Chat',
        type=OpenAI,
        path='/share/new_models/Shanghai_AI_Laboratory/internlm2_5-1_8b-chat/', # 注册的模型名称
        key='sk-123456',
        openai_api_base='http://0.0.0.0:23333/v1/chat/completions', 
        meta_template=api_meta_template,
        query_per_second=1,
        max_out_len=2048,
        max_seq_len=4096,
        batch_size=8),
]
```

然后运行

```bash
opencompass --models hf_internlm2_5_1_8b_chat_api --datasets ceval_gen --debug # opencompass 命令基本等价于 python run.py 命令
```

得到结果: 

![image](https://github.com/user-attachments/assets/2d076f75-3e15-4100-975f-1d2eae31a4b2)
