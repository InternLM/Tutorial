input = """Hello world!  
This is an example.  
Word count is fun.  
Is it fun to count words?  
Yes, it is fun!"""

from collections import Counter
import re

def wordcount(text):
    # 将文本转换为小写，以便不区分大小写
    text = text.lower()
    # 使用空格分割文本，得到单词列表
    words = re.findall(r'\b\w+\b', text)
    # 统计每个单词的个数
    word_counts = Counter(words)
    return word_counts

# 统计单词个数
word_counts = wordcount(input)
# 输出结果
print(word_counts)

