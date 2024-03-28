import torch
import os
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModel
base_path = '/root/models/BaJie-Chat-1_8b'
os.system('apt install git')
os.system('apt install git-lfs')
os.system(f'git clone https://code.openxlab.org.cn/JimmyMa99/BaJie-Chat-1.8b.git {base_path}')
os.system(f'cd {base_path} && git lfs pull')