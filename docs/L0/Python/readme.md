
# Python

<img width="1440" alt="B站封面" src="https://github.com/user-attachments/assets/97ea0f6e-4645-4bf3-a52b-4a1982663d43">

# **Intro**

欢迎来到书生浦语大模型实战营基础部分Python关卡，本关主要由以下四大块内容组成：

- Conda虚拟环境
- pip安装三方依赖包
- VScode中的Python Debug
- Python基础语法

**学习完成后，完成由两个任务经过助教批改视为闯关成功**。
| 任务类型 | 任务内容 | 预计耗时 |
| --- |---| ---|
|闯关任务|Leetcode 383| 15mins|
|闯关任务|Vscode连接InternStudio debug笔记| 15mins|

任务具体描述见[task.md](./task.md)。

TIPS：本关内容覆盖较多，知识点较杂，如果有不清楚或者不懂的地方可以随时提问。同时如果觉得教程有问题的地方也请随时提出，让我们一起把本教程优化得更好，帮助更多的人走进大模型的世界。

# Ch1 Conda虚拟环境
虚拟环境是Python开发中不可或缺的一部分，它允许你在不同的项目中使用不同版本的库，避免依赖冲突。Conda是一个强大的包管理器和环境管理器。

## 1.1 创建新环境
首先，确保你已经安装了Anaconda或Miniconda。在开发机上已经安装好了conda，大家可以直接使用。创建虚拟环境时我们主要需要设置两个参数，一是虚拟环境的名字，二是python的版本。
```shell
conda create --name myenv python=3.9
```
这将创建一个名为myenv的新环境，使用Python 3.9。
在安装包时会有一步二次确认，填y就行。

## 1.2 环境管理
要使用创建好的虚拟环境，我们需要先激活环境。激活我们刚刚创建的myenv环境的命令如下：
```shell
conda activate myenv
```
如果要退出环境，回到默认环境，命令为
```shell
conda deactivate
```
其他常见的虚拟环境管理命令还有
```shell
#查看当前设备上所有的虚拟环境
conda env list
#查看当前环境中安装了的所有包
conda list
#删除环境（比如要删除myenv）
conda env remove myenv
```
## 1.3 安装虚拟环境到指定目录
有时我们会遇到想将整个虚拟环境保存到制定目录来共享，比如在局域网内，或者在InternStudio的团队开发机间共享。此时我们可以把conda的虚拟环境创建到指定目录下。
只需要在创建环境时使用`--prefix`参数制定环境所在的文件夹即可，比如我们想在/share/envs/路径下创建刚刚我们创建过得myenv。
```shell
conda create --prefix /share/envs/myenv python=3.9
```
其他操作就与直接在默认路径下创建新环境没有区别了。想要激活保存在制定目录下的conda虚拟环境也十分简单，直接将环境名替换成所在文件夹就行。
```shell
conda activate /share/envs/myenv
```
myenv这个文件夹里包含了整个虚拟环境，所以理论上将他直接拷贝到任意一台安装了conda的机器上都能直接激活使用，这也是在内网机器上做环境配置的一种效率较高的解决方案。


# Ch2: 使用pip安装Python三方依赖包
在Python开发中，安装和管理第三方包是日常任务。pip是Python官方的包管理工具，全称为“Python Package Installer”，用于方便地安装、升级和管理Python包。
## 2.1 使用pip安装包
注意在使用conda的时候，我们需要先激活我们要用的虚拟环境，再在激活的虚拟环境中，使用pip来安装包。pip安装包的命令为`pip install`。
```shell
pip install somepackages
#比如我想安装pandas和numpy
pip install pandas numpy
#我们也可以指定安装的版本
pip install numpy==2.0
#除了==外，还可以用>,<,>=,>=来指定一个版本的范围
```

## 2.2 安装requirement.txt
如果你有一个包含所有依赖信息的requirements.txt文件，可以使用`-r`一次性安装所有依赖。requirements.txt在各种开源代码中经常可以看到，里面描述了运行该代码所需要的包和对应版本。
```shell
pip install -r requirements.txt
```
比如以下就是我们接下来会接触到的LLM部署框架lmdeploy的requirements.txt 的一部分（只做展示，大家不用自行安装）
```plain text
accelerate>=0.29.3
mmengine-lite
numpy<2.0.0
openai
peft<=0.11.1
transformers
triton>=2.1.0,<=2.3.1;
```

## 2.3 安装到指定目录
为了节省大家的存储空间，本次实战营的conda环境均放在share目录下，但share目录只有读权限，所以我们不能直接使用pip将包安装到对应环境中，需要将我们额外需要的包安装到我们自己的目录下。
这时我们在使用pip的时候可以使用--target或-t参数来指定安装目录，此时pip会将你需要安装的包安装到你指定的目录下。
这里我们用本次实战营最常用的环境`/root/share/pre_envs/pytorch2.1.2cu12.1`来举例。
```shell
#首先激活环境
conda activate /root/share/pre_envs/pytorch2.1.2cu12.1
#假设我们要安装到/root/your_directory下
pip install somepackage --target /root/your_directory
#注意这里也可以使用-r来安装requirements.txt
pip install -r requirements.txt --target /root/your_directory
```
要使用安装在指定目录的python包，可以在import的时候带上完整的路径+包名
```python
#假设我要引用/root/your_directory下的numpy
import /root/your_directory/numpy
```
或者在python脚本开头临时将该路径加入python环境变量中去
```python
import sys  
  
# 你要添加的目录路径  
your_directory = '/root/your_directory'  
  
# 检查该目录是否已经在 sys.path 中  
if your_directory not in sys.path:  
    # 将目录添加到 sys.path  
    sys.path.append(your_directory)  
  
# 现在你可以直接导入该目录中的模块了  
# 例如：import your_module
```

# Ch3 **使用本地Vscode连接InternStudio开发机**
VSCode是由微软开发一款轻量级但功能强大的代码编辑器，开源且完全免费。它拥有丰富的插件生态系统、跨平台支持、以及内置的Git控制功能，为开发者提供了高效便捷的编码体验。

VScode下载地址：[Visual Studio Code - Code Editing. Redefined](https://code.visualstudio.com/)

首先需要安装Remote-SSH插件

![images](https://github.com/InternLM/Tutorial/assets/32959436/1b494c3e-6be2-4ed7-aa2b-937491568990)


安装完成后进入Remote Explorer,在ssh目录下新建一个ssh链接



![images](https://github.com/InternLM/Tutorial/assets/32959436/81461f5a-d751-4cc9-bc3c-72b326c0dda3)

此时会有弹窗提示输入ssh链接命令，回车后还会让我们选择要更新那个ssh配置文件，默认就选择第一个就行（如果你有其他需要的话也可以新建一个ssh配置文件）。

![images](https://github.com/InternLM/Tutorial/assets/32959436/a1eb2d82-146c-4cf7-910b-79af6118c8c5)

![images](https://github.com/InternLM/Tutorial/assets/32959436/db595bd5-83f5-4cef-b536-ca6c45f6facf)


开发机的链接命令可以在开发机控制台对应开发机"SSH连接"找到，复制登录命令到vscode的弹窗中然后回车，vscode就会开始链接InternStudio的服务器，记得此时切回去复制一下ssh的密码，待会会用到。


![images](https://github.com/InternLM/Tutorial/assets/32959436/cb2bb9eb-7aab-44f4-b73f-5c255c4407d2)

在新的弹窗中将ssh密码粘贴进去然后回车。随后会弹窗让选择远程终端的类型，这边我们的开发机是linux系统，所以选择linux就好。

![images](https://github.com/InternLM/Tutorial/assets/32959436/3d48179a-66d9-44bc-8639-e44df8411d2d)

首次连接会进行一些初始化的设置，可能会比较慢，还请耐心等待。后面打开文件夹的时候可能会再需要输入密码，可以一直开着开发机的控制台不要关掉以备不时之需。


看到左下角远程连接已经显示ssh连接地址`SSH:ssh.intern-ai.org.cn`，说明我们已经连接成功了。然后我们就可以像在本地使用vscode一样愉快的使用vscode在开发机上进行任何操作了。



![images](https://github.com/InternLM/Tutorial/assets/32959436/bd6b7430-8ef5-4841-9e89-5f83faceda57)

连接成功后我们打开远程连接的vscode的extensions，在远程开发机上安装好python的插件，后面python debug会用到。也可以一键把我们本地vscode的插件安装到开发机上。

![images](https://github.com/InternLM/Tutorial/assets/32959436/95759a98-8e12-483e-a188-7572968beeda)

![images](https://github.com/InternLM/Tutorial/assets/32959436/e29ab709-68f1-4e0b-8e8a-93242f524e7b)


### 在Vscode中打开终端


单击vscode页面下方有一个X和！的位置可以快速打开vscode的控制台，然后进入TERMINAL。

![images](https://github.com/InternLM/Tutorial/assets/32959436/d8cd9101-c9d5-4d4f-8e85-9725e399f4b1)


`TIPS`：右上方的+可以新建一个TERMINAL。


4. Debug
4.1 使用VSCode进行Python Debug




# Ch4 使用vscode连接开发机进行python debug

VSCode是由微软开发一款轻量级但功能强大的代码编辑器，开源且完全免费。它拥有丰富的插件生态系统、跨平台支持、以及内置的Git控制功能，为开发者提供了高效便捷的编码体验。

VScode下载地址：[Visual Studio Code - Code Editing. Redefined](https://code.visualstudio.com/)

## 4.1 什么是debug？

当你刚开始学习Python编程时，可能会遇到代码不按预期运行的情况。这时，你就需要用到“debug”了。简单来说，“debug”就是能再程序中设置中断点并支持一行一行地运行代码，观测程序中变量的变化，然后找出并修正代码中的错误。而VSCode提供了一个非常方便的debug工具，可以帮助你更容易地找到和修复错误。


## 4.2 **使用Vscode进行Python debug的流程**

### 4.2.1 debug单个python文件
```python
def range_sum(start,end):
    sum_res = 0
    for i in range(start,end):
        sum_res+=i
    return sum_res

if __name__ =="__main__":
    print(range_sum(1,10))
```

**Step1.安装Python扩展**
  - 打开VSCode，点击左侧扩展栏，搜索Python，并安装。

**Step2配置调试**
  - 打开你的Python文件，点击左侧活动栏的“运行和调试”图标。
  - 首次debug需要配置以下，点击“create a launch.json file”，选择python debugger后选择“Python File” config。

  ![image](https://github.com/user-attachments/assets/af0cc60f-74fa-4168-9da8-31928972b352)

  - 可以直接编辑生成的launch.json文件，配置调试参数，比如添加config（Add Configuration）等。

  ![image](https://github.com/user-attachments/assets/81721718-62c3-495f-874b-31473e73d168)

新建python文件后我们如果想要运行，首先需要选择解释器。单击右下角的select interpreter，vsconde会自动扫描开发机上所有的python环境中的解释器。


**Step3.设置断点**

在代码行号旁边点击，可以添加一个红点，这就是断点（如果不能添加红点需要检查一下python extension是否已经正确安装）。当代码运行到这里时，它会停下来，这样你就可以检查变量的值、执行步骤等。该函数的核心代码在第6行，所以接下来我们在第四行这打上断点。

![images](https://github.com/user-attachments/assets/8561f1cc-9ee6-4c6b-b8d7-552b34881110)

**Step4.启动debug**

点击VSCode侧边栏的“Run and Debug”（运行和调试），选择debug配置后点击绿色箭头（开始调试）按钮，或者按F5键。

![image_debug](https://github.com/user-attachments/assets/97b5e791-2490-4d71-8764-e7aadc5e3d4b)



**Step5.查看变量**

当代码在断点处停下来时，你可以查看和修改变量的值。在“Run and Debug”侧边栏的“Variables”（变量）部分，你可以看到当前作用域内的所有变量及其值。

![images](https://github.com/user-attachments/assets/561a5133-2982-4fdb-8a1d-a6f0ed18b77a)

**Step6.单步执行代码**

你可以使用顶部的debug面板的按钮来单步执行代码。这样，你可以逐行运行代码，并查看每行代码执行后的效果。

![images](https://github.com/user-attachments/assets/5cd847ae-c9f3-4226-9f19-975755b2a770)

debug面板各按钮功能介绍：

* `1`: continue: 继续运行到下一个断点

* `2`: step over：跳过，可以理解为运行当前行代码，不进入具体的函数或者方法。

* `3`: step into: 进入函数或者方法。如果当行代码存在函数或者方法时，进入代码该函数或者方法。如果当行代码没有函数或者方法，则等价于step over。

* `4`: step out：退出函数或者方法, 返回上一层。

* `5`: restart：重新启动debug

* `6`: stop：终止debug

**Step7.修复错误并重新运行**

如果你找到了代码中的错误，可以修复它，然后重新运行debug来确保问题已经被解决。

通过遵循以上步骤，你可以使用VSCode的debug功能来更容易地找到和修复你Python代码中的错误。可以自己编写一个简单的python脚本，并尝试使用debug来更好的理解代码的运行逻辑。记住，debug是编程中非常重要的一部分，所以不要怕花时间在这上面。随着时间的推移，你会变得越来越擅长它！

### 4.2.2 不同的断点
在调试（Debug）过程中，断点（Breakpoint）允许程序员在程序的执行流程中设置暂停点。当程序运行到这些断点时，执行会暂时中断，使得我们可以检查此时程序的状态，包括变量的值、内存的内容等。断点为我们提供了一个观察程序运行细节的机会，从而帮助我们定位和解决程序中的错误或问题。在VSCode中，我们还可以设置条件断点，这样断点只有在满足特定条件时才会触发。

1. 普通断点：在代码行号左侧点击，添加断点。
2. 条件断点：在断点标记上右键，选择条件断点（conditional breakpoint）。Vscode中单个程序常用的条件断点主要有三种类型。
* 1. Expression 表达式：输入一个python表达式，每次触发断点时运行该表达式，当表达式的值为True时vscode会暂停执行。如x==10
* 2. Hit count 触发计数：断点触发计数达到输入值的时候才会暂停运行
* 3. Log Message 记录日志：触发该断点的时候在Debug console中输出指定信息，其实就是logpoint。需要输入要输出的信息，如果要用到表达式的话，可以使用{}将表达式括起来。比如每一次都要记录变量i的值可以写x={i}。

#### 表达式条件断点
比如我们想让代码从i=end-1时停下来，就可以这样设置。
现在断点处右键选择条件断点，或者先建立一个普通断点以后编辑断点。

![images](https://github.com/user-attachments/assets/793f31fa-16dd-46f0-911a-d15801b477e2)

回车保存断点，然后运行debug，可以看到程序在i=9的时候停了下来，此时各变量的值如下

![images](https://github.com/user-attachments/assets/ebab013b-e76b-4bb9-93d0-175f94c3cce3)


#### 触发计数条件断点
如果我们想让sum_res+=i在运行5次后停下来，我们可以在这行设置这样的断点

![images](https://github.com/user-attachments/assets/1dab2877-0835-4a3c-80aa-c1a556d0205d)

运行debug后，程序第一次暂停时各变量的状态为

![images](https://github.com/user-attachments/assets/1ce0000f-50d7-411f-9195-22d05aa507fa)

#### 记录日志条件断点
每次触发时记录一下i的值

![images](https://github.com/user-attachments/assets/673a80e2-de0a-4563-ade5-afeb195b9011)

运行debug后我们可以在debug console看到

![images](https://github.com/user-attachments/assets/fae0204a-e2d9-4ed3-983c-5b4f40e7a6ce)

## 4.3 在vscode使用命令行进行debug

很多时候我们要debug的不止是一个简单的python文件，而是很多参数，参数中不止会有简单的值还可能有错综复杂的文件关系,甚至debug一整个项目。这种情况下，直接使用命令行来发起debug会是一个更好的选择。

### 4.3.1 vscode设置


vscode支持通过remote的方法连接我们在命令行中发起的debug server。首先我们要配置一下debug的config。


还是点击VSCode侧边栏的“Run and Debug”（运行和调试)，单击"create a lauch.json file"

![images](https://github.com/InternLM/Tutorial/assets/32959436/394e773d-56e6-4c86-b136-f781fa8973a4)

选择debugger时选择python debuger。选择debug config时选择remote attach就行，随后会让我们选择debug server的地址，因为我们是在本地debug，所以全都保持默认直接回车就可以了，也就是我们的server地址为localhost:5678。

![images](https://github.com/InternLM/Tutorial/assets/32959436/8caf498a-bdda-4e2d-9623-00bdc42ee478)

![images](https://github.com/InternLM/Tutorial/assets/32959436/0b6f6ed2-b996-4768-b21e-c2668e5f1e6a)

![images](https://github.com/InternLM/Tutorial/assets/32959436/c79749a0-8f8a-4f5d-8c70-4031170acb06)

配置完以后会打开配置的json文件，但这不是重点，可以关掉。这时我们会看到run and debug界面有变化，出现了debug选项。

![images](https://github.com/InternLM/Tutorial/assets/32959436/b6d2c147-60e2-42b5-8bab-66ef450bd214)

### 4.3.2 debug命令行

现在vscode已经准备就绪，让我们来看看如何在命令行中发起debug。如果没有安装debugpy的话可以先通过pip install debugpy安装一下。

```shell
python -m debugpy --listen 5678 --wait-for-client ./myscript.py
```

* `./myscript.py`可以替换为我们想要debug的python文件，后面可以和直接在命令行中启动python一样跟上输入的参数。记得要先在想要debug的python文件打好断点并保存。

* `--wait-for-client`参数会让我们的debug server在等客户端连入后才开始运行debug。在这就是要等到我们在run and debug界面启动debug。

先在终端中发起debug server，然后再去vscode debug页面单击一下绿色箭头开启debug。

![images](https://github.com/InternLM/Tutorial/assets/32959436/ffb37e1f-a52c-4d66-816c-a5299e8cec50)

![images](https://github.com/InternLM/Tutorial/assets/32959436/f6468a4e-7994-470d-9b38-375b3d70b302)

接下来的操作就和上面一样了。

![images](https://github.com/InternLM/Tutorial/assets/32959436/5cf91e9f-4588-41c2-934a-352f92c210a7)

### 4.3.3 使用别名简化命令


这边有个不方便的地方，python -m debugpy --listen 5678 --wait-for-client这个命令太长了，每次都打很麻烦。这里我们可以给这段常用的命令设置一个别名。


在`linux`系统中，可以对 *~/.bashrc* 文件中添加以下命令

```shell
alias pyd='python -m debugpy --wait-for-client --listen 5678'
```

然后执行

```shell
source ~/.bashrc
```

这样之后使用 pyd 命令(你可以自己命名) 替代 python 就能在命令行中起debug了，之前的debug命令就变成了

```shell
pyd ./myscript.py
```


# Ch5: Python基础
本课程也提供一个简易的Python基础教程(内容较多，请前往[ch5_python_intro.md](./ch5_python_intro.md)浏览)。