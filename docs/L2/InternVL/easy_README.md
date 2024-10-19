# InternVL 部署微调实践

<img width="900" alt="" src="https://github.com/user-attachments/assets/1dfa4b4b-518b-4a91-898c-671265109fe5">

**本文档为有一定基础可以快速上手的同学准备，比`README.md`的说明更加简洁。**

# 1.环境配置

## 1.1.训练环境配置

### 1.1.a.使用浦语开发机InternStudio

进入预设的虚拟环境，安装相关包:

```Bash
conda activate /root/share/pre_envs/pytorch2.3.1cu12.1
pip install -t /root/internvl_course 'xtuner[deepspeed]' timm==1.0.9  # 防止污染环境
```

### 1.1.b.使用自己的机器

新建虚拟环境并进入:

```Bash
conda create --name xtuner-env python=3.10 -y
conda activate xtuner-env
pip install -U 'xtuner[deepspeed]' timm==1.0.9
```

## 1.2.推理环境配置

配置推理所需环境：

```Bash
conda create -n lmdeploy python=3.8 -y
conda activate lmdeploy
pip install lmdeploy gradio
```

# 2.LMDeploy部署

## 2.1.网页应用部署体验

拉取本教程的github仓库(https://github.com/Control-derek/InternVL2-Tutorial.git)：

```Bash
git clone https://github.com/Control-derek/InternVL2-Tutorial.git
cd InternVL2-Tutorial
```

demo.py文件中，MODEL_PATH处传入InternVL2-2B的路径，如果使用的是InternStudio的开发机则无需修改，否则改为模型路径。

![img](https://dw0fzwkkt9v.feishu.cn/space/api/box/stream/download/asynccode/?code=MWI4NzE1NDVmZWZhNThlMWMzY2RkZmUzY2ExZmNiOGFfS1FRYjF6Rkd5NWJPT3c0THg3aWtQSlljZGV5T2dLUFBfVG9rZW46TVZVWmJQTWpOb1lmOGx4U0VDTmNrUTFtbjAyXzE3MjkzNDAwMTY6MTcyOTM0MzYxNl9WNA)

启动demo:

```Bash
conda activate lmdeploy
python demo.py
```

会看到如下界面：

点击**Start Chat**即可开始聊天，下方**食物快捷栏**可以快速输入图片，**输入示例**可以快速输入文字。输入完毕后，按enter键即可发送。

![img](https://dw0fzwkkt9v.feishu.cn/space/api/box/stream/download/asynccode/?code=YmJjYTRjMWRhZjIyZjE3M2I4ODcyMDY1NDBmYjI1YWZfQlpabDVNVHZhYzNIZmNJenN2cWM0Q2NESThtMkxISXJfVG9rZW46VzlVRGJwTEMxb2dHbzN4Nm1nWmN4bERzbnViXzE3MjkzNDAwMTY6MTcyOTM0MzYxNl9WNA)

## 2.2.多图/轮对话可能会报错

如果输入多张图，或者开多轮对话时报错：

![img](https://dw0fzwkkt9v.feishu.cn/space/api/box/stream/download/asynccode/?code=YmExYTJlYjBiZjg0ZTAwMTYwZmFiZjE3NmJlOTk1YThfT0JIZEV0c1ptZFdKTHlncjUxQllPN083MEpLVk54c2VfVG9rZW46VjhFVWI0a1RWb3J2Wmh4ODJGWWMzVHlWbkplXzE3MjkzNDAwMTY6MTcyOTM0MzYxNl9WNA)

可以参考github的issue(https://github.com/InternLM/lmdeploy/issues/2101)：

![img](https://dw0fzwkkt9v.feishu.cn/space/api/box/stream/download/asynccode/?code=M2I1ODQ2MjAwYWI2Y2NlZTlkNjFiNDgxZDAzMTQxMWVfaVNtbkhSZVpSNnZMeGZGS2h3ZnJaY1JhM0x5bzVQZkVfVG9rZW46SzA4NGIyS2N5bzdmcXR4REhmYWMzMktvbjJlXzE3MjkzNDAwMTY6MTcyOTM0MzYxNl9WNA)

屏蔽报错的engine.py的126，127行，添加`self._create_event_loop_task()`后，即可解决上面报错。

![img](https://dw0fzwkkt9v.feishu.cn/space/api/box/stream/download/asynccode/?code=MTdmYzMxOGY2ZWE3MWE4YzhmOThmMjFhZGU5Y2UwMThfT3p0UWtIUUc2bkdKTTlaY2J5Ym5SNTZwNFBTdWJKM3BfVG9rZW46TFBXOWIybGtjb2prQzF4NTd3NmNaUHZlbm5oXzE3MjkzNDAwMTY6MTcyOTM0MzYxNl9WNA)

# 3.Xtuner微调实践

## 3.1.准备配置文件

进入xtuner文件夹并把我准备好的配置文件复制到指定路径：

```Bash
cd root/xtuner
conda activate xtuner-env  # 或者是你自命名的训练环境
cp /root/InternVL2-Tutorial/xtuner_config/internvl_v2_internlm2_2b_lora_finetune_food.py /root/xtuner/xtuner/configs/internvl/v2/internvl_v2_internlm2_2b_lora_finetune_food.py
```

## 3.2.数据集下载

### 3.3.a.通过huggingface下载

进入该页面https://huggingface.co/datasets/lyan62/FoodieQA申请通过后，在命令行登录huggingface后直接在服务器上下载：

```Bash
huggingface-cli login
```

然后在这里输入huggingface的具有`read`权限的token即可成功登录。

![img](https://dw0fzwkkt9v.feishu.cn/space/api/box/stream/download/asynccode/?code=YjY5MmNjZjQ5MTcyYTA0YzA2OWI2ZDQ3OWVkMzU3NzJfRFYwekJaZUNEWktHSVVwSDBjczNrS2ZuUVh3b05VYnhfVG9rZW46SXdwZmJ5eWtCbzdnenR4U21xSGNzMHpTbjdiXzE3MjkzNDAwMTY6MTcyOTM0MzYxNl9WNA)

再使用命令行下载数据集：

```Bash
huggingface-cli download --repo-type dataset --resume-download lyan62/FoodieQA --local-dir /root/huggingface/FoodieQA --local-dir-use-symlinks False
```

由于原始数据集格式不符合微调需要格式，需要处理方可使用，在`InternVL2-Tutorial`下，运行：

```Bash
python process_food.py
```

即可把数据处理为xtuner所需格式。注意查看`input_path`和`output_path`变量与自己下载路径的区别。

### 3.3.b.通过网盘下载

由于该数据集即需要登录huggingface的方法，又需要申请，下完还需要自己处理，因此我把处理后的文件放在网盘里了🤗。网盘不提供原始数据文件，仅提供完成本课程后续内容所需文件：

> 链接：https://pan.quark.cn/s/ccd8e23bdeca
>
> 提取码：VF45

## 3.4.开始微调🐱🏍

```Bash
export PYTHONPATH=/root/internvl_course:$PYTHONPATH  # 让python能找到第一步安装在其他路径下的包
xtuner train /root/xtuner/xtuner/configs/internvl/v2/internvl_v2_internlm2_2b_lora_finetune_food.py --deepspeed deepspeed_zero2
```

`/root/xtuner/xtuner/configs/internvl/v2/internvl_v2_internlm2_2b_lora_finetune_food.py`为自己配置文件的路径。看到有日志输出，即为启动成功：

![img](https://dw0fzwkkt9v.feishu.cn/space/api/box/stream/download/asynccode/?code=NWViMzQ4MTBmZDI2N2ZjYjY2Y2FjMGM1ZWQ5NTQ3MWRfMmZMOUtGSWE0cWw3U2YzTzFZcTRKMU5PTEpWaHlMNG5fVG9rZW46VXQ0bGJ4TkE2b21hdmd4VFlJUGNpUXpNbmNkXzE3MjkzNDAwMTY6MTcyOTM0MzYxNl9WNA)

微调后，把模型checkpoint的格式转化为便于测试的格式：

```Bash
python xtuner/configs/internvl/v1_5/convert_to_official.py xtuner/configs/internvl/v2/internvl_v2_internlm2_2b_lora_finetune_food.py ./work_dirs/internvl_v2_internlm2_2b_lora_finetune_food/iter_640.pth ./work_dirs/internvl_v2_internlm2_2b_lora_finetune_food/lr35_ep10/ # 输出文件名可以按照喜好设置
```

如果修改了超参数，`iter_xxx.pth`需要修改为对应的想要转的checkpoint。 `./work_dirs/internvl_v2_internlm2_2b_lora_finetune_food/lr35_ep10/`为转换后的模型checkpoint保存的路径，可以按喜好修改。

# 4.与AI美食家玩耍🎉

修改MODEL_PATH为刚刚转换后保存的模型路径：

![img](https://dw0fzwkkt9v.feishu.cn/space/api/box/stream/download/asynccode/?code=MDE4M2FhMDM4YzI2Y2ZhNmViYTJiMzQ4NmZhM2QwNzdfNGNBcThUcm9GaFNQM0pUUkh1NmJzbHZ0ek0xSm9JZ3RfVG9rZW46S2pENmJrM2hHb0dhaTN4N2RsamNnS0pjbmNmXzE3MjkzNDAwMTY6MTcyOTM0MzYxNl9WNA)

就像在第2节中做的那样，启动网页应用：

```Bash
cd /root/InternVL2-Tutorial
conda activate lmdeploy
python demo.py
```

