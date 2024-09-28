# 写在前面
微调内容需要使用 30% A100 才能完成。
本次实战营的微调内容包括了以下两个部分：
1. SFT 数据的获取
2. 使用 [InternLM2.5-7B-Chat](https://huggingface.co/internlm/internlm2_5-7b-chat) 模型微调 

这节课你会收获：
* 针对业务场景（如特殊自我认知的机器人）的微调能力
* 一个属于自己的语言聊天机器人

本节课对应的视频链接：暂无
XTuner 文档链接：[XTuner-doc-cn](https://xtuner.readthedocs.io/zh-cn/latest/)

# 环境配置与数据准备

本节中，我们将演示如何安装 XTuner。
推荐使用 Python-3.10 的 conda 虚拟环境安装 XTuner。
## **步骤 0.** 使用 conda 先构建一个 Python-3.10 的虚拟环境

```shell
mkdir -p /root/finetune && cd /root/finetune
conda create --name xtuner-env python=3.10 -y
conda activate xtuner-env
```
## **步骤 1.** 安装 XTuner
此处推荐源码安装，更多的安装方法请回到前面看 XTuner 文档
```shell
git clone https://github.com/InternLM/xtuner.git
cd /root/finetune/xtuner
pip install -e '.[deepspeed]'
```

<details>
<summary>如果安装过程出现错误，请参考以下解决方案：</summary>
> WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1007)'))': /pypi/simple/bitsandbytes/

> Could not fetch URL https://mirrors.aliyun.com/pypi/simple/bitsandbytes/: There was a problem confirming the ssl certificate: HTTPSConnectionPool(host='mirrors.aliyun.com', port=443): Max retries exceeded with url: /pypi/simple/bitsandbytes/ (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1007)'))) - skipping

> INFO: pip is looking at multiple versions of xtuner to determine which version is compatible with other requirements. This could take a while.

> ERROR: Could not find a version that satisfies the requirement bitsandbytes>=0.40.0.post4 (from xtuner) (from versions: none)，可以 `Ctrl + C` 退出后换成 `pip install --trusted-host mirrors.aliyun.com -e '.[deepspeed]' -i https://mirrors.aliyun.com/pypi/simple/`

</details>

>“-e” 表示在可编辑模式下安装项目，因此对代码所做的任何本地修改都会生效

## 验证安装
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
</details>

> 输出内容为 XTuner 支持微调的模型


# 修改提供的数据
## **步骤 0.** 创建一个新的文件夹用于存储微调数据
```shell
mkdir -p root/finetune/data && cd /root/finetune/data
cp -r /root/JsonData  /root/finetune/data
#复制存放jsonl格式的训练数据的文件夹JsonData到/root/finetune/data
#这里要改一下jsondata的地址！！！
```

<details>
<summary>此时JsonData 文件夹下应该有如下结构</summary>

```
|-- JsonData/
    |-- assistant_Tuner.jsonl
```

</details>

## **步骤 1.** 创建修改脚本

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


## **步骤 2.** 执行脚本

```shell
# usage：python change_script.py {input_file.jsonl} {output_file.jsonl}
cd {path/to/finetune}
python change_script.py ./data/assist_Tuner.jsonl ./data/assist_Tuner_change.jsonl
```

`output_file.jsonl`是修改后符合 XTuner 格式的训练数据。

<details>
<summary>此时 data 文件夹下应该有如下结构</summary>

```
|-- /finetune/data/
    |-- assistant_Tuner.jsonl
	|-- assistant_Tuner_change.jsonl
```

</details>


## **步骤 3.** 查看数据

```shell
cat output_file.jsonl | head -n 3
```
此处结果太长不再展示，主要是检查自己要修改的名字是否在数据中。

# 复制模型并修改训练用的 Config
## **步骤 0.** 复制模型

在InternStudio开发机中的已经提供了微调模型，可以直接软链接即可。

本模型位于/root/share/new_models/Shanghai_AI_Laboratory/internlm2-chat-7b

```shell
mkdir /root/finetune/models
ln -ls /root/share/new_models/Shanghai_AI_Laboratory/internlm2-chat-7b /root/finetune/models/internlm2-chat-7b
```

## **步骤 1.** 修改 Config

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


本教程已经将改好的 config 放在了 `docs/L1/XTuner/config/internlm2_chat_7b_qlora_alpaca_e3_copy.py` 同学们可以直接使用（前置步骤路径一致的情况下）


## **步骤 2.** 启动微调

完成了所有的准备工作后，我们就可以正式的开始我们下一阶段的旅程：XTuner 启动~！

当我们准备好了所有内容，我们只需要将使用 `xtuner train` 命令令即可开始训练。

> `xtuner train` 命令用于启动模型微调进程。该命令需要一个参数：`CONFIG` 用于指定微调配置文件。这里我们使用修改好的配置文件 `internlm2_chat_7b_qlora_alpaca_e3_copy.py`。  
> 训练过程中产生的所有文件，包括日志、配置文件、检查点文件、微调后的模型等，默认保存在 `work_dirs` 目录下，我们也可以通过添加 `--work-dir` 指定特定的文件保存位置。

运行

```shell
cd /root/fintune
conda activate xtuner_env

xtuner train ./internlm2_chat_7b_qlora_alpaca_e3_copy.py --deepspeed deepspeed_zero2 --work-dir ./work_dir
```