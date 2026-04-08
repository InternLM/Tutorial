
# 认证鉴权

所有 书生大模型 API 请求都需要通过 API Key 进行身份认证。根据你使用的 API 服务，获取方式有所不同。

## 社区 API Key

由书生社区 (community.intern-ai.org.cn) 签发，适用于社区 API。

**Key 格式：** `sk-intern-XXXXXXXX_XXXXXXXXXXXXXXXXXXXXXXXX`

**获取步骤：**

1. 登录 [community.intern-ai.org.cn](https://community.intern-ai.org.cn)
2. 进入「个人中心」
3. 切换到「API 密钥」Tab
4. 点击「创建密钥」
5. 复制并妥善保存你的 API Key

**免费额度：** 注册后每日可获得 10K tokens 免费体验额度，更多额度可通过积分购买流量包。

> **注意：** API Key 只在创建时显示一次，请务必立即保存。如果丢失，需要重新创建。

### 使用方式

```bash
Authorization: Bearer sk-intern-xxxxxxxx_xxxxxxxxxxxxxxxxxxxxxxxx
```

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-intern-xxxxxxxx_xxxxxxxxxxxxxxxxxxxxxxxx",
    base_url="https://community.intern-ai.org.cn/api/v1"
)
```

推荐使用环境变量管理 API Key：

```bash
export INTERN_COMMUNITY_API_KEY="sk-intern-xxxxxxxx_xxxxxxxxxxxxxxxxxxxxxxxx"
```

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["INTERN_COMMUNITY_API_KEY"],
    base_url="https://community.intern-ai.org.cn/api/v1"
)
```

---

## 官方 API Key

由上海 AI 实验室官方平台签发，适用于官方 API。

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
export INTERN_OFFICIAL_API_KEY="your-official-api-key"
```

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["INTERN_OFFICIAL_API_KEY"],
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

### 社区 API

| 计划 | 免费额度 | 扩展方式 |
|------|---------|---------|
| 免费体验 | 每日 10K tokens | 积分购买流量包 |

### 官方 API

| 计划 | RPM (请求/分钟) | TPM (Token/分钟) |
|------|----------------|------------------|
| 免费 | 10 | 100,000 |
| 开发者 | 60 | 1,000,000 |
| 企业 | 自定义 | 自定义 |

超过速率限制时，API 将返回 `429 Too Many Requests` 状态码。
