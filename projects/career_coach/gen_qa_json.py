import pandas as pd
import json

# 读取Excel文件
excel_file = './dataset/心理大模型-职场焦虑语料.xlsx'  # 替换成实际的Excel文件路径
df = pd.read_excel(excel_file)

# 设置system的值
system_value = "你是一个专业的，经验丰富的有心理学背景的职场教练。你总是根据有职场焦虑的病人的问题提供准确、全面和详细的答案。"

# 将数据整理成jsonL格式
json_data = []
for index, row in df.iterrows():
    conversation = [
        {
            "system": system_value,
            "input": str(row['q']),
            "output": str(row['a'])
        }
    ]
    json_data.append({"conversation": conversation})

# 将json数据写入文件
output_json_file = 'career_coach.jsonl'  # 替换成实际的输出文件路径
with open(output_json_file, 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False)

print("JSONL文件生成成功！")

