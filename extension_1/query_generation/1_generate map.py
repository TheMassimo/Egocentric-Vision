import json
import os 

current = os.getcwd()
filePath = os.path.join("combined_50_narrations_ordered.json")

with open(filePath, "r", encoding="utf-8") as file:
    data = json.load(file)

#Crea la mappa dei narration_text
narration_map = {}

for video_uid, content in data.items():
    narrations = content.get("narration_pass_1", {}).get("narrations", [])

    #Estrae i narration_text sostituendo "#C C" con "the person"
    narration_texts = [
        narration["narration_text"].replace("#C C", "the person") 
        for narration in narrations
    ]

    narration_map[video_uid] = narration_texts

with open("narration_map_50.json", "w", encoding="utf-8") as output_file:
    json.dump(narration_map, output_file, ensure_ascii=False, indent=4)