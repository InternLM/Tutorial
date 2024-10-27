# InternVL 部署微调实践

<div align="center">
<img width="900" alt="" src="https://github.com/user-attachments/assets/1dfa4b4b-518b-4a91-898c-671265109fe5">
</div>

**本文档为有一定基础可以快速上手的同学准备，比`README.md`的说明更加简洁。**

# 1.环境配置

## 1.1.训练环境配置

进入预设的虚拟环境，安装相关包:

```Bash
conda activate /root/share/pre_envs/pytorch2.3.1cu12.1
pip install -t /root/internvl_course 'xtuner[deepspeed]' timm==1.0.9  # 防止污染环境
```
每次使用前，需要运行一下命令，把自定义的安装包的路径添加到PYTHONPATH环境变量中，这样python才能找到你安装的包;还要把`bin`文件夹添加到PATH环境变量中，这样才能找到你用pip安装的命令行工具（同一个终端下只需运行一次）：
```Bash
export PYTHONPATH=/root/internvl_course:$PYTHONPATH
export PATH=/root/internvl_course/bin:$PATH
```

## 1.2.推理环境配置

配置推理所需环境：

```Bash
conda create -n lmdeploy python=3.10 -y
conda activate lmdeploy
pip install lmdeploy gradio timm==1.0.9
```

# 2.LMDeploy部署

## 2.1.网页应用部署体验

拉取本教程的github仓库[https://github.com/Control-derek/InternVL2-Tutorial.git](https://github.com/Control-derek/InternVL2-Tutorial.git)：

```Bash
git clone https://github.com/Control-derek/InternVL2-Tutorial.git
cd InternVL2-Tutorial
```

demo.py文件中，MODEL_PATH处传入InternVL2-2B的路径，如果使用的是InternStudio的开发机则无需修改，否则改为模型路径。

<div align="center">
<img width="800" alt="" src="https://github.com/user-attachments/assets/062c706e-f58e-41cf-a52a-150ab0cdb8d0">
</div>

启动demo:

```Bash
conda activate lmdeploy
python demo.py
```

会看到如下界面：

点击**Start Chat**即可开始聊天，下方**食物快捷栏**可以快速输入图片，**输入示例**可以快速输入文字。输入完毕后，按enter键即可发送。

<div align="center">
<img width="900" alt="" src="https://github.com/user-attachments/assets/9640fdd8-98a2-4b53-b184-c2dd5081b755">
</div>

## 2.2.多图/轮对话可能会报错

如果输入多张图，或者开多轮对话时报错：

<div align="center">
<img width="800" alt="" src="https://github.com/user-attachments/assets/4b05d649-5b4a-49ba-9fab-2fd8bc69a65f">
</div>

可以参考github的issue[https://github.com/InternLM/lmdeploy/issues/2101](https://github.com/InternLM/lmdeploy/issues/2101)：

<div align="center">
<img width="800" alt="" src="https://github.com/user-attachments/assets/da205682-b51e-4e4c-8fab-07d2e42a3399">
</div>

屏蔽报错的engine.py的126，127行，添加`self._create_event_loop_task()`后，即可解决上面报错。

<div align="center">
<img width="800" alt="" src="https://github.com/user-attachments/assets/4ae8ea76-6f9f-4238-9c76-1fc25eb9d84e">
</div>

# 3.XTuner微调实践

## 3.1.准备配置文件

进入xtuner文件夹并把我准备好的配置文件复制到指定路径：

```Bash
cd root/xtuner
conda activate xtuner-env  # 或者是你自命名的训练环境
cp /root/InternVL2-Tutorial/xtuner_config/internvl_v2_internlm2_2b_lora_finetune_food.py /root/xtuner/xtuner/configs/internvl/v2/internvl_v2_internlm2_2b_lora_finetune_food.py
```

## 3.2.数据集下载
我们采用的是FoodieQA数据集，这篇文章中了2024EMNLP的主会，其引用信息如下：

```
@article{li2024foodieqa,
  title={FoodieQA: A Multimodal Dataset for Fine-Grained Understanding of Chinese Food Culture},
  author={Li, Wenyan and Zhang, Xinyu and Li, Jiaang and Peng, Qiwei and Tang, Raphael and Zhou, Li and Zhang, Weijia and Hu, Guimin and Yuan, Yifei and S{\o}gaard, Anders and others},
  journal={arXiv preprint arXiv:2406.11030},
  year={2024}
}
```

FoodieQA 是一个专门为研究中国各地美食文化而设计的数据集。它包含了大量关于食物的图片和问题，帮助多模态大模型更好地理解不同地区的饮食习惯和文化特色。这个数据集的推出，让我们能够更深入地探索和理解食物背后的文化意义。

**可以通过`3.2.a.`和`3.2.b.`两种方式获取数据集**，根据获取方式的不同，可能需要修改配置文件中的`data_root`变量为你数据集的路径：

<div align="center">
<img width="800" alt="" src="https://github.com/user-attachments/assets/147f09c1-2334-4edc-bb74-862f6b560c23">
</div>

### 3.2.a.通过huggingface下载

有能力的同学，建议去huggingface下载此数据集：[https://huggingface.co/datasets/lyan62/FoodieQA](https://huggingface.co/datasets/lyan62/FoodieQA)。该数据集为了防止网络爬虫污染测评效果，需要向提交申请后下载使用。

由于申请的与huggingface账号绑定，需要在命令行登录huggingface后直接在服务器上下载：

```Bash
huggingface-cli login
```

然后在这里输入huggingface的具有`read`权限的token即可成功登录。

<div align="center">
<img width="800" alt="" src="https://github.com/user-attachments/assets/13af2ac0-86c6-4889-961c-5365423e463f">
</div>

再使用命令行下载数据集：

```Bash
huggingface-cli download --repo-type dataset --resume-download lyan62/FoodieQA --local-dir /root/huggingface/FoodieQA --local-dir-use-symlinks False
```

如果觉得上述过程麻烦，可以用浏览器下载后，再上传服务器即可😊

由于原始数据集格式不符合微调需要格式，需要处理方可使用，在`InternVL2-Tutorial`下，运行：

```Bash
python process_food.py
```

即可把数据处理为XTuner所需格式。注意查看`input_path`和`output_path`变量与自己下载路径的区别。

### 3.2.b.利用share目录下处理好的数据集

由于该数据集即需要登录huggingface的方法，又需要申请，下完还需要自己处理，因此我把处理后的文件放在开发机的`/root/share/datasets/FoodieQA`路径下了。

## 3.3.开始微调🐱🏍

```Bash
export PYTHONPATH=/root/internvl_course:$PYTHONPATH  # 让python能找到第一步安装在其他路径下的包
export PATH=/root/internvl_course/bin:$PATH  # 让系统可以找到你安装的命令行工具
xtuner train /root/xtuner/xtuner/configs/internvl/v2/internvl_v2_internlm2_2b_lora_finetune_food.py --deepspeed deepspeed_zero2
```

`/root/xtuner/xtuner/configs/internvl/v2/internvl_v2_internlm2_2b_lora_finetune_food.py`为自己配置文件的路径。看到有日志输出，即为启动成功：

<div align="center">
<img width="800" alt="" src="https://github.com/user-attachments/assets/17754acc-29bb-477d-8aee-a69e361f7343">
</div>

微调后，把模型checkpoint的格式转化为便于测试的格式：

```Bash
python xtuner/configs/internvl/v1_5/convert_to_official.py xtuner/configs/internvl/v2/internvl_v2_internlm2_2b_lora_finetune_food.py ./work_dirs/internvl_v2_internlm2_2b_lora_finetune_food/iter_640.pth ./work_dirs/internvl_v2_internlm2_2b_lora_finetune_food/lr35_ep10/ # 输出文件名可以按照喜好设置
```

如果修改了超参数，`iter_xxx.pth`需要修改为对应的想要转的checkpoint。 `./work_dirs/internvl_v2_internlm2_2b_lora_finetune_food/lr35_ep10/`为转换后的模型checkpoint保存的路径，可以按喜好修改。

# 4.与AI美食家玩耍🎉

修改MODEL_PATH为刚刚转换后保存的模型路径：

<div align="center">
<img width="800" alt="" src="https://github.com/user-attachments/assets/58553b77-e65d-4d74-87a7-9178958ca621">
</div>

就像在第2节中做的那样，启动网页应用：

```Bash
cd /root/InternVL2-Tutorial
conda activate lmdeploy
python demo.py
```

