# InternVL 部署微调实践

<div align="center">
  <img width="900" alt="" src="https://github.com/user-attachments/assets/1dfa4b4b-518b-4a91-898c-671265109fe5">
</div>

# 0.开发机创建与使用

登录浦语开发平台`studio.intern-ai.org.cn`，登录账号后，点击“创建开发机”。（也可以使用自己的机器实践）
选择以下设置：

- 开发机名称：你自己喜欢的名字
- 镜像：Cuda12.2-conda
- 资源配置：50% A100 * 1
- 其余默认 

点击“立即创建”，成功后，可在“开发机”选栏中看到刚刚创建的开发机，可以点击“进入开发机”，利用terminal、code server进行开发。也可以使用本地的vscode通过“SSH链接”中的信息通过SSH链接进行开发。（强烈建议使用本地的vscode进行连接，前者可能有显示bug）

<div align="center">
  <img width="900" alt="" src="https://github.com/user-attachments/assets/23de33b9-0d86-4894-baef-7b9552471fc2">
</div>

后续在命令行中的操作可在进入开发机的terminal或者vscode的terminal界面中进行。代码的修改在vscode中进行。 

本地vscode连接服务器需要下载扩展：

<div align="center">
  <img width="600" alt="" src="https://github.com/user-attachments/assets/4c052839-356d-4233-ae17-38eb1ce63b49">
</div>

然后根据SSH连接的信息，填写ssh连接配置文件。

<div align="center">
  <img width="600" alt="" src="https://github.com/user-attachments/assets/249bdbde-cb79-42fd-b895-555327468ce1">
</div>

上方马赛克处的数字，即为下面port处要填写的端口号。

<div align="center">
  <img width="600" alt="" src="https://github.com/user-attachments/assets/4bcaa31d-09b2-4d90-9922-91a5d7f277de">
</div>

连接后，操作系统选择"linux"，密码输入SSH连接界面给的密码即可。

# 1.环境配置

## 1.1.训练环境配置

新建虚拟环境并进入:

```Bash
conda create --name xtuner-env python=3.10 -y
conda activate xtuner-env
```

"xtuner-env"为训练环境名，可以根据个人喜好设置，在本教程中后续提到训练环境均指"xtuner-env"环境。

安装与deepspeed集成的xtuner和相关包：

```Bash
pip install xtuner==0.1.23 timm==1.0.9
pip install 'xtuner[deepspeed]'
pip install torch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 --index-url https://download.pytorch.org/whl/cu121
pip install transformers==4.39.0 tokenizers==0.15.2 peft==0.13.2 datasets==3.1.0 accelerate==1.2.0 huggingface-hub==0.26.5 
```

训练环境既为安装成功。

## 1.2.推理环境配置

配置推理所需环境：

```Bash
conda create -n lmdeploy python=3.10 -y
conda activate lmdeploy
pip install lmdeploy==0.6.1 gradio==4.44.1 timm==1.0.9
```

"lmdeploy"为推理使用环境名。

# 2.LMDeploy部署

## 2.1.LMDeploy基本用法介绍

我们主要通过`pipeline.chat` 接口来构造多轮对话管线，核心代码为：

```Python
## 1.导入相关依赖包
from lmdeploy import pipeline, TurbomindEngineConfig, GenerationConfig
from lmdeploy.vl import load_image

## 2.使用你的模型初始化推理管线
model_path = "your_model_path"
pipe = pipeline(model_path,
                backend_config=TurbomindEngineConfig(session_len=8192))
                
## 3.读取图片（此处使用PIL读取也行）
image = load_image('your_image_path')

## 4.配置推理参数
gen_config = GenerationConfig(top_p=0.8, temperature=0.8)
## 5.利用 pipeline.chat 接口 进行对话，需传入生成参数
sess = pipe.chat(('describe this image', image), gen_config=gen_config)
print(sess.response.text)
## 6.之后的对话轮次需要传入之前的session，以告知模型历史上下文
sess = pipe.chat('What is the woman doing?', session=sess, gen_config=gen_config)
print(sess.response.text)
```

lmdeploy推理的核心代码如上注释所述。

## 2.2.网页应用部署体验

我们可以使用UI界面先体验与InternVL对话：

拉取本教程的github仓库[https://github.com/Control-derek/InternVL2-Tutorial.git](https://github.com/Control-derek/InternVL2-Tutorial.git)：

```Bash
git clone https://github.com/Control-derek/InternVL2-Tutorial.git
cd InternVL2-Tutorial
```

demo.py文件中，MODEL_PATH处传入InternVL2-2B的路径，如果使用的是InternStudio的开发机则无需修改，否则改为模型路径。

<div align="center">
  <img width="600" alt="" src="https://github.com/user-attachments/assets/062c706e-f58e-41cf-a52a-150ab0cdb8d0">
</div>

启动demo:

```Bash
conda activate lmdeploy
python demo.py
```

上述命令请在vscode下运行，因为vscode自带端口转发，可以把部署在服务器上的网页服务转发到本地。

启动后，CTRL+鼠标左键点进这个链接或者复制链接到浏览器

<div align="center">
  <img width="800" alt="" src="https://github.com/user-attachments/assets/3d2d63a0-3a75-472a-b128-64b0510fbba3">
</div>

会看到如下界面：

点击**Start Chat**即可开始聊天，下方**食物快捷栏**可以快速输入图片，**输入示例**可以快速输入文字。输入完毕后，按enter键即可发送。

<div align="center">
  <img width="900" alt="" src="https://github.com/user-attachments/assets/9640fdd8-98a2-4b53-b184-c2dd5081b755">
</div>

## 2.3.可能遇到棘手bug的解决

如果输入多张图，或者开多轮对话时报错：

<div align="center">
  <img width="750" alt="" src="https://github.com/user-attachments/assets/4b05d649-5b4a-49ba-9fab-2fd8bc69a65f">
</div>

可以参考github的issue[https://github.com/InternLM/lmdeploy/issues/2101](https://github.com/InternLM/lmdeploy/issues/2101)：

<div align="center">
  <img width="750" alt="" src="https://github.com/user-attachments/assets/da205682-b51e-4e4c-8fab-07d2e42a3399">
</div>

屏蔽报错的engine.py的126，127行，添加`self._create_event_loop_task()`后，即可解决上面报错。

<div align="center">
  <img width="750" alt="" src="https://github.com/user-attachments/assets/4ae8ea76-6f9f-4238-9c76-1fc25eb9d84e">
</div>

# 3.XTuner微调实践

## 3.1.准备基本配置文件

在InternStudio开发机的`/root/xtuner`路径下，即为开机自带的xtuner，先进入工作目录并激活训练环境：

```Bash
cd /root/xtuner
conda activate xtuner-env  # 或者是你自命名的训练环境
```

如果没有该路径，可以从GitHub上克隆一个：

```Bash
cd /root
git clone https://github.com/InternLM/xtuner.git
conda activate xtuner-env
```

原始internvl的微调配置文件在路径`./xtuner/configs/internvl/v2`下，假设上面克隆的仓库在/`root/InternVL2-Tutorial`,复制配置文件到目标目录下：

```Bash
cp /root/InternVL2-Tutorial/xtuner_config/internvl_v2_internlm2_2b_lora_finetune_food.py /root/xtuner/xtuner/configs/internvl/v2/internvl_v2_internlm2_2b_lora_finetune_food.py
```

## 3.2.配置文件参数解读

在第一部分的设置中，有如下参数：

- `path`: 需要微调的模型路径，在InternStudio环境下，无需修改。
- `data_root`: 数据集所在路径。
- `data_path`: 训练数据文件路径。
- `image_folder`: 训练图像根路径。
- `prompt_temple`: 配置模型训练时使用的聊天模板、系统提示等。使用与模型对应的即可，此处无需修改。
- `max_length`: 训练数据每一条最大token数。
- `batch_size`: 训练批次大小，可以根据显存大小调整。
- `accumulative_counts`: 梯度累积的步数，用于模拟较大的batch_size，在显存有限的情况下，提高训练稳定性。
- `dataloader_num_workers`: 指定数据集加载时子进程的个数。
- `max_epochs`:训练轮次。
- `optim_type`:优化器类型。
-  `lr`: 学习率
- `betas`: Adam优化器的beta1, beta2
- `weight_decay`: 权重衰减，防止训练过拟合用
- `max_norm`: 梯度裁剪时的梯度最大值
- `warmup_ratio`: 预热比例，前多少的数据训练时，学习率将会逐步增加。
- `save_steps`: 多少步存一次checkpoint
- `save_total_limit`: 最多保存几个checkpoint，设为-1即无限制

<div align="center">
  <img width="600" alt="" src="https://github.com/user-attachments/assets/4341b52a-fe35-473f-8319-733ad46ca210">
</div>

LoRA相关参数：

<div align="center">
  <img width="600" alt="" src="https://github.com/user-attachments/assets/cde70aee-afdc-4d3d-8dee-b477d7873ae0">
</div>

- `r`: 低秩矩阵的秩，决定了低秩矩阵的维度。
- `lora_alpha` 缩放因子，用于调整低秩矩阵的权重。
- `lora_dropout`  dropout 概率，以防止过拟合。

如果想断点重训，可以在最下面传入参数：

<div align="center">
  <img width="600" alt="" src="https://github.com/user-attachments/assets/641d0589-6e3e-47af-afcc-4a10aaa114cb">
</div>

把这里的`load_from`传入你想要载入的checkpoint，并设置`resume=True`即可断点重续。

## 3.3.数据集下载

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
  <img width="600" alt="" src="https://github.com/user-attachments/assets/147f09c1-2334-4edc-bb74-862f6b560c23">
</div>

### 3.3.a.通过huggingface下载

有能力的同学，建议去huggingface下载此数据集：[https://huggingface.co/datasets/lyan62/FoodieQA](https://huggingface.co/datasets/lyan62/FoodieQA)。该数据集为了防止网络爬虫污染测评效果，需要向提交申请后下载使用。

由于申请的与huggingface账号绑定，需要在命令行登录huggingface后直接在服务器上下载：

```Bash
huggingface-cli login
```

然后在这里输入huggingface的具有`read`权限的token即可成功登录。

<div align="center">
  <img width="600" alt="" src="https://github.com/user-attachments/assets/13af2ac0-86c6-4889-961c-5365423e463f">
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

### 3.3.b.利用share目录下处理好的数据集

由于该数据集即需要登录huggingface的方法，又需要申请，下完还需要自己处理，因此我把处理后的文件放在开发机的`/root/share/datasets/FoodieQA`路径下了。

## 3.4.开始微调🐱🏍

运行命令，开始微调：

```Bash
xtuner train internvl_v2_internlm2_2b_lora_finetune_food --deepspeed deepspeed_zero2
```

看到有日志输出，即为启动成功：

<div align="center">
  <img width="750" alt="" src="https://github.com/user-attachments/assets/17754acc-29bb-477d-8aee-a69e361f7343">
</div>

如果报错如：keyerror或者Filenotfound之类的，可能是XTuner没识别到新写的配置文件，需要指定配置文件的完整路径：

```Bash
xtuner train /root/xtuner/xtuner/configs/internvl/v2/internvl_v2_internlm2_2b_lora_finetune_food.py --deepspeed deepspeed_zero2
```

把`/root/xtuner/xtuner/configs/internvl/v2/internvl_v2_internlm2_2b_lora_finetune_food.py`换成自己配置文件的路径即可。

微调后，把模型checkpoint的格式转化为便于测试的格式：

```Bash
python xtuner/configs/internvl/v1_5/convert_to_official.py xtuner/configs/internvl/v2/internvl_v2_internlm2_2b_lora_finetune_food.py ./work_dirs/internvl_v2_internlm2_2b_lora_finetune_food/iter_640.pth ./work_dirs/internvl_v2_internlm2_2b_lora_finetune_food/lr35_ep10/
```

如果修改了超参数，`iter_xxx.pth`需要修改为对应的想要转的checkpoint。 `./work_dirs/internvl_v2_internlm2_2b_lora_finetune_food/lr35_ep10/`为转换后的模型checkpoint保存的路径。

# 4.与AI美食家玩耍🎉

修改MODEL_PATH为刚刚转换后保存的模型路径：

<div align="center">
  <img width="750" alt="" src="https://github.com/user-attachments/assets/58553b77-e65d-4d74-87a7-9178958ca621">
</div>

就像在第2节中做的那样，启动网页应用：

```Bash
cd /root/InternVL2-Tutorial
conda activate lmdeploy
python demo.py
```

部分case展示：

微调前，把肠粉错认成饺子，微调后，正确识别：

<div align="center">
  <img width="600" alt="" src="https://github.com/user-attachments/assets/54cad835-4e95-402c-85a9-4b84574de2db">
</div>

<div align="center">
  <img width="600" alt="" src="https://github.com/user-attachments/assets/2443ac5f-9a99-45f9-854d-774d83db3310">
</div>

微调前，不认识“锅包又”，微调后，可以正确识别：

<div align="center">
  <img width="600" alt="" src="https://github.com/user-attachments/assets/3a333ea0-b48d-4425-aedd-63b27e87cbe2">
</div>


<div align="center">
  <img width="600" alt="" src="https://github.com/user-attachments/assets/ad011dcf-e093-4335-bee6-e6906979a174">
</div>

<div style="text-align: center; padding: 20px; background-color: #f0f8ff; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
    <h2 style="color: #ff6347; font-size: 2em; margin-bottom: 10px;">恭喜你完成了本课程🎉🎊</h2>
</div>
