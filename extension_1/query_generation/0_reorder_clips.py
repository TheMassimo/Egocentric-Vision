import json

with open('combined_50_narrations.json', 'r') as file:
    data = json.load(file)

for key, value in data.items():
    if "narration_pass_1" in value and "narrations" in value["narration_pass_1"]:

        value["narration_pass_1"]["narrations"].sort(key=lambda x: x["timestamp_sec"])

with open('combined_50_narrations_ordered.json', 'w') as file:
    json.dump(data, file, indent=4)

print("File ordinato e salvato come 'combined_50_narrations_ordered.json'")