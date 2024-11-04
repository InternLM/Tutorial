# Chapter3: Numpy基础(选修)

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
    
