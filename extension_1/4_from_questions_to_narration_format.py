import json
import os

# Percorsi dei file
current = os.getcwd()
source_file = os.path.join(current, "extension_1/llm/output_queries_1260.json")
destination_file = os.path.join(current, "extension_1/combined_10/combined_10_narrations.json")
output_file = os.path.join(current, "extension_1/llm/combined_10_questions.json")

# Leggiamo i file JSON
with open(source_file, "r") as sf:
    source_data = json.load(sf)

with open(destination_file, "r") as df:
    destination_data = json.load(df)

# Creiamo un nuovo dizionario per l'output
output_data = {}

# Iteriamo sui video nel file di origine
for video_id, narration_data in source_data.items():
    # Verifichiamo se il video_id esiste anche nel file di destinazione
    if video_id in destination_data:
        questions = narration_data  # Domande corrispondenti
        narration_pass = destination_data[video_id].get("narration_pass_1", {})
        narrations = narration_pass.get("narrations", [])
        
        # Sostituiamo ogni narrations con la corrispondente domanda
        for i, narration in enumerate(narrations):
            if i < len(questions):  # Se esistono domande sufficienti
                narration["Query"] = questions[i]  # Aggiungiamo "Query" con la domanda
                narration.pop("narration_text", None)  # Rimuoviamo "narration_text"
        
        # Aggiungiamo i dati modificati nell'output
        output_data[video_id] = destination_data[video_id]

# Salviamo il file aggiornato
with open(output_file, "w") as of:
    json.dump(output_data, of, indent=4)

print(f"Dati aggiornati e salvati in {output_file}")


