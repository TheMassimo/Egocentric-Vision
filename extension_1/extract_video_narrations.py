import os
import json

# Percorso del file JSON
current = os.getcwd()
filePath = os.path.join(current, "datasets/ego4d_data/v1/annotations/narration.json")

# Crea una cartella per i file di output, se non esiste
output_dir = os.path.join(current, "extension_1/chunks_output")
os.makedirs(output_dir, exist_ok=True)

# Apri il file JSON e carica i dati
with open(filePath, "r", encoding="utf-8") as f:
    data = json.load(f)  # Carica l'intero file JSON in memoria

# Itera su ogni ID nella struttura JSON
for item_id, item_data in data.items():
    # Percorso del file per il chunk
    output_file = os.path.join(output_dir, f"{item_id}.json")
    
    # Salva i dati relativi all'ID in un file separato
    with open(output_file, "w", encoding="utf-8") as output_f:
        json.dump({item_id: item_data}, output_f, indent=4)  # Salva come JSON formattato
    
    print(f"Chunk per ID {item_id} salvato in: {output_file}")

print("Processo completato. Tutti i chunk sono stati salvati.")




