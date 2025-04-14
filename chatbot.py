try:
    import tqdm
except ImportError:
    os.system("pip install tqdm")

try:
    import requests
except ImportError:
    os.system("pip install requests")

import requests
import tqdm
import os
import string

def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text

def load_mineogo_dataset(input_file):
    dataset = []
    with open(input_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            if "->" in line:
                input_text, response_text = line.split("->")
                cleaned_input = clean_text(input_text.replace("i:", "").strip())
                cleaned_response = clean_text(response_text.replace("o:", "").strip())
                dataset.append((cleaned_input, cleaned_response))
    return dataset

def save_dataset(input_file, dataset):
    with open(input_file, 'w', encoding='utf-8') as f:
        for input_text, response_text in dataset:
            f.write(f"i:{input_text} -> o:{response_text}\n")
    print(f"Dataset saved to {input_file}")

def download_default_dataset(url, output_file):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        total_size = int(response.headers.get('content-length', 0))
        with open(output_file, 'wb') as f, tqdm.tqdm(
            desc="Downloading dataset",
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024
        ) as bar:
            for data in response.iter_content(chunk_size=1024):
                f.write(data)
                bar.update(len(data))
        print("Download complete!")
        return True
    else:
        print("Failed to download dataset.")
        return False

def get_available_datasets():
    api_url = "https://api.github.com/repos/MINEOGO/programmed-ai/contents/"
    response = requests.get(api_url)
    if response.status_code == 200:
        files = response.json()
        return [file['name'] for file in files if file['name'].endswith('.mineogo')]
    else:
        print("Failed to fetch available datasets.")
        return []

def select_dataset():
    datasets = get_available_datasets()
    if not datasets:
        print("No datasets found.")
        return None

    for idx, name in enumerate(datasets):
        print(f"{idx + 1}. {name[:-8]}")

    try:
        choice = int(input("Select a dataset number: ")) - 1
        if 0 <= choice < len(datasets):
            confirm = input(f"Are you sure to download '{datasets[choice][:-8]}'? (yes/no): ").strip().lower()
            if confirm == "yes":
                return datasets[choice]
            else:
                print("Cancelled.")
                return None
        else:
            print("Invalid selection.")
            return None
    except ValueError:
        print("Invalid input.")
        return None

def local_dataset_selector():
    datasets = [f for f in os.listdir() if f.endswith('.mineogo')]
    if len(datasets) == 1:
        return datasets[0]
    elif len(datasets) > 1:
        print("Multiple datasets found:")
        for i, f in enumerate(datasets):
            print(f"{i + 1}. {f}")
        try:
            choice = int(input("Select dataset to use: ")) - 1
            if 0 <= choice < len(datasets):
                return datasets[choice]
            else:
                print("Invalid selection.")
                return None
        except ValueError:
            print("Invalid input.")
            return None
    else:
        return None

def chat_with_bot(dataset):
    print('Chatbot: hi type "/help" to see all cmds, type exit to quit ')
    while True:
        user_input = input("You: ").lower()
        if user_input.startswith('/'):
            handle_command(user_input, dataset)
            continue
        if user_input == 'exit':
            print("Chatbot: Goodbye!")
            break
        for input_text, response_text in dataset:
            if user_input == input_text:
                print(f"Chatbot: {response_text}")
                break
        else:
            print("Chatbot: not trained with this request.")

def handle_command(command, dataset):
    if command == '/train':
        dataset = training_mode(dataset)
        save_dataset("chat_dataset.mineogo", dataset)
    elif command == '/help':
        print("/train /status /clear /help /exit")
    elif command == '/status':
        print(f"Dataset has {len(dataset)} entries.")
    elif command == '/clear':
        clear_dataset_confirmation(dataset)
    else:
        print(f"Unknown command '{command}'")

def training_mode(dataset):
    print("Training mode. Type 'v' to save and exit.")
    while True:
        user_input = input("input?: ").strip().lower()
        if user_input == 'v':
            break
        response_text = input("output?: ").strip().lower()
        cleaned_input = clean_text(user_input)
        cleaned_response = clean_text(response_text)
        dataset.append((cleaned_input, cleaned_response))
    print("Exiting training mode.")
    return dataset

def clear_dataset_confirmation(dataset):
    print("Are you sure you want to clear the dataset?")
    if input("Type 'yes' to confirm: ").lower() == 'yes':
        dataset.clear()
        print("Dataset cleared.")
    else:
        print("Cancelled.")

def main():
    selected_file = local_dataset_selector()
    if not selected_file:
        print("Dataset doesn't exist!")
        print("1 > Download dataset")
        print("2 > Make my own dataset")
        print("3 > Setup later")
        choice = input("Enter your choice (1, 2, 3): ").strip()
        if choice == "1":
            selected = select_dataset()
            if selected:
                url = f"https://raw.githubusercontent.com/MINEOGO/programmed-ai/main/{selected}"
                if download_default_dataset(url, selected):
                    dataset = load_mineogo_dataset(selected)
                    chat_with_bot(dataset)
                else:
                    print("Download failed.")
        elif choice == "2":
            dataset = training_mode([])
            save_dataset("chat_dataset.mineogo", dataset)
            chat_with_bot(dataset)
        elif choice == "3":
            print("Setup later. Exiting.")
        else:
            print("Invalid choice.")
    else:
        dataset = load_mineogo_dataset(selected_file)
        chat_with_bot(dataset)

if __name__ == "__main__":
    main()
