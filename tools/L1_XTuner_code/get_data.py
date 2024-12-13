from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor
import json
import copy
from tqdm import tqdm
import queue
import time
import os

base_id_prompt = "# Role: 问答机器人\n\n## Profile\n- author: 尖米\n- version: 1.0\n- language: 中文\n- description: 你是机智流的问答机器人，你可以对用户输入的图像、文字进行解析，并根据已有的知识库进行精确回答。\n\n## Skills\n1. 图像识别与解析：能够识别用户上传的图像，并提取其中的关键信息。\n2. 自然语言处理：能够理解并解析用户输入的文字信息，准确把握用户意图。\n3. 知识库应用：根据解析结果，查询知识库，提供准确、相关的答案。\n4. 多轮对话：支持与用户进行多轮对话，提供连续性、上下文相关的回答。\n\n## Rules\n1. 必须充分理解用户输入的图像和文字内容。\n2. 回答需要简洁明了，避免过于复杂或含糊的表述。\n3. 在回答过程中，优先查询和引用公司已有的知识库。\n4. 对于无法回答的问题，需要引导用户提供更多信息或寻求人工客服帮助。\n\n## Workflows\n1. 接收并分析用户输入的图像或文字信息。\n2. 基于图像识别或自然语言处理技术，提取关键信息。\n3. 查询知识库，匹配相关信息。\n4. 向用户提供精准、相关的回答。\n5. 如有必要，进行多轮对话，确保问题得到有效解决。\n\n## Init\n欢迎使用机智流的问答机器人，请输入您的问题，我将尽力为您提供帮助。\n",

# 定义客户端
clients = {
    "internlm": OpenAI(
        api_key="your_internlm_api_key",
        base_url="https://internlm-chat.intern-ai.org.cn/puyu/api/v1/",
    ),
    "glm": OpenAI(
        api_key="your_glm_api_key",
        base_url="your_glm_url",
    ),
    "deepseek": OpenAI(
        api_key="your_deepseek_api_key",
        base_url="your_deepseek_url",
    )
}

class BaseDataAPI:
    def __init__(self, questions_path, save_path, repeat=0, client_name="internlm"):
        self.client = clients[client_name]
        self.questions_path = questions_path
        self.save_path = save_path
        self.repeat = repeat
        self.data_template = {
            "conversation": [
                {
                    "system": base_id_prompt,
                    "input": "xxx",
                    "output": "xxx"
                }
            ]
        }

    def get_answer(self, question):
        chat_rsp = self.client.chat.completions.create(
            model="internlm2.5-latest",  # 或 "internlm2-latest" 或 "glm-4"
            messages=[
                {"role": "system", "content": base_id_prompt},
                {"role": "user", "content": question}
            ],
            stream=False,
        )
        return self.build_data(question, chat_rsp)

    def build_data(self, question, chat_rsp):
        temp = copy.deepcopy(self.data_template)
        temp['conversation'][0]['input'] = question
        temp['conversation'][0]['output'] = chat_rsp.choices[0].message.content
        return temp

    def save(self, train_data):
        with open(self.save_path, 'a', encoding='utf-8') as f:
            for item in train_data:
                json.dump(item, f, ensure_ascii=False)
                f.write("\n")

    @staticmethod
    def load_txt(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def read_questions(self):
        prompt = self.load_txt(self.questions_path)
        promptlist = prompt.split('\n')
        if self.repeat != 0:
            promptlist = promptlist * self.repeat
        print(f"Total questions: {len(promptlist)}")
        return promptlist

class GetDataApi(BaseDataAPI):
    def run(self):
        answer_queue = queue.Queue()
        promptlist = self.read_questions()
        with ThreadPoolExecutor(max_workers=10) as pool:
            print("Asking...")
            futures = [pool.submit(self.get_answer, question) for question in promptlist]
            for future in tqdm(futures):
                result = future.result()
                answer_queue.put(result)
                if answer_queue.qsize() >= 10:  # 每10个问题保存一次
                    self.save([answer_queue.get() for _ in range(10)])

        # 保存剩余的回答
        remaining = []
        while not answer_queue.empty():
            remaining.append(answer_queue.get())
        if remaining:
            self.save(remaining)

class ChatData(BaseDataAPI):
    def __init__(self, train_data, save_path, client_name="internlm"):
        save_dir = os.path.dirname(save_path)
        if save_dir:  # 如果save_path包含目录路径
            os.makedirs(save_dir, exist_ok=True)
        
        # 如果文件不存在,创建空文件
        if not os.path.exists(save_path):
            with open(save_path, 'w', encoding='utf-8') as f:
                pass  # 创建空文件
        super().__init__(train_data, save_path, client_name=client_name)
        self.train_data = train_data

    def load_data(self):
        with open(self.train_data, 'r', encoding='utf-8') as f:
            return f.readlines()

    def ask_for_tts(self, question):
        messages = [
            {"role": "system", "content": str(base_id_prompt[0]) if isinstance(base_id_prompt, tuple) else str(base_id_prompt)},
            {"role": "user", "content": str(question)}
        ]
        chat_rsp = self.client.chat.completions.create(
            model="internlm2.5-latest",  # 或 "glm-4"
            messages=messages,
            stream=False,
        )
        return self.build_data(question, chat_rsp)

    def __call__(self):
        train_data = self.load_data()
        answer_queue = queue.Queue()
        with ThreadPoolExecutor(max_workers=1) as pool:
            print("Asking...")
            futures = []
            for item in train_data:
                futures.append(pool.submit(self.ask_for_tts, item))

            for future in tqdm(futures):
                result = future.result()
                answer_queue.put(result)
                if answer_queue.qsize() >= 10:  # 每10个问题保存一次
                    self.save([answer_queue.get() for _ in range(10)])

        # 保存剩余的回答
        remaining = []
        while not answer_queue.empty():
            remaining.append(answer_queue.get())
        if remaining:
            self.save(remaining)

if __name__ == '__main__':
    questions_path = './tools/L1_XTuner_code/Q_list.txt'
    save_path = './data/train_basic.jsonl'

    start_time = time.time()
    chat_data = ChatData(questions_path, save_path)
    chat_data()
    end_time = time.time()
    print('Done')
    print(f'Time used: {end_time - start_time:.2f} seconds')
