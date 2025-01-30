import json
import random
import os

def select_random_narrations(input_file, output_file, n):
    """
    select N consecutive random narrations for every video uid

    :param input_file: imput file path
    :param output_file: output file path
    :param n: number of narrations
    """
    
    with open(input_file, 'r') as f:
        data = json.load(f)

    for item_id, item_data in data.items():
        narrations = item_data['narration_pass_1']['narrations']

        if len(narrations) < n:
            print(f"L'ID {item_id} ha meno di {n} narrazioni disponibili. Verranno selezionate tutte.")
            continue

        start_index = random.randint(0, len(narrations) - n)
        selected_narrations = narrations[start_index:start_index + n]

        item_data['narration_pass_1']['narrations'] = selected_narrations

    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)

n = 5 
current = os.getcwd()

input_file = os.path.join(current, "extension_1/llm/combined_10_questions_ordered.json")
final_output_file = os.path.join(
    current, f"extension_1/llm/combined_{n}_questions_ordered.json"
) 

select_random_narrations(input_file, final_output_file, n)
