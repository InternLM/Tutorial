
| 任务      | 任务描述                                    |
| :-------- | :----------------------------------------- |
| 闯关任务   | 完成SSH连接与端口映射并运行hello_world.py    |
| 可选任务 1 | 将Linux基础命令在开发机上完成一遍            |
| 可选任务 2 | 使用 VSCODE 远程连接开发机并创建一个conda环境 |
| 可选任务 3 | 创建并运行test.sh文件                       |

# 闯关任务
> 完成SSH连接与端口映射并运行hello_world.py

创建开发机
![image](https://img2024.cnblogs.com/blog/1664152/202407/1664152-20240708003430748-322358936.png)

SSH连接
![image](https://img2024.cnblogs.com/blog/1664152/202407/1664152-20240708003437167-1008153445.png)

免密登录
![image](https://img2024.cnblogs.com/blog/1664152/202407/1664152-20240709134616393-1240218492.png)


映射端口：7860，运行hello_world.py
![image](https://img2024.cnblogs.com/blog/1664152/202407/1664152-20240708003509040-1280085319.png)


# 可选任务 1
> 将Linux基础命令在开发机上完成一遍

1.文件管理
在 Linux 中，常见的文件管理操作包括：
- 创建文件：可以使用 **touch** 命令创建空文件。
- 创建目录：使用 **mkdir** 命令。
- 目录切换：使用 **cd** 命令。
- 显示所在目录：使用 **pwd** 命令。
- 查看文件内容：如使用 **cat** 直接显示文件全部内容，**more** 和 **less** 可以分页查看。
- 编辑文件：如 **vi** 或 **vim** 等编辑器。
- 复制文件：用 **cp** 命令。
- 创建文件链接：用 **ln** 命令。
- 移动文件：通过 **mv** 命令。
- 删除文件：使用 **rm** 命令。
- 删除目录：**rmdir**（只能删除空目录）或 **rm -r**（可删除非空目录）。
- 查找文件：可以用 **find** 命令。
- 查看文件或目录的详细信息：使用 **ls** 命令，如使用 **ls -l** 查看目录下文件的详细信息。
- 处理文件：进行复杂的文件操作，可以使用 **sed** 命令。

2. 进程管理
进程管理命令是进行系统监控和进程管理时的重要工具，常用的进程管理命令有以下几种：
- ps：查看正在运行的进程
- top：动态显示正在运行的进程
- pstree：树状查看正在运行的进程
- pgrep：用于查找进程
- nice：更改进程的优先级
- jobs：显示进程的相关信息
- bg 和 fg：将进程调入后台
- kill：杀死进程
- nvidia-smi：NVIDIA 系统管理接口

3. 工具使用
TMUX 是一个终端多路复用器。它可以在多个终端之间轻松切换，分离它们（这不会杀死终端，它们继续在后台运行）和将它们重新连接到其他终端中。

![image](https://img2024.cnblogs.com/blog/1664152/202407/1664152-20240708004510592-986572000.png)
![image](https://img2024.cnblogs.com/blog/1664152/202407/1664152-20240708004516925-1311540573.png)


# 可选任务 2
> 使用 VSCODE 远程连接开发机并创建一个conda环境 

```
conda create -n demo python=3.10
conda env list

#获得环境中的所有配置
conda env export --name demo > demo.yml
#重新还原环境
conda env create -f  demo.yml
```
![image](https://img2024.cnblogs.com/blog/1664152/202407/1664152-20240709133210164-1256195589.png)


# 可选任务 3
> 创建并运行test.sh文件

<details>
<summary>点击查看test.sh代码</summary>

```
#!/bin/bash

# 定义导出环境的函数
export_env() {
    local env_name=$1
    echo "正在导出环境: $env_name"
    # 导出环境到当前目录下的env_name.yml文件
    conda env export -n "$env_name" > "$env_name.yml"
    echo "环境导出完成。"
}

# 定义还原环境的函数
restore_env() {
    local env_name=$1
    echo "正在还原环境: $env_name"
    # 从当前目录下的env_name.yml文件还原环境
    conda env create -n "$env_name" -f "$env_name.yml"
    echo "环境还原完成。"
}

# 检查是否有足够的参数
if [ $# -ne 2 ]; then
    echo "使用方法: $0 <操作> <环境名>"
    echo "操作可以是 'export' 或 'restore'"
    exit 1
fi

# 根据参数执行操作
case "$1" in
    export)
        export_env "$2"
        ;;
    restore)
        restore_env "$2"
        ;;
    *)
        echo "未知操作: $1"
        exit 1
        ;;
esac
```
</details>

```bash
chmod +x test.sh
./test.sh restore demo
```
![image](https://img2024.cnblogs.com/blog/1664152/202407/1664152-20240709133221341-1452255414.png)
