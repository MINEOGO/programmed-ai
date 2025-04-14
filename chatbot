import string
import time
import os

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

def chat_with_bot(dataset):
    print("Chatbot: Hello! Type 'exit' to quit the conversation.")
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
            print("Chatbot: I'm sorry, I didn't understand that.")

def handle_command(command, dataset):
    if command == '/train':
        dataset = training_mode(dataset)
        save_dataset("chat_dataset.mineogo", dataset)
    elif command == '/help':
        print("Chatbot: Here are some available commands:\n - /train: Enter training mode\n - /status: View dataset status\n - /clear: Clear dataset\n - /exit: Exit the conversation")
    elif command == '/status':
        print(f"Chatbot: The dataset currently contains {len(dataset)} input-output pairs.")
    elif command == '/clear':
        clear_dataset_confirmation(dataset)
    else:
        print(f"Chatbot: Unknown command '{command}'")

def training_mode(dataset):
    print("Entering training mode. Type 'v' to exit and save.")
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
    print("Chatbot: Are you sure you want to clear the dataset?")
    if input("Type 'yes' to confirm: ").lower() == 'yes':
        dataset.clear()
        print("Dataset cleared.")
    else:
        print("Clear dataset operation canceled.")

def main():
    input_file = "chat_dataset.mineogo"
    dataset = load_mineogo_dataset(input_file)
    chat_with_bot(dataset)

if __name__ == "__main__":
    main()
