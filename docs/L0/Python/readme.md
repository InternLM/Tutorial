
# Python关卡
# **Intro**

欢迎来到书生浦语大模型实战营基础部分Python关卡，本关主要由以下四大块内容组成：

- Python(Miniconda)的安装
- Python基础语法
- Numpy基础(选修)
- vscode 远程连接 internstudio开发机打断点调试 python 程序

**学习完成后，完成由两个任务经过助教批改视为闯关成功**。
| 任务类型 | 任务内容 | 预计耗时 |
| --- |---| ---|
|闯关任务|Python实现wordcount| 15mins|
|闯关任务|Vscode连接InternStudio debug笔记| 15mins|

任务具体描述见[task.md](./task.md)。

TIPS：本关内容覆盖较多，知识点较杂，如果有不清楚或者不懂的地方可以随时提问。同时如果觉得教程有问题的地方也请随时提出，让我们一起把本教程优化得更好，帮助更多的人走进大模型的世界。

# Chapter1 如何在自己电脑上安装Python
**TIPS: InternStuido开发机已经为大家准备好了conda环境，不需要再安装。**

这部分是为了给那些想在自己电脑上配置环境来练手的,已经装好了的同学可以跳过哈。

推荐直接安装miniconda(anaconda也可以)来安装python，这样方便管理开发环境。

## 1.1 **什么是conda？**

Conda是一个开源的软件包管理系统和环境管理系统，它主要用于安装多个版本的软件包及其依赖关系，并能轻松地在它们之间切换。以下是关于Conda的详细介绍：

### 1.1.1 **功能与作用**：

- **包管理**：Conda可以帮助用户轻松地安装、更新和卸载各种软件包。它提供了一个庞大而丰富的社区仓库——Anaconda仓库，内含数千个优化过并经过验证的常见Python软件包，也包含其他编程语言（如R）的工具。
- **环境管理**：使用Conda，用户可以创建独立且隔离的开发环境，为每个项目或应用程序设置不同的版本或配置文件，确保它们之间不会相互干扰，对于处理不同的依赖关系非常重要。
- **跨平台支持**：Conda适用于Windows、Mac和Linux，使在不同平台上共享代码变得更加容易，避免由于系统差异导致的问题。

### 1.1.2 **常用命令**：

- `conda list`：列出当前conda环境所链接的软件包。
- `conda create`：创建一个新的conda环境。例如，`conda create -n myenv python=3.8`会创建一个名为myenv的新环境，并指定Python版本为3.8。
- `conda activate`：激活一个已存在的conda环境。
- `conda deactivate`：退出当前激活的环境。
- `conda install`：在当前激活的环境中安装包。
- `conda update`：更新包或conda本身到最新版本。
- `conda remove`：从当前环境中卸载包。
- `conda env list`：显示所有已创建的环境。

### 1.1.3 **适用性**：

Conda不仅为Python程序创建，也可以打包和分发其他软件，并且支持多种编程语言，包括Python、R、Ruby、Lua、Scala、Java、JavaScript、C/C++等。它被广泛用于数据分析、科学计算和机器学习领域，提供了简单而强大的工具来创建、部署和维护这些领域所需的环境。总的来说，Conda是一个在数据分析和软件开发领域非常有用的工具，特别是当需要管理多个项目和不同版本的依赖时，Conda可以大大简化环境和依赖管理的复杂性。

## 1.2 **Python安装与学习环境准备**

如果在本地想搭建python环境练手的话，可以安装miniconda。（开发机已经准备好conda环境，无需重复安装）

### 1.2.1 下载miniconda

miniconda和anaconda都可以通过官网下载，也可以去清华源下载。

清华源miniconda下载链接: [清华大学开源软件镜像站 | Tsinghua Open Source Mirror](https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/)(建议选择python3.9以上的版本，比如Miniconda3-py310_24.5.0)

### 1.2.2 安装miniconda

windows可以通过图形化的安装程序直接完成安装记得在最后一步把miniconda加入环境变量
![20240710205631](https://github.com/InternLM/Tutorial/assets/32959436/708fe415-b109-45b9-be68-7464c1a91aee)

<details>
<summary> 如何换源让pip或conda安装包更快？(在境外的同学可以跳过此步骤)</summary>
python的包管理pip与conda的源服务器均在境外，安装包的时候常常会碰到下载慢的情况。这时我们可以把pip与conda的源替换为国内的镜像，下面我们将刚刚安装好的环境替换为清华源。我们需要进入命令行开始进行换源，Windows可以直接打开miniconda powershell promt。

首先将pip替换为清华源，只需要一条命令。

```
 pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

```

接着我们来给conda替换成清华源。各系统都可以通过修改用户目录下的 `.condarc` 文件来修改镜像源。Windows 用户无法直接创建名为 `.condarc` 的文件，可先执行 `conda config --set show_channel_urls yes` 生成该文件之后再修改。在用户目录找到`.condarc` 文件后，使用文本编辑器打开，将下面的内容复制进去并保存。

```
 channels:   - defaults show_channel_urls: true default_channels:
 - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
 - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
 - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2 custom_channels:
 conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
 msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
 bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
 menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
 pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
 pytorch-lts: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
 simpleitk: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
 deepmodeling: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/

```

接着在命令行中运行 `conda clean -i` 清除索引缓存，保证用的是镜像站提供的索引。
</details>

### 1.2.3 创建一个python练习专属的conda虚拟环境

本次教程会需要用到jupyter和numpy，所以安装完miniconda后我们还需要安装jupyter lab和numpy。

打开miniconda powershell promt或者终端，首先我们先创建一个虚拟环境并用Pip安装jupyter lab和numpy。

```
conda create -n python-tutorial python=3.10
conda activate python-tutorial
pip install jupyter lab
pip install numpy

```

本关卡的示例代码与闯关作业均为notebook(ipynb)格式，你们需要自行去github clone或者直接打包下载。下载好后我们激活环境并启动jupyter lab，然后再notebook中打开教程的两个代码文件。就可以开始本次的学习了。

```
conda activate python-tutorial
jupyter lab
```




# Chapter2: Python基础
<details>
<summary>Python基础教程(内容会比较多)</summary>


## 2.1 Python基础语法


```python
#这是一个单行注释
'''
这是一个多行注释
这是一个多行注释
'''
print("hello world")#从hello world开始认识Python
print(1+1)
print(1+2)
#print函数是Python中用于输出信息到控制台的内置函数。
```

    hello world
    2
    3
    

在python中，代码块不使用{}来表示，而是通过行与缩进来表示，同一个代码块有着相同的缩进。


```python
if True:
    print('hello world!')
    print('hello python!')
else:
    print('goodbye python!')
    print('goodbye world!')
```

    hello world!
    hello python!
    

python标识符(变量名，函数名)命名要求：
* 标识符须要由字母，数字和下划线组成
* 首字符必须是字母或者下划线_
* 标识符对大小写敏感
* 标识符不能与python关键字重名

以下代码可以查看python的关键词（保留字符）


```python
import keyword
print(keyword.kwlist)
```

    ['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']
    

## 2.2 基本数据类型

python基本数据类型:
* 数字Number
    * int整数
    * float浮点数
    * complex复数
* 布尔型bool
* 列表list
* 元组tuple
* 集合set
* 字典Dictionary

可以修改的是：列表list，集合set，字典Dictionary

不可以修改的是：数字Number，布尔型bool，元组tuple


```python
#python中变量赋值的方式
a = 1
b = 2
print(a+b)
a,b = 1,2 #另一种单行赋值的方式
print(1,2)

#下面让我们来看看各种类型的数据长什么样
t_int = 1 #整数
t_float = 1.0 #浮点数
t_complex = 1.2j #复数
t_bool = True #布尔类型
t_list = [1,1,3,3,5,5] #列表
t_tuple = (1,1,3,3,5,5) #元组
t_set = (1,3,5) #集合
t_dict = {'day':18,'month':6,'year':2024} #字典

print(" t_int的类型是：",type(t_int),' t_int的值是: ',t_int)
print(" t_float的类型是：",type(t_float),' t_float的值是: ',t_float)
print(" t_complex的类型是：",type(t_complex),' t_complex的值是: ',t_complex)
print(" t_bool的类型是：",type(t_bool),' t_bool的值是: ',t_bool)
print(" t_list的类型是：",type(t_list),' t_list的值是: ',t_list)
print(" t_tuple的类型是：",type(t_tuple),' t_tuple的值是: ',t_tuple)
print(" t_set的类型是：",type(t_set),' t_set的值是: ',t_set)
print(" t_dict的类型是：",type(t_dict),' t_int的值是: ',t_dict)
```

    3
    1 2
     t_int的类型是： <class 'int'>  t_int的值是:  1
     t_float的类型是： <class 'float'>  t_float的值是:  1.0
     t_complex的类型是： <class 'complex'>  t_complex的值是:  1.2j
     t_bool的类型是： <class 'bool'>  t_bool的值是:  True
     t_list的类型是： <class 'list'>  t_list的值是:  [1, 1, 3, 3, 5, 5]
     t_tuple的类型是： <class 'tuple'>  t_tuple的值是:  (1, 1, 3, 3, 5, 5)
     t_set的类型是： <class 'tuple'>  t_set的值是:  (1, 3, 5)
     t_dict的类型是： <class 'dict'>  t_int的值是:  {'day': 18, 'month': 6, 'year': 2024}
    

## 2.3 运算符
### 2.3.1 算数运算符
| 运算符 | 描述 |
| --- | --- |
| `+` | 加 |
| `-` | 减 |
| `*` | 乘 |
| `/` | 除 |
| `//` | 整除,只保留整数 |
| `%` | 模运算或者取余数除法,只保留余数 |
| `**` | 幂运算 |


```python
print("1+1 =",1+1)
print("2-1 =",2-1)
print("2*4 =",2*4)
print("2*4 =",2*4)
print("8//3 =",8//3)
print("8%5 =",8%5)
print("2**3 =",2**3)
```

    1+1 = 2
    2-1 = 1
    2*4 = 8
    2*4 = 8
    8//3 = 2
    8%5 = 3
    2**3 = 8
    

### 2.3.2 比较运算符
| 运算符 | 描述 |
| --- | --- |
| `>` | 大于 |
| `<` | 小于 |
| `>=` | 大于等于 |
| `<=` | 小于等于 |
| `==` | 等于 |
| `!=` | 不等于 |


```python
a,b = 10,20
print("a>b =",a>b)
print("a<b =",a<b)
print("a>=b =",a>=b)
print("a<=b =",a<=b)
print("a==b =",a==b)
print("a!=b =",a!=b)
```

    a>b = False
    a<b = True
    a>=b = False
    a<=b = True
    a==b = False
    a!=b = True
    

### 2.3.3 赋值运算符
| 运算符 | 描述 | 等价表达 |
| --- | --- | --- |
| `=` | 基础赋值 | |
| `+=` | 加法赋值 | a+=b等价于 a=a+b |
| `-=` | 减法赋值 | a-=b等价于 a=a-b |
| `*=` | 小于等于 | a*=b等价于 a=a*b |
| `/=` | 等于 | a/=b等价于 a=a/b |
| `//=` | 等于 | a//=b等价于 a=a//b |
| `%=` | 等于 | a%=b等价于 a=a%b |
| `**=` | 等于 | a**=b等价于 a=a**b |


```python
a,b = 2,2
a += 1
b = b+1
print("a+=1,a=",a)
print("b=b+1,b=",b)

print("-"*20)
a,b = 2,2
a -= 1
b = b-1
print("a-=1,a=",a)
print("b=b-1,b=",b)

print("-"*20)
a,b = 2,2
a *= 2
b = b*2
print("a*=2,a=",a)
print("b=b*2,b=",b)

print("-"*20)
a,b = 2,2
a /= 2
b = b/2
print("a/=2,a=",a)
print("b=b/2,b=",b)

print("-"*20)
a,b = 2,2
a //= 2
b = b//2
print("a//=2,a=",a)
print("b=b//2,b=",b)

print("-"*20)
a,b = 2,2
a %= 3
b = b%3
print("a%=3,a=",a)
print("b=b%3,b=",b)

print("-"*20)
a,b = 2,2
a %= 3
b = b%3
print("a%=3,a=",a)
print("b=b%3,b=",b)

print("-"*20)
a,b = 2,2
a **= 3
b = b**3
print("a**=3,a=",a)
print("b=b**3,b=",b)
```

    a+=1,a= 3
    b=b+1,b= 3
    --------------------
    a-=1,a= 1
    b=b-1,b= 1
    --------------------
    a*=2,a= 4
    b=b*2,b= 4
    --------------------
    a/=2,a= 1.0
    b=b/2,b= 1.0
    --------------------
    a//=2,a= 1
    b=b//2,b= 1
    --------------------
    a%=3,a= 2
    b=b%3,b= 2
    --------------------
    a%=3,a= 2
    b=b%3,b= 2
    --------------------
    a**=3,a= 8
    b=b**3,b= 8
    

### 2.3.4 逻辑运算符
| 运算符 | 描述 |
| --- | --- |
| `and` | 逻辑与 |
| `or` | 逻辑或 |
| `not` | 逻辑非 |


```python
a,b = True,False
print("a and b =",a and b)
print("a or b =",a and b)
print("not b =",not a)
```

    a and b = False
    a or b = False
    not b = False
    

## 2.4 列表
列表是一个有索引的序列，索引从0开始。

列表式一个有序的可重复元素序列。列表是可变的，列表中的元素可以重复，可以是不同的类型。


列表非常重要，他不仅是python开发中最常用的数据结构，同时也是python序列中最具代表性的一个。 当能够理解列表以后，剩下的其他序列学起来就没有那么困难。

### 2.4.1 列表的创建方法


```python
alist = [1,2,3,4,5,6] #列表使用[]表示，每个元素之间用,隔开
print('alist :',alist)
blist = list("hello world!") #列表也可以使用list()函数将其他可迭代的对象转换为列表，比如字符串。字符串的结构我们会在字符串小节里具体介绍
print('blist :',blist)
```

    alist : [1, 2, 3, 4, 5, 6]
    blist : ['h', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd', '!']
    

### 2.4.2 访问元素的方法，索引与切片 

python中的序列均有正向索引与反向索引，正向索引从0开始表示序列第一个元素，反向索引从-1开始表示
以alist为例子，我们打印出alist中每个元素对于的正向索引与反向索引。


```python
print('elements: ','   '.join([str(i) for i in alist]))
print('正向索引:  ','   '.join([str(i) for i in range(0,len(alist))]))
print('反向索引:  ','  '.join([str(i) for i in range(-len(alist),0)]))#这里的len函数是用来获取列表长度的，后面会具体介绍
```

    elements:  1   2   3   4   5   6
    正向索引:   0   1   2   3   4   5
    反向索引:   -6  -5  -4  -3  -2  -1
    


```python
#取列表第一个元素的两种方式
print('第一个元素: ',alist[0])
print('第一个元素: ',alist[-6])

#取列表最后一个元素的两种方式
print('最后一个元素: ',alist[-1])
print('最后一个元素: ',alist[5])

#修改第二个元素
print('alist[1]=0')
alist[1]=0
print(alist)

#删除第二个元素
del alist[1]
print(alist)
```

    第一个元素:  1
    第一个元素:  1
    最后一个元素:  6
    最后一个元素:  6
    alist[1]=0
    [1, 0, 3, 4, 5, 6]
    [1, 3, 4, 5, 6]
    

列表支持切片操作，即截取列表中的一部分长度的操作。

具体语法为 list_name\[start_index:end_index:step\]。

start_index为起点索引，end_index为终点索引，step为步长。要注意截取的部分为\[start_index,end_index\),也就是不包括end_index。

其中step缺省时默认步长为1，start_index缺省时默认为第一个元素，end_index缺省时默认为最后一个元素。


```python
alist = [1,2,3,4,5,6]
print(alist)

print('获取前三个元素')
print('alist[0:3]: ',alist[0:3])
print('alist[:3]: ',alist[:3])

print('获取第二个到第四个元素（索引1至3）')
print('alist[1:4]: ',alist[1:4])

print('获取最后三个元素')
print('alist[-3:]: ',alist[-3:])

print('获取所有索引为奇数的元素')
print('alist[1::2]: ',alist[1::2])

print('获取所有索引为偶数的元素')
print('alist[::2]: ',alist[::2])
```

    [1, 2, 3, 4, 5, 6]
    获取前三个元素
    alist[0:3]:  [1, 2, 3]
    alist[:3]:  [1, 2, 3]
    获取第二个到第四个元素（索引1至3）
    alist[1:4]:  [2, 3, 4]
    获取最后三个元素
    alist[-3:]:  [4, 5, 6]
    获取所有索引为奇数的元素
    alist[1::2]:  [2, 4, 6]
    获取所有索引为偶数的元素
    alist[::2]:  [1, 3, 5]
    

### 2.4.3 列表运算符
| 运算符 | 描述 |
| --- | --- |
| `+` | 拼接两个列表 |
| `*` | 列表*整数，将列表重复 |
| `in` | 元素是否在列表内|


```python
alist = [1,2,3]
blist = [4,5,6]
print('alist+blist: ',alist+blist)
print('alist*3: ',alist*3)
print('3 in alist: ',3 in alist)
print('4 in alist: ',4 in alist)
```

    alist+blist:  [1, 2, 3, 4, 5, 6]
    alist*3:  [1, 2, 3, 1, 2, 3, 1, 2, 3]
    3 in alist:  True
    4 in alist:  False
    

### 2.4.4 列表函数与方法
| 函数名 | 描述 |
| --- | --- |
| `len()` | 列表长度 |
| `max()` | 列表中的最大值|
| `min()` | 列表中的最小值|

| 方法名 | 描述 |返回值|
| --- | --- | --- |
| `list.append(obj)` | 在列表末尾添加新元素 | 无，原地操作 |
| `list.count(obj)` | 统计一个元素在列表中出现的次数 | 返回该元素出现的次数 |
| `list.extend(seq)` | 将一个序列中的所有元素添加到列表末尾 | 无，原地操作 |
| `list.index(obj)` | 从列表中找出某个值第一个匹配项的索引位置 | 返回索引 |
| `list.insert(index, obj)` | 将元素插入列表中的指定位置 | 无，原地操作 |
| `list.pop([index=-1])` | 移除列表中的一个元素（默认最后一个元素），并且返回该元素的值 | 返回移除的元素值 |
| `list.remove(obj)` | 移除列表中某个值第一个匹配项 | 无，原地操作 |
| `list.reverse()` | 逆向排列列表中的所有元素 | 无，原地操作 |
| `list.sort(key=None,reverse=False)` | 对列表内元素进行排序，默认为升序 | 无，原地操作 |
| `list.clear()` | 清空列表 | 无，原地操作 |
| `list.copy()` | 复制列表 | 复制后的列表 |


```python
alist = [0,1,1,2,3,4,5,6,7,8]
print(len(alist))
print(max(alist))
print(min(alist))
alist.sort(key=None,reverse=False)
alist
```

    10
    8
    0
    




    [0, 1, 1, 2, 3, 4, 5, 6, 7, 8]




```python
alist.append(10)#.append不会返回任何内容，直接在原列表上操作
print(alist)
```

    [0, 1, 1, 2, 3, 4, 5, 6, 7, 8, 10]
    


```python
print('10出现的次数:',alist.count(10))#.count会返回该元素出现的次数平
print('1出现的次数:',alist.count(1))
```

    10出现的次数: 1
    1出现的次数: 2
    


```python
alist.extend([11,12])#.extend不会返回任何内容，直接在原列表上操作
print(alist)
```

    [0, 1, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12]
    


```python
print('1出现的首个索引为',alist.index(1))#.index会返回匹配到的首个元素的索引,即1，而非2
print('2出现的首个索引为',alist.index(2))
```

    1出现的首个索引为 1
    2出现的首个索引为 3
    


```python
alist.insert(1,0)#在索引为1的位置插入一个0，没有返回值
print(alist)
```

    [0, 0, 1, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12]
    


```python
print("移除最后一个元素: ",alist.pop())#移除最后元素，没有返回值
print(alist)
print("移除索引为6的元素: ",alist.pop(6))#移除索引为6的元素，没有返回值
print(alist)
```

    移除最后一个元素:  12
    [0, 0, 1, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11]
    移除索引为6的元素:  4
    [0, 0, 1, 1, 2, 3, 5, 6, 7, 8, 10, 11]
    


```python
alist.remove(11)#删除第一个等于11的元素，但没有返回值
print(alist)
```

    [0, 0, 1, 1, 2, 3, 5, 6, 7, 8, 10]
    


```python
alist.reverse()#逆向排列列表中的所有元素
print(alist)
```

    [10, 8, 7, 6, 5, 3, 2, 1, 1, 0, 0]
    


```python
alist.sort()#将列表中的所有元素按升序排列，没有返回值
print(alist)
alist.sort(reverse=True)#将列表中的所有元素按降序排列，没有返回值
print(alist)
```

    [0, 0, 1, 1, 2, 3, 5, 6, 7, 8, 10]
    [10, 8, 7, 6, 5, 3, 2, 1, 1, 0, 0]
    


```python
#copy和clear我们放到一起讲
#如何备份一个alist?直接=和使用copy的区别？
alist_copy = alist#
print('alist_copy: ',alist_copy)
alist_copy.clear()#清空alist_copy
print('alist_copy: ',alist_copy)
print('alist: ',alist)
```

    alist_copy:  [10, 8, 7, 6, 5, 3, 2, 1, 1, 0, 0]
    alist_copy:  []
    alist:  []
    

alist_copy = alist时并没有新建一个对象，而只是单纯赋值了alist的地址给alist_copy。这会导致我们对变量alist_copy的所有操作本质上都是在操作alist。而当我们使用.copy()方法进行赋值时，会复制alist为一个新的对象，此时对新对象的修改不会影响到alist。


```python
alist = [10, 8, 7, 6, 5, 3, 2, 1, 1, 0, 0]
alist_copy = alist.copy()
print('alist_copy: ',alist_copy)
alist_copy.clear()#清空alist_copy
print('alist_copy: ',alist_copy)
print('alist: ',alist)
```

    alist_copy:  [10, 8, 7, 6, 5, 3, 2, 1, 1, 0, 0]
    alist_copy:  []
    alist:  [10, 8, 7, 6, 5, 3, 2, 1, 1, 0, 0]
    


```python
33.6/100
```




    0.336




```python
49.8/150
```




    0.33199999999999996



## 2.5 元组

元组和列表很相似，但是元组创建后不可修改。

元组使用()来表示，创建元组和列表一样，只要在()内添加元素并用逗号隔开就行。


```python
atuple = (1,2,3)
print(atuple[0])
print(atuple[1:3])#元组的索引与切片与列表一致
```

    1
    (2, 3)
    


```python
#当尝试修改元组内部的元素时，会报错
atuple[1]=2
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    ~\AppData\Local\Temp\ipykernel_13796\2873906481.py in <module>
          1 #当尝试修改元组内部的元素时，会报错
    ----> 2 atuple[1]=2
    

    TypeError: 'tuple' object does not support item assignment


### 2.5.1 元组的运算符
元组的运算符与列表一模一样
| 运算符 | 描述 |
| --- | --- |
| `+` | 拼接两个元组 |
| `*` | 列表*整数，将元组重复 |
| `in` | 元素是否在元组内|


```python
atuple = (1,2,3)
btuple = (4,5,6)
print('alist+blist: ',atuple+btuple)
print('alist*3: ',atuple*3)
print('3 in alist: ',3 in atuple)
print('4 in alist: ',4 in atuple)
```

    alist+blist:  (1, 2, 3, 4, 5, 6)
    alist*3:  (1, 2, 3, 1, 2, 3, 1, 2, 3)
    3 in alist:  True
    4 in alist:  False
    

### 2.5.2 元组的函数
元组支持的函数也与列表一模一样
| 函数名 | 描述 |
| --- | --- |
| `len()` | 列表长度 |
| `max()` | 列表中的最大值|
| `min()` | 列表中的最小值|


```python
atuple = (1,2,3,4)
print(len(atuple))
print(max(atuple))
print(min(atuple))
```

    4
    4
    1
    

## 2.6 集合
集合是无序的不重复的元素序列，支持交集、并集、差集等常见的集合操作。

集合的创建使用{}表示，并用,隔开。注意如果需要创建一个空集合需要使用set()。


```python
#新建一个集合
aset = {1,2,3,4,5}
print('这是一个新集合: ',aset)
```

    这是一个新集合:  {1, 2, 3, 4, 5}
    


```python
#新建一个空集合
aset = set()
print('这是一个空集合: ',aset)
```

    这是一个空集合:  set()
    


```python
#将其他序列转换成集合,注意观察转换前后的变化
alist = [1,1,1,1,2,2,2,2,3,3,3]
print('alist: ',alist)
aset = set(alist)
print('aset: ',aset)
```

    alist:  [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3]
    aset:  {1, 2, 3}
    

### 2.6.1 集合的常用方法
| 方法名称 | 描述 | 返回值 |
| --- | --- | --- |
| add() | 为集合添加元素 | 无返回值，原地操作 |
|clear() |移除集合中的所有元素| 无返回值，原地操作 |
| copy() |拷贝一个集合 | 返回拷贝后新创建的集合 |
| difference() | 返回多个集合的差集 | 返回差集结果 |
| intersection() | 返回集合的交集 |返回交集结果 |
| union() | 返回两个集合的并集 | 返回并集结果 |
| symmetric_difference() | 返回两个集合中不重复的元素集合 | 返回两个集合中不重复的元素集合 |
| isdisjoint() | 判断两个集合是否包含相同的元素 | bool,如果没有返回 True，否则返回 False  |
| issubset() | 判断指定集合是否为该方法参数集合的子集 | bool,如果没有返回 True，否则返回 False  |
| issuperset() | 判断该方法的参数集合是否为指定集合的子集 | bool,如果没有返回 True，否则返回 False  |
| update() | 合并两个集合，传入的参数必须是一个集合 | 无返回值，原地操作 |
| pop() | 随机移除元素 | 返回被移除的元素 |
| remove() | 移除指定元素 | 无返回值，原地操作 |
| discard() | 删除集合中指定的元素 | 无返回值，原地操作 |



```python
aset = {1,2,3}
bset = {3,4,5}
```


```python
print(aset)
aset.add(4)
print(aset)
```

    {1, 2, 3}
    {1, 2, 3, 4}
    


```python
#计算差集
print('aset: ',aset)
print('bset: ',bset)
print('aset.difference(bset) :',aset.difference(bset))
```

    aset:  {1, 2, 3, 4}
    bset:  {3, 4, 5}
    aset.difference(bset) : {1, 2}
    


```python
#计算交集
print('aset: ',aset)
print('bset: ',bset)
print('aset.intersection(bset) :',aset.intersection(bset))
```

    aset:  {1, 2, 3, 4}
    bset:  {3, 4, 5}
    aset.intersection(bset) : {3, 4}
    


```python
#计算并集
print('aset: ',aset)
print('bset: ',bset)
print('aset.union(bset) :',aset.union(bset))
```

    aset:  {1, 2, 3, 4}
    bset:  {3, 4, 5}
    aset.union(bset) : {1, 2, 3, 4, 5}
    


```python
#计算两个集合中不重复的元素集合
print('aset: ',aset)
print('bset: ',bset)
print('aset.symmetric_difference(bset) :',aset.symmetric_difference(bset))
```

    aset:  {1, 2, 3, 4}
    bset:  {3, 4, 5}
    aset.symmetric_difference(bset) : {1, 2, 5}
    


```python
#判断两个集合是否包含相同的元素
print('aset: ',aset)
print('bset: ',bset)
print('aset.isdisjoint(bset) :',aset.isdisjoint(bset))
print('aset.isdisjoint({-1,0}) :',aset.isdisjoint({-1,0}))
```

    aset:  {1, 2, 3, 4}
    bset:  {3, 4, 5}
    aset.isdisjoint(bset) : False
    aset.isdisjoint({-1,0}) : True
    


```python
#判判断指定集合是否为该方法参数集合的子集
print('aset: ',aset)
print('bset: ',bset)
print('aset.issubset(bset) :',aset.issubset(bset))
print('aset.issubset(aset.union(bset)) :',aset.issubset(aset.union(bset)))
```

    aset:  {1, 2, 3, 4}
    bset:  {3, 4, 5}
    aset.issubset(bset) : False
    aset.issubset(aset.union(bset)) : True
    


```python
#判判断指定集合是否为该方法参数集合的超集
print('aset: ',aset)
print('bset: ',bset)
print('aset.issuperset(bset) :',aset.issuperset(bset))
print('aset.issuperset(aset.union(bset)) :',aset.issuperset(aset.union(bset)))
```

    aset:  {1, 2, 3, 4}
    bset:  {3, 4, 5}
    aset.issuperset(bset) : False
    aset.issuperset(aset.union(bset)) : False
    


```python
#合并两个集合
print('aset: ',aset)
print('bset: ',bset)
aset.update(bset)
print('aset.update(bset)后的aset :',aset)
```

    aset:  {1, 2, 3, 4}
    bset:  {3, 4, 5}
    aset.update(bset)后的aset : {1, 2, 3, 4, 5}
    


```python
#使用pop随机删除集合中的一个元素
print('aset: ',aset)
print('aset.pop() :',aset.pop())
print('aset: ', aset)
```

    aset:  {1, 2, 3, 4, 5}
    aset.pop() : 1
    aset:  {2, 3, 4, 5}
    


```python
#使用remove或discard删除集合中的指定的一个元素
bset = {3,4,5}
print('bset: ',bset)
bset.remove(3)
print('bset: ', bset)
bset.discard(4)
print('bset: ', bset)
```

    bset:  {3, 4, 5}
    bset:  {4, 5}
    bset:  {5}
    

## 2.7 字典
字典是一个无序的可以修改的序列，每一个元素都由一对key与value组成，key为对应value的索引。

key不可重复，且需要是不可变对象（可hash），可以是数字，字符串，元组等，但不能是列表。value可以重复

字典的创建可以用dict()或者{key1:value1,key2:value2,...}来创建。还记得在集合中我们提过{}能用于创建空集合，是因为{}创建的是一个空字典


```python
adict = {"list" : [1,2,3],'list2':[1,2,3],'interLM': 'LLM', 1:'summer camp',2:'internLM'}
#访问key为list的元素的值
print("adict['list'] :", adict['list'])
#修改key为list的元素的值
adict['list'] = [3]
print("adict['list'] = [3]后的adict: ",adict)
#删除字典中的元素
del adict['list2']
print(adict)
```

    adict['list'] : [1, 2, 3]
    adict['list'] = [3]后的adict:  {'list': [3], 'list2': [1, 2, 3], 'interLM': 'LLM', 1: 'summer camp', 2: 'internLM'}
    {'list': [3], 'interLM': 'LLM', 1: 'summer camp', 2: 'internLM'}
    


```python
#再来看看{}和dict()创建的空字典
print("dict() ",type(dict()))
print("{} ",type({}))
```

    dict()  <class 'dict'>
    {}  <class 'dict'>
    

### 2.7.1 字典的常用方法

|方法名 | 描述 |
| --- | --- |
| dict.clear() | 删除字典内所有元素 | 
| dict.copy() | 返回一个字典的浅复制 |
| dict.fromkeys() | 创建一个新字典，以序列seq中元素做字典的键，val为字典所有键对应的初始值 |
| dict.get(key, default=None) | 返回指定键的值，如果键不在字典中返回 default 设置的默认值 |
| dict.items() | 返回字典内所有的key value对|
| dict.keys() | 返回所有的key |
| dict.values() | 返回所有的values |
| dict.update(dict2) | 把字典dict2的键/值对更新到dict里 |
| pop(key[,default]) | 删除字典 key（键）所对应的值，返回被删除的值。|

示例代码只会展示字典与列表不同的方法，对于名称与功能与列表相同的方法不再做展


```python
#使用fromkeys创建key为[1,2,3,4]
dict.fromkeys([1,2,3,4],0) 
```




    {1: 0, 2: 0, 3: 0, 4: 0}




```python
#使用get查询值，可以使用default参数设置当key不存在时的返回值
print(adict.get("list",1))
print(adict.get("list3"))
print(adict.get('list3',1))
```

    [3]
    None
    1
    


```python
#使用items获取所有的key value对.是一个序列
print(adict.items())
```

    dict_items([('list', [3]), ('interLM', 'LLM'), (1, 'summer camp'), (2, 'internLM')])
    


```python
#使用items获取所有的key
print(adict.keys())
```

    dict_keys(['list', 'interLM', 1, 2])
    


```python
#使用items获取所有的values
print(adict.values())
```

    dict_values([[3], 'LLM', 'summer camp', 'internLM'])
    

## 2.8 字符串
学习LLM，必然逃不过对字符串的处理。

Python中的字符串使用`"`或者`'`来创建,两者等价，但是`"`会高于`'`。

此外，`'''`可以用来创建包含多行的字符串。

字符串本质上是一个不可变的元素可重复的有序序列，这也是为什么本教程会把字符串放在序列内容的最后一节。


```python
astring = 'InternLM'
bstring = "Intern'LM'"#当字符串内有'时，可以使用"
print(list(astring))
```

    ['I', 'n', 't', 'e', 'r', 'n', 'L', 'M']
    

字符串，本质上就是由字符组成的序列，将其转换为list就能看到他的原始数据结构，所以除了不能修改外，他的索引与切片操作跟列表一模一样。


```python
#获取字符串中第3个元素
print(astring[2])
#获取字符串中倒数第二个元素
print(astring[-2])
#获取字符串中的第二个到第四个字符组成的子串
print(astring[1:4])
```

    t
    L
    nte
    

### 2.8.1 字符串的运算符
| 运算符 | 描述 | 例子 |
| --- | --- | ---|
|`+` | 字符串连接 ||
|`*`| 重复输出字符串 | |
|`in` | 成员运算符  如果字符串中包含给定的字符返回 True| |
|`not in` | 成员运算符如果字符串中不包含给定的字符返回 True|'M' not in a 输出结果 True|

### 2.8.2 字符串的方法

| 方法名 | 功能描述 |
| --- | --- |
| capitalize() | 将字符串的第一个字符转换为大写 |
| center(width, fillchar)|返回一个指定的宽度 width 居中的字符串，fillchar 为填充的字符，默认为空格|
| count(str, beg= 0,end=len(string))|返回 str 在 string 里面出现的次数，如果 beg 或者 end 指定则返回指定范围内str 出现的次数 |
| endswith(suffix, beg=0, end=len(string))|检查字符串是否以 suffix 结束，如果 beg 或者 end 指定则检查指定的范围内是否以 suffix 结束，如果是，返回 True,否则返回 False。|
|expandtabs(tabsize=8)|把字符串 string 中的 tab 符号转为空格，tab 符号默认的空格数是 8 |
| find(str, beg=0, end=len(string)) |检测 str 是否包含在字符串中，如果指定范围 beg 和 end ，则检查是否包含在指定范围内，如果包含返回开始的索引值，否则返回-1|
| index(str, beg=0, end=len(string))|跟find()方法一样，只不过如果str不在字符串中会报一个异常|
| isalnum()|如果字符串至少有一个字符并且所有字符都是字母或数字则返 回 True，否则返回 False|
|isalpha()|如果字符串至少有一个字符并且所有字符都是字母或中文字则返回 True, 否则返回 False|
|isdigit()|如果字符串只包含数字则返回 True 否则返回 False..|
|islower()|如果字符串中包含至少一个区分大小写的字符，并且所有这些(区分大小写的)字符都是小写，则返回 True，否则返回 False|
|isnumeric()|如果字符串中只包含数字字符，则返回 True，否则返回 False|
|isspace()|如果字符串中只包含空白，则返回 True，否则返回 False.|
|istitle()|如果字符串是标题化的(见 title())则返回 True，否则返回 False|
|isupper()|如果字符串中包含至少一个区分大小写的字符，并且所有这些(区分大小写的)字符都是大写，则返回 True，否则返回 False|
|join(seq)|以指定字符串作为分隔符，将 seq 中所有的元素(的字符串表示)合并为一个新的字符串|
| ljust(width[, fillchar])|返回一个原字符串左对齐,并使用 fillchar 填充至长度 width 的新字符串，fillchar 默认为空格。|
|lower()|转换字符串中所有大写字符为小写|
|lstrip()|截掉字符串左边的空格或指定字符|
|maketrans()|创建字符映射的转换表，对于接受两个参数的最简单的调用方式，第一个参数是字符串，表示需要转换的字符，第二个参数也是字符串表示转换的目标。|
|max(str)|返回字符串 str 中最大的字母|
|min(str)|返回字符串 str 中最小的字母|
|replace(old, new [, max])|将字符串中的 old 替换成 new,如果 max 指定，则替换不超过 max 次|
|rfind(str, beg=0,end=len(string))|类似于 find()函数，不过是从右边开始查找.|
|rindex( str, beg=0, end=len(string))|类似于 index()，不过是从右边开始|
|rjust(width,[, fillchar])|返回一个原字符串右对齐,并使用fillchar(默认空格）填充至长度 width 的新字符串|
|rstrip()|删除字符串末尾的空格或指定字符。|
|split(str="", num=string.count(str))|以 str 为分隔符截取字符串，如果 num 有指定值，则仅截取 num+1 个子字符串|
| splitlines([keepends])|按照行('\r', '\r\n', \n')分隔，返回一个包含各行作为元素的列表，如果参数 keepends 为 False，不包含换行符，如果为 True，则保留换行符。|
| startswith(substr, beg=0,end=len(string)) |检查字符串是否是以指定子字符串 substr 开头，是则返回 True，否则返回 False。如果beg 和 end 指定值，则在指定范围内检查。|
| strip([chars]) | 在字符串上执行 lstrip()和 rstrip()|
| swapcase() |将字符串中大写转换为小写，小写转换为大写 |
| title() | 返回"标题化"的字符串,就是说所有单词都是以大写开始，其余字母均为小写 |
| translate(table, deletechars="") |根据 table 给出的表(包含 256 个字符)转换 string 的字符, 要过滤掉的字符放到 deletechars 参数中|
|zfill (width)|返回长度为 width 的字符串，原字符串右对齐，前面填充0|
| isdecimal()| 检查字符串是否只包含十进制字符，如果是返回 true，否则返回 false|

要注意的是，因为字符串是不可修改的对象，所以每个修改字符串的方法都是将修改后的字符串作为一个新对象返回。


```python
#字符串的方法实在太多，在在这里我们只取几个比较常用的方法作为示例。
text = "Success is not final, failure is not fatal: It is the courage to continue that counts."
#首先我们把这句话中所有的字母都转换为小写
text = text.lower()
print(text)
#再用replace把所有的标点符号去掉
text = text.replace(','," ").replace(':'," ").replace('.'," ")
print(text)
#再用split把这句话拆成词组成的列表
word_list = text.split(" ")
print(word_list)
#再用join函数用，把这个列表拼会一个字符串
print(','.join(word_list))
```

    success is not final, failure is not fatal: it is the courage to continue that counts.
    success is not final  failure is not fatal  it is the courage to continue that counts 
    ['success', 'is', 'not', 'final', '', 'failure', 'is', 'not', 'fatal', '', 'it', 'is', 'the', 'courage', 'to', 'continue', 'that', 'counts', '']
    success,is,not,final,,failure,is,not,fatal,,it,is,the,courage,to,continue,that,counts,
    

### 2.8.3 字符串的格式化输出

在做LLM开发时避不开对字符串做格式化输出，即指定一个模板把变量放入模板中。接下来我们介绍两种常见的易于实现复杂格式化输出的方法。

第一种为使用字符串的.format()方法，并在在字符串中需要插入值的地方用{}代替，{}也可以加入变量名，方便赋值。


```python
#我们用字典存储一个学生的信息，假设小明是实战营第二期的
#我们需要在输出的时候将他转化成一句话
#小明在12岁的时候参加了书生浦语实战营第二期, 最终获得了优秀学员。
student = {'name':'小明','age':12,'class':"书生浦语实战营第二期",'grade':'优秀学员'}
string_templet = '{}在{}岁的时候参加了{}，获得了{}。'#做一个模板
print(string_templet.format(student['name'],student['age'],student['class'],student['grade']))
#在模板中没有指定变量名时, .format方法就按照顺序来填入值下面来演示一下加入变量名后会有什么不同
string_templet2 = "{name}在{age}岁的时候参加了{course}，获得了{grade}。"#做一个模板
print(string_templet2.format(grade=student['grade'],name=student['name'],age=student['age'],course=student['class']))
#使用这种变量方法命名时, format就可以忽略format参数中的顺序了,对于一些特别长变量特变多的模板来说更清晰。
```

    小明在12岁的时候参加了书生浦语实战营第二期，获得了优秀学员。
    小明在12岁的时候参加了书生浦语实战营第二期，获得了优秀学员。
    

第二种方法我们使用python在3.6推出的f-sting功能，只需在字符串开头加上f，该字符串中的{}中的python代码就会被评估。


```python
student = {'name':'小明','age':12,'class':"书生浦语实战营第二期",'grade':'优秀学员'}
string_out = f"{student['name']}在{student['age']}岁的时候参加了{student['class']}，获得了{student['grade']}。"
print(string_out)
print(f"{1+2}")
```

    小明在12岁的时候参加了书生浦语实战营第二期，获得了优秀学员。
    3
    

## 2.9 控制结构

python中的if语句为:

```python
if condition_1:
    statement_block_1
elif condition_2:
    statement_block_2
else:
    statement_block_3
```

* 如果 "condition_1" 为 True 将执行 "statement_block_1" 块语句
* 如果 "condition_1" 为False，将判断 "condition_2"
* 如果"condition_2" 为 True 将执行 "statement_block_2" 块语句
* 如果 "condition_2" 为False，将执行"statement_block_3"块语句


接下来我们用if语句完成一个成绩等级判定的功能:
* [90,100] A
* [80,90) B
* [70,80) C
* [60,70) D
* [0,60) F


```python
score = 80
if score>=90:
    print('A')
elif score>=80:
    print('B')
elif score>=70:
    print('C')
elif score>=60:
    print('D')
else:
    print('F')
```

    B
    

## 2.10 循环

### 2.10.1 while语句

Python while循环语句语法
```python
while condition:
    statement
```

以上是while语句的形式，当condition为True时，while会执行statement然后再判断condition，直至condition变为False才会结束循环


```python
#用while语句求100以内数字的和
i=0
res = 0
while i<100:
    res+=i
    i+=1
print(res)
```

    4950
    

### 2.10.2 for 语句

Python中for语句的语法为
```python
for <variable> in <sequence>:
    <statements>
else:
    <statements>
```

for循环可以遍历任何可迭代的对象，比如一个列表。


```python
for st in ['InternLM','LLM','transformer','Shanghai']:
    print(st)
```

    InternLM
    LLM
    transformer
    Shanghai
    

提到for循环就不能不提经常与它一起出现的range(start,stop,step)函数，他会生成一个可迭代的对象，以step步长生成[start,stop)。可以只写一个stop，默认从0开始。


```python
for i in range(5):
    print(i)
```

    0
    1
    2
    3
    4
    

### 2.10.3 列表推导式


```python
#列表推导式是一种很方便的写法，但我们在这不作为重点，大家可以看着例子应该就能理解列表推导式的写法
#找出1-100内能被3整除的数
print([i for i in range(1,101) if i%3==0])
```

    [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 78, 81, 84, 87, 90, 93, 96, 99]
    

## 2.11 函数
### 2.11.1 函数的定义方式
python定义函数的关键字为def

```python
def 函数名（参数列表）:
    函数体
```


```python
#定义一个打招呼的函数,别忘了冒号
def hello(name):
    out = 'Hello '+name
    print(out)
```


```python
hello('InternLM2')
```

    Hello InternLM2
    


```python
#注意，函数中定义的变量为局部变量，只有函数内能访问到，这就是变量的作用领域
print(out)
#当我们尝试使用变量out时就会报错，提示out没有被定义
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    ~\AppData\Local\Temp\ipykernel_13796\2663579863.py in <module>
          1 #注意，函数中定义的变量为局部变量，只有函数内能访问到，这就是变量的作用领域
    ----> 2 print(out)
          3 #当我们尝试使用变量out时就会报错，提示out没有被定义
    

    NameError: name 'out' is not defined


### 2.11.2 函数的参数传递

* 参数是可变对象时，传参时传递的是索引，在函数中修改该参数会作用于原对象
* 参数是不可变对象时，传参时会自动复制，在函数中修改该参数不会作用于原对象


```python
def update(number,alist):
    number = 3
    alist[1] = 3
    print("number: ", number)
    print("alist: ", alist)
    print("id(number)",id(number))
    print("id(alist)",id(alist))
a = 2
b = [1,1,1]
print(id(a))
print(id(b))
update(a,b)
```

    140710873047488
    2531815942344
    number:  3
    alist:  [1, 3, 1]
    id(number) 140710873047520
    id(alist) 2531815942344
    

可以看到在update函数内修改了number和alist，函数外面的整数a没有被修改，但是列表b被修改了。
这就是python函数在传参时候的特征导致的。通过使用id()函数可以获取对象在内存中的地址。
可以看到number与a的id不同，他们是两个对象了。但是alist与b的id相同，说明他们两在内存中指向的是同一个对象。
</details>

# Chapter3: Numpy基础(选修)
<details>
<summary>Numpy入门教程</summary>
NumPy是Python中一个强大的科学计算库，它提供了高性能的多维数组对象及这些数组的操作工具。使用NumPy，你可以轻松地进行数学和科学计算，比如线性代数、矩阵运算以及统计分布等，是数据分析和机器学习等领域的基石。Numpy array的操作与Pytorch的Tensor十分相似，了解了array对以后学习pytorch帮助很大。

numpy的安装可以在终端中输入:
```shell
pip install numpy
```
或者直接在notebook中运行
```shell
!pip install numpy
```
TIPS: notebook中加上！可以直接在终端中运行终端命令

## 3.1 numpy Ndarry和创建数组的方式

NumPy数组（ndarray）是NumPy库的核心数据结构，它是一系列同类型数据的集合，以 0 下标为开始进行集合中元素的索引。

ndarray本质上是一个存放同类型元素的多维数组，其中的每个元素在内存中都有相同存储大小的区域。

NumPy数组（ndarray）的特点：

1. **高效的内存使用**：ndarray对象在内存中连续存储，这使得对数组的元素进行切片和迭代等操作非常快速，而不需要额外的内存开销。

2. **快速执行**：NumPy数组的操作是在编译后的代码中执行的，这使得NumPy操作比纯Python代码快得多。

3. **方便易用**：NumPy提供了大量数学和数值计算函数，使得数组操作非常方便。

4. **灵活性**：NumPy数组可以在不同的数据类型之间灵活转换，支持整数、浮点数、复数等多种数据类型。

python中导入第三方包的关键词为 import, 可以用as给包取别名。导入numpy的语句如下所示，numpy的简称一般为np。

```python
import numpy as np
```
创建numpy数组最常见的方法就是将一个列表使用np.array()函数转成ndarray。

TIPS:在notebook中将光标移动到函数的括号中间，按下shift+tab可以看到函数的提示


```python
import numpy as np
array1 = np.array([1,2,3,4,5])
#np.array函数全部的参数有
#np.array(object, dtype=None, *, copy=True, order='K', subok=False, ndmin=0,like=None)
#具体可以尝试上面提到的查看函数提示的方法或者去看numpy的文档
#dtype参数表示array中元素的类型，这个参数在numpy中很常见。
print('array1: \n',array1)
array2 = np.array([[1,2],[3,4]])
print('array2: \n ',array2)
```

    array1: 
     [1 2 3 4 5]
    array2: 
      [[1 2]
     [3 4]]
    


```python
#array常用属性
#查看array数据类型
print("array1.dtype : ",array1.dtype)
#查看数组的维度
print("array1.ndim : ",array1.ndim)
print("array2.ndim : ",array2.ndim)
#查看array的形状
print("array1.shape : ",array1.shape)
print("array2.shape : ",array2.shape)
#查看array中的元素总个数
print("array2.size : ",array2.size)
```

    array1.dtype :  int32
    array1.ndim :  1
    array2.ndim :  2
    array1.shape :  (5,)
    array2.shape :  (2, 2)
    array2.size :  4
    

Numpy还有其他很方便的创建元素值相同的数组的函数：
* np.empty(shape,dtype)创建一个指定形状（shape）、数据类型（dtype）且未初始化的数组
* np.zeros(shape,dtype)创建指定形状（shape），数组元素以 0 来填充
* np.ones(shape,dtype)创建指定形状（shape），数组元素以 1 来填充
* np.zeros_like(array,dtype)创建一个与给定数组具有相同形状的数组，数组元素以 0 来填充
* np.ones_like(array,dtype)创建一个与给定数组具有相同形状的数组，数组元素以 1 来填充

TIPS: 所有dtypes都是可选参数


```python
print("np.empty((2,2))\n",np.empty((2,2)))
#empty创建的数组中所有元素都是未初始化的，但其对应的内存地址可能本来就有值
#所以使用empty创建的数据里面有一些奇怪的数字是正常的
print("np.zeros((2,2))\n",np.zeros((2,2)))
array2 = np.array([[1,2],[3,4]])
print('array2: \n ',array2)
print("np.ones_like(array2)\n",np.ones_like(array2))
```

    np.empty((2,2))
     [[0. 0.]
     [0. 0.]]
    np.zeros((2,2))
     [[0. 0.]
     [0. 0.]]
    array2: 
      [[1 2]
     [3 4]]
    np.ones_like(array2)
     [[1 1]
     [1 1]]
    

### 3.1.2 从数值范围创建数组
也许你还记得在python for循环中我们提到的range(start,stop,step)函数，他能生成一个迭代器。Numpy也有类似的函数，能够直接生成一个数组。

np.arange(start, stop, step, dtype)，他的使用方法与range()一模一样。


```python
print("np.arange(20)\n",np.arange(20))
print("np.arange(1,20,2)\n",np.arange(1,20,2))
```

    np.arange(20)
     [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19]
    np.arange(1,20,2)
     [ 1  3  5  7  9 11 13 15 17 19]
    

此外，numpy还提供一个构建等差数列的函数，只需要设定start和stop，以及要生成的等步长样本数量Num。

np.linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None)

* start	序列的起始值
* stop	序列的终止值，如果endpoint为true，该值包含于数列中
* num	要生成的等步长的样本数量，默认为50
* endpoint	该值为 true 时，数列中包含stop值，反之不包含，默认是True。
* retstep	如果为 True 时，生成的数组中会显示间距，反之不显示。
* dtype	ndarray 的数据类型


```python
print("np.linspace(1,100,50)\n",np.linspace(0,100,30))
```

    np.linspace(1,100,50)
     [  0.           3.44827586   6.89655172  10.34482759  13.79310345
      17.24137931  20.68965517  24.13793103  27.5862069   31.03448276
      34.48275862  37.93103448  41.37931034  44.82758621  48.27586207
      51.72413793  55.17241379  58.62068966  62.06896552  65.51724138
      68.96551724  72.4137931   75.86206897  79.31034483  82.75862069
      86.20689655  89.65517241  93.10344828  96.55172414 100.        ]
    

## 3.2 数组操作

### 3.2.1 数组运算与广播机制

numpy array之前的运算均为元素位置一一对应进行计算，需要两个数组维数相同，且各维度的长度也相同。此外，numpy的广播机制还可以把该条件放宽到两个数组在某个维度上的长度相同即。


```python
array1 = np.array([[1,2,3],[4,5,6]])
array2 = np.array([[2,4,6],[3,5,7]])
print('array1 :\n',array1)
print('array2 :\n', array2)
print('array1+array2:\n',array1+array2)
print('array1*array2:\n',array1*array2)
```

    array1 :
     [[1 2 3]
     [4 5 6]]
    array2 :
     [[2 4 6]
     [3 5 7]]
    array1+array2:
     [[ 3  6  9]
     [ 7 10 13]]
    array1*array2:
     [[ 2  8 18]
     [12 25 42]]
    

### 3.2.2 广播机制

NumPy的广播机制是NumPy库中一个非常强大的功能，它允许我们对形状不完全相同的数组进行算术运算。在广播过程中，NumPy会自动调整数组的形状，以便它们可以在元素级别上进行运算。这种机制使得NumPy在进行数组操作时更加灵活和高效。

#### 广播的基本规则

1. **规则一：维度对齐**
   - 如果两个数组的维度数不同，较小的数组会在其前面补1，直到两个数组的维度数相同。
   - 维度对齐后，从最后一个维度（也称为“后缘维度”）开始比较两个数组的形状。

2. **规则二：兼容维度**
   - 如果两个数组在某个维度上的大小相同，或者其中一个数组在该维度上的大小为1，则这两个数组在该维度上是兼容的。
   - 如果两个数组在所有维度上都是兼容的，那么它们就可以进行广播。

3. **规则三：输出形状**
   - 广播后的输出数组的形状是输入数组形状在各个维度上的最大值。

假设我们有两个数组`a`和`b`，我们想要对它们进行加法运算。


```python
import numpy as np

a = np.array([1, 2, 3])  # 形状为 (3,)
b = np.array([[1], [2], [3]])  # 形状为 (3, 1)

# 使用广播机制进行加法运算
result = a + b
print(result)  # 输出: [[2, 3, 4], [3, 4, 5], [4, 5, 6]]
```

    [[2 3 4]
     [3 4 5]
     [4 5 6]]
    

- 在这个例子中，`a`的形状是`(3,)`，而`b`的形状是`(3, 1)`。
- 根据广播规则一，`a`的形状在逻辑上被扩展为`(1, 3)`，以便与`b`的形状`(3, 1)`对齐。
- 然后，根据规则二，两个数组在所有维度上都是兼容的，因为`a`在第一个维度上的大小为1（逻辑上扩展的），而`b`在该维度上的大小为3；同时，在第二个维度上，两者的大小都是3（或1，对于`a`来说）。
- 因此，可以进行广播，加法运算在元素级别上进行。
- 结果数组`result`的形状是`(3, 3)`，这是两个输入数组形状在各个维度上的最大值。


如果我们不使用NumPy的广播机制，而是手动模拟这一过程，我们可以这样做：



```python
# 手动模拟广播机制
a = np.array([1, 2, 3])  # 形状为 (3,)
b = np.array([[1], [2], [3]])  # 形状为 (3, 1)
print('a\n',a)
print('b\n',b)

a = np.expand_dims(a,0)
#先让两边维数相等
print('\na的形状在逻辑上被扩展为(1,3),a为\n',a)
print('此时a与b的形状为: a {},b {}'.format(a.shape,b.shape))
#此时a与b的形状为: a (1, 3),b (3, 1)
#a会在第0轴上重复三次变成(3,3)
a_broadcast = np.repeat(a,3,0)
#a会在第1轴上重复三次变成(3,3)
b_broadcast =np.repeat(b,3,1)
print('\n广播后的a_broadcast为\n',a_broadcast)
print('广播后的b_broadcast为\n',b_broadcast)
print('\na+b经过广播后就是a_broadcast+b_broadcast\n',a_broadcast+b_broadcast)
```

    a
     [1 2 3]
    b
     [[1]
     [2]
     [3]]
    
    a的形状在逻辑上被扩展为(1,3),a为
     [[1 2 3]]
    此时a与b的形状为: a (1, 3),b (3, 1)
    
    广播后的a_broadcast为
     [[1 2 3]
     [1 2 3]
     [1 2 3]]
    广播后的b_broadcast为
     [[1 1 1]
     [2 2 2]
     [3 3 3]]
    
    a+b经过广播后就是a_broadcast+b_broadcast
     [[2 3 4]
     [3 4 5]
     [4 5 6]]
    

### 3.2.2 修改数组形状
ndarray.reshape(newshape, order='C')不改变数据的条件下修改形状
* newshape：整数或者整数数组，新的形状应当兼容原有形状
* order：'C' -- 按行，'F' -- 按列，'A' -- 原顺序，'k' -- 元素在内存中的出现顺序。

返回修改好形状的数组，并不直接对原数组进行修改


```python
array1 = np.array([[1,2,3],[4,5,6]])
print('array1 :\n',array1)
print('array1.reshape((3,2)) :\n',array1.reshape((3,2)))
print('array1.reshape((6,1)) :\n',array1.reshape((6,1)))
```

    array1 :
     [[1 2 3]
     [4 5 6]]
    array1.reshape((3,2)) :
     [[1 2]
     [3 4]
     [5 6]]
    array1.reshape((6,1)) :
     [[1]
     [2]
     [3]
     [4]
     [5]
     [6]]
    

ndarray.flatten(order='C')将数组展平成一维数组
* order：'C' -- 按行，'F' -- 按列，'A' -- 原顺序，'K' -- 元素在内存中的出现顺序。


```python
array1 = np.array([[1,2,3],[4,5,6],[7,8,9]])
print('array1 :\n',array1)
print('array1.flatten():\n',array1.flatten())
```

    array1 :
     [[1 2 3]
     [4 5 6]
     [7 8 9]]
    array1.flatten():
     [1 2 3 4 5 6 7 8 9]
    

### 3.2.3 翻转数组
对于二维数组就是转置，但对于更高维的数组可以指定axes列表来确定维度的变化。原始数组的维度[0,1,2],可以指定axes为[0,2,1]从而将最后一维放到中间。


```python
array1 = np.array([[1,2,3],[4,5,6]])
print('array1.traspose() 等价于array1.transpose([1,0]) \n'\
        ,array1.transpose())
```

    array1.traspose() 等价于array1.transpose([1,0]) 
     [[1 4]
     [2 5]
     [3 6]]
    

### 3.2.4 修改数组的维度
numpy有两个常用的修改数组维度的函数，一个用于增加维度一个用于减少维度。修改数组维度经常会在进行高维tesnor计算时用于对其维数用到，经过增加一维或者减少一维数来实现。
numpy.expand_dims(arr, axis)通过在指定位置插入新的轴来扩展数组形状
* arr：输入数组
* axis：新轴插入的位置


```python
array1 = np.array([[1,2,3],[4,5,6]])
print('array1\n',array1)
print('array1.shape\n',array1.shape)
array2 = np.expand_dims(array1,0)
print('array2\n',array2)
print('array2.shape\n',array2.shape)
array3 = np.expand_dims(array1,1)
print('array3\n',array3)
print('array3.shape\n',array3.shape)
```

    array1
     [[1 2 3]
     [4 5 6]]
    array1.shape
     (2, 3)
    array2
     [[[1 2 3]
      [4 5 6]]]
    array2.shape
     (1, 2, 3)
    array3
     [[[1 2 3]]
    
     [[4 5 6]]]
    array3.shape
     (2, 1, 3)
    

numpy.squeeze(arr, axis)从给定数组的形状中删除一维的条目
* arr：输入数组
* axis：整数或整数元组，用于选择形状中一维条目的子集


```python
array2 = np.expand_dims(array1,0)
print('array2\n',array2)
print('array2.shape\n',array2.shape)
array4 = np.squeeze(array2)
print('array4=np.squeeze(array2)\n',array4)
print('array4.shape\n',array4.shape)

array3 = np.expand_dims(array1,1)
print('array3\n',array3)
print('array3.shape\n',array3.shape)
array5 = np.squeeze(array3)
print('array5=np.squeeze(array3)\n',array5)
print('array5.shape\n',array5.shape)
```

    array2
     [[[1 2 3]
      [4 5 6]]]
    array2.shape
     (1, 2, 3)
    array4=np.squeeze(array2)
     [[1 2 3]
     [4 5 6]]
    array4.shape
     (2, 3)
    array3
     [[[1 2 3]]
    
     [[4 5 6]]]
    array3.shape
     (2, 1, 3)
    array5=np.squeeze(array3)
     [[1 2 3]
     [4 5 6]]
    array5.shape
     (2, 3)
    

### 3.2.5 拼接数组
numpy有四种拼接数组的函数:

numpy.concatenate(arrays,axis)沿指定轴连接相同形状的两个或多个数组
* arrays：(a1,a2,a3...)相同类型的数组
* axis：沿着它连接数组的轴，默认为 0
  
numpy.stack(arrays, axis)沿新轴连接数组序列
* arrays相同形状的数组序列
* axis：返回数组中的轴，输入数组沿着它来堆叠
  
numpy.hstack(arrays) np.concatenate的特殊情况，相当于axis=1，通过水平堆叠来生成数组

numpy.vstack(arrays) np.concatenate的特殊情况，相当于axis=0，通过垂直堆叠来生成数组

所有用于拼接的数组在拼接的轴上长度必须相同


```python
array1 = np.array([[1,2,3],[4,5,6]])
array2 = np.array([[2,4,6],[3,5,7]])
print("np.concatenate((array1,array2),0)\n",np.concatenate((array1,array2),0))
print("np.concatenate((array1,array2),1)\n",np.concatenate((array1,array2),1))

print("np.stack((array1,array2),0)\n",np.stack((array1,array2),0))
print("np.stack((array1,array2),1)\n",np.stack((array1,array2),1))

print("np.hstack((array1,array2))\n",np.hstack((array1,array2)))
print("np.vstack((array1,array2),1)\n",np.vstack((array1,array2)))
```

    np.concatenate((array1,array2),0)
     [[1 2 3]
     [4 5 6]
     [2 4 6]
     [3 5 7]]
    np.concatenate((array1,array2),1)
     [[1 2 3 2 4 6]
     [4 5 6 3 5 7]]
    np.stack((array1,array2),0)
     [[[1 2 3]
      [4 5 6]]
    
     [[2 4 6]
      [3 5 7]]]
    np.stack((array1,array2),1)
     [[[1 2 3]
      [2 4 6]]
    
     [[4 5 6]
      [3 5 7]]]
    np.hstack((array1,array2))
     [[1 2 3 2 4 6]
     [4 5 6 3 5 7]]
    np.vstack((array1,array2),1)
     [[1 2 3]
     [4 5 6]
     [2 4 6]
     [3 5 7]]
    

### 3.2.6 索引与切片
numpy数据一样有索引与切片，只是其索引的写法与嵌套列表可能会有一点点不一样。

numpy的索引用[]表示，用,隔开每个轴上的索引，比如对于一个二位数组要取第i行第j列的元素的索引就为[i,j]

在索引切片上numpy数组依旧遵循start\:stop:step格式，在每个轴上的切片用,隔开。:或者...可以表示取整个轴上的全部元素。


```python
array1 = np.array([[1,2,3],[4,5,6],[7,8,9]])
print()
print("取array1第1行第3个元素，array1[0,2]=",array1[0,2])
print("取array1第1行前两个元素，array1[0,:2]=",array1[0,:2])
print("取array1每一行前两个元素，array1[0,:2]=\n",array1[...,:2])
```

    
    取array1第1行第3个元素，array1[0,2]= 3
    取array1第1行前两个元素，array1[0,:2]= [1 2]
    取array1每一行前两个元素，array1[0,:2]=
     [[1 2]
     [4 5]
     [7 8]]
    

## 3.3 排序条件筛选

ndarray.sort(axis=-1, kind=None, order=None)
* axis: 沿着它排序数组的轴，如果没有数组会被展开，沿着最后的轴排序， axis=0 按列排序，axis=1 按行排序
* kind: 默认为'quicksort'（快速排序）
* order: 如果数组包含字段，则是要排序的字段


```python
array1 = np.random.randint(1,10,(3,4))
print('array1',array1)
array1.sort(axis=0)
print('对列内数字进行排序,array1.sort(axis=0)\n',array1)
array1.sort(axis=1)
print('对行内数字进行排序,array1.sort(axis=1)\n',array1)
```

    array1 [[7 3 7 6]
     [8 9 3 2]
     [9 9 2 2]]
    对列内数字进行排序,array1.sort(axis=0)
     [[7 3 2 2]
     [8 9 3 2]
     [9 9 7 6]]
    对行内数字进行排序,array1.sort(axis=1)
     [[2 2 3 7]
     [2 3 8 9]
     [6 7 9 9]]
    

ndarray.argmax(axis)与ndarray.argmin(axis)是求数组对应轴上最大或者最小的元素的索引。


```python
array1 = np.random.randint(1,10,(3,4))
print('array1',array1)
print('求每一列最大元素的索引,array1.argmax(axis=0)\n',array1.argmax(axis=0))
print('求每一行最大元素的索引,array1.argmax(axis=1)\n',array1.argmax(axis=1))
```

    array1 [[6 7 8 9]
     [7 2 9 2]
     [6 7 3 4]]
    求每一列最大元素的索引,array1.argmax(axis=0)
     [1 0 1 0]
    求每一行最大元素的索引,array1.argmax(axis=1)
     [3 2 1]
    

numpy数组也支持比较运算，运算结果为bool numpy数组。可以使用np.where()获取其中为ture的元素的索引。


```python
array1 = np.random.randint(1,10,(3,4))
print('array1',array1)
np.where(array1>1)
```

    array1 [[2 7 7 7]
     [8 1 3 1]
     [1 2 2 9]]
    




    (array([0, 0, 0, 0, 1, 1, 2, 2, 2], dtype=int64),
     array([0, 1, 2, 3, 0, 2, 1, 2, 3], dtype=int64))



## 3.6 数学函数
numpy内置了非常多的数学函数，可以直接应用于numpy数组对每一个元素做映射。

常见的函数有np.sin(),np.cos(),np.tan(),np.log()等。

此外，还有np.mean(),np.median(),np.std()等统计函数。

对于取整函数，numpy有np.round()按小数位数四舍五入,np.ceil()向上取整,np.floor()向下取整

## 3.7 线性代数
Numpy的核心就是高性能的矩阵运算，它还提供了线性代数计算包linalg。这里只展示二维数组常用的方法，numpy能做的远远不止这些。


```python
array1 = np.random.randint(1,10,(3,4))
array2 = np.random.randint(1,10,(3,4))
print('array1 \n',array1)
print('array2 \n',array2)
#计算两个矩阵的乘法
print("array1.dot(array2.transpose()):",array1.dot(array2.transpose()))
```

    array1 
     [[1 5 5 9]
     [1 9 1 2]
     [7 2 1 8]]
    array2 
     [[5 1 9 9]
     [8 4 8 6]
     [8 4 2 9]]
    array1.dot(array2.transpose()): [[136 122 119]
     [ 41  64  64]
     [118 120 138]]
    

常用线性代数计算函数
* np.linalg.det() 数组的行列式
* np.linalg.inv() 计算矩阵的乘法逆矩阵
* np.linalg.solve() 求解线性方程



```python
array1 = np.random.randint(1,10,(3,3))
print('array1 \n',array1)
print('array1的行列式: ',np.linalg.det(array1))
```

    array1 
     [[2 7 1]
     [4 5 1]
     [5 3 6]]
    array1的行列式:  -92.00000000000001
    


```python
array1 = np.random.randint(1,10,(3,3))
print('array1 \n',array1)
array1_inv=np.linalg.inv(array1)
print('array1的乘法逆矩阵array1_inv: ',array1_inv)
print('array1.dot(array1_inv)\n',array1.dot(array1_inv))
```

    array1 
     [[4 5 4]
     [8 1 6]
     [5 4 5]]
    array1的乘法逆矩阵array1_inv:  [[ 1.05555556  0.5        -1.44444444]
     [ 0.55555556  0.         -0.44444444]
     [-1.5        -0.5         2.        ]]
    array1.dot(array1_inv)
     [[1. 0. 0.]
     [0. 1. 0.]
     [0. 0. 1.]]
    

求解方程组:

$\begin{cases}
x + y = 5, \\
2x - y = 1.
\end{cases}$



```python
A = np.array([[1, 1],  
              [2, -1]])  
b = np.array([5, 1])  
  
x = np.linalg.solve(A, b)  
  
print(x)
```

    [2. 3.]
    

</details>

# Chapter4 使用vscode连接开发机进行python debug

VSCode是由微软开发一款轻量级但功能强大的代码编辑器，开源且完全免费。它拥有丰富的插件生态系统、跨平台支持、以及内置的Git控制功能，为开发者提供了高效便捷的编码体验。

VScode下载地址：[Visual Studio Code - Code Editing. Redefined](https://code.visualstudio.com/)

## 4.1 什么是debug？

当你刚开始学习Python编程时，可能会遇到代码不按预期运行的情况。这时，你就需要用到“debug”了。简单来说，“debug”就是能再程序中设置中断点并支持一行一行地运行代码，观测程序中变量的变化，然后找出并修正代码中的错误。而VSCode提供了一个非常方便的debug工具，可以帮助你更容易地找到和修复错误。

## 4.2 **使用本地Vscode连接InternStudio开发机**

首先需要安装Remote-SSH插件

![images](https://github.com/InternLM/Tutorial/assets/32959436/1b494c3e-6be2-4ed7-aa2b-937491568990)

安装完成后进入remot explorer,在ssh目录下新建一个ssh链接

![images](https://github.com/InternLM/Tutorial/assets/32959436/81461f5a-d751-4cc9-bc3c-72b326c0dda3)

此时会有弹窗提示输入ssh链接命令，回车后还会让我们选择要更新那个ssh配置文件，默认就选择第一个就行（如果你有其他需要的话也可以新建一个ssh配置文件）。

![images](https://github.com/InternLM/Tutorial/assets/32959436/a1eb2d82-146c-4cf7-910b-79af6118c8c5)

![images](https://github.com/InternLM/Tutorial/assets/32959436/db595bd5-83f5-4cef-b536-ca6c45f6facf)

开发机的链接命令可以在开发机控制台对应开发机"SSH连接"找到，复制登录命令到vscode的弹窗中然后回车，vscode就会开始链接interstudio的服务器，记得此时切回去复制一下ssh的密码，待会会用到。

![images](https://github.com/InternLM/Tutorial/assets/32959436/cb2bb9eb-7aab-44f4-b73f-5c255c4407d2)

在新的弹窗中将ssh密码粘贴进去然后回车。随后会弹窗让选择远程终端的类型，这边我们的开发机是linux系统，所以选择linux就好。

![images](https://github.com/InternLM/Tutorial/assets/32959436/3d48179a-66d9-44bc-8639-e44df8411d2d)

首次连接会进行一些初始化的设置，可能会比较慢，还请耐心等待。后面打开文件夹的时候可能会再需要输入密码，可以一直开着开发机的控制台不要关掉以备不时之需。

看到左下角远程连接已经显示ssh连接地址”SSH: [ssh.intern-ai.org.cn](http://ssh.intern-ai.org.cn/)”，说明我们已经连接成功了。然后我们就可以像在本地使用Vscode一样愉快的使用vscode在开发机上进行任何操作了。

![images](https://github.com/InternLM/Tutorial/assets/32959436/bd6b7430-8ef5-4841-9e89-5f83faceda57)

连接成功后我们打开远程连接的vscode的extensions，在远程开发机上安装好python的插件，后面python debug会用到。也可以一键把我们本地vscode的插件安装到开发机上。

![images](https://github.com/InternLM/Tutorial/assets/32959436/95759a98-8e12-483e-a188-7572968beeda)

![images](https://github.com/InternLM/Tutorial/assets/32959436/e29ab709-68f1-4e0b-8e8a-93242f524e7b)

然后我们就可以像在本地使用vscode一样在远程开发机上愉快地使用vscode了

## 4.3 在vscode中打开终端

单击vscode页面下方有一个X和！的位置可以快速打开vscode的控制台，然后进入TERMINAL。

![images](https://github.com/InternLM/Tutorial/assets/32959436/d8cd9101-c9d5-4d4f-8e85-9725e399f4b1)

TIPS：右上方的+可以新建一个TERMINAL。

## 4.4 **使用Vscode进行Python debug的流程**

### 4.4.1 debug单个python文件
**Step1.打开文件夹**

在VSCode中打开直接打开root文件夹，或者你想要debug的Python文件所在的文件夹。这里可能会需要再次输入密码。下面我们以打开root文件夹为例。单击Open Folder或者左上角菜单File->Open Folder。

![images](https://github.com/InternLM/Tutorial/assets/32959436/60b2d49d-170a-4ad5-a752-1849f7e6bdbe)

这边我们新建一个文件夹，写一个简单的python程序来做debug演示。

![images](https://github.com/InternLM/Tutorial/assets/32959436/f2055734-7c9b-44cc-8a4c-1e4dce1d5dee)
```python
def add_numbers(a,b,c):
    sum = 0#这里其实覆盖了python自带的sum方法。
    sum +=a
    sum +=b
    sum +=c
    print("The sum is ",sum) 

if __name__ =='__main__':
    x,y,z = 1,2,3
    result = add_numbers(x,y,z)#图中代码这里写成1,2,3了
    print("The result of sum is ",result)
```

新建python文件后我们如果想要运行，就需要选择解释器。单击右下角的select interpreter，vsconde会自动扫描开发机上所有的python环境中的解释器。这里我们只要选conda中的base就行了，后面各位如果要使用其他虚拟环境就在这选择对应的解释器就可以。

**Step2.设置断点**

在代码行号旁边点击，可以添加一个红点，这就是断点（如果不能添加红点需要检查一下python extension是否已经正确安装）。当代码运行到这里时，它会停下来，这样你就可以检查变量的值、执行步骤等。

![images](https://github.com/InternLM/Tutorial/assets/32959436/5d4d2fa5-58de-4e5e-8417-1ee5ab04bf1d)

**Step3.启动debug**

点击VSCode侧边栏的“Run and Debug”（运行和调试），然后点击“Run and Debug”（开始调试）按钮，或者按F5键。

![images](https://github.com/InternLM/Tutorial/assets/32959436/68f3e960-9bda-43dc-8149-76be208fabac)

单击后会需要选择debugger和debug配置文件，我们单独debug一个python文件只要选择Python File就行。然后你的代码会在达到第一个断点之前运行，在第一个断点处停下来。

![images](https://github.com/InternLM/Tutorial/assets/32959436/80102b91-3859-450d-b11b-d487eda70c52)

![images](https://github.com/InternLM/Tutorial/assets/32959436/3dfaa830-a8e4-4e18-b917-a5c5827b5e57)

**Step4.查看变量**

当代码在断点处停下来时，你可以查看和修改变量的值。在“Run and Debug”侧边栏的“Variables”（变量）部分，你可以看到当前作用域内的所有变量及其值。

![images](https://github.com/InternLM/Tutorial/assets/32959436/48e444a9-9e54-40c6-af68-c357ab3eb18e)

**Step5.单步执行代码**

你可以使用“Run and Debug”侧边栏顶部的按钮来单步执行代码。这样，你可以逐行运行代码，并查看每行代码执行后的效果。

![images](https://github.com/InternLM/Tutorial/assets/32959436/a8c7d485-4d86-42ce-b185-e06499595423)

debug面板各按钮功能介绍：

* `1`: continue: 继续运行到下一个断点

* `2`: step over：跳过，可以理解为运行当前行代码，不进入具体的函数或者方法。

* `3`: step into: 进入函数或者方法。如果当行代码存在函数或者方法时，进入代码该函数或者方法。如果当行代码没有函数或者方法，则等价于step over。

* `4`: step out：退出函数或者方法, 返回上一层。

* `5`: restart：重新启动debug

* `6`: stop：终止debug

**Step6.修复错误并重新运行**

如果你找到了代码中的错误，可以修复它，然后重新运行debug来确保问题已经被解决。

通过遵循以上步骤，你可以使用VSCode的debug功能来更容易地找到和修复你Python代码中的错误。可以自己编写一个简单的python脚本，并尝试使用debug来更好的理解代码的运行逻辑。记住，debug是编程中非常重要的一部分，所以不要怕花时间在这上面。随着时间的推移，你会变得越来越擅长它！

### 4.4.2 在vscode使用命令行进行debug

很多时候我们要debug的不止是一个简单的python文件，而是很多参数，参数中不止会有简单的值还可能有错综复杂的文件关系,甚至debug一整个项目。这种情况下，直接使用命令行来发起debug会是一个更好的选择。

#### 4.4.2.1 vscode设置

vscode也支持通过remote的方法连接我们在命令行中发起的debug server。首先我们要配置一下debug的config。

还是点击VSCode侧边栏的“Run and Debug”（运行和调试)，单击"create a lauch.json file"

![images](https://github.com/InternLM/Tutorial/assets/32959436/394e773d-56e6-4c86-b136-f781fa8973a4)

选择debugger时选择python debuger。选择debug config时选择remote attach就行，随后会让我们选择debug server的地址，因为我们是在本地debug，所以全都保持默认直接回车就可以了，也就是我们的server地址为localhost:5678。

![images](https://github.com/InternLM/Tutorial/assets/32959436/8caf498a-bdda-4e2d-9623-00bdc42ee478)

![images](https://github.com/InternLM/Tutorial/assets/32959436/0b6f6ed2-b996-4768-b21e-c2668e5f1e6a)

![images](https://github.com/InternLM/Tutorial/assets/32959436/c79749a0-8f8a-4f5d-8c70-4031170acb06)

配置完以后会打开配置的json文件，但这不是重点，可以关掉。这时我们会看到run and debug界面有变化，出现了debug选项。

![images](https://github.com/InternLM/Tutorial/assets/32959436/b6d2c147-60e2-42b5-8bab-66ef450bd214)

#### 4.4.2.2 debug命令行

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

#### 4.4.2.3 使用别名简化命令

但这边有个不方便的地方，python -m debugpy --listen 5678 --wait-for-client这个命令太长了，每次都打很麻烦。这里我们可以给这段常用的命令设置一个别名。

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