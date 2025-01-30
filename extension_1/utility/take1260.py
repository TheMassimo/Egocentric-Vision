import json

def load_narrations(file_path):
    with open(file_path, 'r') as file:
        narrations = json.load(file)
    return narrations

def save_narrations(file_path, narrations):
    with open(file_path, 'w') as file:
        json.dump(narrations, file, indent=4)

def take_batches(narrations, batch_size):
    selected_narrations = {}
    count = 0
    for key, value in narrations.items():
        if count >= batch_size:
            break
        if not any(' Y ' in narration or ' C ' in narration or ' y ' in narration or '#O' in narration or ' c ' in narration or '#C' in narration or ' O ' in narration for narration in value):
            selected_narrations[key] = value
            count += 1
    return selected_narrations

def main():
    input_file = 'narration_map.json'
    output_file = 'narration_map_1260_batches.json'
    batch_size = 1260

    narrations = load_narrations(input_file)
    selected_narrations = take_batches(narrations, batch_size)
    save_narrations(output_file, selected_narrations)

if __name__ == "__main__": 
    main()