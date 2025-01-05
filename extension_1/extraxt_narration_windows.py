import os
import json
import random

# Directory contenente i file dei chunk
current = os.getcwd()

chunks_dir = os.path.join(current, "extension_1/chunks_output")

# Numero di narrazioni da includere per ogni chunk
n_narrations = 10

# Crea una directory di output per i risultati combinati
combined_dir = os.path.join(current, f"extension_1/combined_{n_narrations}")
os.makedirs(combined_dir, exist_ok=True)

# File di output finale
output_file = os.path.join(combined_dir, f"combined_{n_narrations}_narrations.json")

# Dizionario finale da salvare
final_data = {}

# Cicla su tutti i file nella directory dei chunk
for chunk_file in os.listdir(chunks_dir):
    if chunk_file.endswith(".json"):  # Assicurati di processare solo i file JSON
        chunk_path = os.path.join(chunks_dir, chunk_file)
        
        # Carica il file JSON
        with open(chunk_path, "r", encoding="utf-8") as f:
            chunk_data = json.load(f)
        
        # Ottieni l'ID (chiave principale del JSON)
        for chunk_id, chunk_content in chunk_data.items():
            # Estrarre tutte le narrazioni
            narrations = chunk_content.get("narration_pass_1", {}).get("narrations", [])
            
            if narrations:
                # Trova un punto di partenza casuale per la finestra di N narrazioni consecutive
                max_start_index = len(narrations) - n_narrations  # Assicurati che ci siano abbastanza narrazioni
                if max_start_index >= 0:
                    start_index = random.randint(0, max_start_index)
                    
                    # Seleziona N narrazioni consecutive
                    selected_narrations = narrations[start_index:start_index + n_narrations]
                    
                    # Aggiungi al dizionario finale
                    final_data[chunk_id] = {
                        "narration_pass_1": {
                            "narrations": selected_narrations
                        }
                    }

# Salva il file combinato nella directory di output
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(final_data, f, indent=4)

print(f"File combinato generato nella cartella: {combined_dir}")
