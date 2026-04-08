

> 本文档 AI + 社区共建中
# OpenCompass

OpenCompass 是书生生态中的一站式大模型评测平台，支持 100+ 评测基准、50+ 模型架构，提供全面客观的模型能力评估。

## 核心特性

- **全面评测**：知识、语言、理解、推理、考试五大维度
- **100+ 数据集**：MMLU、GSM8K、HumanEval、C-Eval 等
- **多模型支持**：HuggingFace 模型 / OpenAI API / 本地模型
- **竞技场**：Compass Arena 匿名对战，客观排名

## 快速安装

```bash
pip install opencompass
```

## 快速评测

```bash
# 评测 InternLM3 在 GSM8K 上的表现
python run.py \
    --models internlm3_8b_instruct \
    --datasets gsm8k \
    --work-dir outputs/internlm3-gsm8k
```

## 评测报告解读

OpenCompass 生成的评测报告包含：

- **总分**：加权平均分
- **分项得分**：各数据集详细得分
- **对比分析**：与基准模型的对比
- **错误分析**：典型错误案例

## 相关资源

- [GitHub 仓库](https://github.com/open-compass/opencompass)
- [官方文档](https://opencompass.readthedocs.io)
- [排行榜](https://rank.opencompass.org.cn)
