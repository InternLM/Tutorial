
## 应用开发实战：使用浦语 InternLM 大模型一键写书

### 1 在线体验（需正确上网）：
https://book.apps.langgpt.ai/

### 2 本地运行：

#### 2.1 获取项目代码
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
#### 2.2 配置项目 Python 环境
```
pip install -r requirements.txt
```

#### 2.3 配置大模型 API

（1）申请浦语的 API , 获取 API Token：
https://internlm.intern-ai.org.cn/api/document


（2） 修改下面命令中的 API_KEY 等配置，在命令行执行命令，即可完成书籍创作

```
export API_KEY=xxx
export BASE_URL=https://internlm-chat.intern-ai.org.cn/puyu/api/v1/
export MODEL_NAME=internlm2.5-latest

python3 book_writer.py
```
（3）创作好的书籍在 books 文件夹下，写好的书籍示例（仅供参考）： [爱的编码：解密人类情感基因](./book.md).

（4）注意：

> 如果遇到“请求过于频繁，请稍后再试”报错，是 API 存在调用频率限制，可以使用[硅基流动](https://cloud.siliconflow.cn/i/TxUlXG3u)注册免费的 API 服务。配置 API_KEY，修改下面的命令并执行：

注意：写博客时切记删除自己的 api_key！


```
export API_KEY=sk-xxx
export BASE_URL=https://api.siliconflow.cn/v1
export MODEL_NAME=internlm/internlm2_5-7b-chat

python3 book_writer.py
```

#### 2.4 项目拆解

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

#### 2.5 项目优化

当前的写书项目只是个小 demo，还存在许多问题，同学们可以试着优化这些问题。一些已知的问题和优化方向：

    1. 章节正文内容的质量提升。优化内容表达、内容的深度、格式排版等，尤其数学公式的格式和排版。
    2. 各章节内容的连贯性。
    3. 章节正文长度提升。
    4. 让图书图文并茂：使用 mardown 的图片语法配图，或者搭配生图模型生成图片。
    5. 其他你能想到的优化方向。


