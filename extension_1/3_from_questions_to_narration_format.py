import json
import os

current = os.getcwd()
source_file = os.path.join(current, "extension_1/llm/output_queries_1260.json")
destination_file = os.path.join(current, "extension_1/combined_10/combined_10_narrations.json")
output_file = os.path.join(current, "extension_1/llm/combined_10_questions.json")

with open(source_file, "r") as sf:
    source_data = json.load(sf)

with open(destination_file, "r") as df:
    destination_data = json.load(df)

output_data = {}

for video_id, narration_data in source_data.items():

    if video_id in destination_data:
        questions = narration_data
        narration_pass = destination_data[video_id].get("narration_pass_1", {})
        narrations = narration_pass.get("narrations", [])
        
        for i, narration in enumerate(narrations):
            if i < len(questions):
                narration["Query"] = questions[i] 
                narration.pop("narration_text", None) 

        output_data[video_id] = destination_data[video_id]

with open(output_file, "w") as of:
    json.dump(output_data, of, indent=4)

print(f"data updated and saved: {output_file}")


