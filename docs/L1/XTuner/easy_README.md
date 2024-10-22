# XTuner 微调实践微调 

<img width="900" alt="image" src="https://github.com/user-attachments/assets/e374baf5-283b-4c44-a7db-79caf5e0c3ce">

本文档将介绍 InternLM 个人小助手认知

**本文档为有一定基础可以快速上手的同学准备，比`README.md`的说明更加简洁。**

## 写在前面

微调内容需要使用 30% A100 才能完成。
本次实战营的微调内容包括了以下两个部分：
1. SFT 数据的获取
2. 使用 [InternLM2.5-7B-Chat](https://huggingface.co/internlm/internlm2_5-7b-chat) 模型微调 

这节课你会收获：
* 针对业务场景（如特殊自我认知的机器人）的微调能力
* 一个属于自己的语言聊天机器人

本节课对应的视频链接：暂无

XTuner 文档链接：[XTuner-doc-cn](https://xtuner.readthedocs.io/zh-cn/latest/)

## 环境配置与数据准备

本节中，我们将演示如何安装 XTuner。

### **步骤 0.** 使用 conda 激活一个已有的虚拟环境

```shell
cd ~
#git clone 本repo
git clone https://github.com/InternLM/Tutorial.git -b camp4
mkdir -p /root/finetune && cd /root/finetune
conda activate /root/share/pre_envs/pytorch2.3.1cu12.1
```

### **步骤 1.** 安装 XTuner
此处推荐源码安装，更多的安装方法请回到前面看 XTuner 文档

```shell
pip install -t /root/finetune/env 'xtuner[deepspeed]' timm==1.0.9 
```

每次使用前，需要运行一下命令，把自定义的安装包的路径添加到PYTHONPATH环境变量中，这样python才能找到你安装的包（同一个终端下只需运行一次）：

```Bash
export PYTHONPATH=/root/finetune/env:$PYTHONPATH
export PATH=/root/finetune/env/bin:$PATH
```

### 验证安装
为了验证 XTuner 是否安装正确，我们将使用命令打印配置文件。

**打印配置文件：** 在命令行中使用 `xtuner list-cfg` 验证是否能打印配置文件列表。
```shell
xtuner list-cfg
```

<details>
<summary>输出没有报错则为此结果</summary>

xtuner list-cfg
	==========================CONFIGS===========================
	baichuan2_13b_base_full_custom_pretrain_e1
	baichuan2_13b_base_qlora_alpaca_e3
	baichuan2_13b_base_qlora_alpaca_enzh_e3
	baichuan2_13b_base_qlora_alpaca_enzh_oasst1_e3
	...
	internlm2_1_8b_full_alpaca_e3
	internlm2_1_8b_full_custom_pretrain_e1
	internlm2_1_8b_qlora_alpaca_e3
	internlm2_20b_full_custom_pretrain_e1
	internlm2_20b_full_finetune_custom_dataset_e1
	internlm2_20b_qlora_alpaca_e3
	internlm2_20b_qlora_arxiv_gentitle_e3
	internlm2_20b_qlora_code_alpaca_e3
	internlm2_20b_qlora_colorist_e5
	internlm2_20b_qlora_lawyer_e3
	internlm2_20b_qlora_msagent_react_e3_gpu8
	internlm2_20b_qlora_oasst1_512_e3
	internlm2_20b_qlora_oasst1_e3
	internlm2_20b_qlora_sql_e3
	internlm2_5_chat_20b_alpaca_e3
	internlm2_5_chat_20b_qlora_alpaca_e3
	internlm2_5_chat_7b_full_finetune_custom_dataset_e1
	internlm2_5_chat_7b_qlora_alpaca_e3
	internlm2_5_chat_7b_qlora_oasst1_e3
	internlm2_7b_full_custom_pretrain_e1
	internlm2_7b_full_finetune_custom_dataset_e1
	internlm2_7b_full_finetune_custom_dataset_e1_sequence_parallel_4
	internlm2_7b_qlora_alpaca_e3
	internlm2_7b_qlora_arxiv_gentitle_e3
	internlm2_7b_qlora_code_alpaca_e3
	internlm2_7b_qlora_colorist_e5
	internlm2_7b_qlora_json_e3
	internlm2_7b_qlora_lawyer_e3
	internlm2_7b_qlora_msagent_react_e3_gpu8
	internlm2_7b_qlora_oasst1_512_e3
	internlm2_7b_qlora_oasst1_e3
	internlm2_7b_qlora_sql_e3
	...
    
> 输出内容为 XTuner 支持微调的模型
</details>


## 修改提供的数据

### **步骤 0.** 创建一个新的文件夹用于存储微调数据
```shell
mkdir -p /root/finetune/data && cd /root/finetune/data
cp -r /root/Tutorial/data/assistant_Tuner.jsonl  /root/finetune/data
#复制存放jsonl格式的训练数据的文件夹JsonData到/root/finetune/data
#这里要改一下jsondata的地址！！！
```

<details>
<summary>此时 `finetune` 文件夹下应该有如下结构</summary>

```sh
finetune
├── data
│   └── assistant_Tuner.jsonl
└── xtuner
```

</details>

### **步骤 1.** 创建修改脚本

我们写一个脚本生成修改我们需要的微调训练数据，在当前目录下创建一个 `change_script.py` 文件，内容如下：

```bash
# 创建 `change_script.py` 文件
touch /root/finetune/data/change_script.py
```

打开该`change_script.py`文件后将下面的内容复制进去。

```python
import json
import argparse
from tqdm import tqdm

def process_line(line, old_text, new_text):
    # 解析 JSON 行
    data = json.loads(line)
    
    # 递归函数来处理嵌套的字典和列表
    def replace_text(obj):
        if isinstance(obj, dict):
            return {k: replace_text(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [replace_text(item) for item in obj]
        elif isinstance(obj, str):
            return obj.replace(old_text, new_text)
        else:
            return obj
    
    # 处理整个 JSON 对象
    processed_data = replace_text(data)
    
    # 将处理后的对象转回 JSON 字符串
    return json.dumps(processed_data, ensure_ascii=False)

def main(input_file, output_file, old_text, new_text):
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        
        # 计算总行数用于进度条
        total_lines = sum(1 for _ in infile)
        infile.seek(0)  # 重置文件指针到开头
        
        # 使用 tqdm 创建进度条
        for line in tqdm(infile, total=total_lines, desc="Processing"):
            processed_line = process_line(line.strip(), old_text, new_text)
            outfile.write(processed_line + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Replace text in a JSONL file.")
    parser.add_argument("input_file", help="Input JSONL file to process")
    parser.add_argument("output_file", help="Output file for processed JSONL")
    parser.add_argument("--old_text", default="尖米", help="Text to be replaced")
    parser.add_argument("--new_text", default="机智流", help="Text to replace with")
    args = parser.parse_args()

    main(args.input_file, args.output_file, args.old_text, args.new_text)
```

然后修改如下：
打开 `change_script.py` ，修改 `--new_text` 中 `default="机智流"` 为你的名字。

```diff
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Replace text in a JSONL file.")

    parser.add_argument("input_file", help="Input JSONL file to process")

    parser.add_argument("output_file", help="Output file for processed JSONL")

    parser.add_argument("--old_text", default="尖米", help="Text to be replaced")
-	parser.add_argument("--new_text", default="机智流", help="Text to replace with")
+   parser.add_argument("--new_text", default="你的名字", help="Text to replace with")

    args = parser.parse_args()
```


### **步骤 2.** 执行脚本

```shell
# usage：python change_script.py {input_file.jsonl} {output_file.jsonl}
cd ~/finetune
python change_script.py ./data/assist_Tuner.jsonl ./data/assist_Tuner_change.jsonl
```

`assist_Tuner_change.jsonl` 是修改后符合 XTuner 格式的训练数据。

<details>
<summary>此时 data 文件夹下应该有如下结构</summary>

```
|-- /finetune/data/
    |-- assistant_Tuner.jsonl
	|-- assistant_Tuner_change.jsonl
```

</details>


### **步骤 3.** 查看数据

```shell
cat output_file.jsonl | head -n 3
```
此处结果太长不再展示，主要是检查自己要修改的名字是否在数据中。

## 训练启动
### **步骤 0.** 复制模型

在InternStudio开发机中的已经提供了微调模型，可以直接软链接即可。

本模型位于/root/share/new_models/Shanghai_AI_Laboratory/internlm2-chat-7b

```shell
mkdir /root/finetune/models
ln -ls /root/share/new_models/Shanghai_AI_Laboratory/internlm2-chat-7b /root/finetune/models/internlm2-chat-7b
```

### **步骤 1.** 修改 Config

获取官方写好的 config
```shell
# cd {path/to/finetune}
cd /root/finetune
mkdir ./config
cd config
xtuner copy-cfg internlm2_chat_7b_qlora_alpaca_e3 ./
```
修改以下几行

```diff
#######################################################################
#                          PART 1  Settings                           #
#######################################################################
- pretrained_model_name_or_path = 'internlm/internlm2-chat-7b'
+ pretrained_model_name_or_path = '/root/finetune/models/internlm2-chat-7b'

- alpaca_en_path = 'tatsu-lab/alpaca'
+ alpaca_en_path = '/root/finetune/data/assist_Tuner.jsonl'

evaluation_inputs = [
-    '请给我介绍五个上海的景点', 'Please tell me five scenic spots in Shanghai'
+    '请介绍一下你自己', 'Please introduce yourself'
]

#######################################################################
#                      PART 3  Dataset & Dataloader                   #
#######################################################################
alpaca_en = dict(
    type=process_hf_dataset,
-   dataset=dict(type=load_dataset, path=alpaca_en_path),
+   dataset=dict(type=load_dataset, path='json', data_files=dict(train=alpaca_en_path)),
    tokenizer=tokenizer,
    max_length=max_length,
-   dataset_map_fn=alpaca_map_fn,
+   dataset_map_fn=None,
    template_map_fn=dict(
        type=template_map_fn_factory, template=prompt_template),
    remove_unused_columns=True,
    shuffle_before_pack=True,
    pack_to_max_length=pack_to_max_length,
    use_varlen_attn=use_varlen_attn)
```

除此之外，我们还可以对一些重要的参数进行调整，包括学习率（lr）、训练的轮数（max_epochs）等等。

<details>
<summary>常用参数介绍</summary>

| 参数名                     | 解释                                                         |
| -------------------------- | ------------------------------------------------------------ |
| **data_path**              | 数据路径或 HuggingFace 仓库名                                |
| **max_length**             | 单条数据最大 Token 数，超过则截断                            |
| **pack_to_max_length**     | 是否将多条短数据拼接到 max_length，提高 GPU 利用率           |
| **accumulative_counts**    | 梯度累积，每多少次 backward 更新一次参数                     |
| **sequence_parallel_size** | 并行序列处理的大小，用于模型训练时的序列并行                 |
| **batch_size**             | 每个设备上的批量大小                                         |
| **dataloader_num_workers** | 数据加载器中工作进程的数量                                   |
| **max_epochs**             | 训练的最大轮数                                               |
| **optim_type**             | 优化器类型，例如 AdamW                                       |
| **lr**                     | 学习率                                                       |
| **betas**                  | 优化器中的 beta 参数，控制动量和平方梯度的移动平均           |
| **weight_decay**           | 权重衰减系数，用于正则化和避免过拟合                         |
| **max_norm**               | 梯度裁剪的最大范数，用于防止梯度爆炸                         |
| **warmup_ratio**           | 预热的比例，学习率在这个比例的训练过程中线性增加到初始学习率 |
| **save_steps**             | 保存模型的步数间隔                                           |
| **save_total_limit**       | 保存的模型总数限制，超过限制时删除旧的模型文件               |
| **prompt_template**        | 模板提示，用于定义生成文本的格式或结构                       |
| ......                     | ......                                                       |

> 如果想充分利用显卡资源，可以将 `max_length` 和 `batch_size` 这两个参数调大。
⚠但需要注意的是，在训练 chat 模型时调节参数 `batch_size` 有可能会影响对话模型的效果。

</details>


本教程已经将改好的 config 放在了 `~/Tutorial/configs/internlm2_chat_7b_qlora_alpaca_e3_copy.py` 同学们可以直接使用（前置步骤路径一致的情况下）


### **步骤 2.** 启动微调

完成了所有的准备工作后，我们就可以正式的开始我们下一阶段的旅程：XTuner 启动~！

当我们准备好了所有内容，我们只需要将使用 `xtuner train` 命令令即可开始训练。

> `xtuner train` 命令用于启动模型微调进程。该命令需要一个参数：`CONFIG` 用于指定微调配置文件。这里我们使用修改好的配置文件 `internlm2_chat_7b_qlora_alpaca_e3_copy.py`。  
> 训练过程中产生的所有文件，包括日志、配置文件、检查点文件、微调后的模型等，默认保存在 `work_dirs` 目录下，我们也可以通过添加 `--work-dir` 指定特定的文件保存位置。`--deepspeed` 则为使用 deepspeed， deepspeed 可以节约显存。

运行命令进行微调

```shell
cd /root/fintune
conda activate /root/share/pre_envs/pytorch2.3.1cu12.1
export PYTHONPATH=/root/finetune/env:$PYTHONPATH
export PATH=/root/finetune/env/bin:$PATH

xtuner train ./internlm2_chat_7b_qlora_alpaca_e3_copy.py --deepspeed deepspeed_zero2 --work-dir ./work_dirs/assistTuner
```

### **步骤 3.** 权重转换

模型转换的本质其实就是将原本使用 Pytorch 训练出来的模型权重文件转换为目前通用的 HuggingFace 格式文件，那么我们可以通过以下命令来实现一键转换。

我们可以使用 `xtuner convert pth_to_hf` 命令来进行模型格式转换。

> `xtuner convert pth_to_hf` 命令用于进行模型格式转换。该命令需要三个参数：`CONFIG` 表示微调的配置文件， `PATH_TO_PTH_MODEL` 表示微调的模型权重文件路径，即要转换的模型权重， `SAVE_PATH_TO_HF_MODEL` 表示转换后的 HuggingFace 格式文件的保存路径。

除此之外，我们其实还可以在转换的命令中添加几个额外的参数，包括：

| 参数名                | 解释                                         |
| --------------------- | -------------------------------------------- |
| --fp32                | 代表以fp32的精度开启，假如不输入则默认为fp16 |
| --max-shard-size {GB} | 代表每个权重文件最大的大小（默认为2GB）      |


```bash
cd /root/fintune/work_dirs/assistTuner
conda activate /root/share/pre_envs/pytorch2.3.1cu12.1
export PYTHONPATH=/root/finetune/env:$PYTHONPATH
export PATH=/root/finetune/env/bin:$PATH

# 先获取最后保存的一个pth文件
pth_file=`ls -t /root/fintune/work_dirs/assistTuner/*.pth | head -n 1`
export MKL_SERVICE_FORCE_INTEL=1
export MKL_THREADING_LAYER=GNU
xtuner convert pth_to_hf ./internlm2_chat_7b_qlora_alpaca_e3_copy.py ${pth_file} ./hf
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

转换完成后，可以看到模型被转换为 HuggingFace 中常用的 .bin 格式文件，这就代表着文件成功被转化为 HuggingFace 格式了。

此时，hf 文件夹即为我们平时所理解的所谓 “LoRA 模型文件”

> 可以简单理解：LoRA 模型文件 = Adapter

### **步骤 4.** 模型合并

对于 LoRA 或者 QLoRA 微调出来的模型其实并不是一个完整的模型，而是一个额外的层（Adapter），训练完的这个层最终还是要与原模型进行合并才能被正常的使用。

> 对于全量微调的模型（full）其实是不需要进行整合这一步的，因为全量微调修改的是原模型的权重而非微调一个新的 Adapter ，因此是不需要进行模型整合的。

在 XTuner 中提供了一键合并的命令 `xtuner convert merge`，在使用前我们需要准备好三个路径，包括原模型的路径、训练好的 Adapter 层的（模型格式转换后的）路径以及最终保存的路径。

> `xtuner convert merge`命令用于合并模型。该命令需要三个参数：`LLM` 表示原模型路径，`ADAPTER` 表示 Adapter 层的路径， `SAVE_PATH` 表示合并后的模型最终的保存路径。

在模型合并这一步还有其他很多的可选参数，包括：

| 参数名                 | 解释                                                         |
| ---------------------- | ------------------------------------------------------------ |
| --max-shard-size {GB}  | 代表每个权重文件最大的大小（默认为2GB）                      |
| --device {device_name} | 这里指的就是device的名称，可选择的有cuda、cpu和auto，默认为cuda即使用gpu进行运算 |
| --is-clip              | 这个参数主要用于确定模型是不是CLIP模型，假如是的话就要加上，不是就不需要添加 |


```bash
cd /root/fintune/work_dirs/assistTuner
conda activate /root/share/pre_envs/pytorch2.3.1cu12.1
export PYTHONPATH=/root/finetune/env:$PYTHONPATH
export PATH=/root/finetune/env/bin:$PATH

export MKL_SERVICE_FORCE_INTEL=1
export MKL_THREADING_LAYER=GNU
xtuner convert merge /root/finetune/models/internlm2-chat-7b ./hf ./merged --max-shard-size 2GB
```

模型合并完成后，我们的目录结构应该是这样子的。

<details>
<summary>目录结构</summary>

```
├── merged
│   ├── README.md
│   ├── config.json
│   ├── configuration.json
│   ├── configuration_internlm2.py
│   ├── generation_config.json
│   ├── modeling_internlm2.py
│   ├── pytorch_model-00001-of-00008.bin
│   ├── pytorch_model-00002-of-00008.bin
│   ├── pytorch_model-00003-of-00008.bin
│   ├── pytorch_model-00004-of-00008.bin
│   ├── pytorch_model-00005-of-00008.bin
│   ├── pytorch_model-00006-of-00008.bin
│   ├── pytorch_model-00007-of-00008.bin
│   ├── pytorch_model-00008-of-00008.bin
│   ├── pytorch_model.bin.index.json
│   ├── special_tokens_map.json
│   ├── tokenization_internlm2.py
│   ├── tokenization_internlm2_fast.py
│   ├── tokenizer.json
│   ├── tokenizer.model
│   └── tokenizer_config.json
```

</details>

在模型合并完成后，我们就可以看到最终的模型和原模型文件夹非常相似，包括了分词器、权重文件、配置信息等等。

## 模型 WebUI 对话

微调完成后，我们可以再次运行 `xtuner_streamlit_demo.py` 脚本来观察微调后的对话效果，不过在运行之前，我们需要将脚本中的模型路径修改为微调后的模型的路径。

```shell
cd ~/Tutorial/tools/L1_XTuner_code
```

```diff
# 直接修改脚本文件第18行
- model_name_or_path = "Shanghai_AI_Laboratory/internlm2-chat-7b"
+ model_name_or_path = "./merged"
```

然后，我们可以直接启动应用。


```bash
conda activate /root/share/pre_envs/pytorch2.3.1cu12.1
export PYTHONPATH=/root/finetune/env:$PYTHONPATH
export PATH=/root/finetune/env/bin:$PATH

streamlit run /root/InternLM/Tutorial/tools/xtuner_streamlit_demo.py
```

运行后，确保端口映射正常，如果映射已断开则需要重新做一次端口映射。


```bash
ssh -CNg -L 8501:127.0.0.1:8501 root@ssh.intern-ai.org.cn -p *****
```

最后，通过浏览器访问：http://127.0.0.1:8501 来进行对话了。

![image](https://github.com/user-attachments/assets/d7c80ea1-761b-4225-974a-620658b2e99d)

