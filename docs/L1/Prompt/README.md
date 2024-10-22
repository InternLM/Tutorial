# 提示工程(Prompt Engineering)


<img width="900" alt="L1-2" src="https://github.com/user-attachments/assets/4834591e-48dd-4d12-8fe4-3f8e548f849c">


## 1.1 什么是Prompt(提示词)

Prompt是一种用于指导以大语言模型为代表的**生成式人工智能**生成内容(文本、图像、视频等)的输入方式。它通常是一个简短的文本或问题，用于描述任务和要求。

Prompt可以包含一些特定的关键词或短语，用于引导模型生成符合特定主题或风格的内容。例如，如果我们要生成一篇关于“人工智能”的文章，我们可以使用“人工智能”作为Prompt，让模型生成一篇关于人工智能的介绍、应用、发展等方面的文章。

Prompt还可以包含一些特定的指令或要求，用于控制生成文本的语气、风格、长度等方面。例如，我们可以使用“请用幽默的语气描述人工智能的发展历程”作为Prompt，让模型生成一篇幽默风趣的文章。

总之，Prompt是一种灵活、多样化的输入方式，可以用于指导大语言模型生成各种类型的内容。

![](https://files.mdnice.com/user/56306/2bdd81c5-b3f8-4ced-b3f8-7ab471ec11e8.png)

## 1.2 什么是提示工程

提示工程是一种通过设计和调整输入(Prompts)来改善模型性能或控制其输出结果的技术。

在模型回复的过程中，首先获取用户输入的文本，然后处理文本特征并根据输入文本特征预测之后的文本，原理为**next token prediction**，类似我们日常使用的输入法。


![](https://files.mdnice.com/user/43439/b4d0060a-d057-4e04-ad73-ee42d61cbbc7.png)


提示工程是模型性能优化的基石，有以下六大基本原则：

- 指令要清晰
- 提供参考内容
- 复杂的任务拆分成子任务
- 给 LLM“思考”时间(给出过程)
- 使用外部工具
- 系统性测试变化


在提示工程中，第一点给出清晰的指令是至关重要的。一个有效的指令通常包含以下要素：背景、任务、要求、限制条件、示例、输出格式和目标。通过提供这些详细信息，我们可以引导模型生成更符合我们期望的文本。

让我们以"为AI大模型训练营生成介绍文案"为例，来展示如何逐步优化指令，以获得更理想的AI生成内容：

第一版提示词（基础版）：
```
写一段话介绍AI大模型训练营
```

![](https://files.mdnice.com/user/43439/5b256621-a991-47ee-9197-84c1b6cd33c7.jpg)


第二版提示词（增加表情元素）：
```
写一段话介绍AI大模型训练营，添加emoji表情
```

![](https://files.mdnice.com/user/43439/ac0fb42d-f024-43d5-9663-0e7ab99a660b.jpg)


第三版提示词（进一步优化结构）：
```
写一段话介绍AI大模型训练营，添加emoji表情，结构化排版
```

![](https://files.mdnice.com/user/43439/ca0612aa-c99c-4d61-a208-05581a9ee57a.jpg)


通过这个例子，我们可以清楚地看到，随着指令的逐步完善，AI生成的内容质量也随之提升。这种渐进式的提示词优化方法可以帮助我们更好地掌控AI输出，获得更符合需求的结果。

其他技巧我们这里不做过多介绍，如果大家感兴趣可以参考下面的资料：

* [OpenAI 官方提示工程指南](https://platform.openai.com/docs/guides/prompt-engineering)
* [Claude 官方提示工程指南](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
* [LangGPT 知识库](https://langgptai.feishu.cn/wiki/RXdbwRyASiShtDky381ciwFEnpe)
* [万字解读ChatGPT提示词最佳案例](https://langgptai.feishu.cn/wiki/IpdUwZRzgiYYH7kuOsDc3fWrnkg)


## 1.3 提示设计框架

- CRISPE，参考：[https://github.com/mattnigh/ChatGPT3-Free-Prompt-List](https://github.com/mattnigh/ChatGPT3-Free-Prompt-List)

  - **C**apacity and **R**ole (能力与角色)：希望 ChatGPT 扮演怎样的角色。​
  - **I**nsight (洞察力)：背景信息和上下文(坦率说来我觉得用 Context 更好)​
  - **S**tatement (指令)：希望 ChatGPT 做什么。​
  - **P**ersonality (个性)：希望 ChatGPT 以什么风格或方式回答你。​
  - **E**xperiment (尝试)：要求 ChatGPT 提供多个答案。

  写出的提示如下：

  ```
  Act as an expert on software development on the topic of machine learning frameworks, and an expert blog writer. The audience for this blog is technical professionals who are interested in learning about the latest advancements in machine learning. Provide a comprehensive overview of the most popular machine learning frameworks, including their strengths and weaknesses. Include real-life examples and case studies to illustrate how these frameworks have been successfully used in various industries. When responding, use a mix of the writing styles of Andrej Karpathy, Francois Chollet, Jeremy Howard, and Yann LeCun.
  ```

- CO-STAR，参考：[https://aiadvisoryboards.wordpress.com/2024/01/30/co-star-framework/](https://aiadvisoryboards.wordpress.com/2024/01/30/co-star-framework/)

  ![](https://files.mdnice.com/user/56306/ab84b4d0-843c-460b-925a-16e07fefc595.png)

    - **C**ontext (背景): 提供任务背景信息​
    - **O**bjective (目标): 定义需要LLM执行的任务​
    - **S**tyle (风格): 指定希望LLM具备的写作风格​
    - **T**one (语气): 设定LLM回复的情感基调​
    - **A**udience (观众): 表明回复的对象​
    - **R**esponse (回复): 提供回复格式

    例如我们设计一个解决方案专家，用于把目标拆解为可执行的计划，完成的提示词如下：

    ```
    # CONTEXT # 
    我是一名个人生产力开发者。在个人发展和生产力领域,人们越来越需要这样的系统:不仅能帮助个人设定目标,还能将这些目标转化为可行的步骤。许多人在将抱负转化为具体行动时遇到困难,凸显出需要一个有效的目标到系统的转换过程。

    #########

    # OBJECTIVE #
    您的任务是指导我创建一个全面的系统转换器。这涉及将过程分解为不同的步骤,包括识别目标、运用5个为什么技巧、学习核心行动、设定意图以及进行定期回顾。目的是提供一个逐步指南,以无缝地将目标转化为可行的计划。

    #########

    # STYLE #
    以富有信息性和教育性的风格写作,类似于个人发展指南。确保每个步骤的呈现都清晰连贯,迎合那些渴望提高生产力和实现目标技能的受众。

    #########

    # Tone #
    始终保持积极和鼓舞人心的语气,培养一种赋权和鼓励的感觉。应该感觉像是一位友好的向导在提供宝贵的见解。

    # AUDIENCE #
    目标受众是对个人发展和提高生产力感兴趣的个人。假设读者寻求实用建议和可行步骤,以将他们的目标转化为切实的成果。

    #########

    # RESPONSE FORMAT #
    提供一个结构化的目标到系统转换过程步骤列表。每个步骤都应该清晰定义,整体格式应易于遵循以便快速实施。

    #############

    # START ANALYSIS #
    如果您理解了,请询问我的目标。
    ```

# 2. LangGPT结构化提示词

LangGPT 是 **Language For GPT-like LLMs** 的简称，中文名为结构化提示词。LangGPT 是一个帮助你编写高质量提示词的工具，理论基础是我们提出的一套模块化、标准化的提示词编写方法论——结构化提示词。我们希望揭开提示工程的神秘面纱，为大众提供一套可操作、可复现的提示词方法论、工具和交流社群。我们的愿景是让人人都能写出高质量提示词。[LangGPT社区文档](https://langgptai.feishu.cn/wiki/RXdbwRyASiShtDky381ciwFEnpe)：https://langgpt.ai

## 2.1 LangGPT结构

LangGPT框架参考了面向对象程序设计的思想，设计为基于角色的双层结构，一个完整的提示词包含**模块-内部元素**两级，模块表示要求或提示LLM的方面，例如：背景信息、建议、约束等。内部元素为模块的组成部分，是归属某一方面的具体要求或辅助信息，分为赋值型和方法型。

![](https://files.mdnice.com/user/56306/91c1dffe-011d-4932-b6b2-187284a0ad91.png)

## 2.2 编写技巧

- **构建全局思维链**

  对大模型的 Prompt 应用CoT 思维链方法的有效性是被研究和实践广泛证明了的。首先可以根据场景选择基本的模块。

  ![](https://files.mdnice.com/user/56306/05e380a8-b627-42f2-b0e6-343bc9923f3e.png)

  **一个好的结构化 Prompt 模板，某种意义上是构建了一个好的全局思维链。** 如 LangGPT 中展示的模板设计时就考虑了如下思维链:

  > 💡 Role (角色) -> Profile（角色简介）—> Profile 下的 skill (角色技能) -> Rules (角色要遵守的规则) -> Workflow (满足上述条件的角色的工作流程) -> Initialization (进行正式开始工作的初始化准备) -> 开始实际使用

  一个好的 Prompt ，内容结构上最好也是逻辑清晰连贯的。**结构化 prompt 方法将久经考验的逻辑思维链路融入了结构中，大大降低了思维链路的构建难度。**

  构建 Prompt 时，不妨参考优质模板的全局思维链路，熟练掌握后，完全可以对其进行增删改留调整得到一个适合自己使用的模板。例如当你需要控制输出格式，尤其是需要格式化输出时，完全可以增加 `Ouput` 或者 `OutputFormat` 这样的模块。

- **保持上下文语义一致性**

  包含两个方面，一个是**格式语义一致性**，一个是**内容语义一致性**。

  **格式语义一致性是指标识符的标识功能前后一致。** 最好不要混用，比如 `#` 既用于标识标题，又用于标识变量这种行为就造成了前后不一致，这会对模型识别 Prompt 的层级结构造成干扰。

  **内容语义一致性是指思维链路上的属性词语义合适。** 例如 LangGPT 中的 `Profile` 属性词，使之功能更加明确：即角色的简历。结构化 Prompt 思想被广泛使用后衍生出了许许多多的模板，但基本都保留了 `Profile` 的诸多设计，说明其设计是成功有效的。

  **内容语义一致性还包括属性词和相应模块内容的语义一致。** 例如 `Rules` 部分是角色需要遵守规则，则不宜将角色技能、描述大量堆砌在此。

- **有机结合其他 Prompt 技巧**

  LangGPT结构在设计时没有拘泥于具体的方面，相比其他的提示设计框架，更加灵活，具有更强的可扩展性和兼容性，可以很好地结合其他提示设计技巧。

  构建高质量 Prompt 时，将这些方法结合使用，结构化方式能够更便于各个技巧间的协同组织，例如将 CoT 方法融合到结构化 Prompt 中编写提示词。
  汇总现有的一些方法：

  1. 细节法：给出更清晰的指令，包含更多具体的细节
  2. 分解法：将复杂的任务分解为更简单的子任务 （Let's think step by step, CoT，LangChain等思想）
  3. 记忆法：构建指令使模型时刻记住任务，确保不偏离任务解决路径（system 级 prompt）
  4. 解释法：让模型在回答之前进行解释，说明理由 （CoT 等方法）
  5. 投票法：让模型给出多个结果，然后使用模型选择最佳结果 （ToT 等方法）
  6. 示例法：提供一个或多个具体例子，提供输入输出示例 （one-shot, few-shot 等方法）

  上面这些方法最好结合使用，以实现在复杂任务中实现使用不可靠工具（LLMs）构建可靠系统的目标。

## 2.3 常用的提示词模块
结构化提示词更多体现的是一种思想，本章所给出的提示词模板也只是当前的最佳实践，实际使用过程中大家可以根据需要自行增删各个模块，重构相关模块，甚至提出一套全新的模板。

编写提示词时，需要根据不同需求添加不同模块要点。如果采用固定的模式写法，在面对差异巨大的需求场景时，经常会因缺少某些描述而导致效果变差。下面整理了按字母从A-Z排列的共30个角度的模块，使用时，可从其中挑选合适的模块组装。 

- Attention：需重点强调的要点 
- Background：提示词的需求背景 
- Constraints：限制条件
- Command：用于定义大模型指令
- Definition：名词定义 
- Example：提示词中的示例few-shots 
- Fail：处理失败时对应的兜底逻辑 
- Goal：提示词要实现的目标 
- Hack：防止被攻击的防护词 
- In-depth：一步步思考，持续深入
- Job：需求任务描述 
- Knowledge：知识库文件 
- Lawful：合法合规，安全行驶的限制
- Memory：记忆关键信息，缓解模型遗忘问题 
- Merge：是否使用多角色，最终合并投票输出结果 
- Neglect：明确忽略哪些内容 
- Odd：偶尔 （俏皮，愤怒，严肃） 一下
- OutputFormat：模型输出格式 
- Pardon：当用户回复信息不详细时，持续追问 
- Quote：引用知识库信息时，给出原文引用链接
- Role：大模型的角色设定
- RAG：外挂知识库
- Skills：擅长的技能项  
- Tone：回复使用的语气风格  
- Unsure：引入评判者视角，当判定低于阈值时，回复安全词   
- Vaule：Prompt模仿人格的价值观 
- Workflow：工作流程
- X-factor：用户使用本提示词最为重要的内核要素 
- Yeow：提示词开场白设计   
- Zig：无厘头式提示词，如[答案之书]


# 3. 浦语提示词工程实践(LangGPT版)

编写完LangGPT提示词后，可以将其作为系统提示，也可直接作为交互式对话的输入。**推荐作为系统提示**。

![](https://files.mdnice.com/user/56306/3239f0c8-83ec-4943-9cb0-880a548a321f.png)

填入系统提示后保存设置，之后可以与自定义的助手角色进行对话。

## 3.1 LangGPT社区优质应用展示

- 自动化生成LangGPT提示词

    利用下面的提示词引导InternLM扮演提示词生成助手，自动化地生成符合最佳实践的结构化提示词：
```
    你是提示词专家，根据用户的输入设计用于生成**高质量（清晰准确）**的大语言模型提示词。
    - 技能：
    - 📊 分析、写作、编码
    - 🚀 自动执行任务
    - ✍ 遵循提示工程的行业最佳实践并生成提示词
    # 输出要求：
    - 结构化输出内容。
    - 为代码或文章提供**详细、准确和深入**的内容。
    # 📝 提示词模板（使用代码块展示提示内容）：
    ```
    你是xxx（描述角色和角色任务）
    - 技能：
    - 📊 分析、写作、编码
    - 🚀 自动执行任务
    # 💬 输出要求：
    - 结构化输出内容。
    - 为代码或文章提供**详细、准确和深入**的内容。
    -（其他基本输出要求）
    # 🔧 工作流程：
    - 仔细深入地思考和分析用户的内容和意图。
    - 逐步工作并提供专业和深入的回答。
    -（其他基本对话工作流程）
    # 🌱 初始化：
    欢迎用户，友好的介绍自己并引导用户使用。
    ```
    **你的任务是帮助用户设计高质量提示词。**
    开始请打招呼：“您好！我是您的提示词专家助手，请随时告诉我您需要设计什么用途的提示词吧。
```

  效果演示：

![](https://files.mdnice.com/user/43439/a1e3bb2c-3230-4ec3-8f21-6ce457c533d8.png)



- 小红书文案专家

```markdown
你是小红书文案专家，请按照我提供的主题，帮我创作小红书标题和文案。
 
# 技能
 
## 创作有吸引力的标题
- 使用标点：通过标点符号，尤其是叹号，增强语气，创造紧迫或惊喜的感觉！
- 挑战与悬念：提出引人入胜的问题或情境，激发好奇心。
- 结合正负刺激：平衡使用正面和负面的刺激，吸引注意力。
- 紧跟热点：融入当前流行的热梗、话题和实用信息。
- 明确成果：具体描述产品或方法带来的实际效果。
- 表情符号：适当使用emoji，增加活力和趣味性。
- 口语化表达：使用贴近日常交流的语言，增强亲和力。
- 字数控制：保持标题在20字以内，简洁明了。

## 标题创作公式
标题需要顺应人类天性，追求便捷与快乐，避免痛苦。
- 正面吸引：展示产品或方法的惊人效果，强调快速获得的益处。比如：产品或方法+只需1秒（短期）+便可开挂（逆天效果）。
- 负面警示：指出不采取行动可能带来的遗憾和损失，增加紧迫感。比如：你不xxx+绝对会后悔（天大损失）+（紧迫感）
 
标题从下面选择1-2个关键词：
我宣布、我不允许、请大数据把我推荐给、真的好用到哭、真的可以改变阶级、真的不输、永远可以相信、吹爆、搞钱必看、狠狠搞钱、一招拯救、正确姿势、正确打开方式、摸鱼暂停、停止摆烂、救命！、啊啊啊啊啊啊啊！、以前的...vs现在的...、再教一遍、再也不怕、教科书般、好用哭了、小白必看、宝藏、绝绝子、神器、都给我冲、划重点、打开了新世界的大门、YYDS、秘方、压箱底、建议收藏、上天在提醒你、挑战全网、手把手、揭秘、普通女生、沉浸式、有手就行、打工人、吐血整理、家人们、隐藏、高级感、治愈、破防了、万万没想到、爆款、被夸爆
 
## 创作有吸引力的正文：

### 正文创作公式
选择以下一种方式作为文章的开篇引入：
- 引用名言、提出问题、使用夸张数据、举例说明、前后对比、情感共鸣。
 
### 正文要求
- 风格要求：真诚友好、鼓励建议、幽默轻松；口语化的表达风格，有共情力
- 多用叹号、多分段、多用短句
- 重点在前：遵循倒金字塔原则，把最重要的事情放在开头说明
- 逻辑清晰：遵循总分总原则，第一段和结尾段总结，中间段分点说明
 
# 输出要求：
- 标题数量：每次准备10个标题。
- 正文创作：撰写与标题相匹配的正文内容，具有强烈的浓人风格
 
# 🔧 工作流程：
- 请用户提供关键词或主题，确定文案的方向和风格。
- 根据用户主题，自动生成符合小红书平台特点的文案，包括标题、正文和 Tags。

# 🌱 初始化：
欢迎用户，友好的介绍自己。请用户提供关键词或主题，以及期望的文案风格和目标用户群体，依据用户提供的主题创作文案。
```

效果演示：

![](https://files.mdnice.com/user/43439/f4f9ef6d-50ba-4221-8ab7-9ae48f389248.jpg)



## 4.应用开发实战：使用浦语 InternLM 大模型一键写书
### 4.1 在线体验（需正确上网）：
https://book.apps.langgpt.ai/

### 4.2 本地运行：

#### 4.2.1 获取项目代码
项目地址： https://github.com/langgptai/BookAI  
命令：
```
git clone https://github.com/langgptai/BookAI.git
cd BookAI
```

查看项目结构:
```
├── book_writer.py
├── prompts
│   ├── chapter_writer.txt
│   ├── outline_writer.txt
│   └── title_writer.txt
├── README.md
├── requirements.txt
```
#### 4.2.2 配置项目 Python 环境
```
pip install -r requirements.txt
```

#### 4.2.3 配置大模型 API

（1）项目要求的 API 并发度较高，超出了浦语的限制，可以使用硅基流动注册免费的 API，额度更多，获取 API_KEY
https://cloud.siliconflow.cn/i/TxUlXG3u

（2） 配置下面命令中的 API_KEY 并执行命令，即可完成书籍创作

```
export API_KEY=sk-xxx
export BASE_URL=https://api.siliconflow.cn/v1
export MODEL_NAME=internlm/internlm2_5-7b-chat

python3 book_writer.py
```

#### 4.2.4 项目拆解

大模型无法完成这么复杂的任务，因此我们需要拆解任务 ——> 这种方法也称为分治法。

分治法拆解任务：
  - 第一步：创作书籍总体信息：书名，主要内容介绍
  - 第二步：创作书籍分章节大纲：每章章节名+简介
  - 第三步：依据章节大纲创作章节内容

接下来针对每一步骤撰写提示词：

（1）书籍起名提示词
```
# Role: 书籍写作专家

## Profile
- author: LangGPT
- version: 1.0
- language: 中文
- description: 帮助用户为书籍创建有吸引力的标题和简介，确保书名与书籍内容相符，简介清晰传达书籍核心主题。

## Skills
1. 创意标题设计：能够根据书籍主题与风格，设计简洁、吸引读者的书名。
2. 精准简介编写：擅长提炼书籍的核心内容，用简短的文字清晰传达书籍的主题和卖点。
3. 内容风格匹配：根据书籍类型（小说、纪实、科幻等），调整标题和简介的语言风格。
4. 阅读者定位：根据书籍目标读者群体，设计有针对性的书籍标题与简介。

## Rules
1. 根据书籍内容概述、类型和目标读者，生成适合的标题和简介。
2. 标题需简洁、富有吸引力，能够激发读者的兴趣。
3. 简介需简短有力，准确传达书籍核心内容和主题。
4. 避免过于复杂或不相关的描述，突出书籍卖点和读者关心的部分。

## Goals
书籍信息：{theme}
撰写书籍标题和简介(json格式输出)：
{
    "title":"《xxx》",
    "intro":"xxx",
}

## Init
设计合适的标题和简介，只输出json内容，此外不要给出任何无关内容和字符。
```


（2） 书籍大纲提示词
```
# Role: 书籍写作专家

## Profile
- author: LangGPT
- version: 1.0
- language: 中文/英文
- description: 帮助用户根据书籍的标题和简介，设计出完整的书籍大纲，确保结构清晰，逻辑合理，并符合书籍的主题和风格。

## Skills
1. 书籍结构设计：根据书籍的主题和内容，设计清晰、有逻辑的章节和段落结构。
2. 情节和主题发展：擅长为小说、纪实文学等书籍设计情节发展框架，确保每一章节之间的连贯性和发展方向。
3. 内容层次划分：能够根据书籍的核心主题，将内容分为多个合理的层次和部分，确保读者能系统地理解内容。
4. 读者体验优化：根据目标读者的需求和阅读习惯，优化书籍结构，使其易于阅读并具有吸引力。

## Rules
1. 基于用户提供的书籍标题和简介，生成完整的书籍大纲。
2. 大纲需要包括书籍的主要章节和每一章节的关键内容概述。
3. 确保大纲的结构合理，内容连贯，有助于推进书籍的主题和情节发展。
4. 书籍大纲应体现书籍的核心主题，并符合读者的期待。

## Goals
书籍主题：{theme}
书籍标题和简介：
{intro}

撰写书籍大纲（python list 格式,10-20章）
["第一章：《xxx》xxx", "第二章：《xxx》xxx","...", "xxx"]

## Init
设计合适的章节大纲，只输出 python list内容，此外不要给出任何无关内容和字符。
```

（3） 书籍正文内容撰写提示词

```
# Role: 书籍写作专家

## Profile
- author: LangGPT
- version: 1.0
- language: 中文/英文
- description: 帮助用户根据提供的书籍标题、简介和章节大纲，撰写每一章的具体内容，确保语言风格符合书籍定位，内容连贯、专业、正式。

## Skills
1. 章节内容撰写：能够根据用户提供的章节大纲，撰写完整的章节内容，确保情节发展和主题的深度探讨。
2. 文体和风格匹配：根据书籍的类型（小说、纪实、学术等）和目标读者，调整写作风格，使其正式、专业且符合书籍定位。
3. 细节描写与逻辑构建：擅长细节描写，增强故事的真实感与情感深度，保证逻辑严密性。
4. 内容深化与扩展：在大纲基础上，合理扩展和深化内容，使每一章有足够的丰富性和信息量。

## Rules
1. 依据用户提供的书籍标题、简介和大纲，撰写每一章的详细内容。
2. 每章内容需符合书籍主题，并在情节、逻辑和语言风格上保持一致。
3. 确保内容丰富、信息清晰，避免不必要的重复或偏离主题。
4. 保持正式、专业的语言风格，适合目标读者。
5. 不需胡说八道，编造事实。


## Goals
书籍简介：
{book_content}

本章大纲：
{chapter_intro}

请依据本章大纲和书籍简介撰写本章内容。

## OutputFormat:
- 如果需要数学公式，使用写法:"$latex公式$"，使其能被 markdown 正确渲染，示例："$z = \sum_{i=1}^{n} w_i \cdot x_i + b$"。
（注意：你的数学公式不要用 "\[ \]" 写法，这样无法被正确渲染！！！）
- 结构化写作，使用 markdown 格式排版内容。
- 章节标题，示例:"# 第三章：Transformer的基础原理"
- 章节内小标题使用序号, 示例:"## 3.1 Transformer的架构"。
- 合理按需使用粗体，斜体，引用，代码，公式，列表。

## Init
设计合适的章节大纲，只输出本章内容，此外不要给出任何无关内容和字符。
```

（4） 使用代码将这些提示词的输入输出串起来

```
import os
import re
import json
from typing import List, Dict, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import openai
from phi.assistant import Assistant
from phi.llm.openai import OpenAIChat

# 加载 .env 文件
load_dotenv()

def read_prompt(prompt_file: str, replacements: Dict[str, str]) -> str:
    """
    读取提示文件并替换占位符
    """
    with open(prompt_file, 'r', encoding='utf-8') as file:
        prompt = file.read()
    for key, value in replacements.items():
        prompt = prompt.replace(f"{{{key}}}", value)
    return prompt
def convert_latex_to_markdown(text):
    # 使用正则表达式替换公式开始和结束的 \[ 和 \]，但不替换公式内部的
    pattern = r'(?<!\\)\\\[((?:\\.|[^\\\]])*?)(?<!\\)\\\]'
    return re.sub(pattern, r'$$\1$$', text)

class BookWriter:
    """管理书籍生成过程的主类。"""

    def __init__(self, api_key: str, base_url: str, model_name: str, system_prompt=None):
        """初始化BookWriter。"""
        # 使用openai的接口调用书生浦语模型

        self.api_key = os.getenv("API_KEY") if api_key is None else api_key
        self.base_url = os.getenv("BASE_URL") if base_url is None else base_url
        self.model_name = os.getenv("MODEL_NAME") if model_name is None else model_name

        if system_prompt is None:
            system_prompt = "你是一个专业的写作助手，正在帮助用户写一本书。"
        self.assistant = self.create_assistant(self.model_name, self.api_key, self.base_url, system_prompt)
    
    def create_assistant(self, 
                        model_name: str, 
                        api_key: str, 
                        base_url: str, 
                        system_prompt: str) -> str:
        # 润色文本
        self.assistant = Assistant(
            llm=OpenAIChat(model=model_name,
                        api_key=api_key,
                        base_url=base_url,
                        max_tokens=4096,  # make it longer to get more context
                        ),
            system_prompt=system_prompt,
            prevent_prompt_injection=True,
            prevent_hallucinations=False,
            # Add functions or Toolkits
            #tools=[...],
            # Show tool calls in LLM response.
            # show_tool_calls=True
        )
        return self.assistant

    def generate_title_and_intro(self, book_theme, prompt_file = "prompts/title_writer.txt") -> Tuple[str, str]:
        """生成书籍标题和主要内容介绍。

        Args:
            prompt: 用于生成标题和介绍的提示。

        Returns:
            包含生成的标题和介绍的元组。
        """
        prompt_args = {"theme": book_theme}
        prompt = read_prompt(prompt_file, prompt_args)
        #print(prompt)
        for attempt in range(3):
            try:
                response = self.assistant.run(prompt, stream=False)
                # convert to json
                response = response.strip()
                if not response.startswith('{'):
                    response = '{' + response.split('{', 1)[1]
                if not response.endswith('}'):
                    response = response.split('}', 1)[0] + '}'

                book_title_and_intro = json.loads(response)

                #print(book_title_and_intro)

                return book_title_and_intro
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
        return response

    def generate_outline(self, book_theme, book_title_and_intro: str, prompt_file= "prompts/outline_writer.txt") -> List[str]:
        """生成书籍章节大纲。

        Args:
            prompt: 用于生成大纲的提示。
            title: 书籍标题。
            intro: 书籍介绍。

        Returns:
            章节标题列表。
        """
        prompt_args = {"theme": book_theme, "intro": str(book_title_and_intro)}
        prompt = read_prompt(prompt_file, prompt_args)
        for attempt in range(3):
            try:
                response = self.assistant.run(prompt, stream=False)
                #print(response)
                # convert to json
                response = response.strip()
                if not response.startswith('['):
                    response = '[' + response.split('[', 1)[1]
                if not response.endswith(']'):
                    response = response.split(']', 1)[0] + ']'
                chapters = json.loads(response.strip())
                #print(chapters)
                return chapters
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
        return response

    def generate_chapter(self, book_content, chapter_intro, prompt_file= "prompts/chapter_writer.txt") -> str:
        """生成单个章节的内容。

        Args:
            chapter_title: 章节标题。
            book_title: 书籍标题。
            book_intro: 书籍介绍。
            outline: 完整的章节大纲。
            prompt: 用于生成章节的提示。

        Returns:
            生成的章节内容。
        """
        
        prompt_args = {"book_content": str(book_content), "chapter_intro": str(chapter_intro)}
        prompt = read_prompt(prompt_file, prompt_args)
        for attempt in range(3):
            try:
                response = self.assistant.run(prompt, stream=False)
                response.strip()
                if response.startswith('```markdown'):
                    # 删除第一行和最后一行
                    lines = response.splitlines()
                    response = '\n'.join(lines[1:-1])

                return response
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
        response = convert_latex_to_markdown(response)
        return response

    def generate_book(self, custom_theme=None, save_file=False) -> None:
        """生成整本书并将其保存到文件中。

        Args:
            custom_prompts: 自定义提示的字典。可以包括 'title_intro', 'outline' 和 'chapter' 键。
        """

        print("开始生成书籍标题和介绍...")
        theme = custom_theme if custom_theme else "Transformer是什么"
        title_and_intro = self.generate_title_and_intro(theme)
        title = title_and_intro["title"]
        print(f"书籍标题和介绍:\n {title_and_intro}")

        print("\n开始生成章节大纲...")
        chapters = self.generate_outline(theme, title_and_intro)
        print("章节大纲:")
        print(chapters)

        book_intro = title_and_intro
        book_content = "# " + title

        # 使用线程池来并行生成章节内容
        print("\n开始创作正文内容，时间较长（约几分钟）请等待~")
        with ThreadPoolExecutor() as executor:
            chapter_contents = list(executor.map(self.generate_chapter, [book_intro]*len(chapters), chapters))

        for i, chapter in enumerate(chapters, 1):
            print(f"\n正在生成第{i}章：{chapter}")
            chapter_content = chapter_contents[i-1].strip()  # 获取已生成的章节内容
            print(chapter_content)
            book_content += f"\n\n{chapter_content}"
            print(f"第{i}章已完成。")

        print("\n整本书已生成完毕。")
        if save_file:
            filename = f"books/{title.replace(' ', '_')}.md"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(book_content)
            
            print(f"书籍内容已保存到 {filename} 文件中。")
        return book_content

def main():
    """主函数, 演示如何使用BookWriter类。"""
    book_theme = input("请输入书籍主题(如 AI 是什么？): ")

    api_key = os.getenv("API_KEY")
    base_url = os.getenv("BASE_URL")
    model_name = os.getenv("MODEL_NAME")
    print(base_url, model_name)
    book_writer = BookWriter(api_key, base_url, model_name, system_prompt=None)
    book_writer.generate_book(custom_theme=book_theme, save_file=True)

if __name__ == "__main__":
    main()
```

#### 4.2.5 项目优化

当前的写书项目只是个小 demo，还存在许多问题，同学们可以试着优化这些问题。一些已知的问题和优化方向：

    1. 章节正文内容的质量提升。优化内容表达、内容的深度、格式排版等，尤其数学公式的格式和排版。
    2. 各章节内容的连贯性。
    3. 章节正文长度提升。
    4. 让图书图文并茂：使用 mardown 的图片语法配图，或者搭配生图模型生成图片。
    5. 其他你能想到的优化方向。



# 本章小结

本章深入探讨了提示工程（Prompt Engineering）的理论与实践，从基础概念到高级应用，为读者提供了全面的学习路径。

我们首先介绍了提示词（Prompt）的定义及其在生成式人工智能中的重要作用。随后，我们探讨了提示工程的基本原则和技巧，包括CRISPE和CO-STAR等常见的提示词设计框架。

接着，我们重点介绍了LangGPT结构化提示词方法。这种方法借鉴了面向对象程序设计的思想，提供了一种模块化、标准化的提示词编写方法论。我们详细讲解了LangGPT的基本结构、编写技巧以及常用模块，为读者提供了实用的工具来提高提示词的质量和效果。

在实践部分，我们展示了如何使用浦语大模型进行提示工程实践。通过具体的案例，如自动化生成提示词和小红书文案助手，我们展示了LangGPT框架在实际应用中的强大功能。

最后，我们通过一个"一键写书"系统的开发实战，将理论知识应用到实际项目中。我们详细讲解了项目的架构、核心代码实现，以及潜在的优化方向，为读者提供了一个综合性的学习案例。

通过本章的学习，读者应该能够理解提示工程的核心概念，掌握LangGPT结构化提示词的编写方法，并能够将这些知识应用到实际的AI应用开发中。同时，我们也鼓励读者在此基础上进行进一步的探索和创新，以充分发挥大语言模型的潜力。
