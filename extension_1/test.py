import os

# Percorso del file JSON
current = os.getcwd()
filePath = os.path.join(current, "datasets/ego4d_data/v1/annotations/narration.json")

# Crea una cartella per i file di output, se non esiste
output_dir = os.path.join(current, "extension_1/raw_chunks_outputs")
os.makedirs(output_dir, exist_ok=True)

# Specifica il numero di caratteri da leggere alla volta
chunk_size = 100000  # Ad esempio, 100.000 caratteri per chunk

chunk_number = 0
with open(filePath, "r", encoding="utf-8") as f:
    while True:
        # Leggi un chunk di caratteri
        chunk = f.read(chunk_size)
        if not chunk:  # Se non ci sono più dati, esci dal loop
            break
        
        # Salva il chunk in un file separato
        output_file = os.path.join(output_dir, f"chunk_{chunk_number}.json")
        with open(output_file, "w", encoding="utf-8") as output_f:
            output_f.write(chunk)
        
        print(f"Chunk {chunk_number} salvato in: {output_file}")
        chunk_number += 1

print("Processo completato. Tutti i chunk sono stati salvati.")
