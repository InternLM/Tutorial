<img width="1440" alt="head" src="https://github.com/user-attachments/assets/54ce507a-1539-4dce-bcb9-5868cfb38897">
本文将进行使用 OpenCompass 来评测 InternLM2 1.8B实践

# 概览

在 OpenCompass 中评估一个模型通常包括以下几个阶段：配置 -> 推理 -> 评估 -> 可视化。

*   配置：这是整个工作流的起点。您需要配置整个评估过程，选择要评估的模型和数据集。此外，还可以选择评估策略、计算后端等，并定义显示结果的方式。
*   推理与评估：在这个阶段，OpenCompass 将会开始对模型和数据集进行并行推理和评估。推理阶段主要是让模型从数据集产生输出，而评估阶段则是衡量这些输出与标准答案的匹配程度。这两个过程会被拆分为多个同时运行的“任务”以提高效率。
*   可视化：评估完成后，OpenCompass 将结果整理成易读的表格，并将其保存为 CSV 和 TXT 文件。

接下来，我们将展示 OpenCompass 的基础用法，展示书生浦语在 `C-Eval` 基准任务上的评估。它们的配置文件可以在 `configs/eval_demo.py` 中找到。

# 环境配置

## 创建开发机和 conda 环境

在创建开发机界面选择镜像为 Cuda11.7-conda，并选择 GPU 为10% A100。

![image](https://github.com/mattheliu/Tutorial/assets/102272920/1302d976-64db-4fc2-87f6-570e4a71147a)

## 安装——面向GPU的环境安装


```

conda create -n opencompass python=3.10
conda install pytorch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 pytorch-cuda=12.1 -c pytorch -c nvidia -y

conda activate opencompass
git clone -b 0.2.4 https://github.com/open-compass/opencompass
cd opencompass
pip install -e .
pip install protobuf
```

**如果pip install -e .安装未成功,请运行:**

    apt-get update
    apt-get install cmake
    pip install -r requirements.txt
    pip install protobuf

# 数据准备

解压评测数据集到 data/ 处

    cp /share/temp/datasets/OpenCompassData-core-20231110.zip /root/opencompass/
    unzip OpenCompassData-core-20231110.zip

将会在 OpenCompass 下看到data文件夹

## 查看支持的数据集和模型

列出所有跟 InternLM 及 C-Eval 相关的配置

    python tools/list_configs.py internlm ceval

将会看到

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
    | hf_internlm2_chat_20b_with_system      | configs/models/hf_internlm/hf_internlm2_chat_20b_with_system.py      |
    | hf_internlm2_chat_7b                   | configs/models/hf_internlm/hf_internlm2_chat_7b.py                   |
    | hf_internlm2_chat_7b_sft               | configs/models/hf_internlm/hf_internlm2_chat_7b_sft.py               |
    | hf_internlm2_chat_7b_with_system       | configs/models/hf_internlm/hf_internlm2_chat_7b_with_system.py       |
    | hf_internlm2_chat_math_20b             | configs/models/hf_internlm/hf_internlm2_chat_math_20b.py             |
    | hf_internlm2_chat_math_20b_with_system | configs/models/hf_internlm/hf_internlm2_chat_math_20b_with_system.py |
    | hf_internlm2_chat_math_7b              | configs/models/hf_internlm/hf_internlm2_chat_math_7b.py              |
    | hf_internlm2_chat_math_7b_with_system  | configs/models/hf_internlm/hf_internlm2_chat_math_7b_with_system.py  |
    | hf_internlm_20b                        | configs/models/hf_internlm/hf_internlm_20b.py                        |
    | hf_internlm_7b                         | configs/models/hf_internlm/hf_internlm_7b.py                         |
    | hf_internlm_chat_20b                   | configs/models/hf_internlm/hf_internlm_chat_20b.py                   |
    | hf_internlm_chat_7b                    | configs/models/hf_internlm/hf_internlm_chat_7b.py                    |
    | hf_internlm_chat_7b_8k                 | configs/models/hf_internlm/hf_internlm_chat_7b_8k.py                 |
    | hf_internlm_chat_7b_v1_1               | configs/models/hf_internlm/hf_internlm_chat_7b_v1_1.py               |
    | internlm_7b                            | configs/models/internlm/internlm_7b.py                               |
    | ms_internlm_chat_7b_8k                 | configs/models/ms_internlm/ms_internlm_chat_7b_8k.py                 |
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
    | ceval_ppl_93e5ce               | configs/datasets/ceval/ceval_ppl_93e5ce.py                        |
    | ceval_zero_shot_gen_bd40ef     | configs/datasets/ceval/ceval_zero_shot_gen_bd40ef.py              |
    | configuration_internlm         | configs/datasets/cdme/internlm2-chat-7b/configuration_internlm.py |
    | modeling_internlm2             | configs/datasets/cdme/internlm2-chat-7b/modeling_internlm2.py     |
    | tokenization_internlm          | configs/datasets/cdme/internlm2-chat-7b/tokenization_internlm.py  |
    +--------------------------------+-------------------------------------------------------------------+

# 启动评测 (10% A100 8GB 资源)

确保按照上述步骤正确安装 OpenCompass 并准备好数据集后，可以通过以下命令评测 InternLM2-Chat-1.8B 模型在 C-Eval 数据集上的性能。由于 OpenCompass 默认并行启动评估过程，我们可以在第一次运行时以 --debug 模式启动评估，并检查是否存在问题。在 --debug 模式下，任务将按顺序执行，并实时打印输出。

    #环境变量配置
    export MKL_SERVICE_FORCE_INTEL=1
    #或
    export MKL_THREADING_LAYER=GNU

<!---->

    python run.py --datasets ceval_gen --hf-path /share/new_models/Shanghai_AI_Laboratory/internlm2-chat-1_8b --tokenizer-path /share/new_models/Shanghai_AI_Laboratory/internlm2-chat-1_8b --tokenizer-kwargs padding_side='left' truncation='left' trust_remote_code=True --model-kwargs trust_remote_code=True device_map='auto' --max-seq-len 1024 --max-out-len 16 --batch-size 2 --num-gpus 1 --debug

命令解析

    python run.py
    --datasets ceval_gen \
    --hf-path /share/new_models/Shanghai_AI_Laboratory/internlm2-chat-1_8b \  # HuggingFace 模型路径
    --tokenizer-path /share/new_models/Shanghai_AI_Laboratory/internlm2-chat-1_8b \  # HuggingFace tokenizer 路径（如果与模型路径相同，可以省略）
    --tokenizer-kwargs padding_side='left' truncation='left' trust_remote_code=True \  # 构建 tokenizer 的参数
    --model-kwargs device_map='auto' trust_remote_code=True \  # 构建模型的参数
    --max-seq-len 1024 \  # 模型可以接受的最大序列长度
    --max-out-len 16 \  # 生成的最大 token 数
    --batch-size 2  \  # 批量大小
    --num-gpus 1  # 运行模型所需的 GPU 数量
    --debug

如果一切正常，您应该看到屏幕上显示 “Starting inference process”：

    [2024-03-18 12:39:54,972] [opencompass.openicl.icl_inferencer.icl_gen_inferencer] [INFO] Starting inference process...

评测完成后，将会看到：

    dataset                                         version    metric         mode      opencompass.models.huggingface.HuggingFace_Shanghai_AI_Laboratory_internlm2-chat-1_8b
    ----------------------------------------------  ---------  -------------  ------  ---------------------------------------------------------------------------------------
    ceval-computer_network                          db9ce2     accuracy       gen                                                                                       47.37
    ceval-operating_system                          1c2571     accuracy       gen                                                                                       47.37
    ceval-computer_architecture                     a74dad     accuracy       gen                                                                                       23.81
    ceval-college_programming                       4ca32a     accuracy       gen                                                                                       13.51
    ceval-college_physics                           963fa8     accuracy       gen                                                                                       42.11
    ceval-college_chemistry                         e78857     accuracy       gen                                                                                       33.33
    ceval-advanced_mathematics                      ce03e2     accuracy       gen                                                                                       10.53
    ...      

# 作业

作业请访问[作业](./task.md)。
