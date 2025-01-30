import os
import json

# Funzione per caricare e combinare i file JSON
def merge_json_chunks(input_folder, output_file):
    merged_data = {}

    # Trova tutti i file nella directory che corrispondono al pattern "chunk_*.json"
    for file_name in sorted(os.listdir(input_folder)):
        if file_name.startswith("chunk_") and file_name.endswith(".json"):
            file_path = os.path.join(input_folder, file_name)

            with open(file_path, "r", encoding="utf-8") as file:
                chunk_data = json.load(file)
                merged_data.update(chunk_data)

    with open(output_file, "w", encoding="utf-8") as output:
        json.dump(merged_data, output, indent=4, ensure_ascii=False)

# Configurazione
input_folder = "query_50_in_chunks_5" 
output_name = "merged_chunks.json"
output_folder = "all_in_one_narrations"
os.makedirs(output_folder, exist_ok=True)
output_file = os.path.join(output_folder, output_name)

merge_json_chunks(input_folder, output_file)

print(f"Tutti i chunk sono stati uniti nel file: {output_file}")
