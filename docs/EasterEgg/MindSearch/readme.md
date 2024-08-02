# MindSearch 快速部署（InternStudio 版）

选择 InternStudio 算力平台 50% A100 的 cuda 12.2 的开发机，并使用ssh vscode 远程连接到开发机。

## 1. 激活环境

小助手提前帮大家安装好了环境，只需要一步一步按照下面的步骤便可以启动 MindSearch。

```shell
conda activate /share/pre_envs/mindsearch
```

## 2. 启动后端

打开新终端运行以下命令启动推理后端。

```
conda activate /share/pre_envs/mindsearch
cd /share/demo/MindSearchDuck

python -m mindsearch.app --lang zh --model_format internlm_server
```

## 3. 启动前端

```shell
conda activate /share/pre_envs/mindsearch
cd /share/demo/MindSearchDuck

python run.py
```

