# 快速大语言模型评测实践


我们再书生浦语实战营的基础设施上，分别快速使用 OpenCompass 和 VLMEvalKit 快速评测:

- InternLM2.5-Chat-1.8B 模型在 C-Eval 数据集上的性能 
- InternVL2-2B 模型在 MMBench 数据集上的性能



## OpenCompass: 大语言模型评测

OpenCompass 是一个用于大模型评估的一站式平台，支持多种主流大模型和数据集的评测。

step 1. 安装 OpenCompass 及其相关依赖

step 2. 准备评测数据

可以通过命令行下载并解压数据集到特定文件夹，也可从 OpenCompass 存储服务器自动下载，还能使用 ModelScope 按需加载数据集来获得数据.  最快捷的方式是使用 OpenCompass 自动下载功能。只需运行评测命令时添加 `--dry-run` 参数，即可自动从 OpenCompass 存储服务器下载所需数据集。


---
📌 OpenCompass 小知识: 在 OpenCompass 中，--dry-run 参数, e.g. 

`python run.py --datasets ceval_gen --models hf_internlm2_5_1_8b_chat --dry-run` 

功能如下：

- 数据集守门员：触发缺失数据集的自动下载，无需实际评测
- 效率利器：快速验证配置正确性，节省宝贵时间

使用 --dry-run 不仅可以让您提前洞察评测全貌，还能确保评测起跑线上万事俱备，是评测前的必备利器！

---

step 3. 配置模型运行评测

例如评测 internlm2_5-1_8b-chat 模型在 ceval_gen 数据集上的表现，可以如下配置模型：

```python
# /root/opencompass/configs/models/hf_internlm/hf_internlm2_5_1_8b_chat.py
from opencompass.models import HuggingFacewithChatTemplate

models = [
    dict(
        type=HuggingFacewithChatTemplate,
        abbr='internlm2_5-1_8b-chat-hf',
        # path='internlm/internlm2_5-1_8b-chat',
        path='/share/new_models/Shanghai_AI_Laboratory/internlm2_5-1_8b-chat', # 本地路径
        max_out_len=2048,
        batch_size=8,
        run_cfg=dict(num_gpus=1),
    )
]
```

有两种运行评测的方式:

- 命令行配置参数方式
- 配置文件修改参数方式


```bash
python run.py --datasets ceval_gen --models hf_internlm2_5_1_8b_chat 
```


## VLMEvalKit: 多模态大语言模型评测

VLMEvalKit (python 包名为 vlmeval) 是一款专为大型视觉语言模型 (Large Vision-Language Models， LVLMs) 评测而设计的开源工具包。安装方式如下:

```bash
git clone https://github.com/open-compass/VLMEvalKit.git
cd VLMEvalKit
pip install -e .
```

我们可以部署本地模型作为评判 LLM, 例如部署 internlm2_5-1_8b-chat 模型:

```bash
# --cache-max-entry-count 0.4 设置用于减少 GPU 占用
lmdeploy serve api_server /share/new_models/Shanghai_AI_Laboratory/internlm2_5-1_8b-chat/ --cache-max-entry-count 0.4 --server-port 23333
```

然后在  `$VLMEvalKit/.env` 文件中设置：

```
OPENAI_API_KEY=sk-123456
OPENAI_API_BASE=http://0.0.0.0:23333/v1/chat/completions
LOCAL_LLM='/share/new_models/Shanghai_AI_Laboratory/internlm2_5-1_8b-chat'
```


如果设置了 API 密钥, VLMEvalKit 默认使用一个评判 LLM 从输出中提取答案, 否则使用精确匹配模式. 精确匹配模式只能应用于是或否任务和多项选择任务.


Step 1. 模型等配置

**VLM 配置**：所有 VLMs 都在 `vlmeval/config.py` 中配置。在评估时，你应该使用 `vlmeval/config.py` 中 `supported_VLM` 指定的模型名称来选择 VLM。

![config](https://github.com/user-attachments/assets/56578745-a8e1-4aa1-88fb-47d21874864b)


我们这里指定了本地模型的路径 `INTERVL2_2B_MODEL_PTH`. 

Step 2. 评测

我们使用 `run.py` 进行评估:

```bash
python run.py --data MMBench_DEV_EN --model InternVL2-2B --verbose
```

相关参数含义如下:
- `--data (list[str])`: 设置在 VLMEvalKit 中支持的数据集名称（在 `vlmeval/utils/dataset_config.py` 中定义）
- `--model (list[str])`: 设置在 VLMEvalKit 中支持的 VLM 名称（在 `vlmeval/config.py` 中的 `supported_VLM` 中定义）
- `--verbose`: 是否打印详细日志
- `--mode (str, 默认值为 'all', 可选值为 ['all', 'infer'])`：当 mode 设置为 "all" 时，将执行推理和评估；当设置为 "infer" 时，只执行推理
- `--work-dir (str, default to '.')`: 存放测试结果的目录


![local_llm](https://github.com/user-attachments/assets/551da64f-8ce7-4880-84ce-a5f8b808e123)


