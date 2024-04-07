# 基础作业

完成以下任务，并将实现过程记录截图：

* 配置lmdeploy运行环境
* 下载internlm-chat-1.8b模型
* 以命令行方式与模型对话

# 进阶作业

* 开启KV8量化，以命令行方式与模型对话。
* 开启W4A16量化，以命令行方式与模型对话。
* 设置KV Cache最大占用比例为0.4，同时开启KV8和W4A16量化，以命令行方式与模型对话。
* 以API Server方式启动lmdeploy，分别使用命令行客户端与Gradio网页客户端与模型对话。
* 任选一种量化方式以API Server方式启动lmdeploy，调整KV Cache的占用比例，分别使用命令行客户端与Gradio网页客户端与模型对话。
* 任选一种量化方式，调整KV Cache的占用比例，使用Python代码集成的方式运行internlm2-chat-1.8b模型。
* 任选一种量化方式，调整KV Cache的占用比例，使用Python代码集成的方式运行任意第三方模型。