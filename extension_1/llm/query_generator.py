import json
from ollama import chat
from ollama import ChatResponse
import time

def load_narrations(file_path):
    with open(file_path, 'r') as file:
        narrations = json.load(file)
    return narrations

def format_prompt(narrations):
    prompt = 'Given the following narrations describing the actions of a person, generate a simple generic query (one per line) that could be answered corresponding to these narrations: '
    for i, narration in enumerate(narrations, 1):
        prompt += f'{i}. {narration} '
    return prompt

def get_chat_response(prompt):
    start_time = time.time()
    response: ChatResponse = chat(model='gemma2:9b', messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
    return response

def parse_response(response):
    try:
        queries = response['message']['content'].split('\n')
        parsed_queries = [query.split('**')[1] for query in queries if '**' in query]
        return parsed_queries
    except Exception as e:
        print(f"Parsing failed: {e}")
        return None

def retry_bracketed_queries(output_file):
    with open(output_file, 'r') as file:
        output = json.load(file)
    narrations_map = load_narrations('narration_map_1260_batches.json')
    broken_count=0
    for narration_id, queries in output.items():
        if any('(' in query and ')' in query for query in queries) or any(query == "" for query in queries):
            broken_count+=1
            print(f"Retrying bracketed queries for ID: {narration_id}")
            narrations = narrations_map[narration_id]
            prompt = format_prompt(narrations)
            response = get_chat_response(prompt)
            parsed_queries = parse_response(response)
            retry_count = 0
            max_retries = 30
            while (parsed_queries == [] or len(parsed_queries) < 10) and retry_count < max_retries:
                print(f"Retrying... ({retry_count + 1}/{max_retries})")
                response = get_chat_response(prompt)
                parsed_queries = parse_response(response)
                retry_count += 1
            while len(parsed_queries) < 10:
                parsed_queries.append("")
            output[narration_id] = parsed_queries
    print(f"Total broken queries: {broken_count}")
    with open(output_file, 'w') as outfile:
        json.dump(output, outfile, indent=4)



def main():
    narrations_map = load_narrations('narration_map_1260_batches.json')
    output = {}
    start_time = time.time()
    for narration_id, narrations in narrations_map.items():
        print(f"\n\nProcessing ID: {narration_id}")
        prompt = format_prompt(narrations)
        response = get_chat_response(prompt)
        parsed_queries = parse_response(response)
        print(f"Queries before retries: {parsed_queries}\n")
        # Retry if parsing fails
        retry_count = 0
        max_retries = 30
        while (parsed_queries==[] or len(parsed_queries)<10) and retry_count < max_retries:
            print(f"Retrying... ({retry_count + 1}/{max_retries})")
            response = get_chat_response(prompt)
            parsed_queries = parse_response(response)
            retry_count += 1
        # Ensure there are at least 10 queries
        while len(parsed_queries) < 10:
            parsed_queries.append("")
        print(f"Total retries: {retry_count}")
        if retry_count>0:
            print(f"Queries after retries: {parsed_queries}\n")
        if parsed_queries is not None:
            output[narration_id] = parsed_queries
        else:
            print("Failed to parse the response after multiple attempts.")
            output[narration_id] = []

    # Save the output to a file
    with open('output_queries_1260.json', 'w') as outfile:
        json.dump(output, outfile, indent=4)
    end_time = time.time()
    print(f"Total time taken: {end_time - start_time} seconds")

if __name__ == "__main__":
    retry_bracketed_queries('output_queries_1260.json')