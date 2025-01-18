import json
import os 

current = os.getcwd()
filePath = os.path.join(current, "extension_1/combined_10/combined_10_narrations.json")

with open(filePath, "r", encoding="utf-8") as file:
    data = json.load(file)

# Crea la mappa dei narration_text
narration_map = {}

for video_uid, content in data.items():
    narrations = content.get("narration_pass_1", {}).get("narrations", [])
    
    # Estrai i narration_text sostituendo "#C C" con "the person"
    narration_texts = [
        narration["narration_text"].replace("#C C", "the person") 
        for narration in narrations
    ]
    
    # Aggiungi alla mappa
    narration_map[video_uid] = narration_texts

# Stampa o salva il risultato
print(narration_map)

# Se vuoi salvare in un nuovo file JSON:
#with open("narration_map.json", "w", encoding="utf-8") as output_file:
#    json.dump(narration_map, output_file, ensure_ascii=False, indent=4)
