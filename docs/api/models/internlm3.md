
# InternLM3 模型

InternLM3 是书生大模型系列的第三代语言模型，仅使用 4T 高质量数据训练的 8B 模型即超越同量级模型，训练成本节约 75% 以上。

## 可用模型

| 模型 ID | 上下文长度 | 可用 API | 说明 |
|--------|-----------|---------|------|
| `intern-s1-pro` | 32K | 社区 / 官方 | Intern-S1-Pro，推荐使用 |
| `intern-s1` | 32K | 社区 / 官方 | Intern-S1，通用对话与任务处理 |
| `internlm3-latest` | 32K | 社区 / 官方 | 别名，等同于 `intern-s1-pro`（向后兼容） |

> **说明：** "社区"指社区 API (`community.intern-ai.org.cn`)，"官方"指官方 API (`chat.intern-ai.org.cn`)。详见 [API 文档首页](/docs/api) 的对比表。

## 特性

- **高效训练**：精炼数据框架，4T 数据训练即达 SOTA
- **深度思考**：首次融合常规对话与深度思考模式
- **数学推理**：在 GSM8K、MATH 等数学基准上表现优异
- **代码生成**：HumanEval、MBPP 等编程基准领先同量级

## 调用示例

### 基础对话

```python
response = client.chat.completions.create(
    model="intern-s1-pro",
    messages=[
        {"role": "user", "content": "解释一下 Transformer 中的自注意力机制"}
    ],
    temperature=0.7
)
```

### 深度思考模式

```python
response = client.chat.completions.create(
    model="intern-s1-pro",
    messages=[
        {"role": "system", "content": "请使用深度思考模式，逐步分析问题。"},
        {"role": "user", "content": "证明根号2是无理数"}
    ],
    temperature=0.1,
    max_tokens=4096
)
```

## 请求参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `model` | string | 必填 | 模型 ID |
| `messages` | array | 必填 | 对话消息列表 |
| `temperature` | number | 0.7 | 采样温度 (0-2) |
| `max_tokens` | number | 2048 | 最大生成 Token 数 |
| `top_p` | number | 1.0 | 核采样参数 |
| `stream` | boolean | false | 是否启用流式输出 |
| `stop` | string/array | null | 停止生成的标记 |
