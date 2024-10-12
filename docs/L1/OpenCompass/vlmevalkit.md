# VLMEvalKit: 一种多模态大模型评测工具

VLMEvalKit (python 包名为 vlmeval) 是一款专为大型视觉语言模型 (Large Vision-Language Models， LVLMs) 评测而设计的开源工具包。该工具支持在各种基准测试上对大型视觉语言模型进行一键评估，无需进行繁重的数据准备工作，让评估过程更加简便。在 VLMEvalKit 中，我们对所有大型视觉语言模型生成的结果进行评测，并提供基于精确匹配与基于 LLM 的答案提取两种评测结果。


## 评测的基本步骤

在运行评测脚本之前，你需要先**配置** VLMs，并正确设置模型路径。然后你可以使用脚本 `run.py` 进行多个VLMs和基准测试的推理和评估。


### 第0步 安装和设置必要的密钥

**安装**

```bash
git clone https://github.com/open-compass/VLMEvalKit.git
cd VLMEvalKit
pip install -e .
```

**设置密钥**

要使用 API 模型（如 GPT-4v, Gemini-Pro-V 等）进行推理，或使用 LLM API 作为**评判者或选择提取器**，你需要首先设置 API 密钥。如果你设置了密钥，VLMEvalKit 将默认使用一个评判 LLM 从输出中提取答案，否则它将使用**精确匹配模式**（在输出字符串中查找 "Yes", "No", "A", "B", "C"...）。**精确匹配模式只能应用于是或否任务和多项选择任务。**


你可以将所需的密钥放在 `$VLMEvalKit/.env` 中，或直接将它们设置为环境变量。如果你选择创建 `.env` 文件，
VLMEvalKit 会根据你的环境变量配置来决定使用哪个模型作为评判 LLM. 


### 第1步 配置

**VLM 配置**：所有 VLMs 都在 `vlmeval/config.py` 中配置。对于某些 VLMs，在进行评估之前，你需要配置代码根目录（如 MiniGPT-4、PandaGPT 等）或模型权重根目录（如 LLaVA-v1-7B 等）。在评估时，你应该使用 `vlmeval/config.py` 中 `supported_VLM` 指定的模型名称来选择 VLM。


![config](https://github.com/user-attachments/assets/56578745-a8e1-4aa1-88fb-47d21874864b)


例如我们这里指定了本地模型的路径 `INTERVL2_1B_MODEL_PTH, INTERVL2_2B_MODEL_PTH`. 一些 VLMs 需要额外配置步骤, 例如 InstructBLIP 需要安装 LAVIS 库.

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

<!-- **用于评测图像多模态评测集的命令** -->

你可以使用 `python` 或 `torchrun` 来运行脚本评测图像多模态评测集:

```bash
# 使用 `python` 运行时，只实例化一个 VLM，并且它可能使用多个 GPU。
# 这推荐用于评估参数量非常大的 VLMs（如 IDEFICS-80B-Instruct）。

# 在 MMBench_DEV_EN、MME 和 SEEDBench_IMG 上使用 IDEFICS-80B-Instruct 进行推理和评估
python run.py --data MMBench_DEV_EN MME SEEDBench_IMG --model InternVL2-2B --verbose
# 在 MMBench_DEV_EN、MME 和 SEEDBench_IMG 上使用 IDEFICS-80B-Instruct 仅进行推理
python run.py --data MMBench_DEV_EN MME SEEDBench_IMG --model InternVL2-2B --verbose --mode infer

# 使用 `torchrun` 运行时，每个 GPU 上实例化一个 VLM 实例。这可以加快推理速度。
# 但是，这仅适用于消耗少量 GPU 内存的 VLMs。

# 在 MMBench_DEV_EN、MME 和 SEEDBench_IMG 上使用 IDEFICS-9B-Instruct、Qwen-VL-Chat、mPLUG-Owl2。在具有 8 个 GPU 的节点上进行推理和评估。
torchrun --nproc-per-node=8 run.py --data MMBench_DEV_EN MME SEEDBench_IMG --model InternVL2-2B  --verbose
# 在 MME 上使用 Qwen-VL-Chat。在具有 2 个 GPU 的节点上进行推理和评估。
torchrun --nproc-per-node=2 run.py --data MME --model InternVL2-2B --verbose
```

<!-- **用于评测视频多模态评测集的命令**

```bash
# 使用 `python` 运行时，只实例化一个 VLM，并且它可能使用多个 GPU。
# 这推荐用于评估参数量非常大的 VLMs（如 IDEFICS-80B-Instruct）。

# 在 MMBench-Video 上评测 IDEFCIS2-8B, 视频采样 8 帧作为输入，不采用 pack 模式评测
torchrun --nproc-per-node=8 run.py --data MMBench-Video --model InternVL2-1B --nframe 8
# 在 MMBench-Video 上评测 GPT-4o (API 模型), 视频采样 16 帧作为输入，采用 pack 模式评测
python run.py --data MMBench-Video --model InternVL2-1B --nframe 16 --pack
``` -->

评估结果将作为日志打印出来。此外，结果文件也会在目录 `$YOUR_WORKING_DIRECTORY/{model_name}` 中生成。以 `.csv` 结尾的文件包含评估的指标。

## 部署本地语言模型作为评判LLM

上述默认设置使用 OpenAI 的 GPT 作为评判 LLM。你也可以使用 [LMDeploy](https://github.com/InternLM/lmdeploy) 部署本地评判 LLM。

首先进行安装:
```bash
pip install lmdeploy openai
```

假设我们使用 internlm2-chat-1_8b-chat 作为评判，端口为 23333，密钥为 sk-123456（在这个本地部署的场景中，OPENAI_API_KEY 可以随意设置，只要遵循指定的格式（以 "sk-" 开头，后跟任意字符））, 然后可以通过一行代码部署本地评判 LLM：

```bash
# --cache-max-entry-count 0.4 设置用于减少 GPU 占用
lmdeploy serve api_server /share/new_models/Shanghai_AI_Laboratory/internlm2_5-1_8b-chat/ --cache-max-entry-count 0.4 --server-port 23333
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

配置对应环境变量，以告诉 VLMEvalKit 如何使用本地评判 LLM。正如上面提到的，也可以在  `$VLMEvalKit/.env` 文件中设置：

```
OPENAI_API_KEY=sk-123456
OPENAI_API_BASE=http://0.0.0.0:23333/v1/chat/completions
LOCAL_LLM=<model_name you get>
```

最后，你可以运行第2步中的命令，使用本地评判 LLM 来评估你的 VLM, 例如:

```bash
python run.py --data MMBench_DEV_EN MME SEEDBench_IMG --model InternVL2-2B --verbose
```

![local_llm](https://github.com/user-attachments/assets/551da64f-8ce7-4880-84ce-a5f8b808e123)

<!-- 
- 如果你希望将评判 LLM 部署在单独的一个 GPU 上，并且由于 GPU 内存有限而希望在其他 GPU 上评估你的 VLM，可以使用 `CUDA_VISIBLE_DEVICES=x` 这样的方法，例如：
```
CUDA_VISIBLE_DEVICES=0 lmdeploy serve api_server internlm/internlm2-chat-1_8b --server-port 23333
CUDA_VISIBLE_DEVICES=1,2,3 torchrun --nproc-per-node=3 run.py --data HallusionBench  --model qwen_chat --verbose
```
- 如果本地评判 LLM 在遵循指令方面不够好，评估过程可能会失败。请通过 issues 报告此类失败情况。
- 可以以不同的方式部署评判 LLM，例如使用私有 LLM（而非来自 HuggingFace）或使用量化 LLM。请参考 [LMDeploy doc](https://lmdeploy.readthedocs.io/en/latest/serving/api_server.html) 文档。也可以使用其他支持 OpenAI API 框架的方法。 -->