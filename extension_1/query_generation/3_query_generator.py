import json
from ollama import chat
from ollama import ChatResponse
import time
import re
import os
from tqdm import tqdm

def format_prompt(narrations):
    prompt = 'Given the following narrations describing the actions of a person in a video, generate a simple single query that could be answered by looking at the video corresponding to these narrations (don\'t just ask what the person is doing and don\'t be too generic): '
    for i, narration in enumerate(narrations, 1):
        prompt += f'{i}. {narration} '
    return prompt

def get_chat_response(prompt):
    #start_time = time.time()
    response: ChatResponse = chat(model='gemma2:9b', messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])
    end_time = time.time()
    #print(f"\nTime taken: {end_time - start_time} seconds\n")
    return response

def clean_question(question):
    cleaned = re.sub(r'(?i)query:\s*\n?', '', question)
    cleaned = re.sub(r'\*+', '', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def parse_response(response):
    try:
        #print("tot_respose ==>", response['message']['content'])
        queries = response['message']['content'].split('\n')
        #print("just the pick ===>", queries[0])
        #print("\n")
        parsed_queries = clean_question(queries[0])
        return parsed_queries
    except Exception as e:
        #print(f"Parsing failed: {e}")
        return None

def generate_query(narrations):
    prompt = format_prompt(narrations)
    response = get_chat_response(prompt)
    #print(narrations)
    query = parse_response(response)

    retry_count = 0
    max_retries = 10
    while (query == "" or query == " " or query == "```sql") and (retry_count < max_retries):
        #print(f"Retrying... ({retry_count + 1}/{max_retries})")
        response = get_chat_response(prompt)
        query = parse_response(response)
        retry_count += 1

    return query

def process_json_and_save(file_path, output_path, N):
    with open(file_path, 'r') as f:
        data = json.load(f)

    new_data = {}

    total_groups = sum(len(narrations) // N + (1 if len(narrations) % N != 0 else 0) for narrations in data.values())
    pbar = tqdm(total=total_groups, desc="Processing groups")

    for id_key, narrations in data.items():
        new_data[id_key] = []

        for i in range(0, len(narrations), N):
            group = narrations[i:i + N]
            new_data[id_key].append(generate_query(group))
            pbar.update(1)

    pbar.close()

    with open(output_path, 'w') as f:
        json.dump(new_data, f, indent=4)

    print(f"File salvato con successo in: {output_path}")

N = 5
input_folder = "narration_50_in_chunks"
output_folder = f"query_50_in_chunks_{N}"
os.makedirs(output_folder, exist_ok=True)

# Itera sui file da chunk_13.json a chunk_19.json
for i in range(13, 20):
    nome_file = f"chunk_{i}.json"
    input_path = os.path.join(input_folder, nome_file)
    output_path = os.path.join(output_folder, nome_file)

    print(f"Processing {nome_file}...")
    process_json_and_save(input_path, output_path, N)

print("Tutti i file sono stati processati con successo!")
