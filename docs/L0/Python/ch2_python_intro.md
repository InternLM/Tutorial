# Chapter2: Python基础

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
t_set = {1,3,5} #集合
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
     t_set的类型是： <class 'set'>  t_set的值是:  {1, 3, 5}
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
print("not b =",not b)
```

    a and b = False
    a or b = False
    not b = True
    

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
这就是python函数在传参时候的特征导致的。通过使用id()函数可以获取对象在内存中的地址可以看到number与a的id不同，他们是两个对象了。但是alist与b的id相同，说明他们两在内存中指向的是同一个对象。

