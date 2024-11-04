# XTuner微调高级进阶

## 1 增量预训练微调

本节我们先来了解一下增量预训练，这里我们以一个文本续写案例来看看效果。

|      | 微调前                                                       | 微调后                                                       |
| ---- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 输入 | 书生·浦语大模型实战营第三期是                                | 书生·浦语大模型实战营第三期是                                |
| 输出 | 书生·浦语大模型实战营第三期是上周五，上周五我们学习了一个新的知识，那就是关于机器学习的概率统计。…… | 书生·浦语大模型实战营第三期是上海人工智能实验室推出的书生·浦语大模型实战营系列活动的第三批次，将于2024年7月正式进行。…… |

我们需要定义一些基本方法。

- 导入必要的库


```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
```

- 定义模型加载方法


```python
def load_model(model_path):
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.float16, trust_remote_code=True).cuda()
    model = model.eval()
    return tokenizer, model
```

- 定义文本续写方法


```python
def generate(user_input):
    gen_kwargs = {"max_length": 128, "top_p": 0.8, "temperature": 0.8, "do_sample": True, "repetition_penalty": 1.0}

    inputs = tokenizer([user_input], return_tensors="pt")
    for k,v in inputs.items():
        inputs[k] = v.cuda()
    output = model.generate(**inputs, **gen_kwargs)
    output = tokenizer.decode(output[0].tolist(), skip_special_tokens=True)
    return output
```

### 1.1 基座模型推理

我们先来看看基座模型的推理结果。

- 加载模型


```python
tokenizer, model = load_model("Shanghai_AI_Laboratory/internlm2-1_8b")
```

- 文本续写


```python
generate("书生·浦语大模型实战营第三期是")
```

- 释放缓存


```python
del tokenizer, model

torch.cuda.empty_cache()
```

### 1.2 增量预训练

然后我们对基座模型进行增量预训练，让模型增加新的知识。

#### 1.2.1 准备数据文件

为了让模型学习到新的知识，我们需要将新的知识数据整理成指定格式文件，形成数据集，然后让模型来学习这些新数据。这里我们准备一个简单的数据集 `datas/pretrain.json`，仅包含一条知识，然后让数据重复多次。

> 网上有大量的开源数据集可以供我们进行使用，有些时候我们可以在开源数据集的基础上添加一些我们自己独有的数据集，也可能会有很好的效果。


```python
[
    {
        "text": "书生·浦语大模型实战营第三期是上海人工智能实验室推出的书生·浦语大模型实战营系列活动的第三批次，将于2024年7月正式进行。"
    }
]
```

准备好数据文件后，我们的目录结构应该是这样子的。

<details>
<summary>目录结构</summary>

```
├── Shanghai_AI_Laboratory
│   ├── internlm2-1_8b
│   │   ├── README.md
│   │   ├── config.json
│   │   ├── configuration.json
│   │   ├── configuration_internlm2.py
│   │   ├── generation_config.json
│   │   ├── modeling_internlm2.py
│   │   ├── pytorch_model.bin
│   │   ├── special_tokens_map.json
│   │   ├── tokenization_internlm2.py
│   │   ├── tokenization_internlm2_fast.py
│   │   ├── tokenizer.json
│   │   ├── tokenizer.model
│   │   └── tokenizer_config.json
│   └── internlm2-chat-1_8b -> /root/share/new_models/Shanghai_AI_Laboratory/internlm2-chat-1_8b
│       ├── README.md
│       ├── config.json
│       ├── configuration.json
│       ├── configuration_internlm2.py
│       ├── generation_config.json
│       ├── model-00001-of-00002.safetensors
│       ├── model-00002-of-00002.safetensors
│       ├── model.safetensors.index.json
│       ├── modeling_internlm2.py
│       ├── special_tokens_map.json
│       ├── tokenization_internlm2.py
│       ├── tokenization_internlm2_fast.py
│       ├── tokenizer.model
│       └── tokenizer_config.json
├── datas
│   ├── assistant.json
│   └── pretrain.json
├── internlm2_chat_1_8b_qlora_alpaca_e3_copy.py
```

</details>

```bash
tree -l
```

#### 1.2.2 准备配置文件

在准备好了模型和数据集后，我们就要根据我们选择的微调方法结合微调方案来找到与我们最匹配的配置文件了，从而减少我们对配置文件的修改量。

这里我们选择使用 `internlm2_1_8b_full_custom_pretrain_e1` 配置文件。


```bash
xtuner copy-cfg internlm2_1_8b_full_custom_pretrain_e1 .
```

复制好配置文件后，我们的目录结构应该是这样子的。

<details>
<summary>目录结构</summary>

```
├── Shanghai_AI_Laboratory
│   ├── internlm2-1_8b
│   │   ├── README.md
│   │   ├── config.json
│   │   ├── configuration.json
│   │   ├── configuration_internlm2.py
│   │   ├── generation_config.json
│   │   ├── modeling_internlm2.py
│   │   ├── pytorch_model.bin
│   │   ├── special_tokens_map.json
│   │   ├── tokenization_internlm2.py
│   │   ├── tokenization_internlm2_fast.py
│   │   ├── tokenizer.json
│   │   ├── tokenizer.model
│   │   └── tokenizer_config.json
│   └── internlm2-chat-1_8b -> /root/share/new_models/Shanghai_AI_Laboratory/internlm2-chat-1_8b
│       ├── README.md
│       ├── config.json
│       ├── configuration.json
│       ├── configuration_internlm2.py
│       ├── generation_config.json
│       ├── model-00001-of-00002.safetensors
│       ├── model-00002-of-00002.safetensors
│       ├── model.safetensors.index.json
│       ├── modeling_internlm2.py
│       ├── special_tokens_map.json
│       ├── tokenization_internlm2.py
│       ├── tokenization_internlm2_fast.py
│       ├── tokenizer.model
│       └── tokenizer_config.json
├── datas
│   ├── assistant.json
│   └── pretrain.json
├── internlm2_1_8b_full_custom_pretrain_e1_copy.py
├── internlm2_chat_1_8b_qlora_alpaca_e3_copy.py
```

</details>

下面我们将根据项目的需求一步步的进行修改和调整吧！

在 PART 1 的部分，由于我们不再需要在 HuggingFace 上自动下载模型，因此我们先要更换模型的路径以及数据集的路径为我们本地的路径。

为了训练过程中能够实时观察到模型的变化情况，XTuner 贴心的推出了一个 `evaluation_inputs` 的参数来让我们能够设置多个问题来确保模型在训练过程中的变化是朝着我们想要的方向前进的。我们可以添加自己的输入。

在 PART 2 的部分，由于我们复制的配置文件是全参数微调的配置，而我们希望使用 `QLoRA` 算法进行微调，所以可以添加 `QLoRA` 算法的配置。

```diff
+ from peft import LoraConfig

+ import torch

- from transformers import AutoModelForCausalLM, AutoTokenizer
+ from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

#######################################################################
#                          PART 1  Settings                           #
#######################################################################
- pretrained_model_name_or_path = 'internlm/internlm2-1_8b'
+ pretrained_model_name_or_path = 'Shanghai_AI_Laboratory/internlm2-1_8b'

- data_files = ['/path/to/json/file.json']
+ data_files = ['datas/pretrain.json']

- evaluation_inputs = ['上海是', 'Shanghai is']
+ evaluation_inputs = ['书生·浦语大模型实战营第三期是', '上海是', 'Shanghai is']

#######################################################################
#                      PART 2  Model & Tokenizer                      #
#######################################################################
model = dict(
    type=SupervisedFinetune,
    use_varlen_attn=use_varlen_attn,
    llm=dict(
        type=AutoModelForCausalLM.from_pretrained,
        pretrained_model_name_or_path=pretrained_model_name_or_path,
        trust_remote_code=True,
+       quantization_config=dict(
+           type=BitsAndBytesConfig,
+           load_in_4bit=True,
+           load_in_8bit=False,
+           llm_int8_threshold=6.0,
+           llm_int8_has_fp16_weight=False,
+           bnb_4bit_compute_dtype=torch.float16,
+           bnb_4bit_use_double_quant=True,
+           bnb_4bit_quant_type='nf4')
    ),
+   lora=dict(
+       type=LoraConfig,
+       r=64,
+       lora_alpha=16,
+       lora_dropout=0.1,
+       bias='none',
+       task_type='CAUSAL_LM')
)
```

修改完后的完整的配置文件是：[configs/internlm2_1_8b_full_custom_pretrain_e1_copy.py](../../../configs/internlm2_1_8b_full_custom_pretrain_e1_copy.py)。

<details>
<summary>internlm2_1_8b_full_custom_pretrain_e1_copy.py</summary>

```python
# Copyright (c) OpenMMLab. All rights reserved.
"""Data format:[
  {
      "text": "xxx"
  },
  {
      "text": "xxx"
  },
  ...
]
"""  # noqa: E501

from datasets import load_dataset
from mmengine.dataset import DefaultSampler
from mmengine.hooks import (CheckpointHook, DistSamplerSeedHook, IterTimerHook,
                            LoggerHook, ParamSchedulerHook)
from mmengine.optim import AmpOptimWrapper, CosineAnnealingLR, LinearLR
from peft import LoraConfig
import torch
from torch.optim import AdamW
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from xtuner.dataset import process_hf_dataset
from xtuner.dataset.collate_fns import default_collate_fn
from xtuner.dataset.map_fns import pretrain_map_fn
from xtuner.engine.hooks import (DatasetInfoHook, EvaluateChatHook,
                                 VarlenAttnArgsToMessageHubHook)
from xtuner.engine.runner import TrainLoop
from xtuner.model import SupervisedFinetune

#######################################################################
#                          PART 1  Settings                           #
#######################################################################
# Model
pretrained_model_name_or_path = 'Shanghai_AI_Laboratory/internlm2-1_8b'
use_varlen_attn = False

# Data
data_files = ['datas/pretrain.json']
max_length = 2048
pack_to_max_length = True

# Scheduler & Optimizer
batch_size = 1  # per_device
accumulative_counts = 16  # bs = 1 GPU * 1 batch_size_per_device * 16 acc
dataloader_num_workers = 0
max_epochs = 1
optim_type = AdamW
lr = 2e-5
betas = (0.9, 0.999)
weight_decay = 0
max_norm = 1  # grad clip
warmup_ratio = 0.03

# Save
save_steps = 500
save_total_limit = 2  # Maximum checkpoints to keep (-1 means unlimited)

# Evaluate the generation performance during the training
evaluation_freq = 500
SYSTEM = ''
evaluation_inputs = ['书生·浦语大模型实战营第三期是', '上海是', 'Shanghai is']

#######################################################################
#                      PART 2  Model & Tokenizer                      #
#######################################################################
tokenizer = dict(
    type=AutoTokenizer.from_pretrained,
    pretrained_model_name_or_path=pretrained_model_name_or_path,
    trust_remote_code=True,
    padding_side='right')

model = dict(
    type=SupervisedFinetune,
    use_varlen_attn=use_varlen_attn,
    llm=dict(
        type=AutoModelForCausalLM.from_pretrained,
        pretrained_model_name_or_path=pretrained_model_name_or_path,
        trust_remote_code=True,
        quantization_config=dict(
            type=BitsAndBytesConfig,
            load_in_4bit=True,
            load_in_8bit=False,
            llm_int8_threshold=6.0,
            llm_int8_has_fp16_weight=False,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type='nf4')
    ),
    lora=dict(
        type=LoraConfig,
        r=64,
        lora_alpha=16,
        lora_dropout=0.1,
        bias='none',
        task_type='CAUSAL_LM')
)

#######################################################################
#                      PART 3  Dataset & Dataloader                   #
#######################################################################
train_dataset = dict(
    type=process_hf_dataset,
    dataset=dict(type=load_dataset, path='json', data_files=data_files),
    tokenizer=tokenizer,
    max_length=max_length,
    dataset_map_fn=pretrain_map_fn,
    template_map_fn=None,
    remove_unused_columns=True,
    shuffle_before_pack=False,
    pack_to_max_length=pack_to_max_length,
    use_varlen_attn=use_varlen_attn)

train_dataloader = dict(
    batch_size=batch_size,
    num_workers=dataloader_num_workers,
    dataset=train_dataset,
    sampler=dict(type=DefaultSampler, shuffle=True),
    collate_fn=dict(type=default_collate_fn, use_varlen_attn=use_varlen_attn))

#######################################################################
#                    PART 4  Scheduler & Optimizer                    #
#######################################################################
# optimizer
optim_wrapper = dict(
    type=AmpOptimWrapper,
    optimizer=dict(
        type=optim_type, lr=lr, betas=betas, weight_decay=weight_decay),
    clip_grad=dict(max_norm=max_norm, error_if_nonfinite=False),
    accumulative_counts=accumulative_counts,
    loss_scale='dynamic',
    dtype='float16')

# learning policy
# More information: https://github.com/open-mmlab/mmengine/blob/main/docs/en/tutorials/param_scheduler.md  # noqa: E501
param_scheduler = [
    dict(
        type=LinearLR,
        start_factor=1e-5,
        by_epoch=True,
        begin=0,
        end=warmup_ratio * max_epochs,
        convert_to_iter_based=True),
    dict(
        type=CosineAnnealingLR,
        eta_min=0.0,
        by_epoch=True,
        begin=warmup_ratio * max_epochs,
        end=max_epochs,
        convert_to_iter_based=True)
]

# train, val, test setting
train_cfg = dict(type=TrainLoop, max_epochs=max_epochs)

#######################################################################
#                           PART 5  Runtime                           #
#######################################################################
# Log the dialogue periodically during the training process, optional
custom_hooks = [
    dict(type=DatasetInfoHook, tokenizer=tokenizer),
    dict(
        type=EvaluateChatHook,
        tokenizer=tokenizer,
        every_n_iters=evaluation_freq,
        evaluation_inputs=evaluation_inputs,
        system=SYSTEM)
]

if use_varlen_attn:
    custom_hooks += [dict(type=VarlenAttnArgsToMessageHubHook)]

# configure default hooks
default_hooks = dict(
    # record the time of every iteration.
    timer=dict(type=IterTimerHook),
    # print log every 10 iterations.
    logger=dict(type=LoggerHook, log_metric_by_epoch=False, interval=10),
    # enable the parameter scheduler.
    param_scheduler=dict(type=ParamSchedulerHook),
    # save checkpoint per `save_steps`.
    checkpoint=dict(
        type=CheckpointHook,
        by_epoch=False,
        interval=save_steps,
        max_keep_ckpts=save_total_limit),
    # set sampler seed in distributed evrionment.
    sampler_seed=dict(type=DistSamplerSeedHook),
)

# configure environment
env_cfg = dict(
    # whether to enable cudnn benchmark
    cudnn_benchmark=False,
    # set multi process parameters
    mp_cfg=dict(mp_start_method='fork', opencv_num_threads=0),
    # set distributed parameters
    dist_cfg=dict(backend='nccl'),
)

# set visualizer
visualizer = None

# set log level
log_level = 'INFO'

# load from which checkpoint
load_from = None

# whether to resume training from the loaded checkpoint
resume = False

# Defaults to use random seed and disable `deterministic`
randomness = dict(seed=None, deterministic=False)

# set log processor
log_processor = dict(by_epoch=False)
```

</details>

#### 1.2.3 启动微调

完成了所有的准备工作后，我们就可以正式的开始我们下一阶段的旅程：XTuner 启动~！

当我们准备好了所有内容，我们只需要将使用 `xtuner train` 命令令即可开始训练。


```bash
xtuner train ./internlm2_1_8b_full_custom_pretrain_e1_copy.py
```

在训练完后，我们的目录结构应该是这样子的。

<details>
<summary>目录结构</summary>

```
├── work_dirs
│   └── internlm2_1_8b_full_custom_pretrain_e1_copy
│       ├── 20240627_214522
│       │   ├── 20240627_214522.log
│       │   └── vis_data
│       │       ├── 20240627_214522.json
│       │       ├── config.py
│       │       ├── eval_outputs_iter_1499.txt
│       │       ├── eval_outputs_iter_1999.txt
│       │       ├── eval_outputs_iter_2499.txt
│       │       ├── eval_outputs_iter_2623.txt
│       │       ├── eval_outputs_iter_499.txt
│       │       ├── eval_outputs_iter_999.txt
│       │       └── scalars.json
│       ├── internlm2_1_8b_full_custom_pretrain_e1_copy.py
│       ├── iter_2500.pth
│       ├── iter_2624.pth
│       └── last_checkpoint
```

</details>

#### 1.2.4 模型格式转换

模型转换的本质其实就是将原本使用 Pytorch 训练出来的模型权重文件转换为目前通用的 HuggingFace 格式文件，那么我们可以通过以下命令来实现一键转换。


```bash
pth_file=`ls -t ./work_dirs/internlm2_1_8b_full_custom_pretrain_e1_copy/*.pth | head -n 1` && MKL_SERVICE_FORCE_INTEL=1 MKL_THREADING_LAYER=GNU xtuner convert pth_to_hf ./internlm2_1_8b_full_custom_pretrain_e1_copy.py ${pth_file} ./hf
```

模型格式转换完成后，我们的目录结构应该是这样子的。

<details>
<summary>目录结构</summary>

```
├── hf
│   ├── README.md
│   ├── adapter_config.json
│   ├── adapter_model.bin
│   └── xtuner_config.py
```

</details>

#### 1.2.5 模型合并

对于 LoRA 或者 QLoRA 微调出来的模型其实并不是一个完整的模型，而是一个额外的层（Adapter），训练完的这个层最终还是要与原模型进行合并才能被正常的使用。


```bash
MKL_SERVICE_FORCE_INTEL=1 MKL_THREADING_LAYER=GNU xtuner convert merge Shanghai_AI_Laboratory/internlm2-1_8b ./hf ./merged --max-shard-size 2GB
```

模型合并完成后，我们的目录结构应该是这样子的。

<details>
<summary>目录结构</summary>

```
├── merged
│   ├── config.json
│   ├── configuration_internlm2.py
│   ├── generation_config.json
│   ├── modeling_internlm2.py
│   ├── pytorch_model-00001-of-00002.bin
│   ├── pytorch_model-00002-of-00002.bin
│   ├── pytorch_model.bin.index.json
│   ├── special_tokens_map.json
│   ├── tokenization_internlm2.py
│   ├── tokenization_internlm2_fast.py
│   ├── tokenizer.json
│   ├── tokenizer.model
│   └── tokenizer_config.json
```

</details>

### 1.3 目标模型推理

当我们合并完成后，我们就能够正常的调用这个模型进行推理了。


```python
tokenizer, model = load_model("./merged")
```


```python
generate("书生·浦语大模型实战营第三期是")
```


```python
generate("成都是")
```

可以看到，通过增量预训练，确实在基座模型的基础上学习到了新的知识。


```python
del tokenizer, model

torch.cuda.empty_cache()
```

## 2 DeepSpeed介绍

DeepSpeed是一个由微软开发的开源深度学习优化库，旨在提高大规模模型训练的效率和速度。

XTuner 也内置了 `deepspeed` 来加速整体的训练过程，共有三种不同的 `deepspeed` 类型可进行选择，分别是 `deepspeed_zero1`, `deepspeed_zero2` 和 `deepspeed_zero3`。

<details>
<summary>DeepSpeed优化器及其选择方法</summary>
DeepSpeed是一个由微软开发的开源深度学习优化库，旨在提高大规模模型训练的效率和速度。它通过几种关键技术来优化训练过程，包括模型分割、梯度累积、以及内存和带宽优化等，能够降低训练超大规模模型的复杂性和资源需求，使训练变得更快、更高效。DeepSpeed特别适用于需要巨大计算资源的大型模型和数据集。

在DeepSpeed中，引入了ZeRO（Zero Redundancy Optimizer）技术，是一种旨在降低训练大型模型所需内存占用的优化器，通过在分布式环境中分割优化器的状态、梯度和参数，减少冗余的内存占用，允许更大的模型和更快的训练速度。ZeRO 分为几个不同的级别，主要包括：

- **deepspeed_zero1**：这是ZeRO的基本版本，它优化了模型参数的存储，主要通过分区存储优化器状态来减少内存使用。每个GPU设备只保存一部分优化器状态，从而显著减少内存消耗。

- **deepspeed_zero2**：在deepspeed_zero1的基础上，deepspeed_zero2进一步优化了梯度和优化器状态的存储，将梯度也进行分区存储。这样，每个GPU设备只需要保存一部分的优化器状态和梯度，进一步减少内存使用。

- **deepspeed_zero3**：这是目前最高级的优化等级，它包括了deepspeed_zero1和deepspeed_zero2的优化，除了优化器状态和梯度，还将模型参数进行分区存储。每个GPU设备只需要保存一部分的优化器状态、梯度和模型参数，从而最大限度地减少内存使用。

选择哪种deepspeed类型主要取决于你的具体需求，包括模型的大小、可用的硬件资源（特别是GPU内存）以及训练的效率需求。一般来说：

- 如果你的模型较小，或者内存资源充足，可能不需要使用最高级别的优化。
- 如果你需要快速训练模型，可能需要权衡内存优化和计算效率。deepspeed_zero1提供了较低的内存占用，同时保持了较高的计算效率。
- 如果你正在尝试训练非常大的模型，或者你的硬件资源有限，使用deepspeed_zero2或deepspeed_zero3可能更合适，因为它们可以显著降低内存占用，允许更大模型的训练。
- 选择时也要考虑到实现的复杂性和运行时的开销，更高级的优化可能需要更复杂的设置，更频繁的跨GPU通信，这可能需要更高的网络带宽，并可能增加一些计算开销。

</details>

## 3 多卡微调

模型的规模和复杂度不断增加，单张GPU的显存往往无法满足大模型的训练需求。此时，我们可能需要多卡微调，以应对大模型训练过程中显存和计算资源的需求。


XTuner 中使用多卡微调，只需要设置 `NPROC_PER_NODE` 环境变量，并使用 `DeepSpeed` 来进行加速就可以了，其余命令内容与单卡微调时一样。

> 由于开发机只有两张显卡，所以我们设置`NPROC_PER_NODE=2`，并且选择使用`deepspeed_zero3`优化等级。


```bash
MKL_SERVICE_FORCE_INTEL=1 MKL_THREADING_LAYER=GNU NPROC_PER_NODE=2 xtuner train ./internlm2_chat_1_8b_qlora_alpaca_e3_copy.py --deepspeed deepspeed_zero3
```

在执行微调的过程中，我们可以看到两张显卡都有内存使用。

![](https://raw.githubusercontent.com/wux-labs/ImageHosting/main/XTuner/image-06.png)

在训练完后，我们的目录结构应该是这样子的。

<details>
<summary>目录结构</summary>

```
├── work_dirs
│   └── internlm2_chat_1_8b_qlora_alpaca_e3_copy
│       ├── 20240628_205957
│       │   ├── 20240628_205957.log
│       │   └── vis_data
│       │       ├── 20240628_205957.json
│       │       ├── config.py
│       │       ├── eval_outputs_iter_236.txt
│       │       └── scalars.json
│       ├── internlm2_chat_1_8b_qlora_alpaca_e3_copy.py
│       ├── iter_237.pth
│       │   ├── bf16_zero_pp_rank_0_mp_rank_00_optim_states.pt
│       │   ├── bf16_zero_pp_rank_1_mp_rank_00_optim_states.pt
│       │   ├── zero_pp_rank_0_mp_rank_00_model_states.pt
│       │   └── zero_pp_rank_1_mp_rank_00_model_states.pt
│       ├── last_checkpoint
│       └── zero_to_fp32.py
```

</details>

可以看到，通过 `deepspeed` 来训练后得到的权重文件和原本的权重文件是有所差别的，原本的仅仅是一个 .pth 的文件，而使用了 `deepspeed` 则是一个名字带有 .pth 的文件夹，在该文件夹里保存了 .pt 文件。这两者在具体的使用上并没有太大的差别，转换和合并的过程都是一样的。


```bash
pth_file=`ls -t ./work_dirs/internlm2_chat_1_8b_qlora_alpaca_e3_copy | grep pth | head -n 1` && MKL_SERVICE_FORCE_INTEL=1 MKL_THREADING_LAYER=GNU xtuner convert pth_to_hf ./internlm2_chat_1_8b_qlora_alpaca_e3_copy.py ./work_dirs/internlm2_chat_1_8b_qlora_alpaca_e3_copy/${pth_file} ./hf
```


```bash
MKL_SERVICE_FORCE_INTEL=1 MKL_THREADING_LAYER=GNU xtuner convert merge Shanghai_AI_Laboratory/internlm2-chat-1_8b ./hf ./merged --max-shard-size 2GB
```


```python
tokenizer, model = load_model("./merged")
```


```python
chat("请介绍一下你自己")
```


```python
chat("你在实战营做什么")
```


```python
chat("介绍一下成都")
```


```python
del tokenizer, model

torch.cuda.empty_cache()
```

## 4 分布式微调

如果模型的规模和复杂度继续增加，我们还可以使用分布式微调。


```bash
apt-get install -y net-tools
ifconfig
```

分布式微调是主从架构的。主节点协调整个训练过程，管理数据和任务到工作节点的分配。工作节点执行训练步骤的实际计算，处理数据的子集并计算梯度。有时候在一些架构中还需要参数服务器协调所有工作节点之间的模型更新同步，用于聚合来自工作节点的梯度并更新模型参数。

> 我们使用两个节点进行分布式微调，实际上需要启动三个节点。


```bash
MKL_SERVICE_FORCE_INTEL=1 MKL_THREADING_LAYER=GNU OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NPROC_PER_NODE=1 NNODES=2 xtuner train internlm2_chat_1_8b_qlora_alpaca_e3_copy.py

MKL_SERVICE_FORCE_INTEL=1 MKL_THREADING_LAYER=GNU OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NPROC_PER_NODE=1 NNODES=2 NODE_RANK=0 TRITON_CACHE_DIR=node0 PORT=20821 ADDR=192.168.230.182 xtuner train internlm2_chat_1_8b_qlora_alpaca_e3_copy.py --work-dir work_dir_node0

MKL_SERVICE_FORCE_INTEL=1 MKL_THREADING_LAYER=GNU OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NPROC_PER_NODE=1 NNODES=2 NODE_RANK=1 TRITON_CACHE_DIR=node1 PORT=20821 ADDR=192.168.230.182 xtuner train internlm2_chat_1_8b_qlora_alpaca_e3_copy.py --work-dir work_dir_node1
```

首先启动主节点，然后依次启动其他节点。但需要注意的是，需要在一个时间阈值内启动相关的节点，如果超过时间阈值还没启动所有节点，则其他节点会因超时而报错退出。

比如，在两个节点的分布式微调过程中，我们只启动主节点和一个工作节点，另一个节点不启动，则已启动的节点会超时报错退出。

![](https://raw.githubusercontent.com/wux-labs/ImageHosting/main/XTuner/image-07.png)

如果所有节点都正常启动、训练，则可以看到每个节点的显卡均有内存使用。

![](https://raw.githubusercontent.com/wux-labs/ImageHosting/main/XTuner/image-08.png)

在训练完后，我们的目录结构应该是这样子的，训练的模型在工作节点上。

<details>
<summary>目录结构</summary>

```
├── work_dir_node0
│   ├── 20240629_213009
│   │   ├── 20240629_213009.log
│   │   └── vis_data
│   │       ├── 20240629_213009.json
│   │       ├── config.py
│   │       ├── eval_outputs_iter_233.txt
│   │       └── scalars.json
│   ├── internlm2_chat_1_8b_qlora_alpaca_e3_copy.py
│   ├── iter_234.pth
│   └── last_checkpoint
├── work_dir_node1
│   └── 20240629_213009
├── work_dirs
│   └── internlm2_chat_1_8b_qlora_alpaca_e3_copy
```

</details>

## 5 小结

现在，我们又学到了 XTuner 微调的更多高阶知识啦，包括增量预训练微调基座模型、多卡微调、分布式微调等。

是不是感觉其实微调也不过如此！事实上确实是这样的！其实在微调的时候最重要的还是要自己准备一份高质量的数据集，这个才是你能否真微调出效果最核心的利器。