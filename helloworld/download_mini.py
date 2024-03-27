import os
from modelscope.hub.snapshot_download import snapshot_download

# 创建保存模型目录
os.system("mkdir /root/demo/internlm2-chat-1_8b")

# save_dir是模型保存到本地的目录
save_dir="/root/demo/internlm2-chat-1_8b"
snapshot_download("Shanghai_AI_Laboratory/internlm2-chat-1_8b", 
                  cache_dir=save_dir, 
                  revision='v1.1.0')
