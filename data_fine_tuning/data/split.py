import json

# 输入文件路径和输出文件路径
input_file_path = 'ruozhiba_format.jsonl'
train_file_path = 'train.jsonl'
test_file_path = 'test.jsonl'

# 读取原始文件，将所有行存储在一个列表中
with open(input_file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 计算训练集和测试集的分割点
split_index = int(len(lines) * 0.7)

# 拆分数据
train_lines = lines[:split_index]
test_lines = lines[split_index:]

# 写入训练集
with open(train_file_path, 'w', encoding='utf-8') as file:
    for line in train_lines:
        file.write(line)

# 写入测试集
with open(test_file_path, 'w', encoding='utf-8') as file:
    for line in test_lines:
        file.write(line)
