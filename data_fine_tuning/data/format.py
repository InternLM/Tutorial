import json

# 原始和目标文件路径
input_file_path = 'ruozhiba_raw.jsonl'
output_file_path = 'ruozhiba_format.jsonl'

# 打开原始文件进行读取
with open(input_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w', encoding='utf-8') as output_file:
    for line in input_file:
        # 将每行的json字符串转换为字典
        original_data = json.loads(line)

        # 转换格式
        converted_data = {
            "messages": [
                {
                    "role": "user",
                    "content": original_data["instruction"]
                },
                {
                    "role": "assistant",
                    "content": original_data["output"]
                }
            ]
        }

        # 写入新的jsonl文件，确保中文不被转义
        json.dump(converted_data, output_file, ensure_ascii=False)
        output_file.write('\n')  # 每行后添加换行符，以保持jsonl格式
