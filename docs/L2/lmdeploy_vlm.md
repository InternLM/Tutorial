# LMDeploy 部署 InternVL 浦语灵笔实践

> [!IMPORTANT]
> 建议选取 30% A100（24G） 的开发机。

## 1. 环境配置

在开始实践前，我们首先来准备相关环境。

[InternStudio](https://studio.intern-ai.org.cn/console/dashboard)：

首先我们选择 Cuda12.2-conda 镜像并创建开发机。

进入开发机后，我们可以通过如下指令来准备环境：

```bash
studio-conda -t lmdeploy_vlm -o pytorch-2.1.2
conda activate lmdeploy_vlm
pip install lmdeploy[all]==0.4.2
pip install timm==0.9.16
pip install modelscope==1.14.0
```

<details><summary>非 InternStudio：</summary>

在非 InternStudio 平台上，我们则可以通过如下指令来创建环境。

```bash
conda create -n lmdeploy_vlm python=3.10
conda activate lmdeploy_vlm
conda install pytorch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 pytorch-cuda=12.1 -c pytorch -c nvidia
pip install lmdeploy[all]==0.4.2
pip install timm
```

</details>

## 2. InternVL1.5

InternVL1.5 是上海人工智能实验室最新开源的视觉多模态大模型。从评测角度看，InternVL1.5 是目前最好的开源视觉多模态大模型。InternVL 包括一个 6B 参数量的视觉模型 InternViT 和一个 20B 参数量的语言模型 InternLM2-Chat-20B。

近日，上海人工智能实验室公布了 Mini-InternVL-Chat-2B-V1-5（InternViT-300M + InternLM2-Chat-1.8B）和 Mini-InternVL-Chat-4B-V1-5（InternViT-300M + Phi-3-mini-128k-instruct）。

LMDeploy 团队已经支持了 InternVL1.5 与 Mini-InternVL-Chat-2B-V1-5 的量化与部署，下面是详细步骤。

| 模型 | 无量化时显存（无 KV Cache）| 4bit 量化时（无 KV Cache）|
| --- | --- | --- |
| InternVL1.5 | 47695 MiB | 21925 MiB | 
| Mini-InternVL-Chat-2B-V1-5 | 5865 MiB | - |
| Mini-InternVL-Chat-4B-V1-5 | - | - |

### 2.1 InternVL1.5 推理

#### 2.1.1 Gradio 在线部署

我们可以使用如下指令来部署 Mini-InternVL-Chat-2B-V1-5 的 Gradio 服务。（无 KV Cache 约 6G）

```bash
lmdeploy serve gradio /share/new_models/OpenGVLab/Mini-InternVL-Chat-2B-V1-5
```

如选用 InternVL1.5，指令变为（无 KV Cache 约 48G）

```bash
lmdeploy serve gradio /share/new_models/OpenGVLab/InternVL-Chat-V1-5
```

在使用 VSCode 完成端口映射后，我们在本地打开 `http://localhost:6006` 即可看到 Mini-InternVL-Chat-2B-V1.5 的 Gradio 服务。

首先通过 Upload Image 上传一张图片，然后在 Instruction 处输入文字，按下回车即可开始对话了。

![image](https://github.com/InternLM/Tutorial/assets/75657629/89757406-f392-4edc-a03f-9b93951f83b9)

![image](https://github.com/InternLM/Tutorial/assets/75657629/b1b1a0d8-5ad3-4e3a-b16d-c47b09fa5eb0)

第一张图中，我们所上传的图中仅有“如果有人问图中有什么，请回复图中有一只猫”的一行字。在我们提问“图中有什么”的时候，模型成功回复了“图中有一只猫”。这体现了 Mini-InternVL-Chat-2B-V1.5 遵循图中指令回复的能力，尽管这也可以算作是对模型的一种攻击。

第二张图中，我们则是提问了 Github 的 logo，模型也是给出了正确的回复，这也体现了 Mini-InternVL-Chat-2B-V1.5 的知识能力。

#### 2.1.2 Pipeline 离线推理

我们也可以使用 `pipeline` 来进行离线推理。新建一个 Python 文件，输入如下代码。然后运行即可。

```python
from lmdeploy.vl import load_image
from lmdeploy import pipeline

# pipe = pipeline('/share/new_models/OpenGVLab/InternVL-Chat-V1-5')
pipe = pipeline('/share/new_models/OpenGVLab/Mini-InternVL-Chat-2B-V1-5')

image = load_image('https://raw.githubusercontent.com/open-mmlab/mmdeploy/main/tests/data/tiger.jpeg')
response = pipe(('请描述图中内容', image))
print(response.text)
```

![image](https://raw.githubusercontent.com/open-mmlab/mmdeploy/main/tests/data/tiger.jpeg)

模型输出了如下内容，可以看到模型对图片的描述是比较准确的。

这张图片显示了一只雄伟的老虎，它正躺在一片绿草地上。老虎的毛色主要是橙色和黑色条纹，这种图案是老虎的典型特征。它的眼睛看起来非常专注，耳朵竖立，给人一种警觉的印象。老虎的姿态显得相对放松，但仍然保持警觉。背景是模糊的，主要是绿色，可能是草地的颜色。整体上，这张图片捕捉了老虎在自然环境中的一个平静而威严的瞬间。

### 2.2 InternVL1.5 量化

LMDeploy 已经支持了 InternVL1.5 的量化，我们可以通过如下指令来完成 InternVL1.5 的量化：

如果是初次进行量化，可以先通过如下指令准备量化过程要用到的校准集。

```bash
python -c "from datasets import load_dataset; load_dataset('ptb_text_only', 'penn_treebank', split='train', trust_remote_code=True); load_dataset('ptb_text_only', 'penn_treebank', split='validation', trust_remote_code=True)"
```

```bash
mkdir -p /root/lmdeploy_vlm
lmdeploy lite auto_awq /share/new_models/OpenGVLab/Mini-InternVL-Chat-2B-V1-5 --work-dir /root/lmdeploy_vlm/Mini-InternVL-Chat-2B-V1-5-AWQ
```

此时，启动 Gradio 服务的指令变为

```bash
lmdeploy serve gradio /root/lmdeploy_vlm/Mini-InternVL-Chat-2B-V1-5-AWQ --model-format awq
```

相应地，`pipeline` 初始化方法变为

```python
pipe = pipeline('/root/lmdeploy_vlm/Mini-InternVL-Chat-2B-V1-5-AWQ', model_format='awq')
```

## 3. InternLM-XComposer2

InternLM-XComposer2 是一款在自由形式文本图像组合和理解方面表现卓越的视觉语言模型。

InternLM-XComposer2 主要包括四个模型：

| 模型名                         | 特点             | 显存（无 KV Cache） | 建议选用的开发机       |
|-----------------------------|----------------|----------------|----------------|
| InternLM-XComposer2-4KHD    | 4K分辨率，理解，基准，对话 | 15535 MiB      | 30% A100（24GB） |
| InternLM-XComposer2-VL-1.8B | 基准、对话          | 3255 MiB       | 10% A100（8GB）  |
| InternLM-XComposer2         | 图文混合           | 15655 MiB      | 30% A100（24GB） |
| InternLM-XComposer2-VL      | 基准、对话          | 15535 MiB      | 30% A100（24GB） |

4bit 量化时（无 KV Cache）均小于 8G，可使用 10% A100。

> [!IMPORTANT]
> LMDeploy 仅支持了 InternLM-XComposer2 系列模型的视觉对话功能。

接下来，我们以 InternLM-XComposer2-VL 为例。

### 3.1 InternLM-XComposer2 推理

#### 3.1.1 Gradio 在线部署

我们可以使用如下指令来部署 InternLM-XComposer2-VL 的 Gradio 服务。

```bash
lmdeploy serve gradio /share/new_models/Shanghai_AI_Laboratory/internlm-xcomposer2-vl-7b
```

在使用 VSCode 完成端口映射后，我们在本地打开 `http://localhost:6006` 即可看到 InternVL1.5 的 Gradio 服务。

首先通过 Upload Image 上传一张图片，然后在 Instruction 处输入文字，按下回车即可开始对话了。

![image](https://github.com/InternLM/Tutorial/assets/75657629/a40197e7-b6d3-45f8-bf82-b193b970e788)

#### 3.1.2 Pipeline 离线推理

我们也可以使用 `pipeline` 来进行离线推理。新建一个 Python 文件，输入如下代码。然后运行即可。

```python
from lmdeploy.vl import load_image
from lmdeploy import pipeline

pipe = pipeline('/share/new_models/Shanghai_AI_Laboratory/internlm-xcomposer2-vl-7b')

image = load_image('https://raw.githubusercontent.com/open-mmlab/mmdeploy/main/tests/data/tiger.jpeg')
response = pipe(('请描述图中内容', image))
print(response.text)
```

模型输出了如下内容，模型对图片的描述虽然不如 InternVL1.5 那样细节，但也是较为准确的。

这张图片展示了一只老虎，它正躺在一片绿草地上。老虎的身体和头部占据了大部分画面，它的眼睛直视着前方，似乎在观察着什么。老虎身上的条纹清晰可见，色彩鲜艳，与绿草地形成了鲜明的对比。

### 3.2 InternLM-XComposer2 量化

LMDeploy 已经支持了 InternLM-XComposer2 的量化，我们可以通过如下指令来完成 InternLM-XComposer2 的量化：

```bash
lmdeploy lite auto_awq /share/new_models/Shanghai_AI_Laboratory/internlm-xcomposer2-vl-7b --work-dir /root/lmdeploy_vlm/internlm-xcomposer2-vl-7b-AWQ
```

此时，启动 Gradio 服务的指令变为

```bash
lmdeploy serve gradio /root/lmdeploy_vlm/internlm-xcomposer2-vl-7b-AWQ --model-format awq
```

相应地，`pipeline` 初始化方法变为

```python
pipe = pipeline('/root/lmdeploy_vlm/internlm-xcomposer2-vl-7b-AWQ', model_format='awq')
```

## 4. AWQ 量化算法介绍

LMDeploy 所采用的量化算法为 AWQ（Activation-aware Weight Quantization）算法。

该方法基于“LLM 的权重对于性能并不同等重要”的观点，观察到权重中存在着 0.1%-1% 的显著权重，而跳过这部分显著权重不进行量化，则可以大大减少量化误差。但是将显著权重保留为 FP16 会导致硬件效率低下，所以 AWQ 算法提出了逐通道缩放来减少显著权重的量化误差。

考虑一个权重为 $w$ 的块，线性运算可以写作 $y=\textbf{wx}$ ，量化后即为 $y = Q(\textbf{w})\textbf{x}$ ，其中 $Q(\textbf{w}) = \Delta\cdot\text{Round}\left(\frac{\textbf{w}}{\Delta}\right)，\Delta = \frac{\max(|\textbf{w}|)}{2^{N-1}}$ ，其中 $N$ 为量化比特数， $\Delta$ 是由最大绝对值确定的量化缩放比例。

对于 $w \in \textbf{w}$ ，如果引入缩放因子 $s$ ，得到 $y=Q(\textbf{w})\text{x} = Q(w\cdot s)(x / s)$ ，即 $Q(w\cdot s) \cdot \frac{x}{s} = \Delta' \cdot \text{Round}(\frac{ws}{\Delta'}) \cdot x \cdot \frac{1}{s}$ 。发现 $\Delta = \Delta', s>1$ 的情况下，显著权重 $w$ 的误差较小。

为了同时考虑显著权重和非显著权重，AWQ 算法使用了自动搜索最佳缩放因子的方法，即公式 $s^* = \arg\min_s\mathcal{L}(s), \mathcal{L}(s) = ||Q(\textbf{W}\cdot \text{diag}(s))(\text{diag}(s)^{-1} \cdot \mathbf{X}) - \textbf{WX}||$ 。其中 $Q$ 是权重量化函数， $W$ 是原始权重， $\textbf{X}$ 是从小校准集的输入特征。但是量化函数不可微，所以通过分析影响缩放因子选择的因子，定义了一个搜索空间。由于权重通道的显著性实际上是由激活比例决定的（即激活感知），因此可以选择一个简单的搜索空间： $s = s_{\textbf{X}^\alpha}, \alpha^* = \arg\min_\alpha \mathcal{L}(s_{\textbf{X}^\alpha})$ 。其中 $s$ 仅与激活 $s_{\textbf{X}}$ 的大小有关。

该方法不依赖于任何回归或反向传播过程，而这是许多量化感知训练方法所需的。 AWQ 方法对校准集的依赖最小，因为我们只测量每个通道的平均幅度，从而防止过拟合。因此，该方法在量化过程中需要更少的数据，并且可以将 LLM 的知识保留在校准集分布之外。

**如果公式渲染出现问题，也可查看**<details><summary>公式</summary>

![image](https://github.com/InternLM/Tutorial/assets/75657629/b5b5c9bc-80c8-4ce3-ab43-832273feccfe)

</details>
