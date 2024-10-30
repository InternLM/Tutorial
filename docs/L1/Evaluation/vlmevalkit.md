# 多模态大模型评测实践

VLMEvalKit (python 包名为 vlmeval) 是一款专为大型视觉语言模型 (Large Vision-Language Models， LVLMs) 评测而设计的开源工具包。该工具支持在各种基准测试上对大型视觉语言模型进行一键评估，无需进行繁重的数据准备工作，让评估过程更加简便。在 VLMEvalKit 中，我们对所有大型视觉语言模型生成的结果进行评测，并提供基于精确匹配与基于 LLM 的答案提取两种评测结果。


## 评测的基本步骤

在运行评测脚本之前，你需要先**配置** VLMs，并正确设置模型路径。然后你可以使用脚本 `run.py` 进行多个VLMs和基准测试的推理和评估。


### 第0步 安装和设置必要的密钥

**安装**

```bash
git clone https://github.com/open-compass/VLMEvalKit.git
cd VLMEvalKit/
pip install -e .
pip install timm==1.0.11
```

**设置密钥**

要使用 API 模型（如 GPT-4v, Gemini-Pro-V 等）进行推理，或使用 LLM API 作为**评判者或选择提取器**，你需要首先设置 API 密钥。如果你设置了密钥，VLMEvalKit 将默认使用一个评判 LLM 从输出中提取答案，否则它将使用**精确匹配模式**（在输出字符串中查找 "Yes", "No", "A", "B", "C"...）。**精确匹配模式只能应用于是或否任务和多项选择任务。**


你可以将所需的密钥放在 `$VLMEvalKit/.env` 中，或直接将它们设置为环境变量。如果你选择创建 `.env` 文件，
VLMEvalKit 会根据你的环境变量配置来决定使用哪个模型作为评判 LLM. 


### 第1步 配置

**VLM 配置**：所有 VLMs 都在 `vlmeval/config.py` 中配置。对于某些 VLMs，在进行评估之前，你需要配置代码根目录（如 MiniGPT-4、PandaGPT 等）或模型权重根目录（如 LLaVA-v1-7B 等）。在评估时，你应该使用 `vlmeval/config.py` 中 `supported_VLM` 指定的模型名称来选择 VLM。


```python
internvl_series = {
    'InternVL-Chat-V1-1': partial(InternVLChat, model_path='OpenGVLab/InternVL-Chat-V1-1', version='V1.1'),
    'InternVL-Chat-V1-2': partial(InternVLChat, model_path='OpenGVLab/InternVL-Chat-V1-2', version='V1.2'),
    'InternVL-Chat-V1-2-Plus': partial(InternVLChat, model_path='OpenGVLab/InternVL-Chat-V1-2-Plus', version='V1.2'),
    'InternVL-Chat-V1-5': partial(InternVLChat, model_path='OpenGVLab/InternVL-Chat-V1-5', version='V1.5'),
    'Mini-InternVL-Chat-2B-V1-5': partial(InternVLChat, model_path='OpenGVLab/Mini-InternVL-Chat-2B-V1-5', version='V1.5'),
    'Mini-InternVL-Chat-4B-V1-5': partial(InternVLChat, model_path='OpenGVLab/Mini-InternVL-Chat-4B-V1-5', version='V1.5'),
    # InternVL2 series
    'InternVL2-1B': partial(InternVLChat, model_path='OpenGVLab/InternVL2-1B', version='V2.0'),
    # 此处修改成等待评估模型的本地路径
    'InternVL2-2B': partial(InternVLChat, model_path="/share/new_models/OpenGVLab/InternVL2-2B", version='V2.0'), 
    'InternVL2-4B': partial(InternVLChat, model_path='OpenGVLab/InternVL2-4B', version='V2.0'),
    'InternVL2-8B': partial(InternVLChat, model_path='OpenGVLab/InternVL2-8B', version='V2.0'),
    'InternVL2-26B': partial(InternVLChat, model_path='OpenGVLab/InternVL2-26B', version='V2.0'),
    'InternVL2-40B': partial(InternVLChat, model_path='OpenGVLab/InternVL2-40B', version='V2.0', load_in_8bit=True),
    'InternVL2-76B': partial(InternVLChat, model_path='OpenGVLab/InternVL2-Llama3-76B', version='V2.0'),
}
```

此处我们指定好了等待评估模型 `InternVL2-2B` 的本地路径. 一些 VLMs 需要额外配置步骤, 例如 InstructBLIP 需要安装 LAVIS 库.

<!-- **代码准备和安装**: InstructBLIP ([LAVIS](https://github.com/salesforce/LAVIS)), LLaVA ([LLaVA](https://github.com/haotian-liu/LLaVA)), MiniGPT-4 ([MiniGPT-4](https://github.com/Vision-CAIR/MiniGPT-4)), mPLUG-Owl2 ([mPLUG-Owl2](https://github.com/X-PLUG/mPLUG-Owl/tree/main/mPLUG-Owl2)), OpenFlamingo-v2 ([OpenFlamingo](https://github.com/mlfoundations/open_flamingo)), PandaGPT-13B ([PandaGPT](https://github.com/yxuansu/PandaGPT)), TransCore-M ([TransCore-M](https://github.com/PCIResearch/TransCore-M)).

**手动权重文件准备与配置**: InstructBLIP, LLaVA-v1-7B, MiniGPT-4, PandaGPT-13B -->

### 第2步 评测

我们使用 `run.py` 进行评估, 其参数如下:

- `--data (list[str])`: 设置在 VLMEvalKit 中支持的数据集名称（在 `vlmeval/utils/dataset_config.py` 中定义）
- `--model (list[str])`: 设置在 VLMEvalKit 中支持的 VLM 名称（在 `vlmeval/config.py` 中的 `supported_VLM` 中定义）
- `--mode (str, 默认值为 'all', 可选值为 ['all', 'infer'])`：当 mode 设置为 "all" 时，将执行推理和评估；当设置为 "infer" 时，只执行推理
<!-- - `--nproc (int, default to 4)`: 调用 API 的线程数 -->
- `--work-dir (str, default to '.')`: 存放测试结果的目录
<!-- - `--nframe (int, default to 8)`: 从视频中采样的帧数，仅对视频多模态评测集适用 -->
<!-- - `--pack (bool, store_true)`: 一个视频可能关联多个问题，如 `pack==True`，将会在一次询问中提问所有问题 -->


你可以使用 `python` 或 `torchrun` 来运行脚本评测图像多模态评测集:

```bash
# 使用 `python` 运行时，只实例化一个 VLM，并且它可能使用多个 GPU, 这推荐用于评估参数量非常大的 VLMs
# 在 MMBench_DEV_EN、MME 和 SEEDBench_IMG 上使用 InternVL2-2B  进行推理和评估
python run.py --data MMBench_DEV_EN MME SEEDBench_IMG --model InternVL2-2B --verbose
# 在 MMBench_DEV_EN、MME 和 SEEDBench_IMG 上使用 InternVL2-2B  仅进行推理
python run.py --data MMBench_DEV_EN MME SEEDBench_IMG --model InternVL2-2B --verbose --mode infer

# 使用 `torchrun` 运行时稍有不同，每个 GPU 上实例化一个 VLM 实例, 这可以加快推理速度. 但是，这仅适用于消耗少量 GPU 内存的 VLMs。
```

评估结果将作为日志打印出来。此外，结果文件也会在目录 `$YOUR_WORKING_DIRECTORY/{model_name}` 中生成。以 `.csv` 结尾的文件包含评估的指标。

## 部署本地语言模型作为评判LLM

上述默认设置使用 OpenAI 的 GPT 作为评判 LLM。你也可以使用 [LMDeploy](https://github.com/InternLM/lmdeploy) 部署本地评判 LLM。

首先进行安装:
```bash
pip install lmdeploy==0.6.1 openai==1.52.0
```

假设我们使用 internlm2_5-1_8b-chat 作为评判，端口为 23333，密钥为 sk-123456（在这个本地部署的场景中，OPENAI_API_KEY 可以随意设置，只要遵循指定的格式）, 然后可以通过一行代码部署本地评判 LLM：

```bash
# --cache-max-entry-count 0.4 设置用于减少 GPU 占用
lmdeploy serve api_server /share/new_models/Shanghai_AI_Laboratory/internlm2_5-1_8b-chat/ --cache-max-entry-count 0.4 --server-port 23333
```

![image](https://github.com/user-attachments/assets/e84c2ce9-5e49-435b-b4f9-b58a60b49dad)


新打开一个终端, 使用以下 Python 代码获取由 LMDeploy 注册的模型名称：
```python
from openai import OpenAI
client = OpenAI(
    api_key='sk-123456',
    base_url="http://0.0.0.0:23333/v1"
)
model_name = client.models.list().data[0].id
model_name
```
显示结果为 `/share/new_models/Shanghai_AI_Laboratory/internlm2_5-1_8b-chat`, 接着配置对应环境变量，以告诉 VLMEvalKit 如何使用本地评判 LLM。正如上面提到的，也可以在  `$VLMEvalKit/.env` 文件中设置：

```
OPENAI_API_KEY=sk-123456
OPENAI_API_BASE=http://0.0.0.0:23333/v1/chat/completions
LOCAL_LLM='/share/new_models/Shanghai_AI_Laboratory/internlm2_5-1_8b-chat' # 注册的模型名称
```

最后，你可以运行第2步中的命令，使用本地评判 LLM 来评估你的 VLM, 例如:

```bash
python run.py --data MMBench_DEV_EN MME SEEDBench_IMG --model InternVL2-2B --verbose
```
![image](https://github.com/user-attachments/assets/64b48085-6d45-489f-8de9-c5e4426598f0)

