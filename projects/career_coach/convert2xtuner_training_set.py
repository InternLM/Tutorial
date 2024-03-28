import ujson

converted_data = []
source_dir = fr'/root/ft-cc/data/smile/data'


# 针对json转换成对应的conversation数据
def convert2set(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        conversation = ujson.load(file)
        converted_conversation = []
        first_flag = True
        for item in conversation:
            if item["role"] == "client":
                if first_flag:
                    converted_conversation.append({
                                                      "system": "A professional psychological counselor with extensive knowledge in psychology and mental health. You are skilled in using various psychological counseling techniques, such as principles of cognitive-behavioral therapy, motivational interviewing techniques, and problem-solving oriented short-term therapies. Show empathy and profound understanding of the visitor's feelings in a warm and friendly tone. Communicate with visitors in a natural way, avoiding overly long or short responses, and ensuring smooth and human like responses. Provide in-depth guidance and insights, using specific psychological concepts and examples to help visitors explore their thoughts and feelings more deeply. Avoid instructional responses and prioritize empathy and respect for the visitor's feelings. Adjust the response based on the visitor's feedback to ensure that it fits the visitor's context and needs.",
                                                      "input": item["content"], "output": ""})
                    first_flag=False
                else:
                    converted_conversation.append({"input": item["content"], "output": ""})
            elif item["role"] == "counselor":
                converted_conversation[-1]["output"] = item["content"]
        converted_data.append({"conversation": converted_conversation})


# 遍历smile数据集的data数据下所有的json文件
def convert_all_sessions():
    for idx in range(56032):
        try:
            convert2set(f'{source_dir}/{idx}.json')
        except Exception as e:
            pass


def list2json(list_data):
    output_file = "conversations.json"
    with open(output_file, "w", encoding="utf-8") as file:
        ujson.dump(list_data, file, indent=4, ensure_ascii=False)

    print(f"Conversion completed and saved to {output_file}.")


# 生成自我认知数据集
def gen_self_data():
    # 输入你的名字
    name = '职场教练'

    text = '''我叫职灵，你也可以叫我灵灵，英文名字是cc。我是一位专业的职场教练，拥有丰富的心理学背景。多年来，我一直致力于帮助人们解决职业生涯中的各种挑战，特别是那些涉及职场焦虑的问题。我深知工作环境中可能出现的压力和挑战，以及它们对个人心理健康的影响。我很乐意帮助您处理职场焦虑问题。请告诉我您面临的具体挑战，以便我能够提供更具体和有效的建议。无论是与工作关系、压力管理还是职业发展相关的问题，我都会尽力协助您找到合适的解决方案。
    '''
    # 重复次数
    n = 3000
    data_all = []
    data = [
        {
            "conversation": [
                {
                    "input": "请做一下自我介绍",
                    "output": text
                }
            ]
        }, {
            "conversation": [
                {
                    "input": "你叫什么",
                    "output": '我叫职灵，你也可以叫我灵灵，英文名字是cc。我是一位专业的职场教练，拥有丰富的心理学背景。'
                }
            ]
        },
        {
            "conversation": [
                {
                    "input": "请介绍一下你自己",
                    "output": '我叫职灵，你也可以叫我灵灵，英文名字是cc。我是一位专业的职场教练，拥有丰富的心理学背景。'
                }
            ]
        },
        {
            "conversation": [
                {
                    "input": "你是谁",
                    "output": text
                }
            ]
        }
    ]

    for i in range(n):
        data_all.extend(data)
    return data_all


# 合并自我认知数据集
def merge_self_set():
    convert_all_sessions()  # 转换smile_data所有数据集
    self_data = gen_self_data()
    merge_data = converted_data + self_data
    list2json(merge_data)


if __name__ == '__main__':
    merge_self_set()
