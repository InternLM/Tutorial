import torch
import os
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModel
base_path = './BaJie-Chat-1_8b'
os.system('apt install git')
os.system('apt install git-lfs')
os.system(f'git clone https://code.openxlab.org.cn/JimmyMa99/BaJie-Chat-1.8b.git {base_path}')
os.system(f'cd {base_path} && git lfs pull')

model_path = '/root/demo/work/BaJie-Chat-1_8b'
tokenizer = AutoTokenizer.from_pretrained(model_path,trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_path,trust_remote_code=True, torch_dtype=torch.float16).cuda()