import json
import os
def ordina_annotazioni(json_path, output_path):

    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    

    for video_id, video_data in data.items():
        if "narration_pass_1" in video_data and "narrations" in video_data["narration_pass_1"]:
            video_data["narration_pass_1"]["narrations"] = sorted(
                video_data["narration_pass_1"]["narrations"],
                key=lambda x: x["timestamp_sec"]
            )
    

    with open(output_path, 'w', encoding='utf-8') as output_file:
        json.dump(data, output_file, indent=4, ensure_ascii=False)

current = os.getcwd()

input_file = os.path.join(current, "extension_1/llm/combined_10_questions.json")
output_file = os.path.join(current, "extension_1/llm/combined_10_questions_ordered.json")

ordina_annotazioni(input_file, output_file)

print(f"Il file JSON ordinato è stato salvato in {output_file}")
