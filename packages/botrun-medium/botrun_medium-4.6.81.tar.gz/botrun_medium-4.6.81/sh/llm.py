import argparse
import os

import yaml
from dotenv import load_dotenv
from litellm import completion

load_dotenv()


def read_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def write_file(file_path, content):
    # 先抓到路徑資料夾，如果不存在就強迫建立
    folder = os.path.dirname(file_path)
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"\n已替換檔案：{file_path}")


def process_response(response):
    code_blocks = response.split('@begin code')
    for block in code_blocks[1:]:
        end_index = block.find('@end')
        if end_index != -1:
            path_and_code = block[:end_index].strip().split(')', 1)
            path = path_and_code[0].replace('("', '').replace('"', '').strip()
            code = path_and_code[1].strip()
            write_file(path, code)


def main(config_path, model_name):
    print("讀取配置檔案中...")
    config = read_yaml(config_path)
    print("配置檔案讀取完成")
    print(config)

    prompt = config['prompt']
    for path in config['paths']:
        file_content = read_file(path)
        prompt += f'\n@begin code("{path}")\n{file_content}\n@end\n'
        print(f"已讀取檔案：{path}")

    messages = [{"role": "user", "content": prompt}]

    print("向Litellm發送請求中...")
    response = completion(model=model_name, messages=messages, stream=True)
    print("已接收Litellm回應")

    full_response = ""
    for part in response:
        full_response += part.choices[0].delta.content or ""
        if part.choices[0].delta.content:
            print(part.choices[0].delta.content, end='', flush=True)

    process_response(full_response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LLM Code Generator")
    parser.add_argument("--config", type=str, default="./sh/llm.yml", help="Path to the configuration YAML file")
    parser.add_argument("--model", type=str, default="openai/gpt-4o", help="Model name to use with Litellm")

    args = parser.parse_args()

    main(config_path=args.config, model_name=args.model)
