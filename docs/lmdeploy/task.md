# LMDeploy 模型部署 -- 闯关任务

## 任务说明

通关本课程需要完成以下任务。请先按照教材完成 LMDeploy 的安装和环境配置。

## 任务 1：部署模型并启动 API 服务

**要求：**

使用 LMDeploy 部署一个大语言模型，并启动 OpenAI 兼容的 API 服务。

1. 安装 LMDeploy 并验证安装成功（截图 `lmdeploy version` 输出）
2. 使用 `lmdeploy serve api_server` 启动一个模型的 API 服务
3. 使用 curl 或 Python OpenAI SDK 成功调用 API 并获得模型回复

推荐使用 `internlm/internlm3-8b-instruct` 模型，也可以选择其他受支持的模型。

**提交：**

- `lmdeploy version` 的截图
- API 服务启动命令的截图
- 使用 curl 或 Python 调用 API 的截图（需包含完整的请求和响应）

## 任务 2：W4A16 量化并对比 FP16 显存和速度

**要求：**

对一个模型进行 W4A16 量化，并与 FP16 原始模型进行对比。

1. 使用 `lmdeploy lite auto_awq` 对模型进行 W4A16 量化
2. 分别用 FP16 原始模型和 W4A16 量化模型启动 API 服务
3. 记录并对比以下指标：
   - GPU 显存占用（可通过 `nvidia-smi` 查看）
   - 回复同一个问题的响应时间

**提交：**

- 量化命令及执行过程的截图
- FP16 模型的显存占用截图（`nvidia-smi`）
- W4A16 模型的显存占用截图（`nvidia-smi`）
- 对比表格（显存、速度），并简要分析量化的收益与代价

## 任务 3：部署一个多模态模型

**要求：**

使用 LMDeploy 部署一个多模态视觉语言模型，并完成图片理解任务。

1. 部署 InternVL 系列模型（推荐 `OpenGVLab/InternVL2_5-8B`）或 InternSVG
2. 启动 API 服务
3. 发送一张图片给模型，获取模型对图片的描述
4. 使用 Python 代码完成调用，代码需完整可运行

**提交：**

- 模型部署启动命令的截图
- 使用的测试图片
- 模型返回的图片描述结果截图
- 完整的 Python 调用代码
