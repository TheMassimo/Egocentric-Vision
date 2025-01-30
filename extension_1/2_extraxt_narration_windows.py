import os
import json
import random

current = os.getcwd()

chunks_dir = os.path.join(current, "extension_1/chunks_output")

n_narrations = 50

combined_dir = os.path.join(current, f"extension_1/combined_{n_narrations}")
os.makedirs(combined_dir, exist_ok=True)

output_file = os.path.join(combined_dir, f"combined_{n_narrations}_narrations.json")

final_data = {}

for chunk_file in os.listdir(chunks_dir):
    if chunk_file.endswith(".json"): 
        chunk_path = os.path.join(chunks_dir, chunk_file)
        
        with open(chunk_path, "r", encoding="utf-8") as f:
            chunk_data = json.load(f)
        
        for chunk_id, chunk_content in chunk_data.items():

            narrations = chunk_content.get("narration_pass_1", {}).get("narrations", [])
            
            if narrations:
                max_start_index = len(narrations) - n_narrations 
                if max_start_index >= 0:
                    start_index = random.randint(0, max_start_index)
                    
                    selected_narrations = narrations[start_index:start_index + n_narrations]
                    
                    for narration in selected_narrations:
                        narration["narration_text"] = narration["narration_text"].replace("#C C", "the person")
                    
                    final_data[chunk_id] = {
                        "narration_pass_1": {
                            "narrations": selected_narrations
                        }
                    }

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(final_data, f, indent=4)

print(f"combined file generated in the folder: {combined_dir}")

narration_map = {}

for video_uid, content in final_data.items():
    narrations = content.get("narration_pass_1", {}).get("narrations", [])
    
    narration_texts = [
        narration["narration_text"] for narration in narrations
    ]
    
    narration_map[video_uid] = narration_texts

narration_map_file = os.path.join(combined_dir, "narration_map.json")
with open(narration_map_file, "w", encoding="utf-8") as output_file:
    json.dump(narration_map, output_file, ensure_ascii=False, indent=4)

print(f"File narration_map salved in the folder: {combined_dir}")
