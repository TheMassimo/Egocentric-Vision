import json

# Funzione per eseguire le modifiche sulle stringhe
def process_string(s):
    replacements = [
        ("#c c", "the person"),
        ("#c  c", "the person"),
        ("#CC", "the person"),
        ("# C c", "the person"),
        ("# C C", "the person"),
        ("#O", "the"),
        ("#o", "the"),
        (" X ", " "),
        (" x ", " "),
        ("#unsure", ""),
        ("#C ", ""),
        ("#c ", ""),
        ("\n", ""),
        ("\\", ""),
        ("\"", ""),
        ("\u00e9", "e"),
        ("\u2019", "'"),
    ]
    for old, new in replacements:
        s = s.replace(old, new)
    return s

file_path = "narration_map_50.json"

with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Itera su ogni chiave e lista nel JSON
for key, narrations in data.items():
    data[key] = [process_string(narration) for narration in narrations]

output_path = "narration_map_50_cleaned.json"
with open(output_path, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)

print(f"Le modifiche sono state applicate e il file \u00e8 stato salvato in {output_path}.")
