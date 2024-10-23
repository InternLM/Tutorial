<img width="900" alt="image" src="https://github.com/user-attachments/assets/588c8e50-7eba-4d63-8af0-bdeeb8419956">


# OpenCompass 评测


OpenCompass 是一个功能强大的大模型评测工具，支持两种便捷的评测方式：
- **直接评测**：通过加载模型权重文件进行评测
- **API 模式评测**：对已部署的模型服务进行评测，无需加载模型权重

本教程将带你使用 OpenCompass 评测 InternLM2.5-Chat-1.8B 在 C-Eval 数据集上的性能。整个评测过程非常简单，包含三个步骤：
1. 配置阶段：准备环境，选择模型和数据集
2. 推理评估：运行评测获取模型输出并打分
3. 查看报告：自动生成 CSV 和 TXT 格式的评测报告

> 注：如果你对多模态模型感兴趣，可以参考[VLMEvalKit教程](vlmevalkit.md)进行多模态评测。

更多使用说明，请参考 OpenCompass [官方文档](https://opencompass.readthedocs.io/en/latest/tutorial.html)。


## 配置


### 环境准备

创建开发机和 Conda 环境之后, 安装 OpenCompass 及其相关软件包 (注意：一定要先 cd /root)

```bash
conda create -n opencompass python=3.10
conda activate opencompass
conda install pytorch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 pytorch-cuda=12.1 -c pytorch -c nvidia -y

cd /root
git clone -b 0.3.3 https://github.com/open-compass/opencompass
cd opencompass
pip install -e .


apt-get update
apt-get install cmake
pip install -r requirements.txt
pip install protobuf
```

### 数据集准备


```bash
cp /share/temp/datasets/OpenCompassData-core-20231110.zip /root/opencompass/
unzip OpenCompassData-core-20231110.zip
```
将会在 OpenCompass 下看到data文件夹.



### 配置文件

列出所有跟 InternLM 及 C-Eval 相关的配置

```bash
python tools/list_configs.py internlm ceval
```
将会看到如下输出

```
+----------------------------------------+----------------------------------------------------------------------+
| Model                                  | Config Path                                                          |
|----------------------------------------+----------------------------------------------------------------------|
| hf_internlm2_1_8b                      | configs/models/hf_internlm/hf_internlm2_1_8b.py                      |
| hf_internlm2_20b                       | configs/models/hf_internlm/hf_internlm2_20b.py                       |
| hf_internlm2_7b                        | configs/models/hf_internlm/hf_internlm2_7b.py                        |
| hf_internlm2_base_20b                  | configs/models/hf_internlm/hf_internlm2_base_20b.py                  |
| hf_internlm2_base_7b                   | configs/models/hf_internlm/hf_internlm2_base_7b.py                   |
| hf_internlm2_chat_1_8b                 | configs/models/hf_internlm/hf_internlm2_chat_1_8b.py                 |
| hf_internlm2_chat_1_8b_sft             | configs/models/hf_internlm/hf_internlm2_chat_1_8b_sft.py             |
| hf_internlm2_chat_20b                  | configs/models/hf_internlm/hf_internlm2_chat_20b.py                  |
| hf_internlm2_chat_20b_sft              | configs/models/hf_internlm/hf_internlm2_chat_20b_sft.py              |
| ...                                    | ...                                                                  |     
+----------------------------------------+----------------------------------------------------------------------+
+--------------------------------+-------------------------------------------------------------------+
| Dataset                        | Config Path                                                       |
|--------------------------------+-------------------------------------------------------------------|
| ceval_clean_ppl                | configs/datasets/ceval/ceval_clean_ppl.py                         |
| ceval_contamination_ppl_810ec6 | configs/datasets/contamination/ceval_contamination_ppl_810ec6.py  |
| ceval_gen                      | configs/datasets/ceval/ceval_gen.py                               |
| ceval_gen_2daf24               | configs/datasets/ceval/ceval_gen_2daf24.py                        |
| ceval_gen_5f30c7               | configs/datasets/ceval/ceval_gen_5f30c7.py                        |
| ceval_ppl                      | configs/datasets/ceval/ceval_ppl.py                               |
| ceval_ppl_1cd8bf               | configs/datasets/ceval/ceval_ppl_1cd8bf.py                        |
| ceval_ppl_578f8d               | configs/datasets/ceval/ceval_ppl_578f8d.py                        |
| ...                            | ...                                                               |
+--------------------------------+-------------------------------------------------------------------+
```




## 启动评测(10% A100 8GB 资源)

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
``` 
评测完成后，将会看到：

![image](https://github.com/user-attachments/assets/86062cae-2c82-42c3-a0ad-884aa331b58f)


我们也可以使用配置文件来指定数据集和模型，例如：

```bash
cd /root/opencompass/configs/
touch eval_tutorial_demo.py
```

打开eval_tutorial_demo.py 贴入以下代码

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


## 评测 API 模型(选做)

OpenCompass 通过其设计，不会真正区分开源模型和 API 模型。您可以以相同的方式或甚至在一个设置中评估这两种模型类型。

首先安装和部署模型:

```bash
pip install lmdeploy openai

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


使用以下 Python 代码获取由 LMDeploy 注册的模型名称：

```python
from openai import OpenAI
client = OpenAI(
    api_key='sk-123456',
    base_url="http://0.0.0.0:23333/v1"
)
model_name = client.models.list().data[0].id
model_name
```

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
        path='/share/new_models/Shanghai_AI_Laboratory/internlm2_5-1_8b-chat/',
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

得到结果

![image](https://github.com/user-attachments/assets/2d076f75-3e15-4100-975f-1d2eae31a4b2)
