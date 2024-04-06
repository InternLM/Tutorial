import json
import argparse

def generate_new_json(input_file, output_file, repeat_times):
    # 加载原始JSON数据
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 重复数据
    new_data = data * repeat_times

    # 保存新的JSON数据到文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='Generate a new JSON file based on the input file and repetition times.')
    parser.add_argument('-i', '--input', required=True, help='Input JSON file path')
    parser.add_argument('-o', '--output', required=True, help='Output JSON file path')
    parser.add_argument('-n', '--number', type=int, required=True, help='Number of times to repeat the data')
    args = parser.parse_args()

    # 生成新的JSON文件
    generate_new_json(args.input, args.output, args.number)

if __name__ == '__main__':
    main()


