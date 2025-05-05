# InternVL中RLHF及MPO技术的原理与实践


# 0.初始化

## 0.1.开发机创建与使用

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

## 0.2.创建工作目录

本文档工作目录默认在`~/MPO`下进行。新建工作环境：

```bash
cd ~
mkdir -p mpo
```

# 1.LMDeploy部署

在进行MPO微调实战之前，我们先部署一下微调之前的模型，体验一下效果。

## 1.1.环境配置

新建虚拟环境并配置部署所需环境：

```Bash
conda create -n lmdeploy python=3.10 -y
conda activate lmdeploy
pip install lmdeploy==0.6.1 gradio==4.44.1 timm==1.0.9
```

`"lmdeploy"`为推理使用环境名。

## 1.2.可视化部署

拉取可视化推理仓库[https://github.com/Control-derek/MPO-Tutorial.git](https://github.com/Control-derek/MPO-Tutorial.git)：

```bash
git clone https://github.com/Control-derek/MPO-Tutorial.git
```

在`demo.py`中，默认模型路径为浦语开发机自带的`InternVL2_5-1B`，可根据需要修改：

<div align="center">
  <img width="600" alt="" src="https://github.com/user-attachments/assets/573ce406-49a6-44ca-a802-676d523258fb">
</div>

运行推理代码：

```
cd MPO-Tutorial
conda activate lmdeploy
python demo.py
```

上述命令请在vscode下运行，因为vscode自带端口转发，可以把部署在服务器上的网页服务转发到本地。

启动后，CTRL+鼠标左键点进这个链接或者复制链接到浏览器

<div align="center">
  <img width="800" alt="" src="https://github.com/user-attachments/assets/3d2d63a0-3a75-472a-b128-64b0510fbba3">
</div>

会看到如下界面：

点击**`Start Chat`**即可开始聊天，下方**`测试图片`**可以快速输入图片，**`输入示例`**可以快速输入文字。（**`测试图片`**和**`输入示例`**按次序匹配）输入完毕后，按enter键即可发送。结果可与**`正确答案`**比对。

<div align="center">
  <img width="800" alt="" src="https://github.com/user-attachments/assets/7db6b969-3c36-47b9-86cb-76d569239c33">
</div>

试用微调前的模型：

<div align="center">
  <img width="800" alt="" src="https://github.com/user-attachments/assets/673127a1-6c60-4cec-8b42-e02560eb943e">
</div>

虽然看起来很有条理，但是答不对题，代表这个模型可能欠缺几何推理能力。😣

# 2.MPO训练

## 2.1.环境配置

拉取InternVL官方仓库[https://github.com/OpenGVLab/InternVL](https://github.com/OpenGVLab/InternVL)：

```bash
git clone https://github.com/OpenGVLab/InternVL.git
```

修改`requirements/internvl_chat.txt`中的torch、torchvision和transformers的版本，加入flash-attn、datasets、trl：

```
torch==2.4.0
torchvision==0.19.0
flash-attn==2.7.3
datasets==3.2.0
trl==0.10.1
transformers==4.40.1
```

<div align="center">
  <img width="800" alt="" src="https://github.com/user-attachments/assets/c1e6a7d7-db4d-44c5-8b4a-d2f6649cbf60">
</div>

创建新环境`mpo`并配置恰当的环境：

```bash
cd InternVL
conda create -n mpo python=3.10
conda activate mpo
pip install torch==2.4.0
pip install -r requirements/internvl_chat.txt
```

## 2.2.修改配置文件

MPO训练的配置文件在`internvl_chat/shell/internvl2.5_mpo/preference_optimization/ `路径下，为了节省显存，我们选择微调1B的模型，其原始配置文件在`internvl2_5_1b_qwen2_5_0_5b_dynamic_res_mpo.sh`中。

复制一份配置文件到`internvl2_5_1b_qwen2_5_0_5b_dynamic_res_mpo_geom.sh`，以方便我们修改：

```
cd internvl_chat
cp shell/internvl2.5_mpo/preference_optimization/internvl2_5_1b_qwen2_5_0_5b_dynamic_res_mpo.sh shell/internvl2.5_mpo/preference_optimization/internvl2_5_1b_qwen2_5_0_5b_dynamic_res_mpo_geom.sh
```

后缀`_geom`代表我们将对1B模型表现不佳的几何问题上进行微调。



为了在有限资源下启动训练，下面开始修改`internvl2_5_1b_qwen2_5_0_5b_dynamic_res_mpo_geom.sh`：

把默认GPU数量、每个节点的GPU数、Batch size都改为1：

<div align="center">
  <img width="800" alt="" src="https://github.com/user-attachments/assets/466e4436-1e08-498e-9252-13ccb7bdbe6c">
</div>

屏蔽`TRITON_CACHE_DIR`配置，设置`LAUNCHER`为`pytorch`，`RANK`为`0`，`WORLD_SIZE`为`1`：

<div align="center">
  <img width="800" alt="" src="https://github.com/user-attachments/assets/dbdf0b3a-ffc8-4e38-84ad-fd914093a5b6">
</div>

把srun相关启动命令删去，用python启动训练：

<div align="center">
  <img width="800" alt="" src="https://github.com/user-attachments/assets/2cca84aa-7e89-4396-9603-d8303b8f5a9f">
</div>
修改模型、数据集为本地路径，epoch为5：

<div align="center">
  <img width="800" alt="" src="https://github.com/user-attachments/assets/b59eacac-1540-4e47-a595-a840566c695f">
</div>

```shell
--model_name_or_path "/root/share/new_models/OpenGVLab/InternVL2_5/InternVL2_5-1B"
--meta_path "/root/MPO/MPO-Tutorial/mini-MMPR-v1.1/meta.json"
--num_train_epochs 5
```

模型路径为浦语开发机自带的`InternVL2_5-1B`，可根据需要修改

本课程所需数据集也在仓库https://github.com/Control-derek/MPO-Tutorial.git中，在1.2节中，我们已经将该仓库克隆在`/root/MPO/MPO-Tutorial/`下。如果克隆位置与此位置，不一致，需要修改`MPO-Tutorial/mini-MMPR-v1.1/meta.json`中`"root"`与`"annotation"`的路径：

<div align="center">
  <img width="800" alt="" src="https://github.com/user-attachments/assets/cda06e2c-646c-4999-b7b2-74b3463b24cc">
</div>

将`/root/MPO/MPO-Tutorial/`替换为克隆仓库的路径即可。




节省显存：`max_seq_length`修改为`4096`，启用deepspeed的stage3策略，关闭liger(环境可能有冲突)

<div align="center">
  <img width="800" alt="" src="https://github.com/user-attachments/assets/e07aa467-7a17-4487-9558-db369983cc23">
</div>

修改`zero_stage3_config.json`文件，启动显存卸载配置：

<div align="center">
  <img width="800" alt="" src="https://github.com/user-attachments/assets/adc1abfb-1a44-4cdf-bbf0-bafda9ab7814">
</div>
```json
"offload_optimizer": {
    "device": "cpu",
    "pin_memory": true
},
"offload_param": {
    "device": "cpu",
    "pin_memory": true
},
```



## 2.3.启动训练脚本

启动训练脚本：

```bash
bash shell/internvl2.5_mpo/preference_optimization/internvl2_5_1b_qwen2_5_0_5b_dynamic_res_mpo_geom.sh
```

出现日志，即为成功启动训练：

<div align="center">
  <img width="800" alt="" src="https://github.com/user-attachments/assets/f68780d5-b065-48bc-89dc-adce9879bff9">
</div>

大约30min后，训练结束：

<div align="center">
  <img width="800" alt="" src="https://github.com/user-attachments/assets/f87c8d36-434b-407a-b41a-577ac714d81e">
</div>

# 3.二次部署

在`demo.py`中，替换模型路径为刚才的输出路径 `/root/MPO/InternVL/internvl_chat/work_dirs/internvl_chat_v2_5_mpo/Internvl2_5-1B-MPO`：

<div align="center">
  <img width="800" alt="" src="https://github.com/user-attachments/assets/c4db54cd-8a1d-41ec-ad55-59500bdb8f8e">
</div>

启动可视化界面：

```bash
cd ~/MPO/MPO-Tutorial
python demo.py
```

经过MPO训练后，答对了之前未能答对的问题：

<div align="center">
  <img width="800" alt="" src="https://github.com/user-attachments/assets/fc185ddd-301d-42ba-beed-daa5b16f5bc0">
</div>



<div style="text-align: center; padding: 20px; background-color: #f0f8ff; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
    <h2 style="color: #ff6347; font-size: 2em; margin-bottom: 10px;">恭喜你完成了本课程🎉🎊</h2>
</div>