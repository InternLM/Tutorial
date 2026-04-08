
# 认证鉴权

所有 书生大模型 API 请求都需要通过 API Key 进行身份认证。

## API Key

由上海 AI 实验室官方平台签发。

**获取步骤：**

1. 访问 [书生大模型开放平台](https://internlm.intern-ai.org.cn/api/document)
2. 注册并登录
3. 在平台中获取 API Key

### 使用方式

```bash
Authorization: Bearer your-official-api-key
```

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-official-api-key",
    base_url="https://chat.intern-ai.org.cn/api/v1"
)
```

推荐使用环境变量管理 API Key：

```bash
export INTERN_API_KEY="your-api-key"
```

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["INTERN_API_KEY"],
    base_url="https://chat.intern-ai.org.cn/api/v1"
)
```

---

## 安全建议

- 不要将 API Key 硬编码在代码中
- 不要将 API Key 提交到 Git 仓库
- 使用环境变量或密钥管理服务存储
- 定期轮换 API Key
- 如果怀疑泄露，立即在对应平台撤销并重新创建

## 速率限制

| 计划 | RPM (请求/分钟) | TPM (Token/分钟) |
|------|----------------|------------------|
| 免费 | 10 | 100,000 |
| 开发者 | 60 | 1,000,000 |
| 企业 | 自定义 | 自定义 |

超过速率限制时，API 将返回 `429 Too Many Requests` 状态码。
