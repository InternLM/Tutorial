import json
import random

def split_conversations(input_file, train_output_file, test_output_file):
    # Read the input JSONL file
    with open(input_file, 'r', encoding='utf-8') as jsonl_file:
        data = json.load(jsonl_file)

    # Count the number of conversation elements
    num_conversations = len(data)
    
    # Shuffle the data randomly
    random.shuffle(data)
    random.shuffle(data)
    random.shuffle(data)

    # Calculate the split points for train and test
    split_point = int(num_conversations * 0.7)

    # Split the data into train and test
    train_data = data[:split_point]
    test_data = data[split_point:]

    # Write the train data to a new JSONL file
    with open(train_output_file, 'w', encoding='utf-8') as train_jsonl_file:
        json.dump(train_data, train_jsonl_file, indent=4)

    # Write the test data to a new JSONL file
    with open(test_output_file, 'w', encoding='utf-8') as test_jsonl_file:
        json.dump(test_data, test_jsonl_file, indent=4)

    print(f"Split complete. Train data written to {train_output_file}, Test data written to {test_output_file}")

# Replace 'input.jsonl', 'train.jsonl', and 'test.jsonl' with your actual file names
split_conversations('MedQA2019-structured.jsonl', 'MedQA2019-structured-train.jsonl', 'MedQA2019-structured-test.jsonl')
