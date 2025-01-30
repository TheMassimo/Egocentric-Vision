import json
import os

# Configurazione
input_file = "narration_map_50_cleaned.json"  # Nome del file JSON originale
output_folder = "narration_50_in_chunks"  # Cartella per i file divisi
max_ids_per_file = 250  # Numero massimo di ID per file
max_narrations_per_id = 50  # Numero massimo di narrazioni per ID

os.makedirs(output_folder, exist_ok=True)

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Funzione per dividere un dizionario in chunk
def chunk_dict(d, chunk_size):
    items = list(d.items())
    for i in range(0, len(items), chunk_size):
        yield dict(items[i:i + chunk_size])

# Elabora i dati per limitare le narrazioni per ID
processed_data = {k: v[:max_narrations_per_id] for k, v in data.items()}

# Divide i dati in più file con un massimo di `max_ids_per_file`
chunks = chunk_dict(processed_data, max_ids_per_file)

# Salva ogni chunk in un file separato
for i, chunk in enumerate(chunks, start=1):
    output_file = os.path.join(output_folder, f"chunk_{i}.json")
    with open(output_file, "w") as f:
        json.dump(chunk, f, indent=4)
    print(f"File salvato: {output_file}")
